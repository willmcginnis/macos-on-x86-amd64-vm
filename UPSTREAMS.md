# Upstreams

The projects this work builds on, the projects working on something close to it, and this
project's open items with them. Every number is a reading, with the date it was read; none
of it is a judgement of a project or of the people who run it.

**Read on 2026-11-24**, between 22:19 and 22:45 UTC (2:19 to 2:45 PM US Pacific), through
GitHub's and GitLab's public APIs, read-only. Our own open items were read again at about
00:15 UTC on 2026-11-25 (4:15 PM Pacific on 2026-11-24), once more at 03:47 UTC
(7:47 PM Pacific), after the #19 and #22 updates, and again at 16:29 UTC on 2026-11-25
(8:29 AM Pacific) and at 04:51 UTC on 2026-11-26 (8:51 PM Pacific on 2026-11-25), when
nothing in them had changed. The activity tables are from the
2026-11-24 read.

## How each column was read

- **Commits 30 / 90 / 365 d**: commits on the default branch whose committer date is within
  that many days of the read. Merge commits count.
- **Committers, last year**: distinct GitHub logins, else author e-mail addresses, among the
  last 365 days' commits. One person with two identities counts twice.
- **Releases**: GitHub releases, with the latest one's version and date. Tags are given
  where a project tags without making releases.
- **Response sample**: up to 10 of the newest issues and pull requests opened 14 to 120 days
  before the read (2 to 120 days where marked); how many
  got a first comment, review, merge or close from anyone other than the person who opened
  it (bots excluded), and the median time to it. Anyone counts, not only maintainers.
- **Licence**: GitHub's licence field; where GitHub reports one it does not recognise, the
  licence file if it was read. Dates are US Pacific time unless marked UTC.

## What we build on

| Project | What we use it for | Commits 30 / 90 / 365 d | Committers, last year | Releases (latest) | Response sample | Licence | Source |
|---|---|---|---|---|---|---|---|
| QEMU | the hypervisor front end, with KVM | 1,082 / 3,324 / 10,158 | at least 577 (from 10,000 of the year's 10,158 commits) | no GitHub releases; v11.1.3 (2026-10-28), v11.2.0-rc1 (2026-11-18) as tags | not read: GitLab's per-issue notes need a login. Of the first 100 GitLab issues opened 2026-09-25 to 2026-10-25, 69 had a note and 35 were closed | GPL-2.0 and others | [gitlab.com/qemu-project/qemu](https://gitlab.com/qemu-project/qemu) (mirror: [github.com/qemu/qemu](https://github.com/qemu/qemu)) |
| EDK2 (OVMF is its `OvmfPkg`) | the guest's UEFI firmware | 117 / 625 / 1,996 (`OvmfPkg`: 19 / 59 / 221) | 219 | 37 (edk2-stable202611, 2026-11-23) | 8 of 10, median 59 h | not read (GitHub reports none it recognises) | [github.com/tianocore/edk2](https://github.com/tianocore/edk2) |
| OpenCorePkg | the boot loader | 3 / 46 / 83 | 13 | 63 (1.0.8, 2026-09-27) | 3 of 10, median 90 h; its issue tracker, 4 of 10, median 301 h | BSD-3-Clause | [github.com/acidanthera/OpenCorePkg](https://github.com/acidanthera/OpenCorePkg), issues in [acidanthera/bugtracker](https://github.com/acidanthera/bugtracker) |
| OSX-KVM | the OVMF firmware build the guests use | 0 / 0 / 4 | 4 | 0 | 0 of 8 | none detected by GitHub | [github.com/kholia/OSX-KVM](https://github.com/kholia/OSX-KVM) |
| Maclator | the user-space translator for Apple's arm64e programs | 6 / 32 / 32 (32 in all; the repository was created 2026-09-30) | 6 | 0 (no tags) | 7 of 10, median 94 h | MIT | [github.com/linuxkid473/maclator](https://github.com/linuxkid473/maclator) |

Apple's published xnu source, which the project's kernel is built from, is not in the
table: it is published as source drops, not developed in the open.

### Our open items there

| Where | Item | Opened | State, 2026-11-25 |
|---|---|---|---|
| Maclator | [pull request #12](https://github.com/linuxkid473/maclator/pull/12): an unreadable path name returns EFAULT instead of crashing | 2026-11-08 | merged 2026-11-10 |
| Maclator | [pull request #16](https://github.com/linuxkid473/maclator/pull/16): the same for an unreadable sysctl name or MIB | 2026-11-23 | open; one follow-up comment of ours, 2026-11-23 |
| Maclator | [pull request #17](https://github.com/linuxkid473/maclator/pull/17): the same for an unreadable code-signing `fcntl` structure | 2026-11-23 | open |
| Maclator | [pull request #18](https://github.com/linuxkid473/maclator/pull/18): reading an executable mapping's Mach-O header without crashing | 2026-11-23 | open |
| Maclator | [pull request #19](https://github.com/linuxkid473/maclator/pull/19): EFAULT or E2BIG instead of crashing on bad `posix_spawn` or `execve` arguments | 2026-11-23 | open; its description revised by us, 2026-11-24 |
| Maclator | [pull request #22](https://github.com/linuxkid473/maclator/pull/22): answering the runtime's own sysctl names (builds on #16) | 2026-11-23 | open; a commit of ours added (the names stay usable in a forked child) and its description revised, 2026-11-24 |
| Maclator | [issue #20](https://github.com/linuxkid473/maclator/issues/20): each translated launch keeps its own slid copy of the shared cache; would sharing it be welcome? | 2026-11-23 | open |
| Maclator | [issue #21](https://github.com/linuxkid473/maclator/issues/21): store-release ordering on x86; would a small fence fix be welcome? | 2026-11-23 | open |

The items opened on 2026-11-23 were about two days old at the latest read, with no review
or comment from anyone else yet. The repository's earlier
merged pull requests were merged between 6 hours and 19 days after they were opened.

The translator changes this project runs, including ones not offered upstream yet, are on a
public branch of its fork:
[willmcginnis/maclator, branch `queue/boot-tested-2026-11-24`](https://github.com/willmcginnis/maclator/tree/queue/boot-tested-2026-11-24)
(54 commits on Maclator's current main, read on 2026-11-25, with internal comments removed:
the changes behind the project's default test bases, among them one root-owned store of
slid shared-cache data for every user (R2) and the fix for guest memory (Z), which are in
the base adopted on 2026-11-25; the fix for app-sandboxed programs (AA); the fix that keeps WindowManager up (AB; all four in
[docs/translator-patches.md](docs/translator-patches.md)); and some smaller fixes to the
translation cache, the translator's imitation of kernel events and their tests). The
translator built from the branch's tip has not itself been booted. Local builds carrying
R2, Z, AA and AB have been; the smaller fixes have unit tests only.

## Others working on something close

What each project says it does is from its own README, read on 2026-11-24; none of these
was run by this project except where a note says so.

| Project | What it says it does | Commits 30 / 90 / 365 d | Committers, last year | Releases (latest) | Response sample | Licence | Source |
|---|---|---|---|---|---|---|---|
| Liberator | runs macOS 27 on PCs with OpenCore; targets PCs with an NVIDIA card | 72 / 72 / 72 (repository created 2026-11-12) | 1 | 6 prereleases (v3.0.0-beta.6, 2026-11-23) | 3 of 10, median 1.5 h (2 to 120 days) | PolyForm Noncommercial 1.0.0 | [github.com/nullmoth/liberator](https://github.com/nullmoth/liberator) |
| 1401 | macOS on PCs; the base Liberator starts from | 327 / 680 / 680 (created 2026-10-07) | 6 | 83 (v3.1, 2026-11-24) | not sampled | not read (GitHub reports none it recognises) | [github.com/nullmoth/1401](https://github.com/nullmoth/1401) |
| hao-patcher | macOS 27 on a 2012 Intel MacBook Pro | 1,142 / 1,142 / 1,142 (created 2026-11-10) | 1 | 0 (1 tag) | 2 of 10, median 2.6 h (2 to 120 days) | MIT | [github.com/lythka/hao-patcher](https://github.com/lythka/hao-patcher) |
| hao-runtime | an arm64 and arm64e translator for Intel Macs, used by hao-patcher | 440 / 440 / 440 (created 2026-11-10) | 1 | 1 (v0.0.1-beta.1, 2026-11-22) | no items yet | MIT | [github.com/lythka/hao-runtime](https://github.com/lythka/hao-runtime) |
| anathema | aims to translate macOS's arm64 kernel and user space to x86-64 on its own virtual machine; its README says it reaches the start of `launchd` so far | 57 / 57 / 57 (created 2026-11-22) | 3 | 0 | no items old enough | MIT | [github.com/riftaway7-code/anathema](https://github.com/riftaway7-code/anathema) |
| rebar | arm64 macOS programs on x86-64 Macs | 112 / 112 / 112 (created 2026-11-04; no commits after 2026-11-08) | 1 | 9 (v0.8.0, 2026-11-08) | 0 of 3 (2 to 120 days) | MIT | [github.com/OverlordDev/rebar](https://github.com/OverlordDev/rebar) |
| GoldenGate-VM | macOS 27 for Apple silicon under QEMU's emulation of an Apple-silicon virtual Mac, on x86 | 3 / 3 / 3 (created 2026-10-31) | 1 | 0 | not sampled | GPL-2.0 | [github.com/JeanxPereira/GoldenGate-VM](https://github.com/JeanxPereira/GoldenGate-VM) |
| hackmate-goldengate | macOS 27 on an emulated Apple-silicon machine under QEMU | 0 / 57 / 57 (created 2026-09-18) | 2 | 0 | not sampled | none detected by GitHub | [github.com/hackmatelabs/hackmate-goldengate](https://github.com/hackmatelabs/hackmate-goldengate) |
| GoldenAlcatraz | macOS 27 x86 kernel patches for AMD processors | 2 / 2 / 2 (created 2026-11-12) | 1 | 0 | not sampled | none detected by GitHub | [github.com/dssoftx/GoldenAlcatraz](https://github.com/dssoftx/GoldenAlcatraz) |
| graft | a kext that routes kernel functions for other kexts in macOS virtual machines | 38 / 38 / 38 (created 2026-11-10) | 1 | 5 (v0.4.0, 2026-11-16) | not sampled | not read (GitHub reports none it recognises) | [github.com/steelbrain/graft](https://github.com/steelbrain/graft) |
| mos-qemu | an Apple paravirtual GPU device for QEMU on Linux | 0 / 3 / 215 | 1 | 1 (v0.5, 2026-04-19) | not sampled | GPL-2.0 | [github.com/MattJackson/mos-qemu](https://github.com/MattJackson/mos-qemu) |
| OpenCore Legacy Patcher | newer macOS on older Intel Macs (real hardware, not virtual machines) | 42 / 81 / 100 | 4 | 96 (3.0.0-rc.5, 2026-10-28) | 2 of 5, median 119 h | not read (GitHub reports none it recognises) | [github.com/dortania/OpenCore-Legacy-Patcher](https://github.com/dortania/OpenCore-Legacy-Patcher) |
| quickemu | a QEMU launcher, macOS guests among others | 8 / 8 / 149 | 12 | 45 (4.9.9, 2026-02-10) | 2 of 10, median 22 h | MIT | [github.com/quickemu-project/quickemu](https://github.com/quickemu-project/quickemu) |
| Docker-OSX | macOS under KVM in containers | 0 / 0 / 0 | 0 | 0 | 0 of 5 | GPL-3.0 | [github.com/sickcodes/Docker-OSX](https://github.com/sickcodes/Docker-OSX) |
| macOS-Simple-KVM | macOS under KVM | 0 / 0 / 0 | 0 | 0 | not sampled | none detected by GitHub | [github.com/foxlet/macOS-Simple-KVM](https://github.com/foxlet/macOS-Simple-KVM) |
| UTM | a QEMU front end for macOS hosts; macOS guests on Apple silicon | 274 / 451 / 575 | 34 | 136 (v5.0.9-2, 2026-11-18) | 7 of 8, median 42 h | Apache-2.0 | [github.com/utmapp/UTM](https://github.com/utmapp/UTM) |
| Darling | a Darwin user space on Linux (x86-64, and arm64 on arm64 hosts) | 2,363 / 2,381 / 2,464 | 39 | 14 (v0.1.20260608, 2026-06-09) | 5 of 10, median 9 h (2 to 120 days) | GPL-3.0 | [github.com/darlinghq/darling](https://github.com/darlinghq/darling) |
| vphone-cli | tooling for Apple virtual devices | 621 / 1,631 / 1,998 (created 2026-02-26) | 77 | 84 (2.17.1, 2026-11-13) | not sampled | MIT | [github.com/Lakr233/vphone-cli](https://github.com/Lakr233/vphone-cli) |
| darwin-vm | Darwin virtual machine research | 0 / 14 / 14 (created 2026-08-27) | 1 | 0 | not sampled | MIT | [github.com/jprx/darwin-vm](https://github.com/jprx/darwin-vm) |

### Tried in this project's lab

Each was tried for comparison, in throwaway guests: hao-runtime in one boot, Liberator in one
installation over several boots. One try says what can work in that set-up; it says nothing
about how well a project works where it is meant to run.

- **Liberator**, Beta 6, in a KVM guest of macOS 26.7.3 under OpenCore. Its preflight
  check refused the guest because it has no supported NVIDIA card, which is what its
  documentation says it needs. With two configuration changes of ours to the guest, its
  preparation completed; on a later boot, after its first-login setup had been completed in
  an earlier boot, the macOS 27.2 it installed started to a desktop that answered clicks
  (n = 1). Liberator does not say it supports virtual machines, and this is not a
  claim that it does. Notes for its author: [docs/notes-for-liberator.md](docs/notes-for-liberator.md).
- **hao-runtime**, started by hand from the command line on this project's 27.0.1 guest.
  It ran a small arm64 and arm64e test program and a notification and audit probe
  correctly, and kept one of Apple's daemons running for the 120 s it was watched (n = 1).
  Its built-in tables are for macOS 27.2.1, and it said so when run on 27.0.1.
  Daemons started by `launchd`, logins and the desktop were not tried.

## Design references

Projects whose design this work reads, or whose tools it uses in tests. Several translate
in the opposite direction.

| Project | What it is | Commits 30 / 90 / 365 d | Committers, last year | Releases (latest) | Response sample | Licence | Source |
|---|---|---|---|---|---|---|---|
| FEX-Emu | x86 programs on arm64 | 170 / 583 / 2,124 | 48 | 69 (FEX-2611.1, 2026-11-11) | 10 of 10, median 1.1 h | MIT | [github.com/FEX-Emu/FEX](https://github.com/FEX-Emu/FEX) |
| box64 | x86-64 Linux programs on other processors | 178 / 485 / 1,811 | 51 | 22 (v0.4.4, 2026-08-02) | 10 of 10, median 0.8 h | MIT | [github.com/ptitSeb/box64](https://github.com/ptitSeb/box64) |
| remill | lifts machine code, AArch64 among others, to LLVM IR | 2 / 3 / 70 | 14 | 46 (v6.0.1, 2026-04-21) | 6 of 9, median 4.9 h | Apache-2.0 | [github.com/lifting-bits/remill](https://github.com/lifting-bits/remill) |
| Unicorn | a CPU emulator library; this project's lifter tests run against it | 0 / 0 / 2 (its dev branch: 1 / 21 / 50) | 2 | 29 (2.1.4, 2025-09-09) | 4 of 10, median 73 h | GPL-2.0 | [github.com/unicorn-engine/unicorn](https://github.com/unicorn-engine/unicorn) |
| touchHLE | runs old iPhone OS apps on other systems, with an ARM-to-x86 JIT | 0 / 49 / 560 | 13 | 8 (v0.3.0, 2026-10-01) | 8 of 10, median 2.9 h | MPL-2.0 | [github.com/touchHLE/touchHLE](https://github.com/touchHLE/touchHLE) |
| ipsw | Apple firmware and Mach-O research tool | 175 / 456 / 1,381 | 23 | 1,023 (v3.1.751, 2026-11-24) | 10 of 10, median 0.7 h | MIT | [github.com/blacktop/ipsw](https://github.com/blacktop/ipsw) |
| Asahi Linux documentation | Apple platform internals | 10 / 22 / 75 | 26 | 0 | not sampled | not read (GitHub reports none it recognises) | [github.com/AsahiLinux/docs](https://github.com/AsahiLinux/docs) |

## Base check

Once a quarter, best effort, this section asks whether QEMU is still the right base for the
work, and is replaced in place with the date and the answer. Earlier answers are in this
file's git history.

**2026-11-24.** Not yet done as a review of its own. What was read today: QEMU's activity, in
the table above. Of the projects above that run macOS on x86 under another base, GoldenGate-VM
and hackmate-goldengate use QEMU too, but emulate an Apple-silicon machine and run the
arm64 kernel rather than an x86 one, and anathema runs its own virtual machine. No
hypervisor other than QEMU was evaluated. QEMU stays the base. The next check is due by
2027-02-16.

## How this page is kept

- Refreshed best effort, about weekly or every 28 days, when the work brings it up; there is
  no schedule.
- Each refresh is one commit that rewrites the numbers and the read date in place. The git
  history of this file is its changelog.
- Only measured columns. A project's description is what its own README says.
