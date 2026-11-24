# Kernel-collection entries

[&larr; back to the README](../README.md)

Every entry of the kernel collection that the furthest macOS 27.0.1-only root booted
with, and where each one came from.

The classification is a measurement rather than a record of intent: each entry's Mach-O
UUID was compared against the x86-64 extensions in Apple's 27.0.1 Kernel Debug Kit and
against the set borrowed from macOS 26, so an entry is in the class its bytes say it is
in, not the class the build recipe meant to put it in.

<!-- generated:kexts-summary:start -->
| Class | Entries | What it means |
|---|---|---|
| `apple-27-x86_64` | 185 | Apple's own 27.0.1 x86_64 kext from the Kernel Debug Kit |
| `borrowed-tahoe-x86_64` | 9 | an x86_64 kext from macOS 26 (Tahoe); for 8 of the 9, 27.0.1 ships no x86_64 build of it, and AppleRTC is the exception (27.0.1 has one, not yet swapped in) |
| `apple-27-lifted` | 1 | Apple's own 27.0.1 arm64e kext, recompiled to x86_64 by the project's lifter |
| `self-built-kernel` | 1 | the kernel itself, built by the project from Apple's published xnu source (see docs/components.md) |
| **All entries** | 196 | &mdash; |

<sub>Generated from `data/kexts.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:kexts-summary:end -->

The large majority are Apple's own x86-64 builds, taken from the Kernel Debug Kit and
not edited by the project. That is the single most surprising fact about this whole
exercise: for almost every entry this guest's collection needs, Apple still builds an
x86-64 kernel extension in a release that ships only for Apple silicon.

## The entries that are not Apple's 27 x86-64 builds

**Nine borrowed from macOS 26.** Eight of them &mdash; the ACPI set (`AppleACPIPlatform`,
`AppleACPIButtons`, `AppleACPIEC`), the interrupt controller, the EFI runtime and NVRAM
extensions, the high-precision timer and a bus power controller &mdash; are borrowed
because 27.0.1 ships no x86-64 build of them, so there was nothing else to use. The
ninth, `AppleRTC`, is different: 27.0.1's Kernel Debug Kit *does* contain an x86-64 build
of it, so that one is borrowed only because nobody has swapped it yet, and it should be
the easiest entry on this page to retire.

The eight are the most awkward dependency here. They are platform extensions, and a
version mismatch at that layer is exactly the sort of thing that produces a guest panic
that is hard to read. One such panic was in fact traced to the borrowed macOS 26 Sandbox
extension rather than to the program that appeared to cause it, which is part of why that
extension was the first one replaced.

**One recompiled.** The Sandbox extension, which is 27.0.1's own arm64e `Sandbox.kext`
with the 958 reachable functions of its 967 recompiled to x86-64 and wrapped in a
generated adapter.
It loads and it enforces: file read, write and exec denials, a network denial and
default-deny all give the same answers as native macOS 27.0.1 does, across two boots that
agreed on every probe row, plus one on a later kernel. Two things inside it are *not*
closed: the network-outbound probe rows gave no reading, and a named-`sysctl` denial is
consistent with enforcement without proving it. This is the route intended for the eight
borrowed platform extensions that 27.0.1 ships no x86-64 build of.

**One self-built kernel.** Not Apple's. See
[docs/translator-patches.md](translator-patches.md#self-built-kernel-versions).

## Full list

Bundle identifiers only. Versions are not recorded here, which is a gap: an entry's class
is pinned by UUID, but this page does not let a reader tell which macOS 26 build the nine
borrowed extensions came from.

<!-- generated:kexts-table:start -->
### `apple-27-x86_64`

Apple's own 27.0.1 x86_64 kext from the Kernel Debug Kit.

<details>
<summary><strong>185 entries</strong></summary>

| Bundle identifier |
|---|
| `com.apple.AppleEthernetAquantiaAqtionFirmware` |
| `com.apple.AppleFSCompression.AppleFSCompressionTypeDataless` |
| `com.apple.AppleFSCompression.AppleFSCompressionTypeZlib` |
| `com.apple.AppleSystemPolicy` |
| `com.apple.BootCache` |
| `com.apple.audio.TrustedClockingKEXT` |
| `com.apple.driver.AppleAHCIPort` |
| `com.apple.driver.AppleActuatorDriver` |
| `com.apple.driver.AppleBCMWLANBusInterfacePCIeMac` |
| `com.apple.driver.AppleBCMWLANCoreMac` |
| `com.apple.driver.AppleBSDKextStarter` |
| `com.apple.driver.AppleBluetoothDebug` |
| `com.apple.driver.AppleBluetoothDebugService` |
| `com.apple.driver.AppleBluetoothHIDKeyboard` |
| `com.apple.driver.AppleBluetoothHIDMouse` |
| `com.apple.driver.AppleBluetoothModule` |
| `com.apple.driver.AppleBluetoothMultitouch` |
| `com.apple.driver.AppleConvergedIPCOLYBTControl` |
| `com.apple.driver.AppleConvergedPCI` |
| `com.apple.driver.AppleCredentialManager` |
| `com.apple.driver.AppleDiskImages2` |
| `com.apple.driver.AppleEffaceableNOR` |
| `com.apple.driver.AppleEffaceableStorage` |
| `com.apple.driver.AppleEffaceableTDM` |
| `com.apple.driver.AppleEpochManager` |
| `com.apple.driver.AppleEthernetAquantiaAqtion` |
| `com.apple.driver.AppleEthernetRL` |
| `com.apple.driver.AppleFDEKeyStore` |
| `com.apple.driver.AppleFileSystemDriver` |
| `com.apple.driver.AppleGameControllerPersonality` |
| `com.apple.driver.AppleHIDALSService` |
| `com.apple.driver.AppleHIDKeyboard` |
| `com.apple.driver.AppleHIDMouse` |
| `com.apple.driver.AppleHPM` |
| `com.apple.driver.AppleHollywood` |
| `com.apple.driver.AppleIRController` |
| `com.apple.driver.AppleInputDeviceSupport` |
| `com.apple.driver.AppleIntelLpssDmac` |
| `com.apple.driver.AppleIntelLpssGspi` |
| `com.apple.driver.AppleIntelLpssI2C` |
| `com.apple.driver.AppleIntelLpssI2CController` |
| `com.apple.driver.AppleIntelLpssSpiController` |
| `com.apple.driver.AppleKeyStore` |
| `com.apple.driver.AppleLSIFusionMPT` |
| `com.apple.driver.AppleLockdownMode` |
| `com.apple.driver.AppleMemorexCDROMDriver` |
| `com.apple.driver.AppleMobileFileIntegrity` |
| `com.apple.driver.AppleMultiFunctionManagerMac` |
| `com.apple.driver.AppleMultitouchDriver` |
| `com.apple.driver.AppleOLYHALMac` |
| `com.apple.driver.ApplePIODMA` |
| `com.apple.driver.ApplePVPanic` |
| `com.apple.driver.AppleRAID` |
| `com.apple.driver.AppleSEPManager` |
| `com.apple.driver.AppleSMC` |
| `com.apple.driver.AppleSSE` |
| `com.apple.driver.AppleSkywalkAVB` |
| `com.apple.driver.AppleSmartBatteryManager` |
| `com.apple.driver.AppleSyntheticGameController` |
| `com.apple.driver.AppleThunderboltDPAdapterFamily` |
| `com.apple.driver.AppleThunderboltDPInAdapter` |
| `com.apple.driver.AppleThunderboltDPOutAdapter` |
| `com.apple.driver.AppleThunderboltNHI` |
| `com.apple.driver.AppleThunderboltPCIDownAdapter` |
| `com.apple.driver.AppleThunderboltPCIUpAdapter` |
| `com.apple.driver.AppleThunderboltUTDM` |
| `com.apple.driver.AppleTopCaseHIDEventDriver` |
| `com.apple.driver.AppleUSBCardReader` |
| `com.apple.driver.AppleUSBDisplays` |
| `com.apple.driver.AppleUSBHIDMouse` |
| `com.apple.driver.AppleUSBHostMergeProperties` |
| `com.apple.driver.AppleUSBMassStorageInterfaceNub` |
| `com.apple.driver.AppleUSBMergeNub` |
| `com.apple.driver.AppleUSBODD` |
| `com.apple.driver.AppleUSBTDM` |
| `com.apple.driver.AppleUSBTopCaseDriver` |
| `com.apple.driver.AppleVirtIO` |
| `com.apple.driver.AppleXsanScheme` |
| `com.apple.driver.BCMWLANFirmware4364.Hashstore` |
| `com.apple.driver.BCMWLANFirmware4378.Hashstore` |
| `com.apple.driver.BCMWLANFirmware4387.Hashstore` |
| `com.apple.driver.BCMWLANFirmware4388.Hashstore` |
| `com.apple.driver.CoreStorage` |
| `com.apple.driver.CoreStorageFsck` |
| `com.apple.driver.DiskImages` |
| `com.apple.driver.DiskImages.FileBackingStore` |
| `com.apple.driver.DiskImages.HTTPBackingStore` |
| `com.apple.driver.DiskImages.KernelBacked` |
| `com.apple.driver.DiskImages.RAMBackingStore` |
| `com.apple.driver.DiskImages.ReadWriteDiskImage` |
| `com.apple.driver.DiskImages.SparseDiskImage` |
| `com.apple.driver.DiskImages.UDIFDiskImage` |
| `com.apple.driver.IOBluetoothHIDDriver` |
| `com.apple.driver.IOImageLoader` |
| `com.apple.driver.IOSlaveProcessor` |
| `com.apple.driver.MKE_LF_D211A` |
| `com.apple.driver.MKE_SR_8171` |
| `com.apple.driver.NVSMU` |
| `com.apple.driver.PioneerSuperDrive` |
| `com.apple.driver.PlasmonUDO` |
| `com.apple.driver.WriteProtectedMediaDriver` |
| `com.apple.driver.corecapture` |
| `com.apple.driver.iPodSBCDriver` |
| `com.apple.driver.mDNSOffloadUserClient` |
| `com.apple.driver.usb.AppleUSBCommon` |
| `com.apple.driver.usb.AppleUSBEHCI` |
| `com.apple.driver.usb.AppleUSBEHCIPCI` |
| `com.apple.driver.usb.AppleUSBHostBillboardDevice` |
| `com.apple.driver.usb.AppleUSBHostCompositeDevice` |
| `com.apple.driver.usb.AppleUSBHostDeviceSupport` |
| `com.apple.driver.usb.AppleUSBHostPacketFilter` |
| `com.apple.driver.usb.AppleUSBHostiOSDevice` |
| `com.apple.driver.usb.AppleUSBHub` |
| `com.apple.driver.usb.AppleUSBVHCI` |
| `com.apple.driver.usb.AppleUSBVHCICommon` |
| `com.apple.driver.usb.AppleUSBXHCI` |
| `com.apple.driver.usb.AppleUSBXHCIPCI` |
| `com.apple.driver.usb.IOUSBHostHIDDevice` |
| `com.apple.driver.usb.cdc` |
| `com.apple.driver.usb.cdc.ecm` |
| `com.apple.driver.usb.cdc.ncm` |
| `com.apple.driver.usb.ethernet.asix` |
| `com.apple.driver.usb.networking` |
| `com.apple.driver.usb.realtek8153patcher` |
| `com.apple.driver.watchdog` |
| `com.apple.filesystems.apfs` |
| `com.apple.filesystems.autofs` |
| `com.apple.filesystems.hfs.kext` |
| `com.apple.filesystems.lifs` |
| `com.apple.filesystems.tmpfs` |
| `com.apple.iokit.AppleBCM5701Ethernet` |
| `com.apple.iokit.CoreAnalyticsFamily` |
| `com.apple.iokit.EndpointSecurity` |
| `com.apple.iokit.IO80211Family` |
| `com.apple.iokit.IOACPIFamily` |
| `com.apple.iokit.IOAHCIBlockStorage` |
| `com.apple.iokit.IOAHCIFamily` |
| `com.apple.iokit.IOAHCISerialATAPI` |
| `com.apple.iokit.IOATABlockStorage` |
| `com.apple.iokit.IOATAFamily` |
| `com.apple.iokit.IOATAPIProtocolTransport` |
| `com.apple.iokit.IOBDStorageFamily` |
| `com.apple.iokit.IOBluetoothFamily` |
| `com.apple.iokit.IOBufferCopyController` |
| `com.apple.iokit.IOBufferCopyEngineFamily` |
| `com.apple.iokit.IOCDStorageFamily` |
| `com.apple.iokit.IODVDStorageFamily` |
| `com.apple.iokit.IOGameControllerFamily` |
| `com.apple.iokit.IOHIDFamily` |
| `com.apple.iokit.IOKitRegistryCompatibility` |
| `com.apple.iokit.IONVMeFamily` |
| `com.apple.iokit.IONetworkingFamily` |
| `com.apple.iokit.IOPCIFamily` |
| `com.apple.iokit.IORDMAFamily` |
| `com.apple.iokit.IOReportFamily` |
| `com.apple.iokit.IOSCSIArchitectureModelFamily` |
| `com.apple.iokit.IOSCSIBlockCommandsDevice` |
| `com.apple.iokit.IOSCSIMultimediaCommandsDevice` |
| `com.apple.iokit.IOSCSIParallelFamily` |
| `com.apple.iokit.IOSCSIReducedBlockCommandsDevice` |
| `com.apple.iokit.IOSMBusFamily` |
| `com.apple.iokit.IOSerialFamily` |
| `com.apple.iokit.IOSkywalkFamily` |
| `com.apple.iokit.IOSlowAdaptiveClockingFamily` |
| `com.apple.iokit.IOStorageFamily` |
| `com.apple.iokit.IOSurface` |
| `com.apple.iokit.IOThunderboltFamily` |
| `com.apple.iokit.IOTimeSyncFamily` |
| `com.apple.iokit.IOUSBHostFamily` |
| `com.apple.iokit.IOUSBMassStorageDriver` |
| `com.apple.iokit.SCSITaskUserClient` |
| `com.apple.kec.AppleEncryptedArchive` |
| `com.apple.kec.Compression` |
| `com.apple.kec.Libm` |
| `com.apple.kec.XrtHostedXnu` |
| `com.apple.kec.corecrypto` |
| `com.apple.kec.pthread` |
| `com.apple.kext.AppleMatch` |
| `com.apple.kext.CoreTrust` |
| `com.apple.kext.triggers` |
| `com.apple.nke.applicationfirewall` |
| `com.apple.private.KextAudit` |
| `com.apple.security.AppleImage4` |
| `com.apple.security.Image4` |
| `com.apple.security.quarantine` |

</details>

### `borrowed-tahoe-x86_64`

an x86_64 kext from macOS 26 (Tahoe); for 8 of the 9, 27.0.1 ships no x86_64 build of it, and AppleRTC is the exception (27.0.1 has one, not yet swapped in).

<details>
<summary><strong>9 entries</strong></summary>

| Bundle identifier |
|---|
| `com.apple.driver.AppleACPIButtons` |
| `com.apple.driver.AppleACPIEC` |
| `com.apple.driver.AppleACPIPlatform` |
| `com.apple.driver.AppleAPIC` |
| `com.apple.driver.AppleBusPowerController` |
| `com.apple.driver.AppleEFINVRAM` |
| `com.apple.driver.AppleEFIRuntime` |
| `com.apple.driver.AppleHPET` |
| `com.apple.driver.AppleRTC` |

</details>

### `apple-27-lifted`

Apple's own 27.0.1 arm64e kext, recompiled to x86_64 by the project's lifter.

<details>
<summary><strong>1 entries</strong></summary>

| Bundle identifier |
|---|
| `com.apple.security.sandbox` |

</details>

### `self-built-kernel`

the kernel itself, built by the project from Apple's published xnu source (see docs/components.md).

<details>
<summary><strong>1 entries</strong></summary>

| Bundle identifier |
|---|
| `com.apple.kernel` |

</details>

<sub>Generated from `data/kexts.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:kexts-table:end -->
