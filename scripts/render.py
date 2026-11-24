#!/usr/bin/env python3
"""Render the generated tables in README.md and docs/*.md from data/*.json.

Every generated region in a Markdown file is delimited by a pair of fixed
comment markers:

    <!-- generated:NAME:start -->
    ...anything here is replaced...
    <!-- generated:NAME:end -->

`render.py` with no arguments rewrites every such region in place.
`render.py --check` renders to memory and compares, printing a unified diff and
exiting 1 if any file on disk differs from what the data says it should be. That
is what CI runs, so a hand edit inside a generated region, or a change to
data/*.json that nobody re-rendered, fails the build instead of going unnoticed.

Prose outside the markers is hand-written and is never touched.

Markers are located by fixed-string prefix and suffix rather than by regular
expression, per this project's style rule: matching is exact, so a marker either
is one or is not, and a malformed marker raises instead of silently not matching.

Standard library only, so the check needs no install step.

Exit codes:
    0  everything rendered (write mode), or no drift (--check)
    1  drift found (--check only)
    2  a usage, data or marker error: nothing was written
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from collections import Counter
from pathlib import Path

VERSION = "1.1.1"
RELEASED = "2026-11-22"

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data"

START_PREFIX = "<!-- generated:"
START_SUFFIX = ":start -->"
END_PREFIX = "<!-- generated:"
END_SUFFIX = ":end -->"

# The three state words every ordered table in data/ uses, in reporting order.
# A table may add its own extra states (for example "superseded"); those are
# reported after these three rather than being folded into them.
CANONICAL_STATES = ("done", "in progress", "not started")

CC0_URL_FROM_ROOT = "LICENSE-CC0"


class DataError(Exception):
    """A data or marker problem that must stop the run."""


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------


def load(name: str) -> dict:
    path = DATA_DIR / f"{name}.json"
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise DataError(f"missing data file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DataError(f"{path}: invalid JSON: {exc}") from exc


def cell(value: object) -> str:
    """One Markdown table cell: never empty, never containing a raw pipe."""
    if value is None:
        return "&mdash;"
    text = str(value).strip()
    if not text:
        return "&mdash;"
    # A newline or a pipe would end the cell or the row early.
    text = " ".join(text.split())
    return text.replace("|", "\\|")


def code(value: object) -> str:
    text = cell(value)
    if text == "&mdash;":
        return text
    return f"`{text}`"


def table(headers: list[str], rows: list[list[object]]) -> list[str]:
    """A GitHub-flavoured Markdown table as a list of lines."""
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        if len(row) != len(headers):
            raise DataError(f"row has {len(row)} cells, want {len(headers)}: {row!r}")
        out.append("| " + " | ".join(cell(v) for v in row) + " |")
    return out


def state_counts(rows: list[dict], key: str = "state") -> "Counter[str]":
    return Counter(row.get(key) or "not stated" for row in rows)


def canonical_triple(counts: "Counter[str]") -> tuple[int, int, int]:
    return tuple(counts.get(state, 0) for state in CANONICAL_STATES)  # type: ignore[return-value]


def extra_states(counts: "Counter[str]") -> str:
    """The states a table uses beyond the canonical three, as readable text."""
    extras = [(k, v) for k, v in sorted(counts.items()) if k not in CANONICAL_STATES]
    if not extras:
        return ""
    return ", ".join(f"{v} {k}" for k, v in extras)


def counts_sentence(counts: "Counter[str]") -> str:
    """The canonical three counts, then any extra states this table uses."""
    done, progress, not_started = canonical_triple(counts)
    parts = [f"{done} done", f"{progress} in progress", f"{not_started} not started"]
    extra = extra_states(counts)
    if extra:
        parts.append(extra)
    return ", ".join(parts)


def summary_line(title: str, counts: "Counter[str]") -> str:
    return f"<summary><strong>{title}</strong> &mdash; {counts_sentence(counts)}</summary>"


# A few state words read badly inside a comma-separated list, because they contain a
# comma themselves. These are how they are phrased in running text.
PHRASING = {
    "ran, nonzero exit status": "ran but exited nonzero",
}

LAUNCHD_STATE_ORDER = ["ran", "ran, nonzero exit status", "not started"]


def breakdown(counts: "Counter[str]", order: list[str] | None = None) -> str:
    """Counts as readable text, in a given key order where one is supplied."""
    if order is None:
        keys = sorted(counts)
    else:
        keys = [k for k in order if k in counts] + [k for k in sorted(counts) if k not in order]
    return ", ".join(f"{counts[k]} {PHRASING.get(k, k)}" for k in keys)


def stamp(sources: list[str], depth: int) -> list[str]:
    """The per-table provenance and CC0 notice.

    `depth` is how many directories below the repository root the file sits, so
    that the licence link resolves from README.md and from docs/*.md alike.
    """
    prefix = "../" * depth
    names = ", ".join(f"`data/{s}.json`" for s in sources)
    return [
        "",
        f"<sub>Generated from {names} by `scripts/render.py`. "
        f"Data and generated tables: "
        f"[CC0-1.0]({prefix}{CC0_URL_FROM_ROOT}) (public domain).</sub>",
    ]


def details(title: str, counts: "Counter[str]", body: list[str]) -> list[str]:
    """A collapsible section whose summary carries the counts."""
    out = ["<details>", summary_line(title, counts), ""]
    out.extend(body)
    out.extend(["", "</details>"])
    return out


# --------------------------------------------------------------------------
# block renderers
#
# Each takes the depth of the file it is being rendered into and returns a list
# of lines. Registered in BLOCKS at the bottom.
# --------------------------------------------------------------------------


def block_readme_status(depth: int) -> list[str]:
    status = load("status")
    milestones = load("milestones")
    components = load("components")
    boot = load("boot-programs")
    translator = load("translator")
    gaps = load("gaps")

    rows: list[list[object]] = []

    def add(what: str, items: list[dict], link: str) -> None:
        counts = state_counts(items)
        done, progress, not_started = canonical_triple(counts)
        rows.append([what, len(items), done, progress, not_started,
                     extra_states(counts) or None, link])

    add("Milestones", milestones["milestones"], "[docs/milestones.md](docs/milestones.md)")
    for area in components["areas"]:
        add(f"Feature matrix: {area['title']}", area["rows"],
            f"[docs/components.md](docs/components.md#{area['id']})")
    add("Boot-path programs", boot["programs"],
        "[docs/boot-programs.md](docs/boot-programs.md)")
    add("Translator patches", translator["maclator_patches"],
        "[docs/translator-patches.md](docs/translator-patches.md)")
    add("Self-built kernel versions", translator["kernel_versions"],
        "[docs/translator-patches.md](docs/translator-patches.md#self-built-kernel-versions)")
    add("On-disk edits to Apple files", translator["apple_file_edits"],
        "[docs/translator-patches.md](docs/translator-patches.md#on-disk-edits-to-apple-files)")
    add("Open walls", gaps["blockers"], "[docs/gaps.md](docs/gaps.md)")

    out = [
        f"As of **{status['meta']['as_of']}**. "
        f"Guest: **{status['release']['macos']}**. "
        f"Host: {status['release']['host']}.",
        "",
    ]
    out.extend(table(
        ["What", "Rows", "done", "in progress", "not started", "Other", "Detail"],
        rows,
    ))
    out.extend(stamp(["status", "milestones", "components", "boot-programs",
                      "translator", "gaps"], depth))
    return out


def block_readme_inventories(depth: int) -> list[str]:
    kexts = load("kexts")
    labels = load("launchd-labels")
    gaps = load("gaps")

    kext_classes = Counter(k["class"] for k in kexts["kexts"])
    label_classes = Counter(x["class"] for x in labels["labels"])
    label_states = Counter(x["state"] for x in labels["labels"])
    decisions = Counter(r["decision"] for r in gaps["risks"])

    rows: list[list[object]] = [
        ["Kernel-collection entries", len(kexts["kexts"]),
         breakdown(kext_classes, list(kexts["meta"]["classes"])),
         "[docs/kexts.md](docs/kexts.md)"],
        ["launchd job labels, by origin", len(labels["labels"]),
         breakdown(label_classes, list(labels["meta"]["classes"])),
         "[docs/launchd-labels.md](docs/launchd-labels.md)"],
        ["launchd job labels, by what happened in one boot", len(labels["labels"]),
         breakdown(label_states, LAUNCHD_STATE_ORDER),
         "[docs/launchd-labels.md](docs/launchd-labels.md)"],
        [f"Accepted-risk records (a selection from a register of {gaps['meta']['register_total']}), by who decided", len(gaps["risks"]),
         breakdown(decisions, list(gaps["meta"]["decisions"])),
         "[docs/gaps.md](docs/gaps.md#accepted-risk-records)"],
    ]

    out = table(["Inventory", "Rows", "Breakdown", "Detail"], rows)
    out.extend(stamp(["kexts", "launchd-labels", "gaps"], depth))
    return out


def block_readme_headline(depth: int) -> list[str]:
    status = load("status")
    out: list[str] = []
    for item in status["headline"]:
        out.append(f"- {item['claim']} "
                   f"*({item['evidence']}, n = {cell(item.get('n'))})*")
    out.extend(stamp(["status"], depth))
    return out


def block_readme_not_shown(depth: int) -> list[str]:
    status = load("status")
    out = [f"- {line}" for line in status["not_shown"]]
    out.extend(stamp(["status"], depth))
    return out


def block_readme_details(depth: int) -> list[str]:
    milestones = load("milestones")
    components = load("components")
    boot = load("boot-programs")
    translator = load("translator")
    gaps = load("gaps")

    out: list[str] = []

    rows = [[m["id"], m["title"], m["state"], m.get("date")]
            for m in milestones["milestones"]]
    out.extend(details(
        "Milestones",
        state_counts(milestones["milestones"]),
        table(["", "Milestone", "State", "First met"], rows)
        + ["", "Pass conditions, evidence and notes: "
             "[docs/milestones.md](docs/milestones.md)."],
    ))
    out.append("")

    area_rows = []
    for area in components["areas"]:
        counts = state_counts(area["rows"])
        done, progress, not_started = canonical_triple(counts)
        area_rows.append([area["title"], len(area["rows"]), done, progress, not_started])
    out.extend(details(
        "Feature matrix, by area",
        state_counts([r for a in components["areas"] for r in a["rows"]]),
        table(["Area", "Rows", "done", "in progress", "not started"], area_rows)
        + ["", "Every row, with what runs there today: "
             "[docs/components.md](docs/components.md)."],
    ))
    out.append("")

    runs_as = Counter(p["runs_as"] for p in boot["programs"])
    out.extend(details(
        "Boot-path programs",
        state_counts(boot["programs"]),
        table(["How it runs", "Rows"],
              [[k, runs_as[k]] for k in boot["meta"]["runs_as"] if k in runs_as])
        + ["", "Every program, with its note: "
             "[docs/boot-programs.md](docs/boot-programs.md)."],
    ))
    out.append("")

    out.extend(details(
        "Translator patches",
        state_counts(translator["maclator_patches"]),
        [translator["meta"]["upstream_rule"], "",
         "Every patch, what it fixes and how it was tested: "
         "[docs/translator-patches.md](docs/translator-patches.md)."],
    ))
    out.append("")

    out.extend(details(
        "Open walls",
        state_counts(gaps["blockers"]),
        table(["", "Wall", "State"],
              [[b["id"], b["title"], b["state"]] for b in gaps["blockers"]])
        + ["", "Notes, and the accepted-risk records beside them: "
             "[docs/gaps.md](docs/gaps.md)."],
    ))

    out.extend(stamp(["milestones", "components", "boot-programs", "translator", "gaps"],
                     depth))
    return out


def block_readme_data_index(depth: int) -> list[str]:
    specs = [
        ("status.json", "status", "headline", "Headline claims and what is not shown yet"),
        ("milestones.json", "milestones", "milestones", "Milestones, in the order they were set"),
        ("components.json", "components", None, "The feature matrix, by layer"),
        ("boot-programs.json", "boot-programs", "programs", "Boot-path programs; a few rows group several"),
        ("launchd-labels.json", "launchd-labels", "labels", "launchd job labels on the furthest root whose program paths are on 27.0.1's system volume or, for five, its Data-volume template"),
        ("kexts.json", "kexts", "kexts", "Every kernel-collection entry"),
        ("translator.json", "translator", None, "Translator patches, kernel versions, on-disk edits"),
        ("gaps.json", "gaps", None, "Open walls and the accepted-risk records"),
    ]
    rows: list[list[object]] = []
    for filename, name, list_key, what in specs:
        data = load(name)
        if list_key is None:
            count = sum(len(v) for v in data.values() if isinstance(v, list))
            if name == "components":
                count = sum(len(a["rows"]) for a in data["areas"])
        else:
            count = len(data[list_key])
        rows.append([f"`data/{filename}`", count, what])
    out = table(["File", "Rows", "What it holds"], rows)
    out.extend(stamp([s[1] for s in specs], depth))
    return out


def block_components_table(depth: int) -> list[str]:
    components = load("components")
    out: list[str] = []
    for area in components["areas"]:
        counts = state_counts(area["rows"])
        done, progress, not_started = canonical_triple(counts)
        out.append(f'<h2 id="{area["id"]}">{area["title"]}</h2>')
        out.append("")
        out.append(f"{done} done, {progress} in progress, {not_started} not started.")
        out.append("")
        rows = [[r["part"], r["today"], r["state"], r["evidence"], r.get("n"), r.get("note")]
                for r in area["rows"]]
        out.extend(table(["Part", "What runs there today", "State", "Evidence", "n", "Notes"],
                         rows))
        out.append("")
    if out and out[-1] == "":
        out.pop()
    out.extend(stamp(["components"], depth))
    return out


def block_boot_programs_table(depth: int) -> list[str]:
    boot = load("boot-programs")
    rows = [[p["program"], p["apple_27"], p["runs_as"], p["state"], p["evidence"],
             p.get("n"), p.get("note")] for p in boot["programs"]]
    out = table(["Program", "How Apple ships it in 27.0.1", "How it runs here", "State",
                 "Evidence", "n", "Notes"], rows)
    out.extend(stamp(["boot-programs"], depth))
    return out


def block_launchd_summary(depth: int) -> list[str]:
    labels = load("launchd-labels")
    rows_by_class: dict[str, Counter] = {}
    for item in labels["labels"]:
        rows_by_class.setdefault(item["class"], Counter())[item["state"]] += 1

    state_order = LAUNCHD_STATE_ORDER
    rows: list[list[object]] = []
    for klass in list(labels["meta"]["classes"]):
        if klass not in rows_by_class:
            continue
        counts = rows_by_class[klass]
        rows.append([f"`{klass}`", sum(counts.values())]
                    + [counts.get(s, 0) for s in state_order])
    totals = Counter(x["state"] for x in labels["labels"])
    rows.append(["**All labels listed**", len(labels["labels"])]
                + [totals.get(s, 0) for s in state_order])

    out = table(["Where the program comes from", "Labels", "ran",
                 "ran, nonzero exit status", "not started"], rows)
    out.append("")
    out.append(labels["meta"]["left_out"])
    out.extend(stamp(["launchd-labels"], depth))
    return out


def block_launchd_table(depth: int) -> list[str]:
    labels = load("launchd-labels")
    by_class: dict[str, list[dict]] = {}
    for item in labels["labels"]:
        by_class.setdefault(item["class"], []).append(item)

    out: list[str] = []
    for klass in list(labels["meta"]["classes"]):
        items = by_class.get(klass)
        if not items:
            continue
        out.append(f"### `{klass}`")
        out.append("")
        out.append(labels["meta"]["classes"][klass] + ".")
        out.append("")
        counts = Counter(i["state"] for i in items)
        out.append("<details>")
        out.append(f"<summary><strong>{len(items)} labels</strong> &mdash; "
                   + breakdown(counts, LAUNCHD_STATE_ORDER)
                   + "</summary>")
        out.append("")
        rows = [[f"`{i['label']}`", f"`{i['program']}`", i["state"], i.get("exit_status")]
                for i in items]
        out.extend(table(["Label", "Program", "In one boot", "Exit status"], rows))
        out.append("")
        out.append("</details>")
        out.append("")
    if out and out[-1] == "":
        out.pop()
    out.extend(stamp(["launchd-labels"], depth))
    return out


def block_kexts_summary(depth: int) -> list[str]:
    kexts = load("kexts")
    counts = Counter(k["class"] for k in kexts["kexts"])
    rows = [[f"`{k}`", counts[k], kexts["meta"]["classes"][k]]
            for k in list(kexts["meta"]["classes"]) if k in counts]
    rows.append(["**All entries**", len(kexts["kexts"]), ""])
    out = table(["Class", "Entries", "What it means"], rows)
    out.extend(stamp(["kexts"], depth))
    return out


def block_kexts_table(depth: int) -> list[str]:
    kexts = load("kexts")
    by_class: dict[str, list[dict]] = {}
    for item in kexts["kexts"]:
        by_class.setdefault(item["class"], []).append(item)

    out: list[str] = []
    for klass in list(kexts["meta"]["classes"]):
        items = by_class.get(klass)
        if not items:
            continue
        out.append(f"### `{klass}`")
        out.append("")
        out.append(kexts["meta"]["classes"][klass] + ".")
        out.append("")
        out.append("<details>")
        out.append(f"<summary><strong>{len(items)} entries</strong></summary>")
        out.append("")
        out.extend(table(["Bundle identifier"], [[f"`{i['bundle']}`"] for i in items]))
        out.append("")
        out.append("</details>")
        out.append("")
    if out and out[-1] == "":
        out.pop()
    out.extend(stamp(["kexts"], depth))
    return out


def block_translator_tables(depth: int) -> list[str]:
    translator = load("translator")
    out: list[str] = []

    counts = state_counts(translator["maclator_patches"])
    out.append('<h2 id="maclator-patches">Patches to the translator</h2>')
    out.append("")
    out.append(f"{counts_sentence(counts)}.")
    out.append("")
    out.extend(table(["Patch", "Area", "What it fixes", "State", "Evidence", "n", "Notes"],
                     [[p["patch"], p["area"], p["fixes"], p["state"], p["evidence"],
                       p.get("n"), p.get("note")]
                      for p in translator["maclator_patches"]]))
    out.append("")

    out.append('<h2 id="self-built-kernel-versions">Self-built kernel versions</h2>')
    out.append("")
    out.extend(table(["Version", "What changed", "State", "Evidence", "n"],
                     [[v["version"], v["change"], v["state"], v["evidence"], v.get("n")]
                      for v in translator["kernel_versions"]]))
    out.append("")

    out.append('<h2 id="on-disk-edits-to-apple-files">On-disk edits to Apple files</h2>')
    out.append("")
    out.extend(table(["Edit", "Why", "Applied", "State", "Evidence", "n", "Notes"],
                     [[e["edit"], e["why"], e["applied"], e["state"], e["evidence"],
                       e.get("n"), e.get("note")]
                      for e in translator["apple_file_edits"]]))

    out.extend(stamp(["translator"], depth))
    return out


def block_gaps_blockers(depth: int) -> list[str]:
    gaps = load("gaps")
    counts = state_counts(gaps["blockers"])
    done, progress, not_started = canonical_triple(counts)
    out = [f"{done} closed, {progress} narrowed or being fixed, {not_started} open with no "
           "fix under way.", ""]
    out.extend(table(["", "Wall", "State", "Evidence", "Notes"],
                     [[b["id"], b["title"], b["state"], b.get("evidence"), b.get("note")]
                      for b in gaps["blockers"]]))
    out.extend(stamp(["gaps"], depth))
    return out


def block_gaps_risks(depth: int) -> list[str]:
    gaps = load("gaps")
    decisions = Counter(r["decision"] for r in gaps["risks"])
    out = [gaps["meta"]["how_gaps_are_judged"], "", gaps["meta"]["selection"], ""]
    out.extend(table(["Who decided", "Records", "What that means"],
                     [[k, decisions[k], gaps["meta"]["decisions"][k]]
                      for k in list(gaps["meta"]["decisions"]) if k in decisions]))
    out.append("")

    by_area: dict[str, list[dict]] = {}
    for risk in gaps["risks"]:
        by_area.setdefault(risk["area"], []).append(risk)
    for area in sorted(by_area):
        items = by_area[area]
        out.append("<details>")
        out.append(f"<summary><strong>{area}</strong> &mdash; {len(items)} "
                   + ("record" if len(items) == 1 else "records") + "</summary>")
        out.append("")
        out.extend(table(["", "What could go wrong", "Who decided", "Notes"],
                         [[r["id"], r["risk"], r["decision"], r.get("note")]
                          for r in items]))
        out.append("")
        out.append("</details>")
        out.append("")
    if out and out[-1] == "":
        out.pop()
    out.extend(stamp(["gaps"], depth))
    return out


def block_milestones_table(depth: int) -> list[str]:
    milestones = load("milestones")
    out = [milestones["meta"]["what"], ""]
    out.extend(table(["", "Milestone", "Pass condition", "State", "First met", "Evidence",
                      "Notes"],
                     [[m["id"], m["title"], m["pass"], m["state"], m.get("date"),
                       m["evidence"], m.get("note")]
                      for m in milestones["milestones"]]))
    out.extend(stamp(["milestones"], depth))
    return out


BLOCKS = {
    "readme-status": block_readme_status,
    "readme-inventories": block_readme_inventories,
    "readme-headline": block_readme_headline,
    "readme-not-shown": block_readme_not_shown,
    "readme-details": block_readme_details,
    "readme-data-index": block_readme_data_index,
    "components-table": block_components_table,
    "boot-programs-table": block_boot_programs_table,
    "launchd-summary": block_launchd_summary,
    "launchd-table": block_launchd_table,
    "kexts-summary": block_kexts_summary,
    "kexts-table": block_kexts_table,
    "translator-tables": block_translator_tables,
    "gaps-blockers": block_gaps_blockers,
    "gaps-risks": block_gaps_risks,
    "milestones-table": block_milestones_table,
}

TARGETS = [
    "README.md",
    "docs/components.md",
    "docs/boot-programs.md",
    "docs/launchd-labels.md",
    "docs/kexts.md",
    "docs/translator-patches.md",
    "docs/gaps.md",
    "docs/milestones.md",
]


# --------------------------------------------------------------------------
# marker handling
# --------------------------------------------------------------------------


def marker_name(line: str, suffix: str) -> str | None:
    """The block name on a marker line, or None if this is not one.

    Fixed-string, not a pattern: a line either is exactly a marker or is not.
    """
    text = line.strip()
    if not text.startswith(START_PREFIX) or not text.endswith(suffix):
        return None
    name = text[len(START_PREFIX):-len(suffix)]
    if not name or any(ch.isspace() for ch in name):
        raise DataError(f"malformed generated marker: {text!r}")
    return name


def render_file(path: Path) -> str:
    """The file's content with every generated region replaced."""
    if not path.exists():
        raise DataError(f"missing target file: {path}")
    original = path.read_text(encoding="utf-8")
    depth = len(path.relative_to(REPO).parts) - 1

    out: list[str] = []
    lines = original.split("\n")
    index = 0
    seen: list[str] = []

    while index < len(lines):
        line = lines[index]
        name = marker_name(line, START_SUFFIX)
        if name is None:
            stray = marker_name(line, END_SUFFIX)
            if stray is not None:
                raise DataError(f"{path}: end marker for {stray!r} with no start marker")
            out.append(line)
            index += 1
            continue

        if name not in BLOCKS:
            raise DataError(f"{path}: unknown generated block {name!r}; "
                            f"known blocks: {', '.join(sorted(BLOCKS))}")
        if name in seen:
            raise DataError(f"{path}: generated block {name!r} appears twice")
        seen.append(name)

        out.append(line)
        index += 1
        closed = False
        while index < len(lines):
            if marker_name(lines[index], END_SUFFIX) == name:
                closed = True
                break
            index += 1
        if not closed:
            raise DataError(f"{path}: generated block {name!r} is never closed")

        out.extend(BLOCKS[name](depth))
        out.append(lines[index])
        index += 1

    return "\n".join(out)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Render the generated tables in README.md and docs/*.md "
                    "from data/*.json.")
    parser.add_argument("--check", action="store_true",
                        help="render to memory and exit 1 if a file on disk differs; "
                             "writes nothing")
    parser.add_argument("--version", action="version",
                        version=f"render.py {VERSION} (released {RELEASED})")
    args = parser.parse_args(argv)

    try:
        rendered = {name: render_file(REPO / name) for name in TARGETS}
    except DataError as exc:
        print(f"render.py: {exc}", file=sys.stderr)
        return 2

    used = set()
    for name in TARGETS:
        for line in rendered[name].split("\n"):
            found = marker_name(line, START_SUFFIX)
            if found:
                used.add(found)
    unused = sorted(set(BLOCKS) - used)
    if unused:
        print("render.py: these blocks are defined but appear in no file, so a typo in a "
              "marker would go unnoticed: " + ", ".join(unused), file=sys.stderr)
        return 2

    if args.check:
        drifted = []
        for name in TARGETS:
            path = REPO / name
            current = path.read_text(encoding="utf-8")
            if current != rendered[name]:
                drifted.append(name)
                diff = difflib.unified_diff(
                    current.split("\n"), rendered[name].split("\n"),
                    fromfile=f"{name} (on disk)", tofile=f"{name} (from data)",
                    lineterm="", n=1)
                for diff_line in diff:
                    print(diff_line)
        if drifted:
            print("", file=sys.stderr)
            print(f"render.py --check: {len(drifted)} file(s) differ from the data: "
                  + ", ".join(drifted), file=sys.stderr)
            print("Run `python3 scripts/render.py` and commit the result.", file=sys.stderr)
            return 1
        print(f"render.py --check: {len(TARGETS)} file(s) match the data.")
        return 0

    changed = []
    for name in TARGETS:
        path = REPO / name
        if path.read_text(encoding="utf-8") != rendered[name]:
            path.write_text(rendered[name], encoding="utf-8")
            changed.append(name)
    if changed:
        print(f"render.py: rewrote {len(changed)} file(s): " + ", ".join(changed))
    else:
        print(f"render.py: {len(TARGETS)} file(s) already match the data.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
