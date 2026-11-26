# Maintaining this record

[&larr; back to the README](../README.md)

Notes for whoever updates the record. They say which files an update touches, so that
the README stays a stable front page and the pages under `docs/` carry the figures.

## A routine update

A routine update is a new snapshot of the figures: new rows, new counts, new results in
existing rows, a corrected wording. It touches only:

- `data/*.json`, the source of every generated table and chart;
- the hand-written prose of [docs/progress.md](progress.md) (its *Where it stands*
  section and its date), and of any other page under `docs/` whose subject changed;
- [UPSTREAMS.md](../UPSTREAMS.md), when the upstream projects or this project's items with
  them changed;
- the generated regions and the charts, by running `python3 scripts/render.py`;
- [CHANGELOG.md](../CHANGELOG.md) and the version and date in
  [CITATION.cff](../CITATION.cff).

It does **not** touch `README.md`. Check before committing: `git diff --stat` should not
list it, and `python3 scripts/render.py --check` must pass.

## A major milestone

The README changes only at a major milestone. Its generated block shows how many
milestones are met out of how many set, the ones most recently met with their titles and
date, and the ones not met yet with their titles; the README changes exactly when one of
those shown fields changes in `data/milestones.json` (in practice: a milestone first met,
a new one set, one superseded, or a shown title corrected), and `render.py --check` fails
until it is re-rendered, which is the signal. A milestone moving from *not started* to *in progress*,
or a change to its notes, leaves the README as it is. Edit the README's hand-written text at the same time only where the milestone
makes it untrue. A new boot count, a new row in another table or a new result is not a
major milestone; it belongs on the progress page.

The charts are files of their own, so the README's charts change at every update without
`README.md` itself changing. Their descriptions (the alternative text) are generated too;
the milestones one carries the number met, so it changes with the README.

## Versions

[CHANGELOG.md](../CHANGELOG.md) states the rule: **major** when a claim is withdrawn or a
state goes backwards, **minor** for new rows, new pages or new results, **patch** for
corrections and wording. A change to layout alone, with nothing withdrawn, is minor if it
adds a page and a patch otherwise.

## Before publishing

Every update is checked before it is pushed: a scan for anything private, and a review of
the change. On how-to guides the record keeps the position stated in the README and in
[CONTRIBUTING.md](../CONTRIBUTING.md).
