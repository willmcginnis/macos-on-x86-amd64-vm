# Roadmap

As of **2026-11-24**. The goal has not changed: macOS 27 as a virtual machine guest on
ordinary x86-64 hardware, under QEMU and KVM on Linux. What this page adds is the order the
work is done in, and what each stage leans on.

The project works in two stages. **Stage 1 is something that works**, built from whatever
works today, including x86 code from Apple that the project means to stop depending on
later. **Stage 2 is the longer tail**: replacing what stage 1 leans on. Leaning on that code
during stage 1 is the plan, not a departure from the goal.

Every claim here carries how it is known, as in the rest of the repository: *measured*
means seen in a boot or a test, with `n`; *inferred* means reasoned and not measured.

## Stage 1: working first

**The goal of this stage.** macOS 27.0.1 booting under KVM to a desktop someone can use. It
is not reached yet. Every program on the system runs in one of five ways:

| Way | What runs | Example |
|---|---|---|
| Apple's x86-64 build, natively | Apple's own 27.0.1 program, unchanged. Of 27.0.1's 911 `launchd` job files, 604 name a program that still ships an x86-64 build (measured) | `accountsd`, `notifyd`, `configd` |
| Translated | Apple's arm64e program, unchanged, run through the open-source Maclator translator by an exec route in the project's kernel | `loginwindow`, `WindowServer`'s launcher, `amfid` |
| Lifted | Apple's arm64e program recompiled ahead of time to an x86-64 program that calls Apple's x86-64 libraries | `launchd` (pid 1), `xpcproxy` |
| Borrowed from macOS 26 | An x86-64 build from macOS 26 (Tahoe), where 27.0.1 has none or the swap to 27's is still pending | nine kexts, the boot loader's APFS driver, the tool that builds the kernel collection |
| Built by the project | The kernel, from Apple's published xnu source (macOS 26.5's), and a few small pieces | the kernel; a small stand-in for `mount` |

Which program uses which way, row by row: [boot-programs.md](boot-programs.md) and
[launchd-labels.md](launchd-labels.md).

**What done means for stage 1** (the project's working definition): from a cold boot of the
default test base, a user logs in and reaches the desktop, with the menu bar, the Dock and
Finder drawn, and can open and use an app; on more than one boot, not once; drawn without a
GPU (software rendering), as bring-up was always meant to be.

**Where it stands.** The steps reached so far are in the README,
[Where it stands](../README.md#where-it-stands), each with its date and `n`. In
short: the login window is drawn, a typed login is authorized, the user session starts and
the first-login User Account Updater completes; then no window of the first-login Setup
Assistant appears and no Dock or Finder start ([gaps.md](gaps.md), B22, 2 boots). In the
first of those boots the disk also ran out of space after 16 stores of the translator's
cache, mostly duplicated slid shared-cache data, came to about 9 GiB (B23); in the second
it did not, and the screen went black the same way.

## Stage 2: the longer tail

**What it is.** Replacing what stage 1 leans on, so that the boot needs neither macOS 26
pieces nor Apple's x86-64 user space. In this order of priority; parts can run in parallel
where they do not compete:

1. **The remaining macOS 26 pieces.** A known list: the x86 boot loader (`boot.efi`, which
   27.0.1 does not ship), nine kexts, the tool that builds the kernel collection, and the
   boot loader's APFS driver; some boot set-ups also still add macOS 26's `vmxnet3` network
   driver ([gaps.md](gaps.md), G-39). What each needs:
   - the real-time clock kext: 27.0.1's Kernel Debug Kit has an x86-64 build of it, so this
     one is a swap;
   - the kernel-collection builder: a way to build an x86 kernel collection without macOS
     26, since 27's own `kmutil` refuses to build one for x86-64;
   - the APFS driver: 27's APFS container carries no x86 EFI driver;
   - the other eight kexts have no 27 x86-64 build, and the ACPI, APIC, HPET and EFI
     runtime ones have no arm64e counterpart to translate either. How they get replaced is
     not known yet.

   None of these is in the way of the two current stage 1 blockers (inferred: neither
   blocker involves one).
2. **The dependence on Apple's x86-64 libraries.** [gaps.md](gaps.md), G-52, which is
   *pending the owner*. Below.

### The x86-64 library dependency, stated plainly

macOS 27 still ships an x86-64 user space so that Apple's Rosetta can run Intel programs on
Apple silicon: an x86-64 shared library cache of 3,918 libraries in 27.0.1, and an x86-64
build of `dyld`. Every way of running user-space programs listed above (native, lifted
and translated) needs it **as built today**:

- Apple's native x86-64 programs load their libraries from it.
- Lifted programs bind every library call to Apple's x86-64 builds of those libraries.
  Lifting more programs makes more of the boot depend on the full set.
- Translated programs need it too, though far less of it: the translator is itself an
  x86-64 program that starts on Apple's x86-64 `dyld` and `libSystem`. In two boots, a
  translated process was seen to map x86-64 `libSystem` files from Apple's Rosetta
  component (measured, n = 2 boots); whether translated processes also map the x86-64
  shared cache itself has not been settled (the file listings taken cannot answer it: they
  do not show the shared region as a file, even for a native process).

Apple has said that Rosetta stays available as a general-purpose tool through macOS 27, and
that after that only a subset, aimed at older games, will be kept
([Apple's page](https://developer.apple.com/documentation/apple-silicon/about-the-rosetta-translation-environment)).
What that subset will keep is not known. The target is macOS 27, which ships all of it, so
nothing is broken today; but as built, no way of running user-space programs here would
survive a release that drops it.

The planned answer, in order:

1. a translator that needs no x86-64 user space at all (no x86-64 `dyld`, no `libSystem`);
2. a test boot with no x86-64 user-space code: the x86-64 cache and `dyld`'s x86-64 build
   moved aside, every program translated;
3. a boot that translates even the programs that still ship an x86-64 build.

Lifting continues where it pays today (pid 1, programs on hot paths, early boot), as a
layer over the translator. Every lifted program is built from Apple's unchanged arm64e
program, so the plan is that each can fall back to running translated; that the fallback
works has not been checked yet (safeguards below), and it protects against the library
cache going away only once step 1 exists.

Not known in stage 2: what Apple's post-27 subset keeps; whether the x86 kernel in the
Kernel Debug Kit, the kit's x86 kexts and the x86 xnu source keep coming; how fast a fully
translated system runs; and what a lifted program that imports an arm64e-only framework
would do (none has been met so far).

## Safeguards, and their state today

| Practice | State, 2026-11-24 |
|---|---|
| Every lifted program stays runnable under the translator, checked by a boot with only translated programs, in which each program has to do its job, not only start | **Not in place.** On the default test base, the original of at least one lifted program (`xpcproxy`) is not kept beside it. No translated-only test boot has run |
| At each new macOS release or beta, before it is adopted, read what it still ships for x86: the programs' x86-64 builds, the x86-64 library cache and its count, `dyld`'s x86-64 build, whether every library the lifted programs import is still there (an unchanged count can hide a missing one), the Kernel Debug Kit's x86 kernels and kexts, and the x86 xnu source | **Not yet run as one check.** 27.2 was read in parts. First due at the next release adopted |
| A translator with no x86-64 user space (stage 2, step 1) | **Not started.** When it starts is the owner's decision |

## What would change this plan

- **A macOS release or beta that drops or shrinks** the x86-64 library cache, a program's
  x86-64 build, the Kernel Debug Kit's x86 kernels or kexts, or the x86 xnu source: the
  library-dependency work becomes urgent. The release check above is how it would be
  noticed.
- **Apple's post-27 subset keeps the whole cache**: that work becomes insurance rather than a
  requirement.
- **A stage 1 blocker that turns out to need a stage 2 replacement first**: that replacement
  moves ahead.
- **The upstreams.** The translator's changes are kept on a public branch of the project's
  own fork, and each change that fits upstream is still offered there. How much lives
  upstream follows how upstream review goes. QEMU stays the base unless the quarterly base
  check in [UPSTREAMS.md](../UPSTREAMS.md#base-check) says otherwise.
- **The owner's decisions**: when the translator work of stage 2 starts, and the order
  itself.

There are no how-to guides here today; dated, best-effort guides are planned once stage 1
is done.
