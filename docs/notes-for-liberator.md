# Two DriverKit findings from a macOS 27 guest on x86

Notes for the author of [Liberator](https://github.com/nullmoth/liberator), and for anyone
else getting macOS 27 to start on Intel hardware. They are measurements from this
project's guest only, with how many boots each rests on and what was not tested.

**Where they come from.** macOS 27.0.1 (26A434) as a QEMU and KVM guest on Linux, with no
GPU acceleration, on the project's own lab configuration (described in the rest of this
repository). Its kernel is the project's own, built from Apple's published macOS 26.5
source, not Apple's 27.0.1 kernel. That is a different setup from real hardware.

**They may be old news.** Liberator's release notes say it already reaches the desktop on
real hardware. Its public release notes for Beta 1 list *"Start to the login window and the desktop on the NVIDIA card, with
Metal"*, and its Beta 6 notes (v3.0.0-beta.6, 2026-11-23) say *"sharingd, Finder, Dock,
Control Center and the widget service start once and stay up."* So either finding may never come up there. Nothing here asks for
anything, and nothing here says how Liberator works inside.

| | What we saw | Cause | What fixed it | Boots |
|---|---|---|---|---|
| 1 | The I/O Registry never goes quiet; disks other than the boot disk stay hidden | An arm64e-only DriverKit serial extension whose kernel side, `com.apple.driver.driverkit.serial`, had no x86_64 copy in the boot collection (how this holds matching back is inference) | Apple's own x86_64 `IOUserSerial.kext` from 27.0.1's Kernel Debug Kit added to the boot collection; **or** the extension moved out of the folder the system scans | 4 and 7 |
| 2 | Apple's HID driver extension crashes at start and is relaunched over and over | The x86_64 DriverKit shared cache's `libdyld` forwards calls to dyld one table slot short (read statically) | The eight forwarding stubs moved up one slot, and the cache re-signed | 3 |

The boot counts are small. Each fix was seen working in every boot counted, which shows it
can work; it does not show it always does.

## 1. An arm64e-only serial extension keeps the registry busy

27.0.1 ships `com.apple.DriverKit-IOUserDockChannelSerial.dext` in
`/System/Library/DriverExtensions`, with no x86_64 slice. Its kernel side is
`com.apple.driver.driverkit.serial` (`IOUserSerial.kext`), which the kernel collections we
booted did not carry for x86_64.

**Without a fix** (counts are per boot):

| Reading | Result | Boots counted |
|---|---|---|
| `IOUserResources` busy 1 in every sample | yes | 4 |
| `IOUserResources` registered, *not matched* | yes | 2 (the boots with that detailed reading) |
| `kernelmanagerd` stall events, each naming only `IOUserResources` | 4 per boot | 4 |
| WindowServer's `IOKitWaitQuiet: (iokit/common) I/O Timeout` line | 1 to 3 per boot | 3 |
| Disk media hidden from matching (so non-boot disks never appear) | 5 | 1 |

<details>
<summary><strong>Fix A: Apple's x86_64 IOUserSerial.kext in the boot collection</strong> (4 boots)</summary>

The kext comes from 27.0.1's Kernel Debug Kit, which ships it with an x86_64 slice. The
test collection held the same 196 entries as the one it replaced, with identical UUIDs, plus
this one kext. All 373 of its imports resolved against our self-built kernel and `IOSerialFamily`.
The serial extension was left where Apple put it.

| Reading | Result, 4 boots |
|---|---|
| `com.apple.driver.driverkit.serial` loaded | yes (read in 2 boots; the collection carrying it confirmed in all 4) |
| `IOUserResources` | matched, busy 0, after 749 ms to 6.7 s of busy time |
| Registry nodes still busy late in the boot | 0 (of 290 to 394) |
| `kernelmanagerd` stall lines | 0 |
| Hidden disk media | 0 |

The extension itself: in all four boots the kernel logged one short burst for it (a
non-fatal AMFI line, then one `failed to launch server` line), and no later retry was seen
while the boots were observed (8.5 to 15 minutes). In the two boots where it was checked, the
nub was gone afterwards. In the two boots
where `kernelmanagerd`'s own log was read, it logged at least three and at least two launch
attempts in that burst. Longer boots, and what happens on a later rematch or a power
event, were not read.

</details>

<details>
<summary><strong>Fix B: the extension moved out of the scanned folder</strong> (7 boots)</summary>

In one comparison, moving the `.dext` to a folder the system does not scan was the only
change to the system disk from a boot that stalled. Across the seven boots counted with it moved (some also carried
other changes, such as a newer translator):

| Reading | Result |
|---|---|
| Registry quiet late in the boot (0 busy nodes; `IOUserResources` matched wherever it was read) | 7 of 7 |
| `kernelmanagerd` stall events | 0, in every boot that counted them |
| Hidden disk media | 0, in every boot that counted them |
| WindowServer's `IOKitWaitQuiet` timeout line | 0, in the 2 boots where it was counted |

Fix A replaces the boot collection (with one of Apple's own kexts added) and leaves the
`.dext` in place; fix B keeps the collection the boot already had and moves the `.dext`. Which is better for a given setup is a judgement, not a measurement.

</details>

<details>
<summary><strong>What the quiet registry let through: disks</strong></summary>

With either fix, 27's own `diskarbitrationd` (Apple's arm64e program, under translation in
our guest) listed the disks, in some boots only after a delay (below), and a scratch-disk
round passed: the disk formatted, then mounted, unmounted and mounted again through
DiskArbitration, with a file written and read back: **7 of 8 boots**. In the eighth, the scratch disk
was used before DiskArbitration had listed it, so the first mount found no disk.

When DiskArbitration first lists the non-boot disks varies: in one boot all were listed at
the first listing (about 191 s); in another, three were still missing at 453 s. In three
boots at matched host load the delay happened with either fix and was longest with the
extension moved aside. DiskArbitration's log shows it probing disks one
at a time, and the delay followed how late the registry went quiet in that boot (inference,
3 boots; its per-disk log lines are redacted, so per-disk timing is not readable).

</details>

<details>
<summary><strong>What is inference, and what was not tested</strong></summary>

- **Inference:** that the extension's personality, waiting on a kernel side that is not
  there, is what holds `IOUserResources` back. The fixes are measured; the mechanism was not
  traced.
- **Inference:** whether the `IOKitWaitQuiet` timeout matters to anything that waits on
  WindowServer.
- **Not tested:** 27.2, real hardware, Apple's own x86_64 kernel, any collection built
  differently from ours, and
  the other 14 DriverKit extensions in 27.0.1 that have no x86_64 slice (none of them held
  up matching in our boots).

</details>

**Three read-only checks distinguish this registry symptom.** `ioreg -w0 -r -c
IOUserResources -d 2` shows whether `IOUserResources` is matched and whether it or a child
is busy. `kmutil showloaded` shows whether `com.apple.driver.driverkit.serial` is loaded.
`lipo -archs` on the extension's executable shows its slices. If the registry is quiet and
your disks appear, that rules out the problem described in this section.

## 2. The DriverKit `libdyld` calls dyld one slot short

**What we saw** without a fix: Apple's HID driver extension (`com.apple.AppleUserHIDDrivers`)
crashed at start, with SIGBUS, before any driver code ran, and was launched again and
again: 6 launches and 17 crash lines in the boot used as the baseline.

**Cause, read statically from 27.0.1's own files.** In the x86_64 DriverKit shared cache,
eight of the 95 `libdyld` stubs that forward to dyld's API table (those using slots `0x418`
to `0x450`) sit one slot (8 bytes) below where 27.0.1's own dyld keeps those functions; the
other stubs agree with dyld or could not be matched by name. Seven of the eight are matched
by name; the eighth's name is stripped in the cache, and that it is shifted too is inferred
from its two shifted neighbours. For example, `_dyld_call_with_writable_tpro_memory` is
called through `0x420`; dyld keeps it at `0x428`. So each of those calls reaches the
neighbouring function. The same audit, run on the macOS
(not DriverKit) x86_64 cache's `libdyld`, detected no shifted stub. That the DriverKit build of
`libdyld` leaves out one table entry is our guess, not confirmed.

**With the eight stubs moved up one slot** and the cache re-signed (every page hash
re-checked), in 3 boots on two different overlays:

| Reading | Without (1 boot) | With the fix |
|---|---|---|
| HID extension launches | 6 | 1, never relaunched (2 boots read) |
| Crash lines naming it | 17 | 0 (3 boots) |
| Kernel `server launched, validating` | 0 | logged (3 boots) |
| Both HID event services (keyboard and tablet) started | no | yes (1 boot read in full) |
| Still up late in the boot | no | yes, at 15 and 34 minutes (2 boots) |

Two things it did not fix. The extension uses a steady 0.05 to 0.1 CPU-second per second
with no input, for a reason we have not found. And input still does not fully work in our
guest: in two boots with the fix and a recompiled HID plug-in (one of them outside the three
above), key presses reached the keyboard
queue and WindowServer logged the process holding keyboard focus as their destination, while
the last pointer events seen were in the HID queue.

This only matters if Apple's DriverKit drivers are loaded on Intel. It was not tested on
27.2 or with any other driver extension.

## Also seen in our guest, cause not found

| What | Boots | Note |
|---|---|---|
| The login window was not shown in the six boots this row first counted. SecurityAgent logs that it is showing the window; its main thread stays blocked in a synchronous LocalAuthentication call that never gets a reply | 1 (stack samples); the missing window, 6 | See below the table. **Since found to appear; most likely a race** (2026-11-24 update below) |
| `loginwindow`'s child job `com.apple.MenuBarAgent` exits with status 134, three times per boot | 2 | Not shown to relate to anything else |

On the login window: the peer of SecurityAgent's blocked call is probably `coreauthd`, from
a log line on the same thread (inference). In the same boot WindowServer also refused
SecurityAgent the front once, because another program had made itself the only one allowed
there; which of the two holds the window back is not settled. Render-fence timeouts in
WindowServer's log were checked and are not the wall: WindowServer still presented changes
after them.

Both could come from our virtual machine or our translated programs rather than from
macOS 27 on Intel; nothing here says which.

**Update, 2026-11-24.** The login window does appear. Whether it does looks like a race:
SecurityAgent has to show its window before the guest's display goes to sleep, and once the
display sleeps nothing redraws it (inferred from one boot's timing, in which SecurityAgent
logged that it was showing its window one second before the screens slept; no frame of
that boot showed it). The window was drawn in 2 of 2 boots of one set-up and
1 of 2 of another when nothing kept the display awake, and in each of 7 later boots in
which a login was typed; keyboard input typed at it reached it. Where the login goes after
that: [docs/gaps.md](gaps.md), B21 and B22.

---

Boots from 2026-11-09 to 2026-11-24, most of them on 2026-11-22 and 2026-11-23. The counts on
this page come from the project's private working notes, at the revision named in
[`data/status.json`](../data/status.json).
