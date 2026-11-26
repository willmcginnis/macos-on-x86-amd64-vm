# What is being attempted

[&larr; back to the README](../README.md)


macOS 27.0.1 is an Apple-silicon release. Its installer and its boot path are built for
arm64e. But Apple has not finished removing x86-64 from the operating system: most of
the frameworks still carry an x86-64 slice, and 27.0.1's Kernel Debug Kit still ships an
x86-64 kernel. What is missing is the boot path &mdash; `launchd`, `amfid`, `logd`,
`sandboxd`, `kernelmanagerd`, `WindowServer`'s launcher and many daemons are arm64e-only:
of the 421 `launchd` job labels listed in [docs/launchd-labels.md](launchd-labels.md),
122 run a program that 27.0.1 ships without an x86-64 slice (117 distinct programs).

The project closes that gap three ways, and most of the tables in this record are really about
which of the three each piece is using today:

1. **Apple's own x86-64 code**, where 27.0.1 still ships it, used as Apple shipped it
   apart from the few edits listed in
   [docs/translator-patches.md](translator-patches.md#on-disk-edits-to-apple-files).
2. **Recompiling** Apple's arm64e build to x86-64, function by function, and linking it
   against 27's own x86-64 libraries. The project calls this *lifting*. Where a
   user-space row gives a count of functions that pass, the recompiled functions were run
   against Apple's originals under emulation from the same starting state; not every
   recompiled program has such a count, and for the kernel extension only some functions are checked that way
   ([docs/components.md](components.md#tools)).
3. **Translation**: running Apple's arm64e program as itself, through an exec route added
   to a self-built kernel, with an open-source user-space translator as the engine. The
   program keeps its own Apple identity (not yet when a translated program starts an
   arm64-only one itself: [docs/gaps.md](gaps.md), B26); only the instructions are someone
   else's problem.

Where a piece has none of the three yet, a part from macOS 26 (Tahoe) stands in, or a
small script does, and that is recorded as *in progress* rather than done. Replacing
every one of those stand-ins is the remaining work.
