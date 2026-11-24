# Milestones

[&larr; back to the README](../README.md)

Each milestone has a **pass condition**, and the date is when that condition was first
met. The pass conditions of the `M` series, M5 aside, were set in the project's plan
before the work on them started; those of G1, the `R` series and M5 are worded here from
the project's record, some of them after the work. That difference matters: a pass
condition chosen afterwards tends to describe whatever happened, and this list is meant
to be checkable by someone who was not there.

A milestone being *done* means its pass condition was met at least once, on at least one
configuration. It does not mean the thing stayed working as later pieces changed around
it, and in a few cases it did not &mdash; where a later configuration lost something an
earlier milestone had, the note says so. Dates are US Pacific time.

The identifiers are in three series, because the goal was re-cut twice as the work
showed what was actually hard: `M` for the original route, `G` for graphics, and `R` for
the re-cut goal of a root built only from macOS 27's own system volume. The series are
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
| R4 | 27's own launchd as pid 1 and xpcproxy, recompiled | Boots to a running payload; the kernel's hash of pid 1 names the lift | done | 2026-11-08 | measured | Not yet folded into a disk image. |
| R5 | 27's own amfid, logd, logd_helper and sandboxd in place of macOS 26's | Each stays up and does its job | in progress | &mdash; | measured | logd and logd_helper replaced (3 boots, running; read-back measured on other configurations); amfid stays up (4 boots; validation partly tested); sandboxd is not shown staying up under launchd (docs/boot-programs.md). |
| R6 | Fold the furthest configuration into one disk image | The image boots with its placed files verified | not started | &mdash; | not measured | &mdash; |
| R7 | launchd's own sshd reachable from the host | Host logins to launchd's sshd job | not started | &mdash; | not measured | &mdash; |
| R8 | No macOS 26 piece left in the boot | logd, logd_helper, the nine kexts, kmutil and the APFS EFI driver all replaced | in progress | &mdash; | measured | logd and logd_helper replaced (3 boots); the nine kexts, kmutil and the APFS EFI driver remain. So does macOS 26's x86 boot.efi, which the condition as first written left out: 27.0.1 ships no x86 boot loader. |
| M4 | A desktop on 27's own programs | loginwindow, then Finder, with no macOS 26 program in the session | in progress | &mdash; | measured | The pass condition is not met and there is no graphical session. In progress because, on overlays of the 27-only root, 27's WindowServer under translation stays up and in most boots shows the boot progress window, and 27's loginwindow runs; no login window has appeared (docs/gaps.md, B21). |
| M5 | Graphics acceleration | A Metal device in the guest | not started | &mdash; | not measured | &mdash; |

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
  recompiled. So far, on overlays of the 27-only root, 27's WindowServer under
  translation stays up and in most boots shows the boot progress window, and 27's
  `loginwindow` runs, but no login window has appeared ([gaps.md](gaps.md), B21); in an earlier boot
  WindowServer did not open the framebuffer at all, and a recompiled `loginwindow`
  launches and exits in one overlay boot (see [components.md](components.md#graphics) and
  [boot-programs.md](boot-programs.md)). There is no graphical session.
- **M5** (graphics acceleration) needs a Metal device, and there is no route to one yet.
  It is the furthest off, and nothing below it depends on it.
