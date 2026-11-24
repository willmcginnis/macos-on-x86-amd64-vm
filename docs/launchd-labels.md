# `launchd` job labels

[&larr; back to the README](../README.md)

Every `launchd` job label whose program is on 27.0.1's system volume (or, for five under
`/Library/Apple`, in its Data-volume template), on the furthest booted macOS 27.0.1-only
root: where its program comes from, and whether it ran during
one boot of about 1,000 seconds. The counts are of labels, not programs, and the
summary below says exactly which labels each one covers.

This is the widest single measurement in the project and also the shallowest, so the
limits come first.

## What the two columns actually mean

**Where the program comes from** was measured properly. Each job's program path was read
from Apple's 27.0.1 system volume on a Mac running 27.0.1, and its architectures read
path by path; the programs of the five labels under `/Library/Apple` (four programs) were read from the Data-volume
template in Apple's 27.0.1 image instead. So a label classed `apple-27-arm64e-translated` is one
whose program Apple genuinely ships for Apple silicon only.

**Whether it ran** is much weaker, and three things about it matter:

1. It comes from the job table printed to the guest's serial console during **one** boot.
   A label shows as *ran* if a process id or an exit status appeared in some sample.
2. **A job that did not need to start does not show as a failure.** Most `launchd` jobs
   are on-demand. In a 1,000-second boot with no user session, no login and no
   applications, many of them may never have been asked for; the boot did not measure
   requests, only whether a process or an exit status appeared. So *not started* on this
   page means "no start was seen", not "it is broken", and reading the *not started*
   count as a failure count would be wrong.
3. **"Ran" does not mean it did its job.** It means a process existed. Which binary a job
   ran was hashed inside the guest for `launchd` and `xpcproxy` only; for every other
   label it is inferred from the records of what was placed on disk, not measured.

A nonzero exit status is more interesting than *not started*, and the causes of most of
those have not been read. They are the obvious place for anyone wanting to find something
real.

## Summary

Counts below are of the labels listed on this page.

<!-- generated:launchd-summary:start -->
| Where the program comes from | Labels | ran | ran, nonzero exit status | not started |
|---|---|---|---|---|
| `apple-27-x86_64` | 299 | 77 | 2 | 220 |
| `apple-27-arm64e-translated` | 110 | 21 | 10 | 79 |
| `apple-27-lifted` | 7 | 3 | 1 | 3 |
| `borrowed-tahoe-x86_64` | 3 | 2 | 1 | 0 |
| `apple-27-flags-changed` | 2 | 0 | 1 | 1 |
| **All labels listed** | 421 | 103 | 15 | 303 |

What each count covers. Listed here: 421 labels; 388 of them were in that boot's job table and 118 ran, 15 of those with a nonzero exit status; the other 33 were not in that boot's job table at all and show as not started. Not listed: 31 labels that are not programs of 27's system volume or its Data-volume template (scripts, per-boot labels, the lab's own test jobs, and com.apple.MRTd, whose program 27.0.1's image does not contain); 23 of them were in the job table and 8 ran, all with exit status 0. So the whole job table of that boot was 411 labels, of which 126 ran, the figure the feature matrix gives. The 3 borrowed macOS 26 programs were replaced by 27's own in three later boots; their rows show the boot counted here.

<sub>Generated from `data/launchd-labels.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:launchd-summary:end -->

The 110 translated labels are the ones whose programs, in the boot counted, could run
only through the exec route: Apple ships those programs for Apple silicon only, and the
route runs them as themselves, unmodified, with a user-space translator underneath. (One
of them, `loginwindow`, has since also been recompiled; see
[boot-programs.md](boot-programs.md).) Three of them, the
XProtect labels, have their programs in the Data-volume template. In the boot counted, 31
of them ran (10 of those with a nonzero exit status) and 79 did not start. `sandboxd` and
`taskgated` are arm64e-only programs of the same kind, but are counted under
`apple-27-flags-changed` because their file flags were changed.

## Every label

<!-- generated:launchd-table:start -->
### `apple-27-x86_64`

Apple's own 27.0.1 program, which still ships an x86_64 slice; run as Apple shipped it.

<details>
<summary><strong>299 labels</strong> &mdash; 77 ran, 2 ran but exited nonzero, 220 not started</summary>

| Label | Program | In one boot | Exit status |
|---|---|---|---|
| `com.apple.AEServer` | `/System/Library/Frameworks/CoreServices.framework/Frameworks/AE.framework/Versions/A/Support/AEServer` | not started | &mdash; |
| `com.apple.AirPlayXPCHelper` | `/usr/libexec/AirPlayXPCHelper` | not started | &mdash; |
| `com.apple.AppSSODaemon` | `/System/Library/PrivateFrameworks/AppSSO.framework/Support/AppSSODaemon` | not started | &mdash; |
| `com.apple.AppleCredentialManagerDaemon` | `/System/Library/PrivateFrameworks/AppleCredentialManager.framework/AppleCredentialManagerDaemon` | ran | &mdash; |
| `com.apple.AppleQEMUGuestAgent` | `/usr/libexec/AppleQEMUGuestAgent` | not started | &mdash; |
| `com.apple.AssetCacheLocatorService` | `/System/Library/PrivateFrameworks/AssetCacheServices.framework/Versions/A/XPCServices/AssetCacheLocatorService.xpc/Contents/MacOS/AssetCacheLocatorService` | not started | &mdash; |
| `com.apple.AssetCacheManagerService` | `/System/Library/PrivateFrameworks/AssetCacheServicesExtensions.framework/XPCServices/AssetCacheManagerService.xpc/Contents/MacOS/AssetCacheManagerService` | not started | &mdash; |
| `com.apple.AssetCacheTetheratorService` | `/System/Library/PrivateFrameworks/AssetCacheServicesExtensions.framework/XPCServices/AssetCacheTetheratorService.xpc/Contents/MacOS/AssetCacheTetheratorService` | not started | &mdash; |
| `com.apple.BTServer.le` | `/usr/sbin/BTLEServer` | not started | &mdash; |
| `com.apple.BlueTool` | `/usr/sbin/BlueTool` | not started | &mdash; |
| `com.apple.CSCSupportd` | `/usr/libexec/CSCSupportd` | ran | &mdash; |
| `com.apple.CoreAuthentication.daemon` | `/System/Library/Frameworks/LocalAuthentication.framework/Support/coreauthd` | not started | &mdash; |
| `com.apple.CryptoTokenKit.ahp` | `/System/Library/Frameworks/CryptoTokenKit.framework/ctkahp.bundle/Contents/MacOS/ctkahp` | not started | &mdash; |
| `com.apple.DesktopServicesHelper` | `/System/Library/PrivateFrameworks/DesktopServicesPriv.framework/Resources/DesktopServicesHelper` | not started | &mdash; |
| `com.apple.DesktopServicesScriptingHelper` | `/System/Library/PrivateFrameworks/DesktopServicesPriv.framework/Resources/DesktopServicesScriptingHelper` | not started | &mdash; |
| `com.apple.DumpGPURestart` | `/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/DumpGPURestart` | not started | &mdash; |
| `com.apple.DumpPanic` | `/usr/libexec/DumpPanic` | ran | &mdash; |
| `com.apple.DumpPanic.Accessory` | `/usr/libexec/DumpPanic` | not started | &mdash; |
| `com.apple.FileCoordination` | `/usr/sbin/filecoordinationd` | not started | &mdash; |
| `com.apple.GSSCred` | `/System/Library/Frameworks/GSS.framework/Helpers/GSSCred` | ran | &mdash; |
| `com.apple.GameController.gamecontrollerd` | `/usr/libexec/gamecontrollerd` | not started | &mdash; |
| `com.apple.IOAccelMemoryInfoCollector` | `/usr/libexec/IOAccelMemoryInfoCollector` | not started | &mdash; |
| `com.apple.InstallerDiagnostics.installerdiagd` | `/System/Library/PrivateFrameworks/InstallerDiagnostics.framework/Versions/A/Resources/installerdiagd` | not started | &mdash; |
| `com.apple.InstallerDiagnostics.installerdiagwatcher` | `/System/Library/PrivateFrameworks/InstallerDiagnostics.framework/Versions/A/Resources/installerdiagwatcher` | not started | &mdash; |
| `com.apple.Kerberos.digest-service` | `/System/Library/PrivateFrameworks/Heimdal.framework/Helpers/digest-service` | ran, nonzero exit status | 1 |
| `com.apple.Kerberos.kadmind` | `/System/Library/PrivateFrameworks/Heimdal.framework/Helpers/kadmind` | not started | &mdash; |
| `com.apple.Kerberos.kcm` | `/System/Library/PrivateFrameworks/Heimdal.framework/Helpers/kcm` | not started | &mdash; |
| `com.apple.Kerberos.kdc` | `/System/Library/PrivateFrameworks/Heimdal.framework/Helpers/kdc` | not started | &mdash; |
| `com.apple.Kerberos.kpasswdd` | `/System/Library/PrivateFrameworks/Heimdal.framework/Helpers/kpasswdd` | not started | &mdash; |
| `com.apple.LocalAuthentication.UIAgent` | `/System/Library/Frameworks/LocalAuthentication.framework/Support/coreautha.bundle/Contents/MacOS/coreautha` | not started | &mdash; |
| `com.apple.LocalAuthentication.userauthd` | `/System/Library/Frameworks/LocalAuthentication.framework/Support/userauthd` | not started | &mdash; |
| `com.apple.NetworkSharing` | `/usr/libexec/InternetSharing` | not started | &mdash; |
| `com.apple.PasswordService` | `/usr/sbin/PasswordService` | not started | &mdash; |
| `com.apple.PowerUIAgent` | `/usr/libexec/PowerUIAgent` | ran | &mdash; |
| `com.apple.RFBEventHelper` | `/System/Library/CoreServices/RFBEventHelper.bundle/Contents/MacOS/RFBEventHelperd` | not started | &mdash; |
| `com.apple.RemoteDesktop.PrivilegeProxy` | `/System/Library/CoreServices/RemoteManagement/AppleVNCServer.bundle/Contents/Support/VNCPrivilegeProxy` | not started | &mdash; |
| `com.apple.ReportCrash.Root` | `/System/Library/CoreServices/ReportCrash` | ran | &mdash; |
| `com.apple.ReportMemoryException` | `/usr/libexec/ReportMemoryException` | not started | &mdash; |
| `com.apple.ReportSystemMemory` | `/System/Library/CoreServices/ReportSystemMemory` | not started | &mdash; |
| `com.apple.SCHelper` | `/System/Library/Frameworks/SystemConfiguration.framework/Versions/A/Helpers/SCHelper` | not started | &mdash; |
| `com.apple.SafeEjectGPUStartupDaemon` | `/System/Library/CoreServices/Menu Extras/SafeEjectGPUExtra.menu/Contents/MacOS/SafeEjectGPUStartupDaemon` | not started | &mdash; |
| `com.apple.SubmitDiagInfo` | `/System/Library/CoreServices/SubmitDiagInfo` | not started | &mdash; |
| `com.apple.TrustEvaluationAgent.system` | `/System/Library/PrivateFrameworks/TrustEvaluationAgent.framework/Resources/trustevaluationagent` | not started | &mdash; |
| `com.apple.UpdateSettings` | `/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/UpdateSettingsTool` | ran | &mdash; |
| `com.apple.UserEventAgent-System` | `/usr/libexec/UserEventAgent` | ran | &mdash; |
| `com.apple.UserNotificationCenter` | `/System/Library/CoreServices/uncd` | not started | &mdash; |
| `com.apple.ValidUpdater` | `/usr/libexec/ValidUpdater` | ran | &mdash; |
| `com.apple.WirelessRadioManager` | `/usr/sbin/WirelessRadioManagerd` | not started | &mdash; |
| `com.apple.accessoryaccessd` | `/System/Library/Frameworks/AccessoryAccess.framework/Resources/accessoryaccessd` | not started | &mdash; |
| `com.apple.accessoryd` | `/System/Library/PrivateFrameworks/CoreAccessories.framework/Support/accessoryd` | not started | &mdash; |
| `com.apple.accessoryupdaterd` | `/System/Library/PrivateFrameworks/MobileAccessoryUpdater.framework/Support/accessoryupdaterd` | ran | &mdash; |
| `com.apple.adid` | `/System/Library/PrivateFrameworks/CoreADI.framework/adid` | not started | &mdash; |
| `com.apple.akd` | `/System/Library/PrivateFrameworks/AuthKit.framework/Versions/A/Support/akd` | not started | &mdash; |
| `com.apple.alf` | `/usr/libexec/ApplicationFirewall/socketfilterfw` | not started | &mdash; |
| `com.apple.alwaysonexclavesd` | `/usr/libexec/alwaysonexclavesd` | not started | &mdash; |
| `com.apple.analyticsd` | `/System/Library/PrivateFrameworks/CoreAnalytics.framework/Support/analyticsd` | ran | &mdash; |
| `com.apple.aned` | `/usr/libexec/aned` | not started | &mdash; |
| `com.apple.aneuserd` | `/usr/libexec/aneuserd` | not started | &mdash; |
| `com.apple.apfsd` | `/usr/libexec/apfsd` | not started | &mdash; |
| `com.apple.appinstalld` | `/System/Library/PrivateFrameworks/MobileInstallation.framework/Support/appinstalld` | not started | &mdash; |
| `com.apple.appleh16camerad` | `/usr/sbin/appleh16camerad` | not started | &mdash; |
| `com.apple.applekeystored` | `/usr/libexec/applekeystored` | not started | &mdash; |
| `com.apple.appstored` | `/System/Library/PrivateFrameworks/AppStoreDaemon.framework/Support/appstored` | not started | &mdash; |
| `com.apple.aslmanager` | `/usr/sbin/aslmanager` | ran | &mdash; |
| `com.apple.asr` | `/usr/sbin/asr` | not started | &mdash; |
| `com.apple.assetsubscriptiond` | `/usr/libexec/assetsubscriptiond` | ran | &mdash; |
| `com.apple.atrun` | `/usr/libexec/atrun` | not started | &mdash; |
| `com.apple.attentionawarenessd` | `/usr/libexec/attentionawarenessd` | not started | &mdash; |
| `com.apple.audio.AudioComponentRegistrar` | `/System/Library/Frameworks/AudioToolbox.framework/AudioComponentRegistrar` | not started | &mdash; |
| `com.apple.audio.coreaudiod` | `/usr/sbin/coreaudiod` | not started | &mdash; |
| `com.apple.audio.systemsoundserverd` | `/usr/sbin/systemsoundserverd` | not started | &mdash; |
| `com.apple.audioanalyticsd` | `/usr/libexec/audioanalyticsd` | not started | &mdash; |
| `com.apple.audiomxd` | `/usr/libexec/audiomxd` | not started | &mdash; |
| `com.apple.autofsd` | `/usr/libexec/autofsd` | ran | &mdash; |
| `com.apple.automountd` | `/usr/libexec/automountd` | not started | &mdash; |
| `com.apple.avbdeviced` | `/usr/sbin/avbdeviced` | not started | &mdash; |
| `com.apple.backgroundtaskmanagementd` | `/System/Library/PrivateFrameworks/BackgroundTaskManagement.framework/Resources/backgroundtaskmanagementd` | ran | &mdash; |
| `com.apple.backupd` | `/System/Library/CoreServices/TimeMachine/backupd` | ran | &mdash; |
| `com.apple.backupd-helper` | `/System/Library/CoreServices/TimeMachine/backupd-helper` | not started | &mdash; |
| `com.apple.betaenrollmentd` | `/usr/libexec/betaenrollmentd` | not started | &mdash; |
| `com.apple.biomed` | `/System/Library/PrivateFrameworks/BiomeStreams.framework/Support/biomed` | ran | &mdash; |
| `com.apple.bluetoothd` | `/usr/sbin/bluetoothd` | ran | &mdash; |
| `com.apple.bootpd` | `/usr/libexec/bootpd` | not started | &mdash; |
| `com.apple.bridgeOSUpdateProxy` | `/System/Library/PrivateFrameworks/BridgeOSSoftwareUpdate.framework/Support/bosUpdateProxy` | not started | &mdash; |
| `com.apple.cameracaptured` | `/usr/libexec/cameracaptured` | not started | &mdash; |
| `com.apple.cameraispdarwinsimd` | `/usr/libexec/cameraispdarwinsimd` | not started | &mdash; |
| `com.apple.cfnetwork.cfnetworkagent` | `/System/Library/Frameworks/CFNetwork.framework/Versions/A/Support/CFNetworkAgent` | not started | &mdash; |
| `com.apple.cfprefsd.xpc.daemon` | `/usr/sbin/cfprefsd` | ran | &mdash; |
| `com.apple.clocksyncd` | `/usr/libexec/clocksyncd` | ran | &mdash; |
| `com.apple.cloudd` | `/System/Library/PrivateFrameworks/CloudKitDaemon.framework/Support/cloudd` | ran | &mdash; |
| `com.apple.cloudtelemetryd` | `/System/Library/PrivateFrameworks/CloudTelemetry.framework/Support/cloudtelemetryd` | ran | &mdash; |
| `com.apple.cmio.VDCAssistant` | `/System/Library/Frameworks/CoreMediaIO.framework/Resources/VDC.plugin/Contents/Resources/VDCAssistant` | not started | &mdash; |
| `com.apple.cmio.iOSScreenCaptureAssistant` | `/System/Library/Frameworks/CoreMediaIO.framework/Resources/iOSScreenCapture.plugin/Contents/Resources/iOSScreenCaptureAssistant` | not started | &mdash; |
| `com.apple.cmio.registerassistantservice` | `/System/Library/Frameworks/CoreMediaIO.framework/Versions/A/Resources/com.apple.cmio.registerassistantservice` | ran | &mdash; |
| `com.apple.cmio.uvcassistantextension` | `/System/Library/Frameworks/CoreMediaIO.framework/Versions/A/Resources/UVCAssistant.systemextension/Contents/MacOS/UVCAssistant` | not started | &mdash; |
| `com.apple.cmio.videodriverkithostextension` | `/usr/libexec/com.apple.cmio.videodriverkithostextension.systemextension/Contents/MacOS/com.apple.cmio.videodriverkithostextension` | not started | &mdash; |
| `com.apple.colorsync.displayservices` | `/usr/libexec/colorsync.displayservices` | not started | &mdash; |
| `com.apple.colorsyncd` | `/usr/libexec/colorsyncd` | not started | &mdash; |
| `com.apple.configd` | `/usr/libexec/configd` | ran | &mdash; |
| `com.apple.containermanagerd.system` | `/usr/libexec/containermanagerd_system` | ran | &mdash; |
| `com.apple.contextstored` | `/System/Library/PrivateFrameworks/CoreDuetContext.framework/Resources/contextstored` | ran | &mdash; |
| `com.apple.corebrightnessd` | `/usr/libexec/corebrightnessd` | ran | &mdash; |
| `com.apple.coreduetd` | `/usr/libexec/coreduetd` | ran | &mdash; |
| `com.apple.corekdld` | `/System/Library/PrivateFrameworks/CoreKDL.framework/Support/corekdld` | not started | &mdash; |
| `com.apple.corercd` | `/usr/libexec/corercd` | not started | &mdash; |
| `com.apple.coreservices.appleevents` | `/System/Library/CoreServices/appleeventsd` | not started | &mdash; |
| `com.apple.coreservices.launchservicesd` | `/System/Library/CoreServices/launchservicesd` | ran | &mdash; |
| `com.apple.coreservices.sharedfilelistd` | `/System/Library/CoreServices/sharedfilelistd` | not started | &mdash; |
| `com.apple.coreservicesd` | `/System/Library/CoreServices/coreservicesd` | ran | &mdash; |
| `com.apple.corespeechd_system` | `/System/Library/PrivateFrameworks/CoreSpeech.framework/corespeechd_system` | ran | &mdash; |
| `com.apple.corestorage.corestoraged` | `/usr/libexec/corestoraged` | not started | &mdash; |
| `com.apple.corestorage.corestoragehelperd` | `/usr/libexec/corestoragehelperd` | not started | &mdash; |
| `com.apple.countryd` | `/usr/libexec/countryd` | ran | &mdash; |
| `com.apple.csrutil.report` | `/usr/bin/csrutil` | not started | &mdash; |
| `com.apple.ctkd` | `/System/Library/Frameworks/CryptoTokenKit.framework/ctkd` | not started | &mdash; |
| `com.apple.cvmsServ` | `/System/Library/Frameworks/OpenGL.framework/Versions/A/Libraries/CVMServer` | ran | &mdash; |
| `com.apple.dasd` | `/usr/libexec/dasd` | ran | &mdash; |
| `com.apple.deleted_helper` | `/System/Library/PrivateFrameworks/CacheDelete.framework/deleted_helper` | not started | &mdash; |
| `com.apple.deviceconfigurationd` | `/System/Library/PrivateFrameworks/DeviceConfiguration.framework/Versions/A/deviceconfigurationd` | not started | &mdash; |
| `com.apple.deviceinterfaced` | `/Library/Apple/System/Library/PrivateFrameworks/DeviceInterface.framework/Support/deviceinterfaced` | not started | &mdash; |
| `com.apple.devicemanagementclient.managedappsd` | `/usr/libexec/managedappsd` | not started | &mdash; |
| `com.apple.devicemanagementclient.managedeventsd` | `/usr/libexec/managedeventsd` | not started | &mdash; |
| `com.apple.devicemanagementclient.teslad` | `/usr/libexec/teslad` | not started | &mdash; |
| `com.apple.devicerecoveryd` | `/System/Library/PrivateFrameworks/DeviceRecovery.framework/Support/devicerecoveryd` | not started | &mdash; |
| `com.apple.dhcp6d` | `/usr/libexec/dhcp6d` | not started | &mdash; |
| `com.apple.diagnosticextensions.osx.spotlight.helper` | `/System/Library/PrivateFrameworks/DiagnosticExtensions.framework/PlugIns/osx-spotlight.appex/Contents/XPCServices/SpotlightHelper` | not started | &mdash; |
| `com.apple.diagnosticextensions.osx.timemachine.helper` | `/System/Library/PrivateFrameworks/DiagnosticExtensions.framework/PlugIns/osx-timemachine.appex/Contents/XPCServices/timemachinehelper` | not started | &mdash; |
| `com.apple.diagnosticservicesd` | `/System/Library/CoreServices/diagnosticservicesd` | ran | &mdash; |
| `com.apple.diskimagesiod` | `/usr/libexec/diskimagesiod` | not started | &mdash; |
| `com.apple.diskimagesiod.ram` | `/usr/libexec/diskimagesiod` | not started | &mdash; |
| `com.apple.diskimagesiod.spb` | `/usr/libexec/diskimagesiod` | not started | &mdash; |
| `com.apple.diskimagespawner` | `/usr/libexec/diskimagespawner` | not started | &mdash; |
| `com.apple.diskmanagementstartup` | `/usr/libexec/diskmanagementstartup` | not started | &mdash; |
| `com.apple.displaypolicyd` | `/usr/libexec/displaypolicyd` | ran | &mdash; |
| `com.apple.distnoted.xpc.daemon` | `/usr/sbin/distnoted` | ran | &mdash; |
| `com.apple.dprivacyd` | `/usr/libexec/dprivacyd` | not started | &mdash; |
| `com.apple.dt.RemotePairingDataVaultHelper` | `/Library/Apple/System/Library/PrivateFrameworks/RemotePairing.framework/Versions/A/Resources/bin/RemotePairingDataVaultHelper` | not started | &mdash; |
| `com.apple.dt.automationmode-writer` | `/System/Library/PrivateFrameworks/AutomationMode.framework/automationmode-writer` | not started | &mdash; |
| `com.apple.dt.fetchsymbolsd` | `/usr/libexec/dtfetchsymbolsd` | not started | &mdash; |
| `com.apple.dynamic_pager` | `/sbin/dynamic_pager` | not started | &mdash; |
| `com.apple.ecosystemanalyticsd` | `/System/Library/PrivateFrameworks/EcosystemAnalytics.framework/Support/ecosystemanalyticsd` | not started | &mdash; |
| `com.apple.ecosystemd` | `/System/Library/PrivateFrameworks/Ecosystem.framework/Support/ecosystemd` | not started | &mdash; |
| `com.apple.efilogin-helper` | `/System/Library/PrivateFrameworks/EFILogin.framework/Resources/efilogin-helper` | ran | &mdash; |
| `com.apple.endpointsecurity.endpointsecurityd` | `/usr/libexec/endpointsecurityd` | ran | &mdash; |
| `com.apple.eoshostd` | `/usr/libexec/eoshostd` | not started | &mdash; |
| `com.apple.erasecontentsettingshelperd` | `/System/Library/PrivateFrameworks/DeauthorizationKit.framework/Versions/A/Resources/erasecontentsettingshelperd` | not started | &mdash; |
| `com.apple.fairplayd` | `/System/Library/PrivateFrameworks/CoreFP.framework/Versions/A/fairplayd` | not started | &mdash; |
| `com.apple.fairplaydeviceidentityd` | `/usr/libexec/fairplaydeviceidentityd` | not started | &mdash; |
| `com.apple.filesystems.doubleagentd` | `/System/Library/PrivateFrameworks/DoubleAgent.framework/doubleagentd` | not started | &mdash; |
| `com.apple.filesystems.fskitd` | `/usr/libexec/fskitd` | ran | &mdash; |
| `com.apple.filesystems.userfs_helper` | `/System/Library/PrivateFrameworks/UserFS.framework/Resources/userfs_helper` | not started | &mdash; |
| `com.apple.filesystems.userfsd` | `/System/Library/PrivateFrameworks/UserFS.framework/userfsd` | not started | &mdash; |
| `com.apple.findmymacd` | `/System/Library/PrivateFrameworks/FindMyMac.framework/Resources/FindMyMacd` | not started | &mdash; |
| `com.apple.fontmover` | `/System/Library/Frameworks/ApplicationServices.framework/Versions/A/Frameworks/ATS.framework/Versions/A/Support/fontmover` | not started | &mdash; |
| `com.apple.fpassetmanagerd` | `/usr/libexec/fpassetmanagerd` | not started | &mdash; |
| `com.apple.fseventsd` | `/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/FSEvents.framework/Versions/A/Support/fseventsd` | ran | &mdash; |
| `com.apple.fskit.fskit_helper` | `/usr/libexec/fskit_helper` | not started | &mdash; |
| `com.apple.ftp-proxy` | `/usr/libexec/ftp-proxy` | not started | &mdash; |
| `com.apple.gamepolicyd` | `/usr/libexec/gamepolicyd` | not started | &mdash; |
| `com.apple.getty` | `/usr/libexec/getty` | not started | &mdash; |
| `com.apple.griddatad` | `/usr/libexec/griddatad` | not started | &mdash; |
| `com.apple.handwritingd` | `/usr/libexec/handwritingd` | not started | &mdash; |
| `com.apple.ifdreader` | `/System/Library/CryptoTokenKit/com.apple.ifdreader.slotd/Contents/MacOS/com.apple.ifdreader` | not started | &mdash; |
| `com.apple.inboxupdaterd` | `/usr/libexec/inboxupdaterd` | not started | &mdash; |
| `com.apple.installandsetup.systemmigrationd` | `/System/Library/PrivateFrameworks/SystemMigration.framework/Resources/systemmigrationd` | not started | &mdash; |
| `com.apple.installcoordination_proxy` | `/System/Library/PrivateFrameworks/InstallCoordination.framework/Support/installcoordination_proxy` | not started | &mdash; |
| `com.apple.installcoordinationd` | `/System/Library/PrivateFrameworks/InstallCoordination.framework/Support/installcoordinationd` | not started | &mdash; |
| `com.apple.installd` | `/System/Library/PrivateFrameworks/PackageKit.framework/Resources/installd` | not started | &mdash; |
| `com.apple.ioupsd` | `/usr/libexec/ioupsd` | not started | &mdash; |
| `com.apple.kdumpd` | `/usr/libexec/kdumpd` | not started | &mdash; |
| `com.apple.libsqlite3.dbtelemetryd` | `/usr/libexec/dbtelemetryd` | not started | &mdash; |
| `com.apple.lightsoutmanagementd` | `/usr/libexec/lightsoutmanagementd` | not started | &mdash; |
| `com.apple.locationd` | `/usr/libexec/locationd` | ran | &mdash; |
| `com.apple.lockd` | `/usr/sbin/rpc.lockd` | not started | &mdash; |
| `com.apple.logkextloadsd` | `/usr/libexec/logkextloadsd` | not started | &mdash; |
| `com.apple.lsd` | `/usr/libexec/lsd` | ran | &mdash; |
| `com.apple.lskdd` | `/System/Library/PrivateFrameworks/CoreLSKD.framework/Versions/A/lskdd` | not started | &mdash; |
| `com.apple.mDNSResponder.reloaded` | `/usr/sbin/mDNSResponder` | ran | &mdash; |
| `com.apple.mDNSResponderHelper.reloaded` | `/usr/sbin/mDNSResponderHelper` | ran | &mdash; |
| `com.apple.managedappdistributiond` | `/System/Library/Frameworks/ManagedAppDistribution.framework/Support/managedappdistributiond` | not started | &mdash; |
| `com.apple.memory-maintenance` | `/usr/libexec/mmaintenanced` | ran | &mdash; |
| `com.apple.metadata.mds.index` | `/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mds_stores` | not started | &mdash; |
| `com.apple.metadata.mds.index.readonly` | `/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mds_stores` | not started | &mdash; |
| `com.apple.metadata.mds.scan` | `/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mdsync` | ran | &mdash; |
| `com.apple.metadata.mds.spindump` | `/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mdworker` | not started | &mdash; |
| `com.apple.misagent` | `/usr/libexec/misagent` | not started | &mdash; |
| `com.apple.mobile.NRDUpdated` | `/usr/libexec/NRDUpdated` | not started | &mdash; |
| `com.apple.mobile.keybagd` | `/usr/libexec/keybagd` | ran | &mdash; |
| `com.apple.mobile.obliteration` | `/usr/libexec/mobile_obliterator` | not started | &mdash; |
| `com.apple.mobile.softwareupdated` | `/System/Library/PrivateFrameworks/MobileSoftwareUpdate.framework/Support/softwareupdated` | ran | &mdash; |
| `com.apple.mobile.storage_mounter` | `/usr/libexec/MobileStorageMounter` | not started | &mdash; |
| `com.apple.mobile.storage_mounter_proxy` | `/usr/libexec/mobile_storage_proxy` | not started | &mdash; |
| `com.apple.mobile.usermanagerd` | `/usr/libexec/usermanagerd` | ran | &mdash; |
| `com.apple.mobileactivationd` | `/usr/libexec/mobileactivationd` | not started | &mdash; |
| `com.apple.mobileassetd` | `/usr/libexec/mobileassetd` | ran | &mdash; |
| `com.apple.mobilegestalt.xpc` | `/usr/libexec/MobileGestaltHelper` | not started | &mdash; |
| `com.apple.modelcatalogd` | `/System/Library/PrivateFrameworks/ModelCatalogRuntime.framework/Versions/A/modelcatalogd` | ran | &mdash; |
| `com.apple.msrpc.echosvc` | `/usr/libexec/rpcsvchost` | not started | &mdash; |
| `com.apple.msrpc.lsarpc` | `/usr/libexec/rpcsvchost` | not started | &mdash; |
| `com.apple.msrpc.mdssvc` | `/usr/libexec/rpcsvchost` | not started | &mdash; |
| `com.apple.msrpc.netlogon` | `/usr/libexec/rpcsvchost` | not started | &mdash; |
| `com.apple.msrpc.srvsvc` | `/usr/libexec/rpcsvchost` | not started | &mdash; |
| `com.apple.msrpc.wkssvc` | `/usr/libexec/rpcsvchost` | not started | &mdash; |
| `com.apple.multiversed` | `/usr/libexec/multiversed` | not started | &mdash; |
| `com.apple.musicd` | `/System/Library/Frameworks/MusicKit.framework/Support/musicd` | not started | &mdash; |
| `com.apple.nearbyd` | `/usr/libexec/nearbyd` | not started | &mdash; |
| `com.apple.nesessionmanager` | `/usr/libexec/nesessionmanager` | ran | &mdash; |
| `com.apple.netbiosd` | `/usr/sbin/netbiosd` | not started | &mdash; |
| `com.apple.newsyslog` | `/usr/sbin/newsyslog` | not started | &mdash; |
| `com.apple.nfcd` | `/usr/libexec/nfcd` | not started | &mdash; |
| `com.apple.nfsconf` | `/sbin/mount_nfs` | not started | &mdash; |
| `com.apple.nfsd` | `/sbin/nfsd` | not started | &mdash; |
| `com.apple.nlcd` | `/usr/libexec/nlcd` | not started | &mdash; |
| `com.apple.notifyd` | `/usr/sbin/notifyd` | ran | &mdash; |
| `com.apple.ntalkd` | `/usr/libexec/ntalkd` | not started | &mdash; |
| `com.apple.oahd` | `/usr/libexec/rosetta/oahd` | not started | &mdash; |
| `com.apple.oahd-root-helper` | `/usr/libexec/rosetta/oahd-root-helper` | not started | &mdash; |
| `com.apple.online-auth-agent.xpc` | `/usr/libexec/online-auth-agent` | not started | &mdash; |
| `com.apple.opendirectoryd` | `/usr/libexec/opendirectoryd` | ran | &mdash; |
| `com.apple.osanalytics.osanalyticshelper` | `/System/Library/CoreServices/osanalyticshelper` | ran | &mdash; |
| `com.apple.ospredictiond` | `/usr/libexec/ospredictiond` | not started | &mdash; |
| `com.apple.peakpowermanagerd` | `/usr/libexec/peakpowermanagerd` | ran, nonzero exit status | 1 |
| `com.apple.pfctl` | `/sbin/pfctl` | not started | &mdash; |
| `com.apple.pfd` | `/usr/libexec/pfd` | not started | &mdash; |
| `com.apple.postfix.master` | `/usr/libexec/postfix/master` | not started | &mdash; |
| `com.apple.postfix.newaliases` | `/usr/bin/newaliases` | not started | &mdash; |
| `com.apple.powerd` | `/System/Library/CoreServices/powerd.bundle/powerd` | ran | &mdash; |
| `com.apple.powerd.swd` | `/System/Library/CoreServices/powerd.bundle/swd` | not started | &mdash; |
| `com.apple.powerdatad` | `/usr/libexec/powerdatad` | not started | &mdash; |
| `com.apple.printtool.daemon` | `/System/Library/Frameworks/ApplicationServices.framework/Frameworks/PrintCore.framework/Versions/A/printtool` | not started | &mdash; |
| `com.apple.racoon` | `/usr/sbin/racoon` | not started | &mdash; |
| `com.apple.relatived` | `/usr/libexec/relatived` | not started | &mdash; |
| `com.apple.remotemanagementd` | `/System/Library/PrivateFrameworks/RemoteManagement.framework/remotemanagementd` | not started | &mdash; |
| `com.apple.rpcbind` | `/usr/sbin/rpcbind` | not started | &mdash; |
| `com.apple.rtcreportingd` | `/usr/libexec/rtcreportingd` | not started | &mdash; |
| `com.apple.runningboardd` | `/usr/libexec/runningboardd` | ran | &mdash; |
| `com.apple.screensharing` | `/System/Library/CoreServices/RemoteManagement/screensharingd.bundle/Contents/MacOS/screensharingd` | not started | &mdash; |
| `com.apple.security.FDERecoveryAgent` | `/usr/libexec/FDERecoveryAgent` | not started | &mdash; |
| `com.apple.security.agent.login` | `/System/Library/Frameworks/Security.framework/Versions/A/MachServices/SecurityAgent.bundle/Contents/MacOS/SecurityAgent` | not started | &mdash; |
| `com.apple.security.authhost` | `/System/Library/Frameworks/Security.framework/Versions/A/MachServices/authorizationhost.bundle/Contents/MacOS/authorizationhost` | not started | &mdash; |
| `com.apple.security.authtrampoline` | `/System/Library/Frameworks/Security.framework/authtrampoline` | not started | &mdash; |
| `com.apple.security.syspolicy` | `/usr/libexec/syspolicyd` | ran | &mdash; |
| `com.apple.securityd` | `/usr/sbin/securityd` | ran | &mdash; |
| `com.apple.securityd.system` | `/usr/libexec/securityd_system` | not started | &mdash; |
| `com.apple.seld` | `/usr/libexec/seld` | not started | &mdash; |
| `com.apple.smb.preferences` | `/usr/libexec/smb-sync-preferences` | ran | &mdash; |
| `com.apple.smbd` | `/usr/sbin/smbd` | not started | &mdash; |
| `com.apple.sntpd` | `/usr/sbin/sntpd` | not started | &mdash; |
| `com.apple.startupdiskhelper` | `/usr/libexec/startupdiskhelper` | not started | &mdash; |
| `com.apple.statd.notify` | `/usr/sbin/rpc.statd` | not started | &mdash; |
| `com.apple.storagekitd` | `/usr/libexec/storagekitd` | ran | &mdash; |
| `com.apple.storereceiptinstaller` | `/System/Library/PrivateFrameworks/CommerceKit.framework/Versions/A/Resources/ReceiptInstaller` | not started | &mdash; |
| `com.apple.swiftuitracingsupport.xpc` | `/usr/libexec/swiftuitraced` | not started | &mdash; |
| `com.apple.symptomsd` | `/usr/libexec/symptomsd` | ran | &mdash; |
| `com.apple.symptomsd-diag` | `/usr/libexec/symptomsd-diag` | not started | &mdash; |
| `com.apple.sysdiagnose` | `/usr/libexec/sysdiagnosed` | not started | &mdash; |
| `com.apple.sysdiagnose_helper` | `/usr/libexec/sysdiagnose_helper` | not started | &mdash; |
| `com.apple.sysextd` | `/System/Library/Frameworks/SystemExtensions.framework/Versions/A/Helpers/sysextd` | ran | &mdash; |
| `com.apple.syslogd` | `/usr/sbin/syslogd` | ran | &mdash; |
| `com.apple.sysmond` | `/usr/libexec/sysmond` | not started | &mdash; |
| `com.apple.system_installd` | `/System/Library/PrivateFrameworks/PackageKit.framework/Resources/system_installd` | not started | &mdash; |
| `com.apple.systemstats.analysis` | `/usr/sbin/systemstats` | ran | &mdash; |
| `com.apple.systemstats.daily` | `/usr/sbin/systemstats` | not started | &mdash; |
| `com.apple.systemstats.microstackshot_periodic` | `/usr/libexec/microstackshot` | not started | &mdash; |
| `com.apple.systemstatusd` | `/System/Library/PrivateFrameworks/SystemStatusServer.framework/Support/systemstatusd` | ran | &mdash; |
| `com.apple.tailspind` | `/usr/libexec/tailspind` | not started | &mdash; |
| `com.apple.taskgated-helper` | `/usr/libexec/taskgated-helper` | not started | &mdash; |
| `com.apple.tccd.system` | `/System/Library/PrivateFrameworks/TCC.framework/Support/tccd` | ran | &mdash; |
| `com.apple.testmanagerd.remote` | `/usr/libexec/testmanagerd` | not started | &mdash; |
| `com.apple.tftpd` | `/usr/libexec/tftpd` | not started | &mdash; |
| `com.apple.thermalmonitord` | `/usr/libexec/thermalmonitord` | ran | &mdash; |
| `com.apple.threadradiod` | `/System/Library/PrivateFrameworks/CoreThreadRadio.framework/threadradiod` | not started | &mdash; |
| `com.apple.timed` | `/usr/libexec/timed` | ran | &mdash; |
| `com.apple.timezoneupdates.tzd` | `/usr/libexec/tzd` | not started | &mdash; |
| `com.apple.touchbarserver` | `/usr/libexec/TouchBarServer` | not started | &mdash; |
| `com.apple.tracd` | `/usr/libexec/tracd` | not started | &mdash; |
| `com.apple.triald.system` | `/usr/libexec/triald_system` | ran | &mdash; |
| `com.apple.trustd` | `/usr/libexec/trustd` | ran | &mdash; |
| `com.apple.trustdFileHelper` | `/usr/libexec/trustdFileHelper` | not started | &mdash; |
| `com.apple.tzlinkd` | `/usr/libexec/tzlinkd` | ran | &mdash; |
| `com.apple.uarpassetmanagerd` | `/usr/libexec/uarpassetmanagerd` | ran | &mdash; |
| `com.apple.uarpd` | `/usr/libexec/uarpd` | ran | &mdash; |
| `com.apple.uarphidd` | `/usr/libexec/uarphidd` | not started | &mdash; |
| `com.apple.uninstalld` | `/System/Library/PrivateFrameworks/Uninstall.framework/Resources/uninstalld` | not started | &mdash; |
| `com.apple.usbaudiod` | `/System/Library/Audio/Plug-Ins/usbaudio.bundle/Contents/MacOS/usbaudiod` | not started | &mdash; |
| `com.apple.usbmuxd` | `/System/Library/PrivateFrameworks/MobileDevice.framework/Versions/A/Resources/usbmuxd` | ran | &mdash; |
| `com.apple.usbsmartcardreaderd` | `/System/Library/CryptoTokenKit/usbsmartcardreaderd.slotd/Contents/MacOS/usbsmartcardreaderd` | not started | &mdash; |
| `com.apple.uucp` | `/usr/sbin/uucico` | not started | &mdash; |
| `com.apple.wallpaper.export` | `/usr/libexec/wallpaperexportd` | not started | &mdash; |
| `com.apple.warmd` | `/usr/libexec/warmd` | ran | &mdash; |
| `com.apple.watchdogd` | `/usr/libexec/watchdogd` | not started | &mdash; |
| `com.apple.wifianalyticsd` | `/usr/libexec/wifianalyticsd` | not started | &mdash; |
| `com.apple.wifivelocityd` | `/usr/libexec/wifivelocityd` | not started | &mdash; |
| `com.apple.xartstorageremoted` | `/usr/libexec/xartstorageremoted` | not started | &mdash; |
| `com.apple.xpc.uscwoap` | `/bin/bash` | not started | &mdash; |
| `com.apple.xsan` | `/System/Library/Filesystems/acfs.fs/Contents/bin/xsand` | not started | &mdash; |
| `com.vix.cron` | `/usr/sbin/cron` | not started | &mdash; |
| `org.cups.cups-lpd` | `/usr/libexec/cups/daemon/cups-lpd` | not started | &mdash; |
| `org.openldap.slapd` | `/usr/libexec/slapd` | not started | &mdash; |

</details>

### `apple-27-arm64e-translated`

Apple's own 27.0.1 program, shipped without an x86_64 slice (arm64e; arm64e and arm64 for the two programs behind the three XProtect labels); run under translation by the kernel's foreign-architecture exec route.

<details>
<summary><strong>110 labels</strong> &mdash; 21 ran, 10 ran but exited nonzero, 79 not started</summary>

| Label | Program | In one boot | Exit status |
|---|---|---|---|
| `com.apple.AppSSOAgent.login` | `/System/Library/PrivateFrameworks/AppSSO.framework/Support/AppSSOAgent.app/Contents/MacOS/AppSSOAgent` | not started | &mdash; |
| `com.apple.AssetCache.builtin` | `/usr/libexec/AssetCache/AssetCache` | not started | &mdash; |
| `com.apple.ContainerMigrationService` | `/usr/libexec/ContainerMigrationService` | not started | &mdash; |
| `com.apple.CrashReporterSupportHelper` | `/System/Library/CoreServices/CrashReporterSupportHelper` | not started | &mdash; |
| `com.apple.DataDetectorsSourceAccess` | `/usr/libexec/DataDetectorsSourceAccess` | not started | &mdash; |
| `com.apple.DumpPanicRecoveryOS` | `/usr/libexec/DumpPanicRecoveryOS` | not started | &mdash; |
| `com.apple.InstallerProgress` | `/System/Library/CoreServices/Installer Progress.app/Contents/MacOS/Installer Progress` | ran | &mdash; |
| `com.apple.ManagedClient` | `/System/Library/CoreServices/ManagedClient.app/Contents/MacOS/ManagedClient` | not started | &mdash; |
| `com.apple.ManagedClient.enroll` | `/System/Library/CoreServices/ManagedClient.app/Contents/MacOS/ManagedClient` | not started | &mdash; |
| `com.apple.ManagedClient.mechanism` | `/System/Library/CoreServices/ManagedClient.app/Contents/MacOS/ManagedClient` | not started | &mdash; |
| `com.apple.ManagedClient.startup` | `/System/Library/CoreServices/ManagedClient.app/Contents/MacOS/ManagedClient` | not started | &mdash; |
| `com.apple.PerfPowerServices` | `/usr/libexec/PerfPowerServices` | ran | &mdash; |
| `com.apple.PerfPowerServicesExtended` | `/usr/libexec/PerfPowerServicesExtended` | not started | &mdash; |
| `com.apple.RemotePairTool` | `/System/Library/CoreServices/RemotePairTool` | not started | &mdash; |
| `com.apple.Virtualization.AppleVirtualPlatformHIDBridge` | `/usr/libexec/AppleVirtualPlatformHIDBridge` | not started | &mdash; |
| `com.apple.WindowServer` | `/System/Library/PrivateFrameworks/SkyLight.framework/Resources/WindowServer` | ran | &mdash; |
| `com.apple.XProtect.daemon.scan` | `/Library/Apple/System/Library/CoreServices/XProtect.app/Contents/MacOS/XProtect` | not started | &mdash; |
| `com.apple.XProtect.daemon.scan.startup` | `/Library/Apple/System/Library/CoreServices/XProtect.app/Contents/MacOS/XProtect` | ran | &mdash; |
| `com.apple.XprotectFramework.PluginService` | `/Library/Apple/System/Library/CoreServices/XProtect.app/Contents/XPCServices/XProtectPluginService.xpc/Contents/MacOS/XProtectPluginService` | not started | &mdash; |
| `com.apple.airportd` | `/usr/libexec/airportd` | ran, nonzero exit status | 1 |
| `com.apple.appleh13camerad` | `/usr/sbin/appleh13camerad` | not started | &mdash; |
| `com.apple.appleseed.fbahelperd` | `/System/Library/CoreServices/Applications/Feedback Assistant.app/Contents/Library/LaunchServices/fbahelperd` | not started | &mdash; |
| `com.apple.applessdstatistics` | `/usr/libexec/applessdstatistics` | not started | &mdash; |
| `com.apple.apsd` | `/System/Library/PrivateFrameworks/ApplePushService.framework/apsd` | ran, nonzero exit status | 1 |
| `com.apple.audio.isolated.historicalaudiod` | `/usr/libexec/historicalaudiod` | not started | &mdash; |
| `com.apple.audio.isolated.micactivityd` | `/usr/libexec/micactivityd` | not started | &mdash; |
| `com.apple.auditd` | `/usr/sbin/auditd` | not started | &mdash; |
| `com.apple.biometrickitd` | `/usr/libexec/biometrickitd` | not started | &mdash; |
| `com.apple.bootinstalld` | `/usr/libexec/bootinstalld` | not started | &mdash; |
| `com.apple.cameraispd` | `/usr/libexec/cameraispd` | not started | &mdash; |
| `com.apple.captiveagent` | `/usr/libexec/captiveagent` | not started | &mdash; |
| `com.apple.centaurid` | `/usr/libexec/centaurid` | ran, nonzero exit status | 1 |
| `com.apple.corecaptured` | `/usr/libexec/corecaptured` | not started | &mdash; |
| `com.apple.corerepaird` | `/usr/libexec/corerepaird` | ran | &mdash; |
| `com.apple.coresymbolicationd` | `/System/Library/PrivateFrameworks/CoreSymbolication.framework/coresymbolicationd` | ran | &mdash; |
| `com.apple.datastored` | `/usr/libexec/datastored` | not started | &mdash; |
| `com.apple.diagnosticd` | `/usr/libexec/diagnosticd` | not started | &mdash; |
| `com.apple.dvdplayback.setregion` | `/usr/bin/setregion` | not started | &mdash; |
| `com.apple.eapolcfg_auth` | `/System/Library/PrivateFrameworks/EAP8021X.framework/Resources/eapolcfg_auth` | not started | &mdash; |
| `com.apple.eligibilityd` | `/usr/libexec/eligibilityd` | ran | &mdash; |
| `com.apple.familycontrols` | `/System/Library/PrivateFrameworks/FamilyControls.framework/Resources/parentalcontrolsd` | not started | &mdash; |
| `com.apple.findmy.findmybeaconingd` | `/usr/libexec/findmybeaconingd` | not started | &mdash; |
| `com.apple.findmymacmessenger` | `/System/Library/PrivateFrameworks/FindMyMac.framework/Resources/FindMyMacMessenger.app/Contents/MacOS/FindMyMacMessenger` | not started | &mdash; |
| `com.apple.gssd` | `/usr/sbin/gssd` | not started | &mdash; |
| `com.apple.hdiejectd` | `/System/Library/PrivateFrameworks/DiskImages.framework/Resources/hdiejectd` | not started | &mdash; |
| `com.apple.hidd` | `/usr/libexec/hidd` | not started | &mdash; |
| `com.apple.icloud.findmydeviced` | `/usr/libexec/findmydeviced` | ran, nonzero exit status | 1 |
| `com.apple.icloud.searchpartyd` | `/usr/libexec/searchpartyd` | ran, nonzero exit status | 1 |
| `com.apple.iconservices.iconservicesagent` | `/System/Library/CoreServices/iconservicesagent` | ran | &mdash; |
| `com.apple.iconservices.iconservicesd` | `/System/Library/CoreServices/iconservicesd` | ran | &mdash; |
| `com.apple.iomfb_bics_daemon` | `/usr/libexec/IOMFB_bics_daemon` | ran | &mdash; |
| `com.apple.iomfb_fdr_loader` | `/usr/bin/IOMFB_FDR_Loader` | ran, nonzero exit status | 1 |
| `com.apple.ionodecache` | `/System/Library/CoreServices/ionodecache` | ran | &mdash; |
| `com.apple.kcgend` | `/usr/libexec/kcgend` | not started | &mdash; |
| `com.apple.kcproxy` | `/usr/libexec/kcproxy` | not started | &mdash; |
| `com.apple.kernelmanager_helper` | `/usr/libexec/kernelmanager_helper` | ran | &mdash; |
| `com.apple.kernelmanagerd` | `/usr/libexec/kernelmanagerd` | ran | &mdash; |
| `com.apple.kuncd` | `/usr/libexec/kuncd` | not started | &mdash; |
| `com.apple.liquiddetectiond` | `/System/Library/CoreServices/liquiddetectiond.app/liquiddetectiond` | not started | &mdash; |
| `com.apple.logd_reporter` | `/usr/libexec/logd_reporter` | not started | &mdash; |
| `com.apple.logind` | `/System/Library/CoreServices/logind` | ran | &mdash; |
| `com.apple.loginwindow` | `/System/Library/CoreServices/loginwindow.app/Contents/MacOS/loginwindow` | not started | &mdash; |
| `com.apple.mbsystemadministration` | `/System/Library/CoreServices/Setup Assistant.app/Contents/Resources/mbsystemadministration` | not started | &mdash; |
| `com.apple.mbusertrampoline` | `/System/Library/CoreServices/Setup Assistant.app/Contents/Resources/mbusertrampoline` | not started | &mdash; |
| `com.apple.mdmclient.daemon` | `/usr/libexec/mdmclient` | not started | &mdash; |
| `com.apple.mdmclient.daemon.runatboot` | `/usr/libexec/mdmclient` | not started | &mdash; |
| `com.apple.mediaremoted` | `/System/Library/PrivateFrameworks/MediaRemote.framework/Support/mediaremoted` | ran, nonzero exit status | 1 |
| `com.apple.metadata.mds` | `/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mds` | ran | &mdash; |
| `com.apple.mobile.notification_proxy` | `/usr/libexec/notification_proxy` | not started | &mdash; |
| `com.apple.modelmanagerd` | `/usr/libexec/modelmanagerd` | ran, nonzero exit status | -9 |
| `com.apple.nand.aspcarry` | `/usr/libexec/ASPCarryLog` | not started | &mdash; |
| `com.apple.nand_task_scheduler` | `/usr/libexec/NANDTaskScheduler` | not started | &mdash; |
| `com.apple.nehelper` | `/usr/libexec/nehelper` | ran | &mdash; |
| `com.apple.netauth.sys.auth` | `/System/Library/CoreServices/NetAuthAgent.app/Contents/MacOS/NetAuthSysAgent` | not started | &mdash; |
| `com.apple.netauth.sys.gui` | `/System/Library/CoreServices/NetAuthAgent.app/Contents/MacOS/NetAuthAgent` | not started | &mdash; |
| `com.apple.nsurlsessiond_privileged` | `/usr/libexec/nsurlsessiond` | ran | &mdash; |
| `com.apple.ocspd` | `/usr/sbin/ocspd` | not started | &mdash; |
| `com.apple.odproxyd` | `/usr/libexec/odproxyd` | not started | &mdash; |
| `com.apple.pcapd` | `/usr/libexec/pcapd` | not started | &mdash; |
| `com.apple.perfpowermetricd` | `/usr/libexec/perfpowermetricd` | not started | &mdash; |
| `com.apple.powerlogHelperd` | `/usr/libexec/powerlogHelperd` | not started | &mdash; |
| `com.apple.preferences.timezone.admintool` | `/System/Library/PreferencePanes/DateAndTime.prefPane/Contents/Resources/TimeZone.prefPane/Contents/Resources/TimeZoneAdminTool` | not started | &mdash; |
| `com.apple.rapportd` | `/usr/libexec/rapportd` | not started | &mdash; |
| `com.apple.remoted` | `/usr/libexec/remoted` | ran, nonzero exit status | 1 |
| `com.apple.retimerd` | `/usr/libexec/retimerd` | not started | &mdash; |
| `com.apple.revisiond` | `/System/Library/PrivateFrameworks/GenerationalStorage.framework/Versions/A/Support/revisiond` | ran | &mdash; |
| `com.apple.scsid` | `/usr/libexec/scsid` | not started | &mdash; |
| `com.apple.secinitd` | `/usr/libexec/secinitd` | not started | &mdash; |
| `com.apple.security.cryptexd` | `/usr/libexec/cryptexd` | not started | &mdash; |
| `com.apple.security.xprotectd` | `/usr/libexec/xprotectd` | ran | &mdash; |
| `com.apple.sessionlogoutd` | `/System/Library/CoreServices/sessionlogoutd` | not started | &mdash; |
| `com.apple.signpost.signpost_reporter` | `/usr/libexec/signpost_reporter` | not started | &mdash; |
| `com.apple.softwareupdated` | `/System/Library/CoreServices/Software Update.app/Contents/Resources/softwareupdated` | not started | &mdash; |
| `com.apple.spindump` | `/usr/sbin/spindump` | not started | &mdash; |
| `com.apple.srp-mdns-proxy` | `/usr/libexec/srp-mdns-proxy` | not started | &mdash; |
| `com.apple.storage.spinandd` | `/usr/libexec/spinandd` | not started | &mdash; |
| `com.apple.storagede.helper` | `/usr/libexec/StorageDEHelper` | not started | &mdash; |
| `com.apple.suhelperd` | `/System/Library/CoreServices/Software Update.app/Contents/Resources/suhelperd` | ran | &mdash; |
| `com.apple.systemkeychain` | `/usr/sbin/systemkeychain` | not started | &mdash; |
| `com.apple.unmountassistant.sysagent` | `/System/Library/CoreServices/UnmountAssistantAgent.app/Contents/Resources/UASysAgent` | not started | &mdash; |
| `com.apple.usbctelemetryd` | `/usr/libexec/usbctelemetryd` | not started | &mdash; |
| `com.apple.usbpowerd` | `/usr/libexec/usbpowerd` | not started | &mdash; |
| `com.apple.vsdbutil` | `/usr/sbin/vsdbutil` | not started | &mdash; |
| `com.apple.wifiFirmwareLoader` | `/usr/libexec/wifiFirmwareLoader` | ran, nonzero exit status | 1 |
| `com.apple.wifip2pd` | `/usr/libexec/wifip2pd` | not started | &mdash; |
| `com.apple.xpc.smd` | `/usr/libexec/smd` | ran | &mdash; |
| `com.apple.xscertadmin` | `/usr/sbin/xscertadmin` | not started | &mdash; |
| `com.apple.xscertd` | `/usr/libexec/xscertd` | not started | &mdash; |
| `com.apple.xscertd-helper` | `/usr/libexec/xscertd-helper` | not started | &mdash; |
| `com.openssh.sshd` | `/usr/libexec/sshd-keygen-wrapper` | not started | &mdash; |

</details>

### `apple-27-lifted`

Apple's own 27.0.1 arm64e program, recompiled to x86_64 by the project's lifter and linked against 27's x86_64 libraries.

<details>
<summary><strong>7 labels</strong> &mdash; 3 ran, 1 ran but exited nonzero, 3 not started</summary>

| Label | Program | In one boot | Exit status |
|---|---|---|---|
| `com.apple.IFCStart` | `/usr/libexec/ifcstart` | not started | &mdash; |
| `com.apple.KernelEventAgent` | `/usr/sbin/KernelEventAgent` | ran, nonzero exit status | 74 |
| `com.apple.bsd.dirhelper` | `/usr/libexec/dirhelper` | ran | &mdash; |
| `com.apple.diskarbitrationd` | `/usr/libexec/diskarbitrationd` | ran | &mdash; |
| `com.apple.powerexperienced` | `/usr/libexec/powerexperienced` | ran | &mdash; |
| `com.apple.prngseedd` | `/usr/libexec/seputil` | not started | &mdash; |
| `com.apple.xpc.roleaccountd` | `/usr/libexec/xpcroleaccountd` | not started | &mdash; |

</details>

### `borrowed-tahoe-x86_64`

an x86_64 build of the same program from macOS 26 (Tahoe), used in the boot counted here; 27's own arm64e builds replaced all three in three later boots.

<details>
<summary><strong>3 labels</strong> &mdash; 2 ran, 1 ran but exited nonzero</summary>

| Label | Program | In one boot | Exit status |
|---|---|---|---|
| `com.apple.MobileFileIntegrity` | `/usr/libexec/amfid` | ran, nonzero exit status | -11 |
| `com.apple.logd` | `/usr/libexec/logd` | ran | &mdash; |
| `com.apple.logd_helper` | `/usr/libexec/logd_helper` | ran | &mdash; |

</details>

### `apple-27-flags-changed`

Apple's own 27.0.1 file, bytes unchanged, file flags changed.

<details>
<summary><strong>2 labels</strong> &mdash; 1 ran but exited nonzero, 1 not started</summary>

| Label | Program | In one boot | Exit status |
|---|---|---|---|
| `com.apple.sandboxd` | `/usr/libexec/sandboxd` | ran, nonzero exit status | -6 |
| `com.apple.taskgated` | `/usr/libexec/taskgated` | not started | &mdash; |

</details>

<sub>Generated from `data/launchd-labels.json` by `scripts/render.py`. Data and generated tables: [CC0-1.0](../LICENSE-CC0) (public domain).</sub>
<!-- generated:launchd-table:end -->
