# Contributing

The most useful contribution to this repository is **a correction to a measurement**. A
row here that is wrong, or that claims more than its evidence supports, is a worse
problem than a row that is missing.

## Edit the data, not the table

Every table inside a generated region of `README.md` and `docs/` is generated, and so is
every chart under `docs/charts/`; the few short tables outside those regions are
hand-written. If you edit a rendered table
directly, CI will fail and your edit will be overwritten the next time anyone runs the
renderer.

```sh
$EDITOR data/boot-programs.json    # make the change here
python3 scripts/render.py          # rewrite the tables
python3 scripts/render.py --check  # should print that everything matches
git add data README.md docs
```

`render.py` needs Python 3 and nothing else &mdash; no packages, no virtual environment.

Generated regions look like this, and the renderer replaces everything between the two
markers:

```markdown
<!-- generated:boot-programs-table:start -->
<!-- generated:boot-programs-table:end -->
```

Prose outside the markers is hand-written and is never touched, so a correction to the
*wording* of a page goes straight into the Markdown. Which files a routine update touches,
and when the README changes: [docs/maintaining.md](docs/maintaining.md).

## How the data files are shaped

Each file under `data/` has a `meta` object that defines its own vocabulary &mdash; the
state words it uses, the evidence levels, and what each class means &mdash; and then one
or more arrays of rows. The renderer reads the vocabulary out of `meta` rather than
hard-coding it, so adding a new state or class usually means adding it to `meta`. Adding
a state may also require updating the summary columns in `scripts/render.py`.

Two conventions matter more than the rest:

- **`evidence` is required on any row that makes a claim**, and must be `measured`,
  `inferred` or `not measured`. Do not write `measured` for something that follows from
  a measurement without having been measured; that is what `inferred` is for.
- **`n` says how much.** For `measured` rows it is the number of boots, or of test cases
  where the note makes that clear. `null` means the row records a state rather than a
  count. An `n` of 1 is normal here and should not be inflated.

Row ordering in the files is meaningful and the renderer preserves it. Milestones are in
the order they were set; feature-matrix areas run from the host upwards. Append rather
than re-sorting.

Identifiers (`M3`, `R4`, `B15`, `G-27`, patch letters) are stable and are not renumbered,
because earlier write-ups refer to them. If something is superseded, mark it and leave the
identifier alone.

## Corrections that need no evidence

Spelling, grammar, a broken link, an unclear sentence, a table that renders wrongly: send
those without ceremony.

## Corrections that do need evidence

A change to a measurement, a state or an `n` should say how you know. "This does not work
for me" is useful as an issue; it is not enough to flip a row to `not measured`, because
the row records what was observed on a specific configuration, not a general claim.

If a row's `evidence` or `n` overstates what was actually done, say so even without a
replacement figure &mdash; weakening a claim to match its evidence is always a valid
change.

## What this repository will not take

- **Apple code**, in any quantity, including small excerpts of disassembly or bytes from
  macOS files. Describe what the code does; do not paste it.
- **Tooling.** The lifter, link tools and boot recipes are not published here, and a pull
  request adding code that builds images is out of scope.
- **Instructions for running macOS on non-Apple hardware, for now.** There are none today;
  dated, best-effort guides are planned later and will be written for this repository; until
  they exist, guide contributions are not taken. This record itself is not written as a
  how-to. See the note in
  `README.md` about the terms under which Apple licenses macOS.

## Licensing of contributions

By sending a change you agree to it being licensed as the rest of that part of the
repository is: code (`scripts/` and the CI workflow) under MIT OR Apache-2.0, prose under
MIT OR Apache-2.0 OR CC-BY-4.0, and anything under `data/`, the generated tables and
`CITATION.cff` into the public domain under CC0-1.0. The per-directory table in
`README.md` is the full statement.
