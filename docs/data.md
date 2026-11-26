# The data, and how the tables and charts are made

[&larr; back to the README](../README.md)

Every table inside a generated region, and every chart, is generated; the tables outside
the generated regions (the step table on the progress page, the reading guide, the page
list, the chart list below and the licence table) are hand-written. The source of truth is `data/*.json`; the Markdown is built from it by
[`scripts/render.py`](../scripts/render.py), which needs only Python 3 and the standard
library.

<!-- generated:data-index:start -->
| File | Rows | What it holds |
|---|---|---|
| `data/status.json` | 6 | Headline claims and what is not shown yet |
| `data/milestones.json` | 26 | Milestones, in the order they were set |
| `data/components.json` | 38 | The feature matrix, by layer |
| `data/boot-programs.json` | 31 | Boot-path programs; a few rows group several |
| `data/launchd-labels.json` | 421 | launchd job labels on the furthest root whose program paths are on 27.0.1's system volume or its Data-volume template |
| `data/kexts.json` | 196 | Every kernel-collection entry |
| `data/translator.json` | 42 | Translator patches, kernel versions, on-disk edits |
| `data/gaps.json` | 78 | Open walls and the accepted-risk records |

<sub>Generated from `data/status.json`, `data/milestones.json`, `data/components.json`, `data/boot-programs.json`, `data/launchd-labels.json`, `data/kexts.json`, `data/translator.json`, `data/gaps.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:data-index:end -->

```sh
python3 scripts/render.py           # rewrite the generated regions in place
python3 scripts/render.py --check   # exit 1 if any file differs from the data
```

Generated regions are delimited by `<!-- generated:NAME:start -->` and
`<!-- generated:NAME:end -->`. Prose outside those markers is hand-written and the
renderer never touches it. `--check` is what
[CI](../.github/workflows/check.yml) runs, so an edit made inside a generated region by
hand, or a change to `data/` that nobody re-rendered, fails the build rather than
quietly leaving the page disagreeing with the data.

The figures are a snapshot. The project's working notes are kept privately; each
snapshot records which internal revision it reflects, in `data/status.json`, so that a
later update can say what changed between the two.

## The charts

The charts under [`docs/charts/`](charts) are drawn from the same data files by
[`scripts/charts.py`](../scripts/charts.py), which `render.py` calls; `--check` compares
them byte for byte as it compares the tables. Each chart is drawn twice, once for GitHub's
light theme and once for its dark theme, and the pages show the pair through a
`<picture>` element, so a reader sees the one that matches the theme they use.

| Chart | What it shows | Drawn from |
|---|---|---|
| `milestones` | Every milestone as a tile in the order set, marked by state; and milestones met, counted by the date each was first met | `data/milestones.json` |
| `status-overview` | For each progress table, the share of its rows in each state | `data/milestones.json`, `data/components.json`, `data/boot-programs.json`, `data/translator.json`, `data/gaps.json`; its date from `data/status.json` |
| `feature-matrix` | Every feature-matrix row as a tile, a column per area | `data/components.json` |
| `how-pieces-run` | The boot-path program rows, the listed `launchd` job labels and the kernel-collection entries, split by where their code comes from, each with its own date | `data/boot-programs.json`, `data/launchd-labels.json`, `data/kexts.json` |

Each colour has one meaning in every chart. For a state: green is *done*, blue is *in
progress*, gray is *not started*, and a second, fainter gray is *superseded*. For where
code comes from: violet is Apple's own x86-64 code, orange is lifted, aqua is translated,
yellow is a piece of macOS 26, magenta is anything else (named in the legend), and gray is
not running yet.

Colour is not the only cue. Each chart has a legend; state tiles carry a shape as well (a
filled disc for *done*, a half disc for *in progress*, a ring for *not started*, a slashed
ring for *superseded*); bars print their counts where they fit and keep a fixed order of
states; the status chart says how many of each table's rows are done; and every figure
in a chart is also in a table, on [docs/progress.md](progress.md) or the detail page it
belongs to. The state colours, and the origin colours, pass a colour-blind separation
check in both themes. Against the white page of the light theme, several fills (the
origin colours other than violet, and the grays) are below 3:1, so those marks rely on
their legend and labels. The number printed on a mark is white or near-black, whichever
reads better on that fill.
