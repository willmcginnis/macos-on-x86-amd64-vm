"""Draw the progress charts under docs/charts/ from data/*.json, as SVG text.

Each chart is drawn twice, once for GitHub's light theme and once for its dark
theme; the Markdown pages show the pair through a <picture> element. Nothing is
drawn from anything but the data files, and render.py --check compares these
files exactly as it compares the generated tables.

Colours have one meaning each across every chart:

    state  done = green, in progress = blue, not started = gray,
           superseded = pale gray
    origin Apple's own x86_64 code = violet, lifted = orange,
           translated = aqua, macOS 26 (Tahoe) = yellow, anything else = magenta,
           not running yet = gray

Besides colour: every chart has a legend; state tiles carry a glyph (filled
disc = done, half disc = in progress, ring = not started, slashed ring =
superseded); bars print their counts where they fit, keep a fixed order, and
the status chart says how many of each table's rows are done; and every
figure is also in a table (docs/progress.md and the detail pages).

Standard library only. Text widths are estimated, not measured, so labels are
placed with generous room rather than packed to the edge.
"""

from __future__ import annotations

import datetime
from collections import Counter
from collections.abc import Callable
from html import escape

WIDTH = 880
TICK_GAP = 60  # px between date labels on a time axis
FONT = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

# GitHub's own page surfaces, so a chart sits flush on the page in each theme.
THEMES = {
    "light": {
        "surface": "#ffffff", "ink": "#1f2328", "ink2": "#59636e",
        "grid": "#e7e7e7", "axis": "#c2c2c2",
        "done": "#008a17", "in progress": "#257de0", "not started": "#9c9c9c",
        "superseded": "#c4c4c4",
        "x86": "#6a4ce2", "lifted": "#f47230", "translated": "#00b894",
        "tahoe": "#f2a600", "other": "#ee7fac", "none": "#9c9c9c",
    },
    "dark": {
        "surface": "#0d1117", "ink": "#f0f6fc", "ink2": "#9198a1",
        "grid": "#262c36", "axis": "#474747",
        "done": "#0aac23", "in progress": "#338ced", "not started": "#8b949e",
        "superseded": "#484f58",
        "x86": "#9887ef", "lifted": "#e76624", "translated": "#00a888",
        "tahoe": "#d28e05", "other": "#e24d8b", "none": "#8b949e",
    },
}

STATES = ("done", "in progress", "not started", "superseded")

LABEL_INKS = ("#ffffff", "#0b0b0b")

# Keys drawn as an outline rather than a fill, so they differ from every fill by shape.
HOLLOW = {"none"}

ORIGINS = ("x86", "lifted", "translated", "tahoe", "other", "none")

# Every origin class the data files use, mapped to the colour family above.
ORIGIN_OF = {
    "Apple x86_64": "x86", "apple-27-x86_64": "x86",
    "lifted": "lifted", "apple-27-lifted": "lifted",
    "translated": "translated", "apple-27-arm64e-translated": "translated",
    "borrowed from 26": "tahoe", "borrowed-tahoe-x86_64": "tahoe",
    "none": "none",
}


class ChartError(Exception):
    """A data shape the charts cannot draw."""


# --------------------------------------------------------------------------
# primitives
# --------------------------------------------------------------------------


def luminance(hex_colour: str) -> float:
    """WCAG relative luminance of a #rrggbb colour."""
    channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def ink_on(fill: str) -> str:
    """White or near-black, whichever reads better on a fill."""
    return max(LABEL_INKS, key=lambda ink: contrast(ink, fill))


def text_width(text: str, size: float) -> float:
    """A deliberately generous estimate of rendered text width."""
    return len(text) * size * 0.58


def wrap(text: str, size: float, width: float) -> list[str]:
    """Word-wrap text to a width; a single long word keeps its own line."""
    lines: list[str] = []
    line = ""
    for word in text.split():
        candidate = f"{line} {word}".strip()
        if line and text_width(candidate, size) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def label(x: float, y: float, text: str, fill: str, size: float = 12,
          anchor: str = "start", weight: str = "normal") -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(text)}</text>')


def rect(x: float, y: float, w: float, h: float, fill: str, radius: float = 0,
         opacity: float = 1.0) -> str:
    extra = f' fill-opacity="{opacity}"' if opacity < 1 else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" '
            f'height="{h:.1f}" rx="{radius}" fill="{fill}"{extra}/>')


def swatch(x: float, y: float, w: float, h: float, key: str, theme: dict,
           radius: float) -> str:
    """A filled mark, or for a HOLLOW key an outlined one."""
    if key not in HOLLOW:
        return rect(x, y, w, h, theme[key], radius=radius)
    return (f'<rect x="{x + 0.75:.1f}" y="{y + 0.75:.1f}" width="{max(w - 1.5, 0):.1f}" '
            f'height="{h - 1.5:.1f}" rx="{radius}" fill="{theme["surface"]}" '
            f'stroke="{theme[key]}" stroke-width="1.5"/>')


def glyph(cx: float, cy: float, state: str, colour: str, surface: str) -> str:
    """The shape that carries a state besides its colour."""
    r = 4.5
    if state == "done":
        return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{colour}"/>'
    ring = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r - 0.75}" fill="{surface}" '
            f'stroke="{colour}" stroke-width="1.5"/>')
    if state == "in progress":
        half = (f'<path d="M{cx:.1f},{cy - r:.1f} A{r},{r} 0 0 1 {cx:.1f},{cy + r:.1f} Z" '
                f'fill="{colour}"/>')
        return ring + half
    if state == "superseded":
        slash = (f'<line x1="{cx - 3:.1f}" y1="{cy + 3:.1f}" x2="{cx + 3:.1f}" y2="{cy - 3:.1f}" '
                 f'stroke="{colour}" stroke-width="1.5"/>')
        return ring + slash
    if state == "not started":
        return ring
    raise ChartError(f"no shape for the state {state!r}")


def legend(x: float, y: float, entries: list[tuple[str, str, str | None]],
           theme: dict, glyphs: bool) -> tuple[list[str], float]:
    """One row of legend entries; returns the parts and the row's end x."""
    parts: list[str] = []
    for key, text, state in entries:
        if glyphs and state is not None:
            parts.append(glyph(x + 5, y - 4, state, theme[key], theme["surface"]))
        else:
            parts.append(swatch(x, y - 9, 10, 10, key, theme, radius=2))
        parts.append(label(x + 16, y, text, theme["ink2"]))
        x += 16 + text_width(text, 12) + 18
    return parts, x


def document(title: str, description: str, height: float, body: list[str],
             theme: dict) -> str:
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
            f'height="{height:.0f}" viewBox="0 0 {WIDTH} {height:.0f}" role="img" '
            f'font-family="{FONT}">')
    return "\n".join([
        head,
        f"<title>{escape(title)}</title>",
        f"<desc>{escape(description)}</desc>",
        rect(0, 0, WIDTH, height, theme["surface"]),
        *body,
        "</svg>",
        "",
    ])


def heading(title: str, subtitle: str, theme: dict) -> list[str]:
    return [label(16, 26, title, theme["ink"], size=15, weight="600"),
            label(16, 46, subtitle, theme["ink2"])]


def segmented_bar(x: float, y: float, width: float, height: float,
                  parts: list[tuple[str, int]], theme: dict) -> tuple[list[str], set[str]]:
    """A bar split into parts, 2px surface gaps between them, counts printed
    inside where they fit. Returns the marks and the keys that printed a count."""
    total = sum(count for _, count in parts)
    if total == 0:
        raise ChartError("a segmented bar needs at least one counted part")
    shown = [(key, count) for key, count in parts if count]
    usable = width - 2 * (len(shown) - 1)
    marks: list[str] = []
    printed: set[str] = set()
    cursor = x
    for key, count in shown:
        w = usable * count / total
        marks.append(swatch(cursor, y, w, height, key, theme, radius=3))
        text = str(count)
        if text_width(text, 12) + 10 <= w:
            ink = theme["ink"] if key in HOLLOW else ink_on(theme[key])
            marks.append(label(cursor + 6, y + height / 2 + 4, text, ink, weight="600"))
            printed.add(key)
        cursor += w + 2
    return marks, printed


# --------------------------------------------------------------------------
# the charts
# --------------------------------------------------------------------------


def state_parts(rows: list[dict]) -> list[tuple[str, int]]:
    counts = Counter(row["state"] for row in rows)
    unknown = set(counts) - set(STATES)
    if unknown:
        raise ChartError(f"state words the charts have no colour for: {sorted(unknown)}")
    return [(state, counts.get(state, 0)) for state in STATES]


def milestones_chart(milestones: dict, theme: dict) -> str:
    rows = milestones["milestones"]
    counts = state_parts(rows)
    as_of = datetime.date.fromisoformat(milestones["meta"]["as_of"])
    if any(m["state"] == "done" and not m.get("date") for m in rows):
        raise ChartError("a milestone marked done has no date")
    # The step line is history: every recorded first-met date counts, whatever the
    # milestone's state is now (a milestone met and later superseded was still met).
    met = []
    for m in rows:
        if m.get("date") and m["state"] not in ("done", "superseded"):
            raise ChartError(f"milestone {m['id']} has a first-met date but is "
                             f"{m['state']}, not met")
        if m.get("date"):
            when = datetime.date.fromisoformat(m["date"])
            if when > as_of:
                raise ChartError(f"milestone {m['id']} was first met on {when}, after the "
                                 f"snapshot date {as_of}")
            met.append(when)
    met.sort()
    if not met:
        raise ChartError("no milestone has been met, so there is nothing to plot")
    total = len(rows)
    done_now = sum(1 for m in rows if m["state"] == "done")
    body = heading(f"Milestones: {done_now} of the {total} set so far are met",
                   f"Each tile is one milestone, in the order they were set. "
                   f"As of {as_of.isoformat()}. From data/milestones.json.", theme)

    # The track: one tile per milestone.
    tile_w = (WIDTH - 32 - 2 * (total - 1)) / total
    y = 64
    for index, m in enumerate(rows):
        x = 16 + index * (tile_w + 2)
        state = m["state"]
        body.append(rect(x, y, tile_w, 26, theme[state], radius=4))
        ink = ink_on(theme[state])
        body.append(label(x + tile_w / 2, y + 17, m["id"], ink, size=11,
                          anchor="middle", weight="600"))
        body.append(glyph(x + tile_w / 2, y + 38, state, theme[state], theme["surface"]))
    entries = [(s, f"{s} ({n})", s) for s, n in counts if n]
    parts, _ = legend(16, y + 64, entries, theme, glyphs=True)
    body.extend(parts)

    # The step chart: milestones met, counted by the date each was first met.
    top, bottom, left, right = y + 96, y + 296, 56, WIDTH - 110
    start = met[0] - datetime.timedelta(days=1)
    span = max((as_of - start).days, 1)

    def px(day: datetime.date) -> float:
        return left + (right - left) * (day - start).days / span

    def py(count: int) -> float:
        return bottom - (bottom - top) * count / total

    for tick in (t for t in range(0, total + 1, 5) if total - t >= 3 or t == total):
        body.append(f'<line x1="{left}" x2="{right}" y1="{py(tick):.1f}" y2="{py(tick):.1f}" '
                    f'stroke="{theme["grid"]}" stroke-width="1"/>')
        body.append(label(left - 8, py(tick) + 4, str(tick), theme["ink2"], size=11,
                          anchor="end"))
    body.append(f'<line x1="{left}" x2="{right}" y1="{py(total):.1f}" y2="{py(total):.1f}" '
                f'stroke="{theme["axis"]}" stroke-width="1"/>')
    body.append(label(right - 4, py(total) + 14, f"{total} set as of {as_of.isoformat()}",
                      theme["ink2"], size=11, anchor="end"))
    body.append(f'<line x1="{left}" x2="{right}" y1="{bottom}" y2="{bottom}" '
                f'stroke="{theme["axis"]}" stroke-width="1"/>')
    # Ticks on Mondays, thinned so labels stay at least TICK_GAP px apart as the
    # span grows; the as-of date is labelled unless a tick already sits too close.
    mondays = [start + datetime.timedelta(days=d) for d in range(span + 1)
               if (start + datetime.timedelta(days=d)).weekday() == 0]
    ticks: list[datetime.date] = []
    for day in mondays:
        if not ticks or px(day) - px(ticks[-1]) >= TICK_GAP:
            ticks.append(day)
    if not ticks or px(as_of) - px(ticks[-1]) >= TICK_GAP:
        ticks.append(as_of)
    for day in ticks:
        body.append(label(px(day), bottom + 18, f"{day:%b} {day.day}", theme["ink2"],
                          size=11, anchor="middle"))

    steps = sorted(Counter(met).items())
    points = [(px(start), py(0))]
    count = 0
    for when, added in steps:
        points.append((px(when), py(count)))
        count += added
        points.append((px(when), py(count)))
    points.append((px(as_of), py(count)))
    path = " ".join(f"{a:.1f},{b:.1f}" for a, b in points)
    area = f"{path} {px(as_of):.1f},{bottom} {px(start):.1f},{bottom}"
    body.append(f'<polygon points="{area}" fill="{theme["done"]}" fill-opacity="0.10"/>')
    body.append(f'<polyline points="{path}" fill="none" stroke="{theme["done"]}" '
                f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    count = 0
    for when, added in steps:
        count += added
        body.append(f'<circle cx="{px(when):.1f}" cy="{py(count):.1f}" r="4" '
                    f'fill="{theme["done"]}" stroke="{theme["surface"]}" stroke-width="2"/>')
    body.append(label(px(as_of) + 8, py(count) + 4, f"{count} first met", theme["ink"],
                      size=12, weight="600"))
    body.append(label(16, top - 8, "Milestones first met, counted by date",
                      theme["ink2"], size=12))

    height = bottom + 34
    superseded = [m["id"] for m in rows if m["state"] == "superseded"]
    description = (f"{done_now} of {total} milestones met as of {as_of.isoformat()}. "
                   "First met, by date: "
                   + "; ".join(f"{when.isoformat()}: {added}" for when, added in steps)
                   + ". Not yet met: "
                   + ", ".join(f"{m['id']} ({m['state']})" for m in rows
                               if m["state"] not in ("done", "superseded")) + "."
                   + (f" Superseded: {', '.join(superseded)}." if superseded else ""))
    return document("Milestones", description, height, body, theme)


def status_chart(groups: list[tuple[str, list[tuple[str, list[dict]]]]], as_of: str,
                 theme: dict) -> str:
    """Share of rows in each state, one bar per progress table."""
    body = heading("Where each progress table stands",
                   f"Share of each table's rows by state; the number in a bar is a count of rows. "
                   f"As of {as_of}.", theme)
    entries = [(s, s, s) for s in STATES]
    parts, _ = legend(16, 72, entries, theme, glyphs=False)
    body.extend(parts)
    label_w, bar_x, bar_w = 240, 256, WIDTH - 256 - 96
    y = 92
    lines: list[str] = []
    for group, tables in groups:
        if group:
            body.append(label(16, y + 14, group, theme["ink"], size=12, weight="600"))
            y += 22
        for name, rows in tables:
            indent = 30 if group else 16
            for i, line in enumerate(wrap(name, 12, label_w - indent)):
                body.append(label(indent, y + 15 + 14 * i, line, theme["ink"]))
            marks, _ = segmented_bar(bar_x, y + 2, bar_w, 20, state_parts(rows), theme)
            body.extend(marks)
            done = sum(1 for row in rows if row["state"] == "done")
            body.append(label(bar_x + bar_w + 10, y + 16, f"{done} of {len(rows)} done",
                              theme["ink2"], size=11))
            sentence = ", ".join(f"{n} {s}" for s, n in state_parts(rows) if n)
            lines.append(f"{name}: {len(rows)} rows, {sentence}")
            y += 30
    description = f"As of {as_of}. " + "; ".join(lines) + "."
    return document("Where each progress table stands", description, y + 8, body, theme)


def feature_grid_chart(components: dict, theme: dict) -> str:
    """One tile per feature-matrix row, a column per area."""
    areas = components["areas"]
    column_w = (WIDTH - 32 - 8 * (len(areas) - 1)) / len(areas)
    body = heading("The feature matrix, part by part",
                   f"One tile per row of docs/components.md, a column per area. "
                   f"As of {components['meta']['as_of']}.", theme)
    entries = [(s, s, s) for s in STATES[:3]]
    parts, _ = legend(16, 72, entries, theme, glyphs=True)
    body.extend(parts)
    bottom = 0.0
    lines: list[str] = []
    header_lines = max(len(wrap(a["title"], 11.5, column_w - 4)) for a in areas)
    for index, area in enumerate(areas):
        x = 16 + index * (column_w + 8)
        y = 96.0
        for line in wrap(area["title"], 11.5, column_w - 4):
            body.append(label(x, y, line, theme["ink"], size=11.5, weight="600"))
            y += 14
        y = 96.0 + 14 * header_lines
        done = sum(1 for r in area["rows"] if r["state"] == "done")
        body.append(label(x, y, f"{done} of {len(area['rows'])} done", theme["ink2"], size=11))
        y += 10
        lines.append(f"{area['title']}: " + "; ".join(f"{r['part']} ({r['state']})"
                                                       for r in area["rows"]))
        for row in area["rows"]:
            state = row["state"]
            if state not in theme:
                raise ChartError(f"no colour for the state {state!r}")
            text = wrap(row["part"], 11, column_w - 26)
            h = 12 + 14 * len(text)
            body.append(rect(x, y, column_w, h, theme[state], radius=4, opacity=0.14))
            body.append(rect(x, y, 4, h, theme[state], radius=2))
            body.append(glyph(x + column_w - 9, y + 10, state, theme[state], theme["surface"]))
            for i, line in enumerate(text):
                body.append(label(x + 10, y + 17 + 14 * i, line, theme["ink"], size=11))
            y += h + 4
        bottom = max(bottom, y)
    description = "Feature matrix. " + " | ".join(lines)
    return document("The feature matrix, part by part", description, bottom + 8, body, theme)


def origin_parts(classes: Counter, order: list[str]) -> list[tuple[str, str, int]]:
    """(colour family, class name, count) in the fixed family order."""
    named = [(ORIGIN_OF.get(name, "other"), name, classes[name])
             for name in order if classes.get(name)]
    unlisted = set(classes) - set(order)
    if unlisted:
        raise ChartError(f"classes missing from their file's meta: {sorted(unlisted)}")
    return sorted(named, key=lambda part: ORIGINS.index(part[0]))


def origins_chart(bars: list[tuple[str, str, list[tuple[str, str, int]]]],
                  theme: dict) -> str:
    """How the pieces run: one segmented bar per list, each with its own data date."""
    body = heading("How the pieces run",
                   "Where each piece's code comes from, as a share of each list. Each list "
                   "carries its own date.", theme)
    y = 72
    lines: list[str] = []
    for title, as_of, parts in bars:
        total = sum(count for _, _, count in parts)
        body.append(label(16, y + 4, f"{title} ({total}; as of {as_of})", theme["ink"],
                          size=12, weight="600"))
        if any(n > 1 for n in Counter(f for f, _, _ in parts).values()):
            raise ChartError(f"{title}: two classes share one colour in one bar")
        marks, _ = segmented_bar(16, y + 12, WIDTH - 32, 28,
                                 [(family, count) for family, _, count in parts], theme)
        body.extend(marks)
        entries = [(family, f"{name} ({count})", None) for family, name, count in parts]
        legend_y = y + 60
        x = 16.0
        for family, text, _ in entries:
            width = 16 + text_width(text, 12) + 18
            if x + width > WIDTH - 16:
                x, legend_y = 16.0, legend_y + 18
            row, x = legend(x, legend_y, [(family, text, None)], theme, glyphs=False)
            body.extend(row)
        lines.append(f"{title}, {total}, as of {as_of}: "
                     + ", ".join(f"{count} {name}" for _, name, count in parts))
        y = legend_y + 26
    description = "; ".join(lines) + "."
    return document("How the pieces run", description, y, body, theme)


# --------------------------------------------------------------------------
# entry point for render.py
# --------------------------------------------------------------------------


def chart_specs(load: Callable[[str], dict]) -> dict[str, tuple[str, Callable]]:
    """name -> (alt text, draw(theme) -> svg). `load` reads a data file by name."""
    milestones = load("milestones")
    components = load("components")
    boot = load("boot-programs")
    translator = load("translator")
    gaps = load("gaps")
    kexts = load("kexts")
    labels = load("launchd-labels")
    as_of = load("status")["meta"]["as_of"]

    groups = [
        ("", [("Milestones", milestones["milestones"])]),
        ("Feature matrix", [(a["title"], a["rows"]) for a in components["areas"]]),
        ("", [("Boot-path programs", boot["programs"]),
              ("Translator patches", translator["maclator_patches"]),
              ("Self-built kernel versions", translator["kernel_versions"]),
              ("On-disk edits to Apple files", translator["apple_file_edits"]),
              ("Open walls", gaps["blockers"])]),
    ]
    origin_bars = [
        ("Boot-path program rows, by how each runs", boot["meta"]["as_of"],
         origin_parts(Counter(p["runs_as"] for p in boot["programs"]),
                      list(boot["meta"]["runs_as"]))),
        ("Listed launchd job labels on the furthest root, by where the program comes from",
         labels["meta"]["as_of"],
         origin_parts(Counter(x["class"] for x in labels["labels"]),
                      list(labels["meta"]["classes"]))),
        ("Kernel-collection entries, by where each comes from", kexts["meta"]["as_of"],
         origin_parts(Counter(k["class"] for k in kexts["kexts"]),
                      list(kexts["meta"]["classes"]))),
    ]

    met = sum(1 for m in milestones["milestones"] if m["state"] == "done")
    first_met = sum(1 for m in milestones["milestones"] if m.get("date"))
    total = len(milestones["milestones"])
    return {
        "milestones": (
            (f"Milestone chart: tiles show each of the {total} milestones in the order set, "
             f"by its state now ({met} met); a step line counts milestones by the date each "
             f"was first met ({first_met} so far). Every milestone is also in the table of "
             "docs/milestones.md."),
            lambda theme: milestones_chart(milestones, theme)),
        "status-overview": (
            ("Bar chart: for each progress table, the share of its rows that are done, in "
            "progress, not started or superseded. The same counts are in the status table of "
            "docs/progress.md."),
            lambda theme: status_chart(groups, as_of, theme)),
        "feature-matrix": (
            ("Tile chart: every feature-matrix row as a tile, a column per area, marked "
            "done, in progress or not started. Every row is also in the tables of "
            "docs/components.md."),
            lambda theme: feature_grid_chart(components, theme)),
        "how-pieces-run": (
            ("Segmented bars: the boot-path program rows, the listed launchd job labels and "
            "the kernel-collection entries, split by where their code comes from (Apple's "
            "x86_64 code, lifted, translated, macOS 26, other, not running yet). The same counts are in the tables of "
            "docs/progress.md."),
            lambda theme: origins_chart(origin_bars, theme)),
    }
