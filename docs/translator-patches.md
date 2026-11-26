# Translator patches, kernel versions and on-disk edits

[&larr; back to the README](../README.md)

Three tables that together describe the main changes this project makes outside its own
code: the patches it carries to a third-party translator, the versions of the kernel it
builds itself, and the edits it makes to files Apple shipped. Two smaller changes are
recorded on other pages: the file flags changed on `sandboxd` and `taskgated`
([docs/launchd-labels.md](launchd-labels.md)), and the renumbered message ids in 27's
disk-arbitration client, record G-08 in [docs/gaps.md](gaps.md).

## Where the patches live, and what has gone upstream

The user-space translator is Maclator, an existing open-source project. Since 2026-11-24
the changes this project runs are kept on a public branch of its own fork,
[willmcginnis/maclator, `queue/boot-tested-2026-11-24`](https://github.com/willmcginnis/maclator/tree/queue/boot-tested-2026-11-24):
54 commits on upstream's current main, read on 2026-11-25, with internal comments removed:
the changes behind the project's default test bases (R2 and Z below are in the one adopted
on 2026-11-25), AA, AB, and some smaller fixes to the translation cache, the translator's
imitation of kernel events and their tests. The translator built from the branch's tip has
not itself been booted. Local builds carrying R2, Z, AA and AB have been; the smaller fixes
have unit tests only. Each change that fits upstream
is still offered there as a small, self-contained change framed around what that project
is itself trying to do; the measured state of those offers is in
[UPSTREAMS.md](../UPSTREAMS.md).

So far **one of these patches, G, has gone upstream**: posted on 2026-11-08 and merged on
2026-11-10 as commit `de04499f` (pull request #12). Patch K, redone as a single change on
upstream's current main, was posted on 2026-11-23 (pull request #16), and the same day
three more fault-safety changes (#17, #18 and #19), K's follow-up (#22) and two questions
as issues (#20 and #21) were posted; all were open, with no reply from upstream yet, at this snapshot.
Two of the others are not in a shape to send: patch J is about 3,750 lines and needs
splitting, and patch Y, which does the same job as X by another mechanism and has
replaced it, is still under test.

Upstream has moved on since this stack was built. Its main branch is now at `2d2f5b3e`,
which has also merged two other contributors' pull requests: #7, to the JIT, the AOT cache
format and the reported CPU features, and #14, to launching app bundles. Several of the remaining
patches touch the same files, so the stack was rebased onto that base on 2026-11-22
before any more of it is sent. The rebased queue is 25 commits, and the translator's
own tests pass on the build machine when run serially (190 passed, 0 failed and 6
ignored, plus 13 passed in the core crate). One timing test of the fork locks fails when
the suite runs in parallel, as it did before the rebase. The queue does not map one to
one onto the first table below: G's upstream cut is merged and the queue keeps only the
remainder of the local patch; W and X give way to Y; and M, O and V are not in the
current engine (M's job moved to the kernel's own identity route), so *done* on those
three rows refers to work before the rebase. In the patch tables on this page, *done*
means only that a patch is built and tested.

Three control boots have been run so far with the rebased engine installed as the
guest's translator (its hash was checked inside the guest), each a single boot, and they
are still being diagnosed. In one, the logd job kept one process for ten minutes and a test
log message was read back in 2 of 2 rounds. In the other two, one of them with a variant
build of the engine, diskarbitrationd kept one process and a disk listing was answered,
but mounting a scratch volume failed. In all three, a planned check of one reported CPU
feature got no answer, so none of them is a pass by the conditions written down
beforehand. The boots' own readings did not find the engine among the files either
daemon had mapped, so these results are not yet evidence about the rebased engine
either way, and whether the mount failure has anything to do with the rebase is not
known.

A later engine, the rebased queue plus three more local changes (a follow-up to K that
answers name lookups for the sysctl names the translator itself provides, a report of
refused guest reads together with interpreting code the JIT cannot read, and a change to R
in two revisions), ran a full comparison boot on a root with the
registry stall fixed ([gaps.md](gaps.md), B18), with its hash checked inside the guest (later
boots carried the same engine). Every disk row of the boot before it held again, including a
scratch disk formatted, then mounted and read back with DiskArbitration doing the mounts; K's follow-up passed
its 14 test cases on arm64 and on arm64e; and in the two store directories sampled, the
translator's file count rose in one early step and then showed no net growth over the last
ten samples. That comparison is one boot.

The build behind the default test base adopted on 2026-11-24 is that later engine plus Q2, the fix for
mapping a short shared-memory object; the fork's branch as first published on 2026-11-24
was its corresponding source, rebuilt and unit-tested separately, not the binary the boots
ran. From 2026-11-24 until the next day that build was the default translator on the
default test base (`amfid` still runs an older build, and recompiled programs are not
translated): in that base's two test boots every required
row passed (24 of 24 and 22 of 22), and with it the user session first started after a
login (milestone L3 in [milestones.md](milestones.md)). On 2026-11-25 that base was replaced
by one whose default translator is a later build, adding R2 and Z, with an empty root-owned
shared store: in its two test boots every required row passed (31 of 31 and 29 of 29), and
no per-home copies of the slid data were found.

Several of these are not Apple-specific at all. The memory-ordering fix (B), the
reserve-before-mapping fix (P) and the page-rounding fix (Q) are the sort of thing any
user-space translator gets wrong once; P was fixed by doing what Wine, QEMU's user mode
and FEX already do, which is generally the right place to look.

<!-- generated:translator-tables:start -->
<h2 id="maclator-patches">Patches to the translator</h2>

23 done, 4 in progress, 0 not started, 2 superseded.

| Patch | Area | What it fixes | State | Evidence | n | Notes |
|---|---|---|---|---|---|---|
| A | Mach-O slice choice | Picked the wrong arm64e subslice in 27's fat files; now ranks the subtype | done | measured | unit tests and boots | &mdash; |
| B | Memory ordering | Store-release instructions could show outcomes the Arm memory model forbids (27,999 in 200,000 before) | done | measured | 200,000-iteration litmus test | &mdash; |
| C | JIT memory | 27's x86 kernel refuses an anonymous read-write-execute mapping without MAP_JIT | done | measured | both kernels | &mdash; |
| D | Path rewriting | An empty-name *at call was rewritten, which broke 27's dyld mapping its cache | done | measured | unit tests | &mdash; |
| E, E2 | Path rewriting | Kept descriptor-bound *at flags and the no-follow-any flags when a name is rewritten | done | measured | unit tests | &mdash; |
| F | Path rewriting | A sysroot given through a symlink broke no-follow lookups | done | measured | unit tests | &mdash; |
| G | Guest memory | An unreadable path pointer crashed the translator where the kernel answers EFAULT | done | measured | unit tests | Posted upstream on 2026-11-08, the first of the stack, after two independent reviews; its upstream cut was merged 2026-11-10 (de04499f, pull request #12), and a smaller remainder of the local patch stays in the queue. A local follow-up reports a refused guest read instead of failing silently; in one boot of an engine carrying it, no such report appeared in the error output that could be read (most daemons' error output goes nowhere visible). |
| H | Path rewriting | A '..' after a cache prefix could climb out of the sysroot | done | measured | unit tests | Eight corner cases are recorded as accepted coverage gaps (docs/gaps.md). |
| J | fork safety | A forked child could hang or die on a lock another thread held at fork time | done | measured | 15,500 children in a guest | Large (about 3,750 lines); needs splitting before it goes upstream. |
| K | sysctl | Crashed on an unreadable sysctl name; answered writes and hardware-feature names unlike native | done | measured | unit tests | Redone as a single change on upstream's current main (2d2f5b3e), with its own guest test, and posted upstream on 2026-11-23 as pull request #16, open at this snapshot. A local follow-up answers name lookups for the sysctl names the translator itself provides: its 14 test cases passed on arm64 and on arm64e under an engine carrying it (1 boot); posted on 2026-11-23 as pull request #22, open. On 2026-11-24 a commit was added to it: a forked child could wait forever on the lock that holds those names if another thread held it at the fork; the lock is now taken around the guest's fork, and a unit test forks while another thread holds it. |
| L | Path rewriting | A descriptor race between a check and the call it guards | done | measured | unit tests | &mdash; |
| M | Process identity | A translated program asking about its own code signature got the translator's answer; it now gets its own, using Apple's own validator code | done | measured | 1 boot | Its first spawn at boot gets no answer from a framework check and falls back (a recorded gap). |
| N | Path rewriting | Adds a mode with no sysroot, for running at 27's real paths | done | measured | unit tests | &mdash; |
| O | Residuals | Closed the earlier accepted gaps that turned out to be real defects | done | measured | unit tests | &mdash; |
| P | Shared-cache mapping | Mapped over unmapped space with MAP_FIXED, raising kernel guard exceptions (fatal in a platform binary); now reserves the range first, as Wine, QEMU user mode and FEX do | done | measured | guard exceptions 102 to 0 | &mdash; |
| Q | Page size | An anywhere VM map was not rounded to the 16 KiB pages the guest believes in, so freeing one took its neighbour | done | measured | unit tests | &mdash; |
| Q2 | Page size | Rounded every file mapping up to 16 KiB, so mapping notifyd's 4 KiB shared-memory object failed; every translated process's notification registration then failed, and 27's loginwindow stopped the login at its audit step. Now, when the rounded mapping is refused with EINVAL and the program asked for less, it retries at the program's own length (a retry the kernel refuses is still refused) | done | measured | 4 unit tests; 12 login boots; 2 test boots of each default base | Matches Apple silicon, whose kernel maps the short object. The user session first started with it. On the fork's public branch; not yet offered upstream. |
| R | Shared cache | Each process kept its own slid copy of the cache; now one file mapped copy-on-write | done | measured | 396 MB to 19 MB for one daemon | Two later local revisions: each slid file is checked once per boot and then trusted through a stamp, and a file that failed a whole check is refused for the rest of the boot. In one 38-minute boot of an engine carrying them, stamps were written, and all 14 early stamps kept their modification times while more translated programs started, which is consistent with reuse; in the two store directories sampled, the file count rose in one early step and then showed no net growth over the last ten samples (other per-daemon stores were not sampled). |
| R2 | Shared cache | R's slid store was kept per home directory, so the same files were copied into each home directory and sandbox container that used it (16 stores in one boot held about 9 GiB of cache files, mostly duplicated slid data, and the disk ran out of space); now, where a root-owned shared store exists, every user maps root's copy, and a process that cannot use it slides privately rather than write a copy under its home; where the shared store is missing or not trustworthy, the old per-home store is still used | in progress | measured | unit tests; 11 boots on the login line, 8 of them through a login; 2 test boots of the default base | Its first build booted twice on 2026-11-24, in two arrangements. With nearly every translated program on it, the shared store held one copy (14 data files, about 560 MiB) and the disk did not fill, but no login window appeared. Named for 81 programs on the login path, with another build as the default, the login went through, but the programs on the other build made 140 copies in 10 per-home stores and free space fell to about 2.15 GiB by the end of the boot. A later build, which keeps each reader's own checks of the shared store in that reader's own store, passed the whole test suite; it and the first build each booted once with no login window, in a set-up in which a disk-management service kept crashing (docs/boot-programs.md, diskarbitrationd). In the login boots after that, with the fix named for 97 programs, the lowest free space was 2.33 GiB, and 126 slid files outside the shared store were in 9 per-home stores when sampled, a tenth getting a set later (1 boot); named for about 120, the lowest was 5.71, 5.49 and 5.12 GiB, with four per-home stores (56 slid files) left, written, where the writer was named, by programs on another build (3 boots). In the next two login boots the lowest was 5.84 and 4.55 GiB, with three per-home stores left in each; in one login boot on the default test base adopted on 2026-11-25, where it is the default for nearly every translated program, 6.24 GiB, with one per-home store of slid data left (its writer not read) and the translator's other cached files still kept per home. The default test base adopted on 2026-11-25 uses a later build as its default translator, with an empty shared store: no per-home copies were found at any sample of its 2 test boots, and over about 20 minutes from early in a boot free space fell by 1.54 GiB, against 5.23 GiB for a matched control boot of the previous base (1 boot each). So disk use through a login with every program on it is not shown yet. That every user's processes trust root's copy is a lab policy the owner has not ruled on. On the fork's public branch since 2026-11-25; not yet offered upstream. |
| S | Loader | Refused to load a position-independent image when its preferred base was taken; now slides it as the kernel does | done | measured | engine tests and boots | This is what let 27's amfid load. |
| T | Memory limits | The translator's own memory was not charged to the process's limit | done | measured | 1 boot | &mdash; |
| U | JIT | Aborted when MAP_JIT is refused (27's sandbox profile for sandboxd denies it); now falls back to the interpreter | done | measured | 1 boot | &mdash; |
| V | Diagnostics | A log-only diagnostic for a failed guest-pointer write | done | measured | 1 boot | Developer side only. |
| W | Guest memory | A fallback for a refused guest-pointer write | superseded | measured | &mdash; | Superseded by X after review. |
| X | Guest memory | Writes a kernel out-parameter to guest memory through a pipe when a direct write is refused | superseded | measured | 2 boots | Superseded by Y, which the rebased queue carries instead (2026-11-22). Before that it removed the sandboxd failure for a hand-started copy in 2 of 2 boots; in the second, the launchd-started copy was still restarting, though it ran with a trace option the hand-started one did not, so the two were not a controlled comparison. An open race from review stood. |
| Y | Guest memory | The same write as X, by a VM copy instead of a pipe | in progress | measured | unit tests | Built and its tests pass. Carried in the rebased queue in place of X. An engine carrying it has been booted, but what those boots showed is not written up in this record yet, and the control boots of the rebased engine did not test this fallback. |
| Z | Guest memory | Read and wrote the program's memory through whatever name the kernel answered, asked afresh on every access, for the program's own task (in a test on an Apple silicon Mac, repeated asks raised the reference count on the same name until it saturated, and the name still worked; on the x86 guest this is not read). In one boot those reads were refused in every WindowManager process (why the kernel's answer stopped working there is not read), the translator's imitation of the kernel's workloop passed each refusal on as a bad address, and Apple's dispatch library stopped the program on purpose. Now it uses the task name libSystem keeps, as native code and the rest of the translator do, and a workloop state check answers a bad address only for a bad address | done | measured | unit tests; 5 login boots; 2 test boots of the default base | Refused-read warnings: 1,001 across 125 WindowManager processes in the boot before, 0 in the boot with it (1 boot each), and 0 in the captured output of the default base's 2 test boots and of the 3 login boots since. Three new regression tests fail on the old code and pass on the new; the other new tests check assumptions and controls. On the fork's public branch; not yet offered upstream. |
| AA | App Sandbox | The translator is an x86_64 program that starts on Apple's x86_64 libSystem, so in each translated process libSystem's start-up ran for the translator as well as for the program. In the four app-sandboxed session agents diagnosed, the translator's start-up asked for the program's sandbox first, the program's own request was then refused, and the program stopped before its main function. Now the translator's own start-up reads the process's entitlements without the App Sandbox key, so only the program asks, once, under its own name, as natively | in progress | measured | tests on an Apple silicon Mac running macOS 27.0.1; 4 boots, for the five session agents tracked and a test program, TextEdit in 2, and two more programs seen asking under their own names in 1 | In the boot before it, four of the session's app-sandboxed agents stopped there (239 crash reports). With it, each process of the five it was given to asked once, none stopped there, and four stayed up; a test program in its app container was sandboxed and refused files outside it, as natively (1 boot). It is not yet given to every translated program, and programs seen on another build in that boot still made a request under the translator's name. Apple's Rosetta runtime is a static program that loads no libraries, so it has no such second start-up (read on 27.0.1). On the fork's public branch; not yet offered upstream. In the 3 login boots since, each process of the five again asked once and all were running at the end; TextEdit, given it in 2 of them, asked once. |
| AB | Sandboxed start-up | Some of the translator's own start-up ran after the program's own sandbox was in force, and the program's profile refused it: in WindowManager the kernel event queues the translator makes for its imitation of the kernel's thread pool were refused, and the translator took the refusal for a descriptor (docs/gaps.md, B25). Now the translator makes those queues, and raises the process's memory limit, before the program starts; it never takes a refused queue for a descriptor; and in a sandboxed process it leaves its own stores of translated code alone | in progress | measured | unit tests; 3 login boots, for 11 or 12 programs | With it, WindowManager ran as one instance all boot with no crash report, and the kernel's collected sandbox lines recorded no refused event-queue call, memory-limit call or store access for a program given it (3 boots; each boot's collection had a few short gaps); the session's app-sandboxed agents were given it too (3 boots), and TextEdit (2). It is not yet given to every translated program: in a login boot on the default test base adopted on 2026-11-25, one daemon on that base's default build was refused the memory-limit call (inferred to be a case this patch fixes), and another wrote 19 abort crash reports, whose cause is not read. On the fork's public branch since 2026-11-25, followed by five more commits (a message when the descriptor limit cannot be put back, test and comment changes, and two corrections to the translator's imitation of kernel events) that have unit tests only; the translator built from the branch's tip has not been booted. Not yet offered upstream. |

<h2 id="self-built-kernel-versions">Self-built kernel versions</h2>

| Version | What changed | State | Evidence | n |
|---|---|---|---|---|
| 1.0 to 1.3 | Builds from source; 27's missing exports, syscalls and MIG routines; the CPU-registration wait before lockdown; the foreign-architecture exec option | done | measured | 4 boots to loginwindow |
| 1.4.x | Fixes to the exec option after two independent reviews; removes a circular wait at exec that could freeze the boot | done | measured | 1 boot per arm |
| 1.5.0 | A translated process may raise its own memory limit, up to a cap | done | measured | 1 |
| 1.5.1, 1.5.2 | Two exports the recompiled Sandbox kext needs | done | measured | 1 |
| 1.5.4 | A sysctl 27's libraries read at boot, added after a launchd abort was seen without it; the build with it booted, and the cause of the abort was not isolated | done | measured | 3 boots |

<h2 id="on-disk-edits-to-apple-files">On-disk edits to Apple files</h2>

| Edit | Why | Applied | State | Evidence | n | Notes |
|---|---|---|---|---|---|---|
| Kernel load-time patches (Apple's 27.0.1 kernel only) | Early-boot code assumes arm64; the commpage is never mapped into user processes | boot loader kernel patches | done | measured | many boots | Not needed on the self-built kernel. |
| Main shared cache re-signed at 4 KiB hash pages | The x86 kernel rejected the 16 KiB hash pages Apple signed the main macOS x86_64 shared cache with (the DriverKit cache ran with its own 16 KiB pages) | on disk | done | measured | many boots | Lossless: the cache's signature is ad hoc. |
| Two device-tree properties made by boot.efi | 27's userland expects them from firmware | on disk, boot.efi | done | measured | 1 boot each way | &mdash; |
| CoreDisplay display-state reply, 20 bytes (hybrid image) | 27's x86_64 encoder and arm64e decoder disagree on one field | on disk, found by pattern per build | done | measured | 4 builds, warm and cold boots | Also placed in the 27-only root's cache for the display test boots. |
| SkyLight backdrop clip, 1 byte (hybrid image) | 27's code assumes a Metal compositor | on disk, found by pattern per build | done | measured | 2 boots per arm | Also placed in the 27-only root's cache for the display test boots. |
| Data volume group id written offline | 27's system volume ships with a zero group id and no tool sets it | offline superblock edit, checksums recomputed | done | measured | many boots | &mdash; |
| DriverKit shared cache: eight libdyld forwarding stubs moved up one table slot | They call dyld's API table one slot short of where 27.0.1's dyld keeps those functions (seven matched by name; the eighth stub's name is stripped and its target was inferred from its neighbours), which crashed the HID driver extension at start | on disk, cache re-signed with its own 16 KiB hash pages | done | measured | 3 boots | All eight moved, every page hash re-checked. Not yet in the furthest configuration. |
| A DriverKit serial extension moved out of the scanned folder | It has no x86_64 slice, and its kernel side had no x86_64 build in the collection; with it moved, the registry goes quiet (why it held matching back is inference) | on disk, the .dext moved to another folder | done | measured | 7 boots | One of two fixes for the registry stall (docs/gaps.md, B18); the other adds Apple's own x86_64 kext to the boot collection and edits no Apple file. The project's default test bases since 2026-11-24 take the other fix and leave this extension in place. |

<sub>Generated from `data/translator.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:translator-tables:end -->

## What the kernel actually is

The self-built kernel is built from **Apple's own published xnu source** &mdash;
`xnu-12377.121.6`, which is macOS 26.5's &mdash; plus the interfaces macOS 27 needs that
that source does not have. Those were re-derived from 27's own x86-64 machine code:
missing system calls, Mach interface routines and exports, and for a few closed routines
with no published source, re-emitted from 27's machine code and checked instruction by
instruction.

Three consequences follow, and all three should be stated whenever this kernel is
mentioned:

- **It is not Apple's kernel.** It reports version 25.5.0, because that is what its
  source is.
- **It needs none of the load-time patches** that Apple's own 27.0.1 x86-64 kernel needs.
  That is the main reason it exists: on this guest Apple's x86-64 kernel for 27 does not
  boot as shipped, since several of its early-boot paths assume arm64 behaviour, and
  seven patches are required to get past them.
- **Its RELEASE builds work; a DEVELOPMENT build did not in the two boots tried.** Both
  were on an earlier version and have not been repeated since: the build boots and then
  core daemons end themselves in a loop. The cause has not been found.

A 66-minute soak was run side by side with Apple's kernel on the same disk: no panics
either way, and the same crash reports at the same rate. That was on an earlier version
and has not been repeated on the 1.5.x series, so it should not be quoted as current.

## Edits to Apple's files

These are the edits the boot recipes apply to files Apple shipped. Each is recorded as
what it changes and why; the bytes are not published. The last two rows are applied only in
test boots so far, not in the furthest configuration.

Two of them &mdash; the display-state reply and the backdrop clip, both on the hybrid
image &mdash; are found by pattern per build rather than by fixed offset, so a new macOS
build does not silently get the edit applied in the wrong place. The remaining risk is
that a pattern matches somewhere subtly wrong on a later build, which is recorded in
[docs/gaps.md](gaps.md) (G-33) as a risk pending the owner's acceptance, rather than
solved; the mitigation is that every built image is booted once.

The main shared-cache re-signing is worth separating from the rest, because it loses
nothing: the x86 kernel rejected the 16 KiB hash pages Apple signed the main macOS x86_64
shared cache with, so it is re-signed at 4 KiB (the DriverKit cache ran with its own 16 KiB
pages), and since the cache's own signature is ad hoc there is nothing to
preserve.
