# How to read the tables

[&larr; back to the README](../README.md)


Every row of a progress table carries how strongly it is known. This is the most
important convention here:

| Label | Means |
|---|---|
| **measured** | seen in a boot or a test. The `n` column says how many boots or cases |
| **inferred** | a reading that follows from something measured, but that nobody has measured directly |
| **not measured** | unknown |

`n` is usually small. Many rows are **one boot of one configuration**, and several were
taken on a lab machine under heavy load; read each row's `n` before generalising. A single boot is enough to show that something
can work; it is not enough to show that it works reliably, and nothing here should be
read as the latter. Where a figure is a count of test cases rather than boots, the note
says so.

The two inventories (kernel-collection entries and `launchd` job labels) are not rated
row by row: each page, and the `meta` block of its JSON, says once what in it was
measured and what was inferred. For the `launchd` labels, where a program comes from and
whether a process existed are measured; which binary was executing is inferred from what
was placed on disk, except for `launchd` and `xpcproxy`.

The state words mean:

| State | Means |
|---|---|
| **done** | 27's own piece (or a piece needing no replacement) is in place and was seen working at least once |
| **in progress** | a stand-in is still used, or 27's piece runs but hits a known wall |
| **not started** | nothing runs yet |

In the translator patch tables, *done* means only that a patch is built and tested.
