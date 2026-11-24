# Boot-path programs

[&larr; back to the README](../README.md)

The programs that have to work before anything else can. For each one: how Apple ships
it in macOS 27.0.1, how it is being run here, and what is actually known about it.

The second column is the reason the project exists. Where it says **arm64e only**, Apple
ships no x86-64 build of that program in 27.0.1, so it has to be recompiled, translated,
borrowed from macOS 26, or stood in for. Where it says **x86_64**, Apple's own build runs
unchanged and the row is there only to record that it was seen working.

<!-- generated:boot-programs-table:start -->
| Program | How Apple ships it in 27.0.1 | How it runs here | State | Evidence | n | Notes |
|---|---|---|---|---|---|---|
| launchd (pid 1) | arm64e only | lifted | done | measured | 3 | All 1,468 functions lifted, 1,403 pass the differential test, 0 fail. In one boot the kernel's code-directory hash for pid 1 equals the lift's, proving which launchd ran. Not yet folded into a disk image. Stopping a service no longer panics the guest: 0 panics in 2 boots with the fix, against 1 in a control boot without it. |
| xpcproxy | arm64e only | lifted | done | measured | 2 | 100 of 100 functions lifted, 99 pass. 0 environment errors in 1,020 job spawns; macOS 26's xpcproxy fails beside 27's launchd. |
| amfid | arm64e only | translated | in progress | measured | 4 | Stays up, exit status 0, in 4 boots, where macOS 26's amfid crashes in every boot. In one boot it refused an ad hoc signed program carrying a restricted entitlement, with Apple's error for that case; an edited-signature test did not discriminate. |
| logd | arm64e only | translated | in progress | measured | 3 | 27's own logd runs translated as the logd job on the furthest configuration, exit status 0 in 3 of 3 boots; in one, the kernel's code-directory hash for it equals Apple's arm64e build. 27's log command reading its messages back was measured on other configurations (2 of 2), not yet on this one. |
| logd_helper | arm64e only | translated | in progress | measured | 3 | 27's own logd_helper runs translated on the furthest configuration, exit status 0 in 3 of 3 boots; in one, the kernel's code-directory hash for it equals Apple's arm64e build. Doing its job is not measured. |
| sandboxd | arm64e only | translated | in progress | measured | 2 | Died at boot when launchd started it, before patch X. With X, a hand-started copy got past the failure in 2 of 2 boots; in the second, the launchd-started copy was still restarting, though that copy ran with a trace option the hand-started one did not, so the two are not a controlled comparison. That fix (patch X) had an open race and has been replaced by patch Y, whose boots are not written up in this record yet. |
| taskgated | arm64e only | translated | in progress | measured | 1 | Not started in the boot measured (on demand). |
| kernelmanagerd | arm64e only | translated | in progress | measured | 1 | Starts and checks in. The 240-second registry stall it reported is explained (docs/gaps.md, B18): with either measured fix, 0 stall lines in every test boot counted. Neither fix is in the furthest configuration yet. |
| kmutil and kextload | arm64e only | translated | in progress | measured | 1 | Run to rc 0 in the guest, but rc 0 was not a load: a kext was not loaded afterwards. Collections are still built by macOS 26's kmutil. |
| sshd | arm64e only | translated | in progress | measured | 9 | Started in debug mode by a test payload, not by launchd. With a 180 s login timeout, 3 of 3 logins in 8 of 9 boots and 1 of 3 in one; with a 60 s timeout, none (docs/components.md). |
| diskarbitrationd | arm64e only | lifted | in progress | measured | several boots; 1 serving | 603 functions pass, 0 fail. Relinked with the newer link tools, on a root with the registry stall fixed, it ran the whole boot and both disk rounds (a scratch disk and a RAM disk) passed through it (1 boot). Earlier, in one image, its clients got no answer from it, lifted or translated. Apple's own arm64e build under translation served the scratch-disk round in 7 of 8 boots counted with the registry quiet. |
| powerexperienced | arm64e only | lifted | done | measured | several boots | 726 functions pass, 0 fail. Runs for the whole boot. Under translation it needed the translator to count its own memory against the process limit. |
| dirhelper | arm64e only | lifted | done | measured | several boots; 2 for the folder | 38 of 38 functions pass. Serves for the whole boot. It creates the root of the system's per-user temporary folders itself, so the copy the project used to pre-create on the image is retired (2 of 2 boots). |
| fsck | arm64e only | lifted | done | measured | several boots | Boot task. The real work is in 27's x86_64 fsck_apfs, which it calls. |
| dirs_cleaner | arm64e only | lifted | done | measured | several boots | Boot task. An early kernel panic at its exit was traced to the borrowed macOS 26 Sandbox kext, not to this program; the recompiled 27 Sandbox kext does not have it. |
| cc_fips_test | arm64e only | lifted | done | measured | several boots | Boot task. Calls 27's x86_64 corecrypto. |
| seputil (prngseedd) | arm64e only | lifted | done | measured | several boots | Boot task (data protection), run to success. The prngseedd job label, which uses the same program, did not start in the boot counted in docs/launchd-labels.md. |
| xpcroleaccountd | arm64e only | lifted | in progress | measured | several boots | Placed; launchd runs it as a boot task, but whether the task succeeds has not been read. Its job label did not start in the boot counted in docs/launchd-labels.md. |
| rootless-init, prng_seedctl, init_exclavekit, ifcstart, launchctl | arm64e only | lifted | done | measured | several boots | Boot tasks and tools; run to success. |
| KernelEventAgent | arm64e only | lifted | in progress | measured | 1 | Exited with status 74 about every 10 s, at an indirect call into a lazy-load helper section the link tools did not translate. Relinked with the newer link tools, it ran once for the whole boot with 0 such exits (1 boot). What it does is not read. |
| mount (for the Preboot volume) | arm64e only | stand-in | in progress | measured | several boots | A 945-byte shell script that runs 27's own x86_64 apfs_boot_util. Lifting 27's mount would retire it. |
| tccd | x86_64 | Apple x86_64 | done | measured | 2 | Crashed about 11 times per boot until the recompiled Sandbox kext answered a storage-class check; 0 crashes since. |
| configd, notifyd, syslogd, mDNSResponder, securityd, cfprefsd, opendirectoryd, trustd, powerd | x86_64 | Apple x86_64 | done | measured | many boots | Running. Doing their job is measured only for configd (a DHCP address) and the shells. |
| WindowServer launcher | arm64e only | translated | in progress | measured | several boots | Starts under translation on the 27-only root. In one boot it never opened the framebuffer; in 6 later boots, with the two display byte edits placed in the root's cache, it stayed up, 5 of them showed the boot progress window, and none showed a login window (docs/components.md). The graphics stack it starts (SkyLight) does ship x86_64. |
| loginwindow | arm64e only | lifted | in progress | measured | 1 | Measured on one boot of a later overlay of the 27-only root, signed as a bundle with the lab key: it launches, then exits with status 70 every time (236 starts, 236 exits, no crash report). The cause of status 70 is not read. On the display test overlays 27's arm64e loginwindow runs translated instead and keeps running through the observed boots (3 read); in one boot it logged that it had registered for the notification that the login window was shown. |
| Dock, Finder, SystemUIServer | arm64e only | none | not started | measured | &mdash; | Planned as 27's own programs. |
| Apple HID driver extension (keyboard and tablet services) | x86_64 | Apple x86_64 | in progress | measured | 1 boot crashing read in full, 3 with the fix, and a static reading | Apple's HID driver extension (com.apple.AppleUserHIDDrivers) ships an x86_64 slice, which runs against 27's x86_64 DriverKit shared cache. It crashed at start with SIGBUS before any driver code ran, and was launched again and again (6 launches and 17 crash lines in one boot; 6 and 5 crash reports in two boots of later overlays). Cause, read statically from 27.0.1's own files: that cache's libdyld forwards calls to dyld one table slot short, so a call reaches the neighbouring function, which writes into a read-only code page. With the shifted forwarding stubs moved up one slot and the cache re-signed, it launched once and was not relaunched (2 boots read), no crash line named it (3 boots on two overlays), and both HID event services started (1 boot read in full). Keyboard and mouse input does not work yet. |

<sub>Generated from `data/boot-programs.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:boot-programs-table:end -->

## The two rows that carry the most weight

**`launchd` (pid 1)** is the one that makes the rest meaningful. It is Apple's own
arm64e `launchd` from 27.0.1, recompiled to x86-64: all 1,468 of its functions, 1,403 of
which pass a test that runs the recompiled function and Apple's original under emulation
from the same starting state and compares the results, with none failing and the
remainder giving no reading. In one boot the kernel's own code-directory hash for pid 1
matched the hash of the recompiled binary, which is what makes the claim "this launchd
ran" a measurement rather than an inference from a file having been placed on disk.

**`xpcproxy`** matters because it is how `launchd` starts everything else. macOS 26's
`xpcproxy` fails next to 27's `launchd`; the recompiled 27 one produced no environment
errors across 1,020 job spawns.

## What the states hide

Several rows say *in progress* for quite different reasons, and the distinction is worth
making explicit:

- **Runs but is not known to work.** `amfid` stays up for a whole boot, where macOS 26's
  crashes in every boot &mdash; but its signature checks are only partly tested. In one
  boot it refused an ad hoc signed program carrying a restricted entitlement, with
  Apple's error for that case (n = 1); a test with an edited signature did not
  discriminate. So nothing broader should be concluded about code-signing enforcement on
  this configuration.
- **Runs and does not serve.** `diskarbitrationd` runs for the whole boot, and 603 of its
  functions pass the differential test, yet in one image its clients get no answer from
  it. That is true whether it is recompiled or translated, which points at something
  other than the recompile.
- **Exits with a status nobody has read yet.** `KernelEventAgent` exited with status 74
  in the one boot measured. The cause has not been looked at.
- **Succeeds without doing the thing.** `kmutil` and `kextload` run to exit status 0
  under translation, but no extension was loaded afterwards. Exit 0 here is not evidence
  of success, and collections are still built with macOS 26's `kmutil`.
- **Dies.** `sandboxd` died at boot when `launchd` started it, before patch X. That
  translator fix removed the failure for a hand-started copy in 2 of 2 boots; in the second of them the
  `launchd`-started copy kept restarting (it ran with a trace option the hand-started one
  did not). That fix (patch
  X) had an open race and has been replaced by patch Y, whose boots are not written up in
  this record yet.

The last point in that list is the general caution for this whole page: for most of these
programs the measurement is that the process existed and kept running. Only a few
(`configd` getting a DHCP address, the shells, `dirhelper` serving, `tccd` stopping its
crashes) were measured doing their job.
