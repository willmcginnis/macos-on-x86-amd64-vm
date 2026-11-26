# Open walls and accepted risks

[&larr; back to the README](../README.md)

Two different things, kept on one page because they are easy to confuse:

- an **open wall** is something that does not work yet and is being worked on;
- an **accepted risk** is a known way the work can go wrong where a fix exists and was
  deliberately not paid for.

The second list is the more useful one to a reader checking this project, and it is the
list most write-ups of this kind do not have. A gap that has been written down with who
decided to leave it open is a different thing from a gap nobody noticed.

## Open walls

<!-- generated:gaps-blockers:start -->
11 closed, 11 narrowed or being fixed, 4 open with no fix under way.

|  | Wall | State | Evidence | Notes |
|---|---|---|---|---|
| B1 | Identity of a program under translation | done | measured | The kernel's exec option gives an arm64e program its own Apple identity. For a recompiled program that must be a platform binary, a lab key is trusted through Apple's developer trusted-key mechanism; how that would work in a user install is undecided. For an arm64-only program that a translated program starts itself, only with patch AC, which hands the start to the kernel; builds without it, and the cases AC keeps on the old re-launch, still give such a child the translator's identity: B26. |
| B2 | No Data volume beside 27's system volume | done | measured | The volume group id was written offline; a real volume group boots. |
| B3 | Mounting the Preboot volume needs an arm64e-only program | in progress | measured | Closed by a 945-byte stand-in script; lifting 27's mount would retire it. |
| B4 | No x86_64 Sandbox kext for 27 | done | measured | 27's own Sandbox kext, recompiled, boots and enforces. Inside it: network-outbound rows are no reading, a sysctl deny is not closed, and ten deny pairs against real 27 are undecided. |
| B5 | fork safety under translation | in progress | measured | 15,500 children at 4 vCPU: none hung, none wrong, no guest panic; the 1,000 that died did so where the native program dies the same way. 8 vCPU under heavy host load not retested. |
| B6 | pid 1 from 27's own launchd | in progress | measured | Works on the furthest configuration (3 boots); since 2026-11-24 also in the default test bases, each one standalone disk image (2 test boots each). Whether the lab trusted-key route stays is the owner's decision. |
| B7 | Display-state mismatch and the backdrop abort (hybrid image) | done | measured | Both are small byte edits on disk, found by pattern per build. One risk, that an edit could be silently wrong, is the owner's to accept. |
| B8 | No GPU | not started | measured | Below the main line. A software Vulkan compute test passes in the guest. |
| B9 | Building the kernel collection with 27's own tools | in progress | measured | Still macOS 26's kmutil in a recovery guest. 27's kmutil runs under translation but has not loaded a kext. |
| B10 | 27's own logd | in progress | measured | 27's own logd and logd_helper run translated on the furthest configuration, exit status 0 in 3 of 3 boots. Reading messages back through 27's logd is measured only on other configurations (2 of 2), not yet on this one. |
| B11 | 27's own amfid | in progress | measured | Runs and stays up (4 boots of the furthest configuration). In one boot it refused an ad hoc signed program carrying a restricted entitlement; an edited-signature test did not discriminate, so validation is partly tested. A recompiled amfid has not been linked with the current tools. On the display test overlays used for login boots, macOS 26's x86_64 build had been in place: it wrote 7 and 9 crash reports in the 2 boots read, after calling a method that 27's code-signing framework has renamed. Since 2026-11-25 Apple's 27 amfid is back there, named for a translator build carrying patch S (which build ran it was not read directly): one process all boot, no crash report, and no kernel line of a code-directory check finding its server gone (3 login boots; 11 such lines in a boot before). The default test base adopted on 2026-11-25 still carries the macOS 26 build: the 6 amfid crash reports of its first login boot name it, and its two later login boots wrote 6 and 7 (which build they name was not read). |
| B12 | Daemons that run but do not yet serve | in progress | measured | In one boot, before 27's own amfid replaced macOS 26's, 126 of the 411 labels in launchd's job table ran and 15 had a nonzero status; causes of 12 of them are unread. |
| B13 | DEVELOPMENT build of the self-built kernel | not started | measured | Boots; core daemons end themselves in a loop. |
| B14 | A circular wait at exec that could freeze the boot | done | measured | Read from kernel stacks in five boots; removed in kernel 1.4.3, with a follow-up fix in 1.4.4. |
| B15 | The first translated run of a boot is slow | not started | measured | Up to 233 s and 412 s for a first read, 9 to 65 s later, on a host at load 130 to 198 with no translation cache kept across boots. Not split between translation cost and starvation. |
| B16 | File flags lost on the Data volume | done | measured | Restored and read back, 14,024 of 14,024 flagged entries equal. |
| B17 | 27's sandboxd did not stay up under launchd | done | measured | Traced to a refused write to guest memory; a translator fix removed it for a hand-started copy in 2 of 2 boots, while in the second the launchd-started copy kept restarting (with a trace option the hand-started one lacked). That fix (patch X) had an open race and has been replaced by patch Y. On the display test overlays used for login boots, sandboxd ran on an older translator build that lacks patch U, so it was stopped at once when its own sandbox profile refused run-time code (17 crash reports in each of 2 boots read). Closed on 2026-11-25 by naming it for a newer translator build carrying U: in that login boot launchd's sandboxd ran as one process all boot, never exited, wrote no crash report, and lived through the one refusal of run-time code its profile still made (by the interpreter fallback, inferred). It stayed up the same way, with no crash report, in 2 more login boots on 2026-11-26, the second on the build from the fork's public branch (its use for sandboxd there is inferred from its setting). Whether all its answers are right has not been read. In the three login boots on the default test base adopted on 2026-11-25 no sandboxd crash report was written (which build it ran on there was not read). |
| B18 | The 240-second registry stall and the HID driver extension | in progress | measured | An arm64e-only DriverKit serial extension, whose kernel side (com.apple.driver.driverkit.serial) had no x86_64 build in the boot collection, keeps IOUserResources from ever matching (the mechanism is inference; the fixes are measured). Two fixes work: Apple's x86_64 IOUserSerial.kext from the Kernel Debug Kit added to the boot collection (4 boots), or the extension moved out of the scanned folder (7 boots). With either, the registry went quiet in every boot, and no stall line or hidden disk was seen in any boot that counted them. With the registry quiet, 27's own DiskArbitration served the scratch-disk round in 7 of 8 boots counted. The project's default test bases since 2026-11-24 carry the first fix (2 test boots each); most rows of this record predate them. The HID extension's crash at start is fixed in 3 boots (docs/boot-programs.md). Keyboard input typed at the login window has reached it in each login boot since (B21); pointer events reached the HID queue in earlier boots, and after a login clicks have opened controls (the Apple menu in 3 boots, a Finder window from the Dock in 6; milestone L7). Both written up for other projects: docs/notes-for-liberator.md. |
| B19 | A launchd-managed sshd on the furthest configuration | not started | measured | Logins so far are to a debug sshd the test payload starts. |
| B20 | Stopping a service panicked the guest | done | measured | The recompiled launchd exited when it stopped a service, and the kernel panicked (1 control boot). With the fix: 0 panics in 2 boots; in one, launchd waited its 10 s exit timeout, then killed a service that ignored the stop request, and stayed pid 1. |
| B21 | No login window on the display test overlays | done | measured | Closed: the login window appears. In six earlier boots, WindowServer stayed up and in 5 of them showed the boot progress window (the sixth stayed on the text console), but no login window appeared. Whether it appears looks like a race: SecurityAgent has to show its window before the guest's display goes to sleep, and once the display sleeps nothing redraws it (inferred from one boot's timing, in which SecurityAgent logged that it was showing its window one second before the screens slept). The window was drawn in 2 of 2 boots of one set-up and 1 of 2 of another when nothing held the display awake, and in each of 19 later scored boots in which a login was typed. In 4 other boots, set up differently, it did not appear; the cause is read for some of them only. On the login line, every boot without a window (4, one of which may be among those 4) had a disk-management service crashing; with Apple's own disk-arbitration daemon in place of the recompiled one, the window appeared in all 12 scored boots (B22; docs/boot-programs.md, diskarbitrationd). What follows the login: B22. |
| B22 | No usable desktop after the first login | in progress | measured | After the first login, User Account Updater completes (14 boots). In the 2 boots in which loginwindow then launched the first-login Setup Assistant, no pane of it appeared (in the first it was seen to become the frontmost app); the screen stayed black to the end of the boot and no Dock or Finder process started, the same final frame byte for byte in both. In the first the disk also ran out of space (B23); in the second it did not, so running out of space is not why. Marking Setup Assistant's record for the user complete beforehand did not stop it being launched (1 boot). Why no pane appears is not read. Since 2026-11-24 a per-user marker, placed by the test before the login, makes the updater skip Setup Assistant; the Dock, Finder, SystemUIServer and Control Center then start and stay up (12 boots). With the fix for app-sandboxed programs (B24) a menu bar and a wallpaper are drawn (9 boots), and since WindowManager stays up (B25, closed) a Finder window opens (8 boots) and TextEdit takes typed text (7 boots). What is still wrong, read in frames of those boots: the Dock is drawn late, first seen between about 10 and 50 minutes after the login (11 of 12 boots), or not at all (1); most app icons in a Finder window stay placeholders for minutes; Control Center opens with unnamed modules and no slider tracks, and About This Mac shows the model and chip as Unknown (2 boots); a box of old boot-console text covered part of the menu bar for a time (8 boots); the Dock's Safari tile is a question mark, Safari's files being in Apple's App cryptex, which these overlays do not mount (1 boot read). On the display test overlays the causes are not read. On the default test base adopted on 2026-11-25, where the Dock came only after 35 minutes, by about 50, in the first two login boots and the guest's load stayed 5 to 10 times higher while it was used, the load is read: three network daemons (airportd, wifip2pd and searchpartyd) exit and are restarted about every 10 seconds all boot, the guest having no Wi-Fi hardware; on that base's default translator build each run lasts seconds, at many of airportd's exits the translator starts background work to rebuild its saved translations (read in its source; that the extra processes seen are that work is inferred), and many runs crossed their memory limit (inferred to be the runs that loaded a saved translation). With the translator's saved-translation cache turned off for those three, as a diagnostic, the load while the guest was used fell to the display overlays' level and the Dock was drawn within 15 minutes (1 boot). The fix meant is a translator change, built and not booted, not that setting. About This Mac's Unknown model and chip are inferred to come from a model identity missing from the guest's firmware description, which also makes a daemon there abort (which identity the guest should present is pending the owner). Boots of this line that showed no login window at all (4) each had storagekitd, a disk-management service, crashing; in the 5 that showed one, its last exit status was 0 (no crash report in the one of them read for it), and one more was void; with Apple's own disk-arbitration daemon in place of the recompiled one, the window appeared in all 12 scored boots (docs/boot-programs.md, diskarbitrationd). |
| B23 | The translator's shared-cache data fills the disk | in progress | measured | The translator's store of slid shared-cache data (docs/translator-patches.md, R) is kept per home directory, and macOS gives every sandbox container and daemon user its own, so the same files are copied into a store for each that uses it: in one boot 16 stores held about 9 GiB of cache files, mostly duplicated slid data, and the root's 51.5 GB container ran out of space. A fix keeps one root-owned store for every user (R2). In the login boots since, with it named for 81, then 97, then about 120 programs of the login session and the rest on another build, the lowest free space was 2.15, 2.33, then 5.71, 5.49 and 5.12 GiB; in the last three, four per-home stores (56 slid files) remained, written, where the writer was named, by programs on another build. In the next five login boots on the display test overlays it was 5.84, 4.55, 5.52, 5.51 and 5.04 GiB, with three per-home stores left in each. On the default test base adopted on 2026-11-25, which uses it as the default translator, no per-home copies were found in its 2 test boots, which take no login; in its three login boots the lowest free space was 6.24, 5.23 and 6.36 GiB and one per-home store of slid data remained in each (its writer not read), while the translator's other cached files were still kept per home. So disk use through a login with every program on the fix is not shown yet. That every user's processes trust root's copy is a lab policy the owner has not ruled on. |
| B24 | The session's app-sandboxed agents stop before their main function | in progress | measured | Four agents the session needs for its menu bar, notifications, AirPlay and wallpaper stopped before their main function, refused a second sandbox profile (239 crash reports in 1 boot); in the same boot the menu-bar agent's launches after the login failed earlier still, in the launcher, at a step of the test's own logging set-up (inferred), and a fifth app-sandboxed agent exited with the same status, at a point not read. Read in the logs and in Apple's code: the translator starts on Apple's x86_64 libSystem, whose start-up, seeing the program's App Sandbox entitlement, asked for the program's sandbox first; the program's own start-up then asked again, and the guest's Sandbox policy refused the second profile. In a stand-in test on an Apple silicon Mac running macOS 27.0.1, two such requests under the earlier translator were both accepted, so that refusal is not shown to match Apple. Native x86_64 app-sandboxed programs in the boot that showed the traps started and stayed up. With patch AA (docs/translator-patches.md) each process of the five asked once, under its own name, and none stopped there; four stayed up, and, with Setup Assistant skipped by the test's marker, a menu bar and a wallpaper were drawn (1 boot). Not closed: the fix is not yet given to every translated program, and programs seen on another build in that boot still made a request under the translator's name. In the 8 login boots since, each process of the five again asked once and all five were running at the end. |
| B25 | WindowManager kept crashing after the login | done | measured | WindowManager crashed soon after each start and was restarted. In the first login boots that ran it, it exited with status 134 again and again, the reason not read; in the next, with its error output captured, every crash followed the translator's refused reads of the program's own memory, and patch Z removed those (1,001 refused-read warnings across 125 processes, then 0; 1 boot each). It then died at a different point, a disconnect Apple's libraries treat as impossible: 9 times, after which it stayed up from its tenth start (1 boot); in the next boot it did not settle, and its run count reached 297 (1 boot). The cause, read in the second of those boots, each step in code or a log but the whole chain not watched live: WindowManager applies its own sandbox profile, Apple's, which lists the system calls it may make; the translator, imitating the kernel's thread pool for the program, creates kernel event queues, which the real program never does and the profile does not allow; the translator does not check that the call failed, and the failure surfaces as that disconnect. No Apple profile gives Rosetta extra system calls, and Apple's published kernel filters translated programs like any other. Closed by patch AB (docs/translator-patches.md), which makes the translator's event queues before the program starts, and so before it applies its own profile, and no longer takes a refused queue for a descriptor: in the 8 login boots since, WindowManager ran as one instance all boot, with no crash report, and the collected sandbox lines (with a few short gaps) showed no refused system call for it (the first boot with its tracing on, the others without). Programs on other translator builds do not have the fix yet (B22; docs/translator-patches.md, AB). |
| B26 | An arm64-only program started by a translated program carries the translator's identity | done | measured | When a translated program started another program that 27.0.1 ships for arm64e only, the translator started a copy of itself with that program as an argument instead of handing the start to the kernel, so the kernel's record of the child named the translator's file, and any other process that asked the kernel for the child's signature or entitlements got the translator's (read in the translator's source and in Apple's published kernel source). Programs the kernel starts itself, launchd's jobs among them, are not affected (B1). Seen as a refusal: a disk-image helper started by a translated disk-image tool was refused by Apple's disk-image eject daemon for a missing entitlement. Closed on 2026-11-26 by patch AC (docs/translator-patches.md), which hands such a start to the kernel: in a login boot that day the translated disk-image tool, on a build with AC, attached a RAM disk and detached it; its helper was started by the kernel as itself (the kernel's record named the helper's own file, its signature valid, with its own entitlement) and no process was refused an entitlement, while in the same boot the same tool on a build without AC failed for the missing entitlement, as before. The pair read the same way in a second login boot that day, on the build from the fork's public branch, where the control's helper was also read carrying the translator's identity and no entitlement. Not shown: the identity of other kinds of child (it was read only for the disk-image helper's family; in the second boot a parent with AC also handed another program's start to the kernel and the command worked, how that child then ran not read), and the cases AC keeps on the old re-launch beyond one test each. Programs on builds without AC still start their children this way (one seen). |

<sub>Generated from `data/gaps.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:gaps-blockers:end -->

### The ones that are not going to close quietly

**B1, identity under translation**, is the one with a consequence outside the lab. The
kernel's exec route gives an arm64e program its own Apple identity, which is the clean
case. But a *recompiled* program is a new binary, and some of these must be platform
binaries for the system to accept them, so they have to be signed by something the guest
trusts. Here that is a key the lab generated and then told the guest to trust. That works
inside a virtual machine nobody else uses, and it is explicitly **not** a mechanism a real
install could rely on. How it would work outside a lab is undecided, and it may be that
it cannot.

**B15, the slow first translated run.** The first translated program in a boot can take
up to 233 seconds, and a first read up to 412, against 9 to 65 seconds later in the same
boot. Those numbers were taken on a machine at a load average of 130 to 198 with no
translation cache kept between boots, and the cost has **not** been split between the
translation itself and simply being starved of processor time. So the honest statement is
that nobody yet knows how slow translation is, only that the first run is slow on a busy
machine.

**B12, daemons that run but do not serve.** Of the job labels on the furthest root, a
minority ran during the boot measured, and fifteen exited with a nonzero status; the
causes of twelve of those have not been read. This is the largest pool of unexamined
failure on the project.

**B5, fork safety.** 15,500 forked children in a guest at 4 virtual processors: none
hung, none produced a wrong result, no guest panic, and the thousand that died did so
where the native program dies the same way. That is a real result. It has not been
repeated at 8 virtual processors under heavy host load, which is where the original
failure was found, so it is not closed.

## Accepted-risk records

<!-- generated:gaps-risks:start -->
Every gap is judged by three questions: what the fix costs, whether the gap arises on the macOS 27 path at all, and whether a general translation route would close it along with others. The project's rule is also to compare how Rosetta, Wine, QEMU, FEX-Emu and box64 handle the same thing, and to copy them where they agree. Most records carry such a comparison, but not all: some were judged not to be translation gaps (a value the boot loader supplies, a limit of the project's own test script), at least one still owes its comparison until its cause is read, one has no comparison field at all, and at least one says outright that no translator was compared. The comparisons are in the project's private working notes, not in this table. Where the project's behaviour equals Apple's own, on the hardware macOS 27 ships on, and being stricter would be optional, the project matches Apple rather than being stricter, and records the case as bug-for-bug compatible with Apple.

The risks table is a selection: 52 rows drawn from the project's register of 83 accepted-risk records. Related records are combined into one row (for example, eight path-rewriting corner cases are one row). Which records were left out, and why, is not recorded here. The register's total is an earlier count of 82 plus the one record added since (G-52's); counts of the register's ID fields differ from it by one or two, depending on how combined records are counted.

| Who decided | Records | What that means |
|---|---|---|
| accepted by the owner | 6 | the project owner accepted the risk, often as interim |
| bug-for-bug compatible with Apple | 1 | the owner accepted it because it is what Apple's own system does, on the hardware macOS 27 ships on (the term is Wine's: it aims at "bug-for-bug" compatibility with Windows); a stricter choice was possible and was declined, and the record is looked at again if Apple changes. Never used where the project is looser than Apple |
| direction set by the owner | 4 | not accepted as a gap; the owner chose the fix |
| project default | 15 | fails loudly and loses nothing, so the project accepted it by its own rule; the owner may overturn it |
| pending the owner | 15 | could fail silently or loosens a policy, so only the owner may accept it; not yet decided |
| fixed | 8 | the fix was built and measured |
| retired | 3 | the thing it was about is no longer used day to day |

<details>
<summary><strong>Analysis tools</strong> &mdash; 3 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-06 | The string cross-reference tool matched raw bytes and could name a call site that is not one | direction set by the owner | Fix to full coverage. |
| G-14 | A jump table with no recognised dispatch is not decoded | accepted by the owner | Filled from Ghidra's switch recovery since. |
| G-15 | Two places the cross-reference tool reports a lead rather than a fact | project default | &mdash; |

</details>

<details>
<summary><strong>Apple's kernel</strong> &mdash; 2 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-01 | An early commpage mapping was never torn down, leaking two entries per process | fixed | The owner chose the proper fix: the commpage now has a real map entry. |
| G-02 | That fix widens each 64-bit task's maximum address, adds a commpage map entry and keeps a port | accepted by the owner | &mdash; |

</details>

<details>
<summary><strong>Boot loader</strong> &mdash; 2 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-04 | A kext the boot loader injects that fails to link is silent | accepted by the owner | Interim, with the cause worked in parallel. |
| G-48 | With one device-tree property made, kmutil still stopped at the second | fixed | &mdash; |

</details>

<details>
<summary><strong>Exec route</strong> &mdash; 5 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-34 | With the exec option on, a native process may register a signature form Apple's Intel kernel would refuse | bug-for-bug compatible with Apple | Matches Apple's kernel on Apple silicon, where macOS 27 ships: from Apple's published source, it accepts code-signature pages of 4 KiB or of the kernel's own page size, from every process. On Apple silicon that page is 16 KiB, which is the page size a native process reads there; the source does not fix it. Apple's Intel kernel accepts 4 KiB only, so the match is with the Apple silicon kernel, not the Intel one. A stricter kernel was built and not adopted: it would refuse a registration one of Apple's own drivers makes on every boot checked (four). Nothing wrong measured. |
| G-35 | The runtime writes the engine's stack below its own frame, past a very small stack | project default | &mdash; |
| G-36 | The exec route trusts the translator runtime by its fixed path, a lab policy | pending the owner | To be pinned when the runtime settles. |
| G-37 | A circular wait at exec could freeze the boot | fixed | &mdash; |
| G-47 | With 27's own amfid in place, a check of the translator runtime had no answer and amfid did not start | pending the owner | Cause narrowed, not pinned. |

</details>

<details>
<summary><strong>Graphics</strong> &mdash; 3 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-09 | Skipping a compositor assertion in live memory | direction set by the owner | Replaced by an on-disk edit; the real fix is a GPU path. |
| G-10 | A live-memory fix to the display-state mismatch | retired | Developer-only since the on-disk edit. |
| G-33 | An on-disk edit to Apple's cache could be silently wrong on a later build | pending the owner | Recommendation: accept, with the per-build check, which boots each built image once. |

</details>

<details>
<summary><strong>Image checks</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-05 | The image verifier could not tell 'never placed' from 'wrong path asked' | fixed | &mdash; |

</details>

<details>
<summary><strong>Kernel-side tests</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-42 | The spec generator refused a function that stores a stack address | fixed | &mdash; |

</details>

<details>
<summary><strong>Kext adapter</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-43 | A proof that a global has no setter scans direct stores only | project default | &mdash; |

</details>

<details>
<summary><strong>Link tools</strong> &mdash; 16 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-17 | Four calling-convention corners: narrow or floating-point stack arguments, narrow results of unknown width, aggregates the two ABIs place differently, a native caller's stack arguments | pending the owner | Silent if hit. |
| G-18 | Async Swift calls are refused | project default | &mdash; |
| G-19 | An unknown native pointer called with every register sees one register's value | project default | &mdash; |
| G-20 | The smallest lifted functions are entered through a trap | project default | &mdash; |
| G-21 | Call-site screens see only straight-line code; a variadic function behind a pointer; capped argument copies | pending the owner | &mdash; |
| G-22 | Refusals the review added, the replay oracle's view of selectors, undeclared imports passed a stack address | project default | &mdash; |
| G-23 | Objective-C classes defined in the lifted image | fixed | &mdash; |
| G-24 | Weak symbol coalescing takes the loaded library's definition | pending the owner | &mdash; |
| G-25 | A category property redeclaring a native class's own keeps the class's attributes | pending the owner | &mdash; |
| G-26 | Three Objective-C residuals that fail loudly | project default | &mdash; |
| G-27 | Commpage fields shared by name use the running system's values; long double and large struct varargs read wrongly through a converted va_list | pending the owner | Recommendation: accept. |
| G-28 | A commpage access that bypasses the load callbacks; the CPU number answers with cluster 0 | project default | &mdash; |
| G-29 | An import variant bound to the wrong symbol | fixed | &mdash; |
| G-30 | A native va_list passed into a lifted function; an undeclared import only called through a pointer | pending the owner | Recommendation: accept. |
| G-31 | What reading Apple's x86_64 code for a private import's convention cannot see | pending the owner | Recommendation: accept. |
| G-32 | Private imports that route leaves refused | project default | &mdash; |

</details>

<details>
<summary><strong>Network</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-39 | Some boot recipes still inject macOS 26's vmxnet3 driver | project default | &mdash; |

</details>

<details>
<summary><strong>Platform</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-52 | Every way programs run here needs Apple's x86_64 libraries, which macOS 27 ships for Rosetta and a later release may drop | pending the owner | Native and recompiled programs load them; the translator itself starts on Apple's x86_64 dyld and libSystem. macOS 27, the target, ships them. Apple has said general-purpose Rosetta stays through macOS 27 and only a subset after. A translator needing no x86_64 user space would remove most of the exposure; it is not started (docs/roadmap.md). |

</details>

<details>
<summary><strong>Sandbox</strong> &mdash; 3 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-03 | With the borrowed macOS 26 Sandbox kext, profile loading is bypassed, so services run unsandboxed | retired | Gone on the 27-only root, which uses 27's own recompiled kext; accepted as interim on the hybrid and bridge images. |
| G-41 | Bridge-root boots run the borrowed kext with its bypass, and one stopped on a 27-format profile it cannot read | project default | &mdash; |
| G-45 | The recompiled Sandbox kext ran only on Apple's kernel | fixed | Built against the self-built kernel and booted, 2 of 2. |

</details>

<details>
<summary><strong>Self-built kernel</strong> &mdash; 3 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-44 | One sanitizer query always answers 0 | project default | &mdash; |
| G-46 | Recompiled launchd aborted without a sysctl 27 registers | pending the owner | Fix built and booted; causation not isolated. |
| G-51 | A translated process may raise its own memory limit, by up to 64 MB | pending the owner | It loosens a kernel policy. |

</details>

<details>
<summary><strong>Tests</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-38 | A test script step that could trigger that wait by its own order | project default | &mdash; |

</details>

<details>
<summary><strong>Translator</strong> &mdash; 2 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-49 | A check-then-store race in the guest-memory write fallback | pending the owner | It can crash the translator. |
| G-50 | A shared slid-cache file changed in place, in a part this process does not sample | pending the owner | Could give a wrong result silently. |

</details>

<details>
<summary><strong>Translator identity patch M</strong> &mdash; 2 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-16 | Three ways a translated program's view of its own signature could still differ | direction set by the owner | Fix by reusing Apple's own code; partly done. |
| G-40 | At boot the first spawn of one daemon gets no answer from a framework check, falls back and crashes | project default | &mdash; |

</details>

<details>
<summary><strong>Translator patch L</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-13 | Four descriptor or rename races between a check and the call it guards | accepted by the owner | &mdash; |

</details>

<details>
<summary><strong>Translator path patch H</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-11 | Eight corner cases where path rewriting still differs from the kernel (link budgets, check-then-use, long joined paths, effective ids, searchability) | accepted by the owner | Documented coverage gaps; one is resolved by running at 27's real paths. |

</details>

<details>
<summary><strong>Translator sysctl patch K</strong> &mdash; 1 record</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-12 | Five corner cases in sysctl answers (bad buffers, unlisted hardware names, name normalisation) | accepted by the owner | &mdash; |

</details>

<details>
<summary><strong>Userland</strong> &mdash; 2 records</summary>

|  | What could go wrong | Who decided | Notes |
|---|---|---|---|
| G-07 | An in-image import rename to let the plug-in daemon link | retired | Dropped from boot recipes; plug-ins will use 27's own daemon under translation. |
| G-08 | 36 message ids in 27's disk-arbitration client renumbered to match macOS 26's daemon | direction set by the owner | Stop mixing versions: run 27's own daemon instead. |

</details>

<sub>Generated from `data/gaps.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:gaps-risks:end -->

### How to read this list

The **who decided** column is the point. A record marked *project default* is one that
fails loudly and loses nothing if it is hit, so it was accepted under a standing rule
without being escalated; anything that could fail *silently*, lose data or loosen a
security policy has to be accepted by the project owner personally, and until it is, it
sits as **pending the owner**. The pending ones are therefore the interesting rows: they
are the gaps judged serious enough that nobody has signed them off.

Several records are marked *fixed* or *retired* rather than accepted. Those are kept
deliberately. A gap that was accepted, then turned out to be a real defect and was fixed,
is evidence about how well the accepting is being done, and deleting the row would remove
that evidence.

### What is not in this list

- Gaps nobody has thought of. The list is bounded by what review has reached, and the
  review is mostly the project's own, with some cross-checking from other sources.
- Anything about the host machine or the lab it runs in. This page is about the guest.
- Exact code locations. A record says what could go wrong and what the fix would be, not
  where to find the line.
