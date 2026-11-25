# Changelog

Notable changes to this record. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions are
[semantic](https://semver.org/) &mdash; for a record of measurements, a **major** change
means a claim was withdrawn or a state went backwards, a **minor** change means new rows
or new pages or new results in existing rows, and a **patch** change means corrections and
wording.

Dates are US Pacific time. The underlying work happened over a longer period than this
file covers; the dates in [docs/milestones.md](docs/milestones.md) are the history, and
this file records only changes to the published record.

## [3.1.0] &mdash; 2026-11-24

Later the same day: the results of two more login boots, what was read in an earlier one,
and two updates to the project's items with Maclator.

### Changed

- A second boot got through the login and User Account Updater (2 boots now): Setup
  Assistant was launched anyway, although its record for the user was marked complete
  beforehand, and the screen went black in the same way, with the same final frame; the
  disk did not run out in that boot, so running out of space is not why (B22). The login
  steps' counts are 7 boots for the window and an authorized login, 5 for the session and
  2 for User Account Updater.
- R2 and B23: the first build of the one root-owned store has booted in two arrangements.
  With nearly every translated program on it, one copy and no full disk, but no login
  window (the boot 3.0.0 recorded, now with what was read in it: the guest's load rose past
  300, which may be why); named for 81 programs on the login path, a login, but 140 per-home copies made by
  the programs on another build. A later build has booted once, with no login window.
- B21: two more boots without a login window. B22: one more, which placed a per-user
  marker that may let the first login skip Setup Assistant; whether it does is not read.
  Its control boot has no result yet.
- Patch K and `UPSTREAMS.md`: a commit was added to pull request #22 (the runtime's own
  sysctl names stay usable in a forked child), and the descriptions of #19 and #22 were
  revised.

## [3.0.0] &mdash; 2026-11-24

### Added

- `docs/roadmap.md`: the two stages of the work (something that works first, then
  replacing what it leans on), what done means for the first, the dependence on Apple's
  x86-64 libraries stated plainly, the safeguards and their state, and what would change
  the plan.
- `UPSTREAMS.md`: the projects this work builds on and others close to it, with measured
  activity read on 2026-11-24, this project's open items with them, a quarterly base check,
  and how the page is kept.
- `README.md`: a dated *Where it stands* section with the first stage's steps, their dates
  and boot counts, and the two current blockers.
- Milestones L1 to L4: the login window on the 27-only root (2026-11-23), a typed login
  authorized, the user session started, and the first-login User Account Updater completed
  (2026-11-24).
- Open walls B22 (no desktop after the first login: no window of the first-login Setup
  Assistant appears) and B23 (the translator's shared-cache data fills the disk).
- Translator patches Q2 (mapping a short shared-memory object at the program's own length;
  the user session first started with it) and R2 (one root-owned store of slid shared-cache
  data for every user; built, booted once with the disk not filling, not yet through a login).
- Boot-path programs: Setup Assistant (first login), and `accountsd` with `ScreenTimeAgent`.
- Accepted-risk record G-52, which is *pending the owner*: every way programs run here needs
  Apple's x86-64 libraries, which a release after macOS 27 may drop.

### Changed

- The record is refreshed as of 2026-11-24.
- B21 is closed: the login window appears; whether it does looks like a race with the
  guest's display going to sleep (inferred from one boot's timing). The Liberator notes page says so in a dated update.
- `loginwindow` is recorded as running *translated*, which is how it runs in the login
  boots; the recompiled build still exits with status 70.
- `xpcproxy`, relinked with the newer link tools, lets the two `launchd` jobs that name a
  cryptex start; the link tools' row says so.
- The project's default test base, adopted on 2026-11-24, carries the registry-stall fix
  that adds Apple's x86-64 `IOUserSerial.kext` to the boot collection, and the translator
  build with Q2 as its default translator; the rows that named "not in the furthest
  configuration yet" say so.
- Keyboard input typed at the login window reaches it; the earlier "keyboard and mouse
  input does not work yet" is replaced. Whether a click reaches a control is not tested.
- The translator: the earlier "no long-lived fork" is replaced. The changes the project
  runs are kept on a public branch of its fork, and each change that fits upstream is still
  offered there. The withdrawn "no long-lived fork" statement makes this a major version.
  Pull requests #17, #18, #19 and #22 and issues #20 and #21, posted on
  2026-11-23, are recorded, all open.
- The risks table is 52 rows drawn from a register of 83.

## [2.0.0] &mdash; 2026-11-23

### Added

- A decision for accepted-risk records, *bug-for-bug compatible with Apple* (the term is
  Wine's, for its aim of "bug-for-bug" compatibility with Windows): the project's
  behaviour equals Apple's own on the hardware macOS 27 ships on, a stricter choice was
  possible and was declined, and the record is looked at again if Apple changes. G-34 is
  its first record.
- `docs/notes-for-liberator.md`: two DriverKit findings written up for other projects
  booting macOS 27 on Intel (the registry stall's cause and its two fixes, and the
  DriverKit `libdyld` calling dyld one table slot short), with the boots each rests on and
  what was not tested.
- An open wall, B21: no login window on the display test overlays, so the open-walls table
  has 21 rows.
- Two on-disk edits to Apple files: the DriverKit shared cache's eight `libdyld`
  forwarding stubs moved up one slot (3 boots), and a DriverKit serial extension moved out
  of the scanned folder (7 boots).

### Changed

- The record is refreshed as of 2026-11-23:
  - B18: the 240-second registry stall is explained, with two fixes measured in test boots
    (Apple's x86_64 `IOUserSerial.kext` added to the boot collection, 4 boots; the
    extension moved aside, 7 boots); neither is in the furthest configuration yet.
  - With the registry quiet, 27's own DiskArbitration serves the scratch-disk round in 7
    of 8 boots counted, and the recompiled `diskarbitrationd`, relinked, serves both disk
    rounds in 1 boot.
  - The HID driver extension's crash at start: its fix held in 3 boots; input does not
    work yet.
  - The link tools: a recompiled daemon that died about every 10 s at a lazy-load helper
    ran the whole boot after relinking (1 boot); `KernelEventAgent`'s row says so.
  - A later translator engine, with three more local changes (the third a change to R in two revisions), kept every disk row in a
    full comparison boot; K's follow-up and the change to R are noted.
  - The HID driver extension's row: it ships and runs an x86_64 slice, so it moves from
    *translated* (arm64e only) to Apple's x86_64.
  - Graphics: on overlays of the 27-only root, WindowServer stays up and in 5 of 6 boots
    shows the boot progress window, no login window has appeared, and render-fence timeouts were
    checked and are not the wall (n = 1 for the reading of the login agent). M4,
    `loginwindow` and the desktop rows say so.
  - Patch K posted upstream on 2026-11-23 as pull request #16, open; patch G's merged
    pull request is named (#12).
- `README.md` and `CONTRIBUTING.md`: there are no how-to guides today; dated, best-effort
  guides are planned later (the earlier "there will not be" is withdrawn for guides and
  tooling; disk images and Apple code are still never included).
- The statement: "The images are built and the guests are run privately, on the author's
  own hardware", in place of "The work is done privately".
- `CITATION.cff` names the repository's home, `willmcginnis/macos-on-x86-amd64-vm`.
- G-34 moves from *pending the owner* to *bug-for-bug compatible with Apple*: it is
  what Apple's kernel on Apple silicon does (Apple's Intel kernel is stricter), a
  stricter kernel was built and not adopted, and nothing wrong was measured.
- The short note in `README.md` on Apple's licence terms is replaced by a statement of
  what this project does and does not do. It includes a paragraph on *Apple Inc. v.
  Corellium, Inc.*, cited as the courts stated it and not as a claim that this work is
  lawful.
- `boot.efi` is named as macOS 26's (27.0.1 ships no x86 boot loader) and added to the
  lists of macOS 26 pieces still in the boot, which are now twelve files.
- WindowServer on the 27-only root: 27's arm64e WindowServer runs under translation but
  did not open the framebuffer in the boot read then, so its rows are *in progress*, not
  *not started*.
- Patch G is recorded as merged upstream on 2026-11-10 (`de04499f`), after it was posted
  on 2026-11-08; as of the 2026-11-22 snapshot the other patches had not been posted. Upstream's main branch is now at
  `2d2f5b3e`.
- The record is refreshed as of 2026-11-22.
- The translator queue is recorded as rebased onto that base (25 commits; the
  translator's tests pass when run serially), with the rows it does not carry named.
  Three single boots with the rebased translator, or a variant of it, installed are
  stated as measured and not yet diagnosed. Patch K is noted as a single change on that base, not posted as of 2026-11-22. Patch X is
  now *superseded* by Y, and the sandboxd rows say so.
- M4 (a desktop) moves from *not started* to *in progress*, to agree with the desktop
  row; its pass condition is not met.
- Further narrowing: *done* in the patch table; sandboxd stated in the past tense with
  no result claimed for patch Y; the translated class as "no x86-64 slice"; the kernel's
  added sysctl and the DEVELOPMENT comparison without a claimed cause; the HID drivers
  as crashing at start; what *not started* means for a `launchd` label; and what R7 and
  R8 still need.
- A feature-matrix row for mutation tests of the project's own tool self-tests: 603
  deliberate bugs in 31 tables, all caught in one run.
- Narrower wording from a further review: which recompiled functions are checked against
  Apple's originals; what one longer-timeout ssh boot shows; Apple's x86-64 kernel and
  the DEVELOPMENT build described by what was tried; the kernel-collection and `launchd`
  inventories described by what they list; `loginwindow` as both translated and
  recompiled; "many", not "most", rows resting on one boot; the boot tasks row; and the
  licence summary in `CONTRIBUTING.md`.
- `scripts/render.py` 1.1.1 &mdash; two table labels reworded.
- 27's own loginwindow, recompiled to x86_64, gets its own row: in one boot of an overlay
  of the 27-only root it launches and exits with status 70 every time, so it and the
  desktop row are *in progress*, not *not started*. Dock, Finder and SystemUIServer stay
  *not started*.
- The HID user drivers' crash at start is described, with its cause as read statically
  from 27.0.1's own binaries (`n` is now two boots).
- Corrections from a review of the whole record: the `n` for xpcproxy (2, not 3) and for
  sshd (9 boots); xpcroleaccountd from *done* to *in progress* (it is not shown working);
  G-34 to *pending the owner*, since it loosens a policy; patch G's evidence is its unit
  tests, not its reviews; label counts told apart from program counts; the reason for each
  display byte edit; R3 met on the hybrid image; eight, not nine, platform extensions for
  the recompile route; one Kernel Debug Kit, not each; the Sandbox kext's 958 reachable
  functions of 967; when the milestone pass conditions were written; the load figures
  for B15; and narrower wording where a claim said "every", "nothing" or "all".
- Corrections from a second pass: the `launchd` inventory's scope now names the five
  labels whose programs sit under `/Library/Apple` in the Data-volume template; the three
  XProtect labels move from `apple-27-x86_64` to `apple-27-arm64e-translated`, since 27.0.1
  ships those two programs for Apple silicon only; `com.apple.MRTd` leaves the listed
  labels, since 27.0.1's image has no MRT and that boot's job table did not hold it (421
  labels listed, from 422; 299 and 110 by class, from 303 and 107); the inventory metadata separates what was measured from what was inferred; and "every
  row" and "every table" are narrowed to the progress tables and inventories.

## [1.1.0] &mdash; 2026-11-08

### Added

- An open wall, B20 (stopping a service panicked the guest; fixed), so 20 open walls.
- A short note in `README.md` on Apple's licence terms.
- `scripts/render.py` 1.1.0 &mdash; says on each page that the accepted-risk table is a
  selection from a larger register.

### Changed

- The two `launchd` label counts (126 of 411 and 118 of 422) now each say which labels
  they count; both are from one boot.
- 27's own amfid, logd and logd_helper now replace macOS 26's on the furthest
  configuration; the ssh login counts and their cause are stated per boot.
- Corrected the arm64e-only count in the README, the other-translator claim in the gaps
  page, and the sandbox and login `n` values.

## [1.0.0] &mdash; 2026-11-08

First snapshot, covering the project through 2026-11-08.

### Added

- `data/` &mdash; eight JSON files holding every figure on the site: headline claims and
  limits, milestones, the feature matrix, boot-path programs, 422 `launchd` job labels,
  196 kernel-collection entries, the translator and kernel patch tables, and 19 open
  walls with 51 accepted-risk records (a selection from a register of 82).
- `scripts/render.py` 1.0.0 &mdash; renders every generated table in `README.md` and `docs/`
  from `data/`, with `--check` to fail on drift. Standard library only.
- `README.md` &mdash; status at a glance, the measured claims, what is not shown yet, and
  the per-directory licence terms.
- `docs/` &mdash; seven pages: milestones, the feature matrix, boot-path programs,
  `launchd` labels, kernel-collection entries, translator patches, and open walls and
  accepted risks.
- `CITATION.cff`, `CONTRIBUTING.md` and a CI workflow running `render.py --check`.

### Known limits of this snapshot

Carried here as well as in the README because they bound everything above:

- Many progress rows rest on **one boot of one configuration**, several of them on a
  heavily loaded machine. One boot shows that something can work, not that it does
  reliably.
- For most programs only *running* was measured, not that they did their job.
- There is no desktop on the macOS 27-only root and no graphics acceleration anywhere.
- Pieces of macOS 26 are still in the furthest boot (nine kexts, the tool that builds
  the kernel collection, and the APFS driver the boot loader uses), and the kernel is
  self-built from Apple's published macOS 26.5 source rather than being Apple's macOS 27
  kernel.
- Recompiled programs that must be platform binaries are signed with a key generated in
  the lab and trusted only inside the guest. That is a lab arrangement and not a
  mechanism a real install could use.
