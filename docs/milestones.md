# Milestones

[&larr; back to the README](../README.md)

Each milestone has a **pass condition**, and the date is when that condition was first
met. The pass conditions of the `M` series, M5 aside, were set in the project's plan
before the work on them started; those of G1, the `R` and `L` series and M5 are worded
here from the project's record, some of them after the work. That difference matters: a pass
condition chosen afterwards tends to describe whatever happened, and this list is meant
to be checkable by someone who was not there.

A milestone being *done* means its pass condition was met at least once, on at least one
configuration. It does not mean the thing stayed working as later pieces changed around
it, and in a few cases it did not &mdash; where a later configuration lost something an
earlier milestone had, the note says so. Dates are US Pacific time.

The identifiers are in four series, because the goal was re-cut twice as the work
showed what was actually hard: `M` for the original route, `G` for graphics, `R` for
the re-cut goal of a root built only from macOS 27's own system volume, and `L` for the
steps from the login window to the desktop on that root. The series are
kept as they were rather than renumbered, so that earlier write-ups still refer to the
same things.

<!-- generated:milestones-table:start -->
Milestones, in the order they were set. Dates are when the pass condition was first met, US Pacific time.

|  | Milestone | Pass condition | State | First met | Evidence | Notes |
|---|---|---|---|---|---|---|
| M0 | Harness control: macOS 26 x86 recovery boots under QEMU, KVM and OpenCore | Verbose kernel log on serial, root mounted, launchd running | done | 2026-10-26 | measured | &mdash; |
| M1a | Build a kernel collection around 27.0.1's x86_64 kernel | A collection holding 27's kernel and the requested kexts | done | 2026-10-26 | measured | &mdash; |
| M1 | Boot 27.0.1's x86_64 kernel | 27's kernel banner on serial, then root mount | done | 2026-10-26 | measured | Needed seven early-boot patches. |
| M1b | Map the commpage into user processes | launchd survives its first commpage read | done | 2026-10-26 | measured | &mdash; |
| M2 | 27's x86_64 frameworks under macOS 26's boot daemons | Multi-user boot and an ssh root shell | done | 2026-10-26 | measured | &mdash; |
| M3 | 27's own userland: 27's x86_64 dyld, shared cache and programs | A root shell, and sw_vers reads 27 | done | 2026-10-27 | measured | The cache had to be re-signed at 4 KiB hash pages. |
| G1 | A window on screen (hybrid image) | Recovery window, Disk Utility and the installer drawn and taking input | done | 2026-10-26 | measured | Software compositor; small on-disk edits since 2026-11-04. |
| R1 | A root built only from 27.0.1's own system volume | Boots with a Data volume to launchd's daemon phase | done | 2026-11-04 | measured | &mdash; |
| R2 | 27's own Sandbox kext, recompiled to x86_64, enforcing | Deny probes give native 27.0.1's results | done | 2026-11-04 | measured | &mdash; |
| R3 | A kernel built from Apple's published source boots 27.0.1 | loginwindow and ssh, no kernel patch | done | 2026-11-04 | measured | Self-built; not Apple's kernel. Met on the hybrid image (macOS 26's recovery volume with 27's files placed over it); the 27-only root has no graphical session. |
| R4 | 27's own launchd as pid 1 and xpcproxy, recompiled | Boots to a running payload; the kernel's hash of pid 1 names the lift | done | 2026-11-08 | measured | Since 2026-11-24 the project's default test bases, each one standalone disk image, carry both (2 test boots each). |
| R5 | 27's own amfid, logd, logd_helper and sandboxd in place of macOS 26's | Each stays up and does its job | in progress | &mdash; | measured | logd and logd_helper replaced (3 boots, running; read-back measured on other configurations); amfid stays up (4 boots; validation partly tested); sandboxd is not shown staying up under launchd (docs/boot-programs.md). |
| R6 | Fold the furthest configuration into one disk image | The image boots with its placed files verified | not started | &mdash; | not measured | &mdash; |
| R7 | launchd's own sshd reachable from the host | Host logins to launchd's sshd job | not started | &mdash; | not measured | &mdash; |
| R8 | No macOS 26 piece left in the boot | logd, logd_helper, the nine kexts, kmutil and the APFS EFI driver all replaced | in progress | &mdash; | measured | logd and logd_helper replaced (3 boots); the nine kexts, kmutil and the APFS EFI driver remain. So does macOS 26's x86 boot.efi, which the condition as first written left out: 27.0.1 ships no x86 boot loader. |
| M4 | A desktop on 27's own programs | loginwindow, then Finder, with no macOS 26 program in the session | in progress | &mdash; | measured | The pass condition is not met: there is no usable desktop yet. On test overlays of the 27-only root, 27's loginwindow under translation draws the login window, a typed login is authorized, the user session starts and the first-login User Account Updater completes (milestones L1 to L4). With a per-user marker, placed by the test, that skips the first-login Setup Assistant, the Dock, Finder, SystemUIServer and Control Center start (L5), and in one boot a menu bar and a wallpaper were drawn and a click opened the Apple menu (L6, L7); but WindowManager keeps crashing and no Finder window has been drawn (docs/gaps.md, B22 and B25). |
| M5 | Graphics acceleration | A Metal device in the guest | not started | &mdash; | not measured | &mdash; |
| L1 | 27's login window on the 27-only root | The login window drawn on screen on a test overlay of the 27-only root | done | 2026-11-23 | measured | Drawn in 2 of 2 boots of one set-up and 1 of 2 of another when nothing held the display awake: whether it appears looks like a race with the guest's display going to sleep (inferred from one boot's timing, in which SecurityAgent logged that it was showing its window one second before the screens slept). It was also drawn in each of the 11 later boots in which a login was typed. |
| L2 | A typed login authorized | A name and password typed at the login window, and the console login authorized | done | 2026-11-24 | measured | In the first 2 boots no session followed; authorized again in each of the 9 later login boots. |
| L3 | The user session starts | Processes of the logged-in user run after the login | done | 2026-11-24 | measured | Needed a translator fix for mapping short shared-memory objects (docs/translator-patches.md, Q2). 9 boots. |
| L4 | The first-login User Account Updater completes | loginwindow reports that User Account Updater exited with success after the first login | done | 2026-11-24 | measured | Needed xpcproxy relinked with the newer link tools, so that accountsd could start (docs/boot-programs.md). 6 boots. Its Screen Time plug-in logged a failed call along the way in each. |
| L5 | The Dock, Finder, SystemUIServer and Control Center start after the first login | All four running after the first login and still running, once each, at the last reading of the boot | done | 2026-11-24 | measured | With a per-user marker, placed by the test, that skips the first-login Setup Assistant; in the 2 boots in which Setup Assistant ran, the Dock, Finder and SystemUIServer never started (Control Center did). 4 boots. The Dock was drawn in 3 of 4 boots, each between about 20 and 35 minutes after the login. |
| L6 | A menu bar and a wallpaper drawn after the login | Both on screen in a frame taken after the first login | done | 2026-11-25 | measured | With the per-user marker that skips Setup Assistant (L5). 1 boot, the first completed login boot with the translator fix for app-sandboxed programs (docs/translator-patches.md, AA). WindowManager crashed and was restarted all through it (docs/gaps.md, B25). |
| L7 | A click reaches a control | A pointer click on a menu-bar item opens its menu | done | 2026-11-25 | measured | With the per-user marker that skips Setup Assistant (L5). One click, on the Apple menu, which then showed its whole menu in the later frames (1 boot). An earlier click, on a display test overlay, changed nothing on screen. |

<sub>Generated from `data/milestones.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:milestones-table:end -->

## What the remaining ones need

The milestones still open are not all of the same size:

- **R5** is not finished engineering. `logd`, `logd_helper` and `amfid` run, but
  `sandboxd` is not shown staying up when `launchd` starts it: a translator fix removed
  the failure when it was started by hand (2 boots), yet the `launchd`-started instance kept
  restarting in the second of them. That fix (patch X) had an open race and has been
  replaced by patch Y, whose boots are not written up in this record yet.
- **R6** is folding work: the pieces exist and have been seen running, and what is left
  is getting them into one disk image at the same time.
- **R7** needs a host login to `launchd`'s own `sshd` job, in place of the debug
  `sshd` the test payload starts. **R8** needs a replacement for each piece still
  borrowed from macOS 26: the boot loader, nine kernel extensions, the collection
  builder and the boot loader's APFS driver.
- **M4** (a desktop) needs the arm64e-only session programs to run, translated or
  recompiled. So far, on test overlays of the 27-only root, 27's WindowServer and
  `loginwindow` under translation draw the login window, a typed login is authorized, the
  user session starts and the first-login User Account Updater finishes (L1 to L4). With
  Setup Assistant skipped by a per-user marker the test places, the Dock, Finder,
  SystemUIServer and Control Center start, and in one boot a menu bar and a wallpaper were
  drawn and a click opened the Apple menu (L5 to L7). What is missing is a usable desktop:
  WindowManager keeps crashing and no Finder window has been drawn ([gaps.md](gaps.md), B22
  and B25). A recompiled `loginwindow`
  launches and exits in one overlay boot (see [components.md](components.md#graphics) and
  [boot-programs.md](boot-programs.md)).
- **M5** (graphics acceleration) needs a Metal device, and there is no route to one yet.
  It is the furthest off, and nothing below it depends on it.
