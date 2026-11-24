# Running macOS 27 on x86 hardware

A progress record for a hobby research project: getting macOS 27, which Apple ships
for Apple silicon only, to boot and run on an ordinary x86-64 PC as a virtual machine
guest.

This repository holds the **progress tables and the notes that explain them**, not the
work itself. There is no build or translation tooling, no disk image and no Apple code
here. Disk images and Apple code never will be: the images are built from Apple's own
files, and those files are Apple's. There are no how-to guides today either;
dated, best-effort guides are planned later. The only code here is [`scripts/render.py`](scripts/render.py),
which renders the tables. What is here is a record of what has been tried, what was
measured, and what is still broken, kept in machine-readable form under [`data/`](data)
and rendered into the tables below.

## What is being attempted

macOS 27.0.1 is an Apple-silicon release. Its installer and its boot path are built for
arm64e. But Apple has not finished removing x86-64 from the operating system: most of
the frameworks still carry an x86-64 slice, and 27.0.1's Kernel Debug Kit still ships an
x86-64 kernel. What is missing is the boot path &mdash; `launchd`, `amfid`, `logd`,
`sandboxd`, `kernelmanagerd`, `WindowServer`'s launcher and many daemons are arm64e-only:
of the 421 `launchd` job labels listed in [docs/launchd-labels.md](docs/launchd-labels.md),
122 run a program that 27.0.1 ships without an x86-64 slice (117 distinct programs).

The project closes that gap three ways, and most of the tables below are really about
which of the three each piece is using today:

1. **Apple's own x86-64 code**, where 27.0.1 still ships it, used as Apple shipped it
   apart from the few edits listed in
   [docs/translator-patches.md](docs/translator-patches.md#on-disk-edits-to-apple-files).
2. **Recompiling** Apple's arm64e build to x86-64, function by function, and linking it
   against 27's own x86-64 libraries. The project calls this *lifting*. Where a
   user-space row gives a count of functions that pass, the recompiled functions were run
   against Apple's originals under emulation from the same starting state; not every
   recompiled program has such a count, and for the kernel extension only some functions are checked that way
   ([docs/components.md](docs/components.md#tools)).
3. **Translation**: running Apple's arm64e program as itself, through an exec route added
   to a self-built kernel, with an open-source user-space translator as the engine. The
   program keeps its own Apple identity; only the instructions are someone else's problem.

Where a piece has none of the three yet, a part from macOS 26 (Tahoe) stands in, or a
small script does, and that is recorded as *in progress* rather than done. Replacing
every one of those stand-ins is the remaining work.

## How to read the tables

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

## Status at a glance

<!-- generated:readme-status:start -->
As of **2026-11-23**. Guest: **macOS 27.0.1 (build 26A434)**. Host: an ordinary x86_64 PC running Linux, QEMU and KVM.

| What | Rows | done | in progress | not started | Other | Detail |
|---|---|---|---|---|---|---|
| Milestones | 17 | 11 | 3 | 3 | &mdash; | [docs/milestones.md](docs/milestones.md) |
| Feature matrix: Host, firmware and boot loader | 5 | 3 | 2 | 0 | &mdash; | [docs/components.md](docs/components.md#host) |
| Feature matrix: Kernel | 5 | 4 | 1 | 0 | &mdash; | [docs/components.md](docs/components.md#kernel) |
| Feature matrix: Kernel extensions | 5 | 1 | 4 | 0 | &mdash; | [docs/components.md](docs/components.md#kexts) |
| Feature matrix: Boot-path userland | 9 | 4 | 5 | 0 | &mdash; | [docs/components.md](docs/components.md#userland) |
| Feature matrix: Network and remote access | 3 | 2 | 1 | 0 | &mdash; | [docs/components.md](docs/components.md#network) |
| Feature matrix: Graphics and desktop | 4 | 0 | 3 | 1 | &mdash; | [docs/components.md](docs/components.md#graphics) |
| Feature matrix: Translation tooling | 7 | 5 | 2 | 0 | &mdash; | [docs/components.md](docs/components.md#tools) |
| Boot-path programs | 27 | 11 | 15 | 1 | &mdash; | [docs/boot-programs.md](docs/boot-programs.md) |
| Translator patches | 24 | 21 | 1 | 0 | 2 superseded | [docs/translator-patches.md](docs/translator-patches.md) |
| Self-built kernel versions | 5 | 5 | 0 | 0 | &mdash; | [docs/translator-patches.md](docs/translator-patches.md#self-built-kernel-versions) |
| On-disk edits to Apple files | 8 | 8 | 0 | 0 | &mdash; | [docs/translator-patches.md](docs/translator-patches.md#on-disk-edits-to-apple-files) |
| Open walls | 21 | 7 | 10 | 4 | &mdash; | [docs/gaps.md](docs/gaps.md) |

<sub>Generated from `data/status.json`, `data/milestones.json`, `data/components.json`, `data/boot-programs.json`, `data/translator.json`, `data/gaps.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](LICENSE-CC0) (public domain).</sub>
<!-- generated:readme-status:end -->

Inventories, which are lists rather than progress trackers:

<!-- generated:readme-inventories:start -->
| Inventory | Rows | Breakdown | Detail |
|---|---|---|---|
| Kernel-collection entries | 196 | 185 apple-27-x86_64, 9 borrowed-tahoe-x86_64, 1 apple-27-lifted, 1 self-built-kernel | [docs/kexts.md](docs/kexts.md) |
| launchd job labels, by origin | 421 | 299 apple-27-x86_64, 110 apple-27-arm64e-translated, 7 apple-27-lifted, 3 borrowed-tahoe-x86_64, 2 apple-27-flags-changed | [docs/launchd-labels.md](docs/launchd-labels.md) |
| launchd job labels, by what happened in one boot | 421 | 103 ran, 15 ran but exited nonzero, 303 not started | [docs/launchd-labels.md](docs/launchd-labels.md) |
| Accepted-risk records (a selection from a register of 82), by who decided | 51 | 6 accepted by the owner, 1 bug-for-bug compatible with Apple, 4 direction set by the owner, 15 project default, 14 pending the owner, 8 fixed, 3 retired | [docs/gaps.md](docs/gaps.md#accepted-risk-records) |

<sub>Generated from `data/kexts.json`, `data/launchd-labels.json`, `data/gaps.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](LICENSE-CC0) (public domain).</sub>
<!-- generated:readme-inventories:end -->

## What has been measured

The claims the rest of the repository rests on. Each says how it is known and how many
times.

<!-- generated:readme-headline:start -->
- A root built only from macOS 27.0.1's own system volume, with a real Data volume, boots under QEMU and KVM and reaches launchd's daemon phase. *(measured, n = many boots)*
- On that root, macOS 27's own launchd (pid 1) and xpcproxy run as x86_64 programs recompiled from Apple's arm64e builds by the project's lifter. *(measured, n = 3 boots for launchd and 2 for xpcproxy, one configuration each)*
- macOS 27's own arm64e Sandbox kext, its 958 reachable functions (of 967) recompiled to x86_64, loads and enforces: file read, write and exec denies, a network deny and default-deny give the same results as native 27.0.1. *(measured, n = 2 boots on Apple's kernel image; on the self-built kernel, 2 boots agreeing on every probe row plus 1 on a later version)*
- Root logins over ssh return sw_vers 27.0.1 on x86_64. *(measured, n = 3 of 3 logins in 8 of 9 boots of the furthest configuration with a 180 s login timeout, 1 of 3 in one; 0 with a 60 s timeout, explained in docs/components.md)*
- The kernel the furthest configuration uses is built by the project from Apple's published xnu source (macOS 26.5's), plus the interfaces 27 needs, re-derived from 27's own x86_64 machine code. It is not Apple's kernel and reports version 25.5.0. *(measured, n = build reproduced for each version)*

<sub>Generated from `data/status.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](LICENSE-CC0) (public domain).</sub>
<!-- generated:readme-headline:end -->

## What is not shown yet

This list is the point of the page. It is kept at least as current as the one above,
because a progress record that lists only the wins is not a record of anything.

<!-- generated:readme-not-shown:start -->
- No desktop on the 27-only root. On overlays of it, with the hybrid image's two display byte edits also placed in its cache, 27's WindowServer stays up; in 5 of 6 such boots it showed the boot progress window (Apple's logo and a progress bar), and in the remaining boot the screen stayed on the text console. None showed a login window. In one boot the login agent (SecurityAgent) logged that it was showing its window while its main thread stayed blocked waiting for a reply that never came; WindowServer had also refused it the front once. Which of these holds the window back is not settled. Full windows are shown only on a hybrid image (macOS 26's recovery volume with 27's files placed over it), which draws the recovery window, Disk Utility and the installer with a software compositor.
- The kernel is self-built from Apple's macOS 26.5 source, not Apple's 27.0.1 kernel. Apple's own 27.0.1 x86_64 kernel also boots, but only with load-time patches.
- No GPU acceleration: there is no Metal device.
- Pieces of macOS 26 (Tahoe) are still in the boot: the x86 boot loader (boot.efi, which 27.0.1 does not ship), nine kexts, the tool that builds the kernel collection, and the APFS driver the boot loader uses. 27's own logd and logd_helper replaced macOS 26's in three boots.
- The ssh logins are to a debug sshd the test payload starts, not to launchd's own sshd job, and that sshd is 27's arm64e program under translation.
- macOS 27's own amfid runs under translation and stays up (4 boots). In one boot it refused an ad hoc signed program carrying a restricted entitlement, as Apple's does; whether it answers every signature check correctly has not been tested, and an edited-signature test did not discriminate.
- sandboxd is not shown staying up when launchd starts it. With an earlier fix, a hand-started copy got past the failure in 2 of 2 boots, while the launchd-started copy kept restarting in the second (it ran with a trace option the hand-started one did not). That fix (patch X) had an open race and has been replaced by patch Y, whose boots are not written up in this record yet.
- The 240-second registry stall early in boot is explained, and two fixes for it work in test boots (docs/gaps.md, B18), but neither is in the furthest configuration yet; without one, the network attaches only after the stall. The HID driver extension's crash at start has a fix that held in 3 boots, but keyboard and mouse input does not work yet: in two boots WindowServer logged the process holding keyboard focus as the destination of key presses, while the last pointer events seen were in the HID queue.
- For most programs only 'running' was measured, not that they do their job.
- Many results are one boot per configuration, often on a heavily loaded lab host. Behaviour past a 1-minute load average of about 100 has not been tested systematically; the first-run timings in docs/gaps.md (B15) were taken at a load of 130 to 198.
- Lifted programs that must be platform binaries are signed with a lab key that Apple's developer trusted-key mechanism is told to trust. That is a lab arrangement, not something a user install could rely on.

<sub>Generated from `data/status.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](LICENSE-CC0) (public domain).</sub>
<!-- generated:readme-not-shown:end -->

Two further limits worth stating plainly, because no single row carries them:

- **Nothing here is a usable macOS install.** There is no desktop on the 27-only root,
  no graphics acceleration, and the parts that work do so in a lab configuration
  assembled by hand for each boot. Nobody should read this as a route to running macOS 27
  on their own PC.
- **"Runs" mostly means "was running".** For most programs the measurement is that the
  process existed and did not die. Whether it actually did its job was measured for only
  a handful of them, and the tables say which.

## Detail

<!-- generated:readme-details:start -->
<details>
<summary><strong>Milestones</strong> &mdash; 11 done, 3 in progress, 3 not started</summary>

|  | Milestone | State | First met |
|---|---|---|---|
| M0 | Harness control: macOS 26 x86 recovery boots under QEMU, KVM and OpenCore | done | 2026-10-26 |
| M1a | Build a kernel collection around 27.0.1's x86_64 kernel | done | 2026-10-26 |
| M1 | Boot 27.0.1's x86_64 kernel | done | 2026-10-26 |
| M1b | Map the commpage into user processes | done | 2026-10-26 |
| M2 | 27's x86_64 frameworks under macOS 26's boot daemons | done | 2026-10-26 |
| M3 | 27's own userland: 27's x86_64 dyld, shared cache and programs | done | 2026-10-27 |
| G1 | A window on screen (hybrid image) | done | 2026-10-26 |
| R1 | A root built only from 27.0.1's own system volume | done | 2026-11-04 |
| R2 | 27's own Sandbox kext, recompiled to x86_64, enforcing | done | 2026-11-04 |
| R3 | A kernel built from Apple's published source boots 27.0.1 | done | 2026-11-04 |
| R4 | 27's own launchd as pid 1 and xpcproxy, recompiled | done | 2026-11-08 |
| R5 | 27's own amfid, logd, logd_helper and sandboxd in place of macOS 26's | in progress | &mdash; |
| R6 | Fold the furthest configuration into one disk image | not started | &mdash; |
| R7 | launchd's own sshd reachable from the host | not started | &mdash; |
| R8 | No macOS 26 piece left in the boot | in progress | &mdash; |
| M4 | A desktop on 27's own programs | in progress | &mdash; |
| M5 | Graphics acceleration | not started | &mdash; |

Pass conditions, evidence and notes: [docs/milestones.md](docs/milestones.md).

</details>

<details>
<summary><strong>Feature matrix, by area</strong> &mdash; 19 done, 18 in progress, 1 not started</summary>

| Area | Rows | done | in progress | not started |
|---|---|---|---|---|
| Host, firmware and boot loader | 5 | 3 | 2 | 0 |
| Kernel | 5 | 4 | 1 | 0 |
| Kernel extensions | 5 | 1 | 4 | 0 |
| Boot-path userland | 9 | 4 | 5 | 0 |
| Network and remote access | 3 | 2 | 1 | 0 |
| Graphics and desktop | 4 | 0 | 3 | 1 |
| Translation tooling | 7 | 5 | 2 | 0 |

Every row, with what runs there today: [docs/components.md](docs/components.md).

</details>

<details>
<summary><strong>Boot-path programs</strong> &mdash; 11 done, 15 in progress, 1 not started</summary>

| How it runs | Rows |
|---|---|
| Apple x86_64 | 3 |
| lifted | 13 |
| translated | 9 |
| stand-in | 1 |
| none | 1 |

Every program, with its note: [docs/boot-programs.md](docs/boot-programs.md).

</details>

<details>
<summary><strong>Translator patches</strong> &mdash; 21 done, 1 in progress, 0 not started, 2 superseded</summary>

No long-lived fork. Every Maclator patch is meant to go upstream as a small, clean change framed around that project's own goals; patch J still needs splitting first. The upstream cut of patch G was merged on 2026-11-10 (de04499f, pull request #12); patch K was posted on 2026-11-23 (pull request #16) and is open; the rest have not been posted.

Every patch, what it fixes and how it was tested: [docs/translator-patches.md](docs/translator-patches.md).

</details>

<details>
<summary><strong>Open walls</strong> &mdash; 7 done, 10 in progress, 4 not started</summary>

|  | Wall | State |
|---|---|---|
| B1 | Identity of a program under translation | done |
| B2 | No Data volume beside 27's system volume | done |
| B3 | Mounting the Preboot volume needs an arm64e-only program | in progress |
| B4 | No x86_64 Sandbox kext for 27 | done |
| B5 | fork safety under translation | in progress |
| B6 | pid 1 from 27's own launchd | in progress |
| B7 | Display-state mismatch and the backdrop abort (hybrid image) | done |
| B8 | No GPU | not started |
| B9 | Building the kernel collection with 27's own tools | in progress |
| B10 | 27's own logd | in progress |
| B11 | 27's own amfid | in progress |
| B12 | Daemons that run but do not yet serve | in progress |
| B13 | DEVELOPMENT build of the self-built kernel | not started |
| B14 | A circular wait at exec that could freeze the boot | done |
| B15 | The first translated run of a boot is slow | not started |
| B16 | File flags lost on the Data volume | done |
| B17 | 27's sandboxd staying up under launchd is not shown | in progress |
| B18 | The 240-second registry stall and the HID driver extension | in progress |
| B19 | A launchd-managed sshd on the furthest configuration | not started |
| B20 | Stopping a service panicked the guest | done |
| B21 | No login window on the display test overlays | in progress |

Notes, and the accepted-risk records beside them: [docs/gaps.md](docs/gaps.md).

</details>

<sub>Generated from `data/milestones.json`, `data/components.json`, `data/boot-programs.json`, `data/translator.json`, `data/gaps.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](LICENSE-CC0) (public domain).</sub>
<!-- generated:readme-details:end -->

Each section above links to a full page:

| Page | What it holds |
|---|---|
| [docs/milestones.md](docs/milestones.md) | Milestones, with the pass condition each one had to meet |
| [docs/components.md](docs/components.md) | The feature matrix: every layer, and what runs there today |
| [docs/boot-programs.md](docs/boot-programs.md) | Boot-path programs (a few rows group several), with what is and is not known |
| [docs/launchd-labels.md](docs/launchd-labels.md) | The `launchd` job labels on the furthest booted root whose program paths are on 27.0.1's system volume or, for five, its Data-volume template |
| [docs/kexts.md](docs/kexts.md) | Every entry of the kernel collection that root booted with |
| [docs/translator-patches.md](docs/translator-patches.md) | Translator patches, kernel versions, and the on-disk edits to Apple files |
| [docs/gaps.md](docs/gaps.md) | Open walls, and the record of risks that were accepted rather than fixed |
| [docs/notes-for-liberator.md](docs/notes-for-liberator.md) | Two DriverKit findings written up for other projects booting macOS 27 on Intel |

## The data, and how these tables are made

Every progress table and inventory in this repository is generated; the few short tables
outside the generated regions (the reading guide, the page list and the licence table)
are hand-written. The source of truth is `data/*.json`; the Markdown is built from it by
[`scripts/render.py`](scripts/render.py), which needs only Python 3 and the standard
library.

<!-- generated:readme-data-index:start -->
| File | Rows | What it holds |
|---|---|---|
| `data/status.json` | 5 | Headline claims and what is not shown yet |
| `data/milestones.json` | 17 | Milestones, in the order they were set |
| `data/components.json` | 38 | The feature matrix, by layer |
| `data/boot-programs.json` | 27 | Boot-path programs; a few rows group several |
| `data/launchd-labels.json` | 421 | launchd job labels on the furthest root whose program paths are on 27.0.1's system volume or, for five, its Data-volume template |
| `data/kexts.json` | 196 | Every kernel-collection entry |
| `data/translator.json` | 37 | Translator patches, kernel versions, on-disk edits |
| `data/gaps.json` | 72 | Open walls and the accepted-risk records |

<sub>Generated from `data/status.json`, `data/milestones.json`, `data/components.json`, `data/boot-programs.json`, `data/launchd-labels.json`, `data/kexts.json`, `data/translator.json`, `data/gaps.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](LICENSE-CC0) (public domain).</sub>
<!-- generated:readme-data-index:end -->

```sh
python3 scripts/render.py           # rewrite the generated regions in place
python3 scripts/render.py --check   # exit 1 if any file differs from the data
```

Generated regions are delimited by `<!-- generated:NAME:start -->` and
`<!-- generated:NAME:end -->`. Prose outside those markers is hand-written and the
renderer never touches it. `--check` is what
[CI](.github/workflows/check.yml) runs, so an edit made inside a generated region by
hand, or a change to `data/` that nobody re-rendered, fails the build rather than
quietly leaving the page disagreeing with the data.

The figures are a snapshot. The project's working notes are kept privately; each
snapshot records which internal revision it reflects, in `data/status.json`, so that a
later update can say what changed between the two.

## Repository layout

```
data/        the numbers, as JSON. Every generated progress table and inventory
             is rendered from these
docs/        one page per large table, with the notes that explain it
scripts/     render.py, which builds the tables
```

## Licences

Stated per directory and file, because the three kinds of content here are not under the same
terms:

| Directory | Content | Licence |
|---|---|---|
| `scripts/`, `.github/workflows/check.yml` | code | **MIT OR Apache-2.0** ([MIT](LICENSE-MIT), [Apache-2.0](LICENSE-APACHE)) |
| `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `docs/` | prose and write-ups | **MIT OR Apache-2.0 OR CC-BY-4.0** ([CC-BY-4.0](LICENSE-CC-BY-4.0)) |
| `data/`, and every generated table | data and generated tables | **CC0-1.0** ([CC0-1.0](LICENSE-CC0)), public domain |
| `CITATION.cff` | citation metadata | **CC0-1.0** |

`OR` is as in [SPDX](https://spdx.dev/): you may take whichever of the listed licences
you prefer. The data is CC0 so that the measurements can be quoted, checked and
re-used with no attribution requirement at all; every generated region carries that
notice beneath it.

No Apple code, and no file from macOS, is in this repository. The tables name Apple's
programs, their paths and its kernel-extension identifiers in order to describe them;
none of the licences above covers anything of Apple's.

## What this project does and does not do

This is a non-commercial research record. It documents an attempt to understand how
macOS boots, and whether it can be made to run as a guest on x86 hardware the author
owns. It is not affiliated with, sponsored by or endorsed by Apple Inc.

We keep to these rules:

- This repository contains no Apple software: no binaries, disk images, installers,
  firmware, kernel caches, keys, or disassembled or decompiled Apple code. It describes
  what was changed and measured, not the bytes.
- Anyone working in this area must use their own copy of macOS, obtained from Apple, and
  is responsible for the terms under which they obtained it. Apple's licence for macOS
  limits it to Apple-branded hardware; read it before you do anything.
- The repository contains no tool or instructions for circumventing any technical
  protection measure.
- The images are built and the guests are run privately, on the author's own hardware. No
  macOS image or running guest is sold, hosted or offered as a service, and the project
  takes no payment.
- Apple, Mac and macOS are trademarks of Apple Inc., used here only to say what the
  research concerns.

Courts have recognised that research uses of an operating system can be fair use: in
*Apple Inc. v. Corellium, Inc.* (S.D. Fla. 2020; 11th Cir. 2023, unpublished,
non-precedential), copying iOS into a security-research tool that added its own features
was held to be fair use. That case did not decide whether the product violated the
anti-circumvention rules (that claim settled), although the trial court held that fair
use is no defence to them; it decided no claim under Apple's licence, and concerned
security research rather than this project's goal. We cite it to explain why research of
this kind is worth recording, not as a claim that this work is lawful.

This is not legal advice. If you have concerns about your own situation, consult a
lawyer.

## Contributing

Corrections to the measurements are the most useful thing anyone can send. See
[CONTRIBUTING.md](CONTRIBUTING.md) for how the data files are shaped and why a
correction has to edit `data/` rather than the rendered table.

## Citing

See [CITATION.cff](CITATION.cff). Please cite the date and the snapshot's internal
revision along with it, since the figures move.
