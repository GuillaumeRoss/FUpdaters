# FUpdaters

**F updaters.** A macOS configuration profile (`FUpdaters.mobileconfig`) that disables as many built-in third-party auto-updaters as possible.

## Why
I hate running a background service to update an app I rarely use (looking at you, Microsoft), but I find it equally annoying if less insulting to have apps constantly telling me an update is available when I have work to do, and tools to deal with those updates anyway. 

This also helps protect against supply chain malware, provided your source has a cooldown period or other checks (hound them down if they don't!).

The list of supported apps is heavily biased towards things I use, feel free to submit PRs for other apps, there isn't much downside to loading a profile blocking updaters for apps you do not have anyway.

## Watch out

> [!IMPORTANT]
> Disabling an app's self-updater only makes sense if **something else** is keeping it patched. This profile only disables updaters for apps that have an **available** patching/install source (Alectrona, Fleet, Installomator, or Homebrew Cask — see Coverage columns). **If you disable an updater and nothing is actually updating the app, you will run vulnerable, out-of-date software.**

Customize the profile by deleting apps you don't have coverage for (or use `fupdaters.py`, below), or be aware they won't get updated.

## A cleaner alternative for per-app profiles

If you want individual, well-maintained, per-app profiles rather than one bundled config, use Alectrona's collection:

**https://github.com/alectrona/alectrona-patch-resources/tree/main/Disable-Built-In-Updaters**

## What this profile disables

Most payloads use a `com.apple.ManagedClient.preferences` (managed/forced preferences) payload to push settings into each app's preference domain. Mac App Store builds are out of scope — they update through the App Store and ignore these preferences.

### Status legend

The **Status** column reflects the *evidence* behind each payload, not a live behavioral test on every build:

| Status | Meaning |
|--------|---------|
| **Official** | Vendor-documented managed preference. Behavior per current vendor docs. |
| **Sparkle** | Standard [Sparkle](https://sparkle-project.org/documentation/) framework keys, confirmed by inspecting the app bundle. Direct-download builds only. |
| **Community** | A real preference that works but is not vendor-documented (reverse-engineered, staff-forum, or open-source-derived). |
| **Untested** | A candidate key has been identified but **not** verified to actually stop the updater. Best-effort, pending live testing. |

> [!NOTE]
> I have not tested any of these seriously. For apps I do run, if I ever get an update pop-up again, I will fix the profiles. If you spot anything, feel free to submit an issue.

### Coverage columns

- **Alectrona** - in the [Alectrona Patch Catalog](https://www.alectrona.com/patch-catalog)
- **Fleet** - a [Fleet-maintained app](https://fmalibrary.com/)
- **Installomator** — has an [Installomator](https://github.com/Installomator/Installomator) label
- **Cask** - ships as a [Homebrew Cask](https://formulae.brew.sh/cask/)

`X` means it is part of the catalog, and where possible, links to the app's page in that catalog where one exists.

### App table

<!-- This table is generated from apps.json + the profile by scripts/render_readme.py. Do not edit by hand. -->
<!-- APPS_TABLE:BEGIN -->
| App | Preference domain | Key(s) set | Status | Docs | Alectrona | Fleet | Installomator | Cask |
|-----|-------------------|------------|--------|------|:---------:|:-----:|:------------:|:----:|
| 1Password 8 | `com.1password.1password` | `updates.autoUpdate=false` | Official [^1password] | [1Password MDM](https://support.1password.com/mobile-device-management/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/1password/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/1password8.sh) | [X](https://formulae.brew.sh/cask/1password) |
| 1Password 7 | `com.agilebits.onepassword7` | `CheckForSoftwareUpdatesEnabled=false` | Community | — | X | — | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/1password7.sh) | [X](https://formulae.brew.sh/cask/1password@7) |
| Acorn | `com.flyingmeat.Acorn8` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/acorn/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/acorn.sh) | [X](https://formulae.brew.sh/cask/acorn) |
| Audio Hijack | `com.rogueamoeba.audiohijack` | `SUAutomaticallyUpdate=false`, `versionCheckEnabled=false` | Untested [^rogueamoeba] | — | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/audio-hijack/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/rogueamoebaaudiohijack4.sh) | [X](https://formulae.brew.sh/cask/audio-hijack) |
| BetterTouchTool | `com.hegenberg.BetterTouchTool` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/bettertouchtool/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/bettertouchtool.sh) | [X](https://formulae.brew.sh/cask/bettertouchtool) |
| Camtasia | `com.techsmith.camtasia` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/camtasia/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/camtasia2026.sh) | [X](https://formulae.brew.sh/cask/camtasia) |
| Claude Desktop | `com.anthropic.claudefordesktop` | `disableAutoUpdates=true` | Official | [Claude enterprise config](https://support.claude.com/en/articles/12622667-enterprise-configuration-for-claude-desktop) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/claude/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/claudedesktop.sh) | [X](https://formulae.brew.sh/cask/claude) |
| CleanShot X | `pl.maketheweb.cleanshotx` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false`, `automaticallyCheckForUpdates=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/cleanshot/darwin.json) [^fleet-cleanshot] | — | [X](https://formulae.brew.sh/cask/cleanshot) |
| Codex / ChatGPT | `com.openai.codex` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle [^codex] | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/codex-app/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/codex.sh) | [X](https://formulae.brew.sh/cask/codex-app) |
| Cursor | `com.todesktop.230313mzl4w4u92` | `UpdateMode=none` | Official | [Cursor deployment](https://cursor.com/docs/enterprise/deployment-patterns) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/cursor/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/cursorai.sh) | [X](https://formulae.brew.sh/cask/cursor) |
| Cyberduck | `ch.sudo.cyberduck` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/cyberduck/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/cyberduck.sh) | [X](https://formulae.brew.sh/cask/cyberduck) |
| DaisyDisk | `com.daisydiskapp.DaisyDiskStandAlone` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/daisydisk/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/daisydisk.sh) | [X](https://formulae.brew.sh/cask/daisydisk) |
| Firefox | `org.mozilla.firefox` | `DisableAppUpdate=true`, `EnterprisePoliciesEnabled=true` | Official | [Mozilla policies](https://mozilla.github.io/policy-templates/#disableappupdate) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/firefox/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/firefox.sh) | [X](https://formulae.brew.sh/cask/firefox) |
| Ghostty | `com.mitchellh.ghostty` | `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/ghostty/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/ghostty.sh) | [X](https://formulae.brew.sh/cask/ghostty) |
| Google Software Update (Keystone) | `com.google.Keystone` | `updatePolicies.global.UpdateDefault=2` | Official [^keystone] | [Chrome Enterprise update policy](https://support.google.com/chrome/a/answer/7591084) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/google-chrome/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/googlechrome.sh) | [X](https://formulae.brew.sh/cask/google-chrome) |
| HandBrake | `fr.handbrake.HandBrake` | `SUAllowsAutomaticUpdates=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/handbrake-app/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/handbrake.sh) | [X](https://formulae.brew.sh/cask/handbrake-app) |
| iMazing Profile Editor | `com.DigiDNA.iMazingProfileEditorMac` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/imazing-profile-editor/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/imazingprofileeditor.sh) | [X](https://formulae.brew.sh/cask/imazing-profile-editor) |
| iTerm2 | `com.googlecode.iterm2` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/iterm2/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/iterm2.sh) | [X](https://formulae.brew.sh/cask/iterm2) |
| Loopback | `com.rogueamoeba.Loopback` | `SUAutomaticallyUpdate=false`, `versionCheckEnabled=false` | Untested [^rogueamoeba] | — | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/loopback/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/rogueamoebaloopback2.sh) | [X](https://formulae.brew.sh/cask/loopback) |
| Low Profile | `com.ninxsoft.lowprofile` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/low-profile/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/lowprofile.sh) | [X](https://formulae.brew.sh/cask/low-profile) |
| Microsoft AutoUpdate (MAU) | `com.microsoft.autoupdate2` | `AcknowledgedDataCollectionPolicy=RequiredDataOnly`, `DisableOptInNotification=true`, `EnableCheckForUpdatesButton=false`, `HowToCheck=Manual`, `IgnoreUIOpenAfterInstall=true` | Official [^mau] | [MAU preferences](https://learn.microsoft.com/en-us/microsoft-365-apps/mac/mau-preferences) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/microsoft-auto-update/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/microsoftautoupdate.sh) | [X](https://formulae.brew.sh/cask/microsoft-auto-update) |
| Mimestream | `com.mimestream.Mimestream` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/mimestream/darwin.json) | — | [X](https://formulae.brew.sh/cask/mimestream) |
| NetNewsWire | `com.ranchero.NetNewsWire-Evergreen` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/netnewswire/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/netnewswire.sh) | [X](https://formulae.brew.sh/cask/netnewswire) |
| NordVPN | `com.nordvpn.macos` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/nordvpn/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/nordvpn.sh) | [X](https://formulae.brew.sh/cask/nordvpn) |
| Notion | `notion.id` | `NotionNoAutoUpdates=true` | Official | [Notion macOS deployment](https://www.notion.com/help/deploy-notion-for-macos) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/notion/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/notion.sh) | [X](https://formulae.brew.sh/cask/notion) |
| OmniFocus | `com.omnigroup.OmniFocus4` | `OSUCheckEnabled=false`, `OSUSoftwareUpdateAtLaunch=false` | Community [^omnifocus] | [Omni source](https://github.com/omnigroup/OmniGroup/blob/main/Frameworks/OmniSoftwareUpdate/OSUPreferences.m) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/omnifocus/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/omnifocus4.sh) | [X](https://formulae.brew.sh/cask/omnifocus) |
| Opera | `com.operasoftware.Opera` | `OPDisableAutoUpdate=true` | Community [^opera] | [Opera staff forum](https://forums.opera.com/topic/11657/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/opera/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/opera.sh) | [X](https://formulae.brew.sh/cask/opera) |
| Orion | `com.kagi.kagimacOS` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle [^orion] | [Sparkle](https://sparkle-project.org/documentation/) | X | — | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/orion.sh) | [X](https://formulae.brew.sh/cask/orion) |
| Paw / RapidAPI | `com.luckymarmot.Paw` | `SUEnableAutomaticChecks=false`, `SUHasLaunchedBefore=true` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/rapidapi/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/rapidapi.sh) | [X](https://formulae.brew.sh/cask/rapidapi) |
| RingCentral | `com.ringcentral.glip` | `ZAutoUpdate=false` | Community | — | X | — | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/ringcentralapp.sh) | [X](https://formulae.brew.sh/cask/ringcentral) |
| Slack | `com.tinyspeck.slackmacgap` | `AutoUpdate=false` | Official | [Slack app configuration](https://slack.com/help/articles/11906214948755-Manage-desktop-app-configurations) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/slack/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/slack.sh) | [X](https://formulae.brew.sh/cask/slack) |
| SwiftBar | `com.ameba.SwiftBar` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/swiftbar/darwin.json) | — | [X](https://formulae.brew.sh/cask/swiftbar) |
| Tailscale | `io.tailscale.ipn.macsys` | `SUEnableAutomaticChecks=false`, `SUHasLaunchedBefore=true` | Sparkle [^direct-build] | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/tailscale-app/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/tailscale.sh) | [X](https://formulae.brew.sh/cask/tailscale-app) |
| The Unarchiver | `com.macpaw.site.theunarchiver` | `SUEnableAutomaticChecks=false` | Sparkle [^direct-build] | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/the-unarchiver/darwin.json) [^fleet-unarchiver] | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/theunarchiver.sh) | [X](https://formulae.brew.sh/cask/the-unarchiver) |
| Transmit | `com.panic.Transmit` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/transmit/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/transmit5.sh) | [X](https://formulae.brew.sh/cask/transmit) |
| Tunnelblick | `net.tunnelblick.tunnelblick` | `updateCheckAutomatically=false` | Official [^tunnelblick] | [Tunnelblick forced prefs](https://tunnelblick.net/cPreferences.html) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/tunnelblick/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/tunnelblick.sh) | [X](https://formulae.brew.sh/cask/tunnelblick) |
| VLC | `org.videolan.vlc` | `SUAllowsAutomaticUpdates=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/vlc/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/vlc.sh) | [X](https://formulae.brew.sh/cask/vlc) |
| Visual Studio Code | `com.microsoft.VSCode` | `EnableFeedback=false`, `TelemetryLevel=off`, `UpdateMode=none` | Official | [VS Code enterprise policies](https://code.visualstudio.com/docs/enterprise/policies) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/visual-studio-code/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/microsoftvisualstudiocode.sh) | [X](https://formulae.brew.sh/cask/visual-studio-code) |
| Wireshark | `org.wireshark.Wireshark` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/wireshark-app/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/wireshark.sh) | [X](https://formulae.brew.sh/cask/wireshark-app) |
| Zoom | `us.zoom.config` | `AU2_EnableAutoUpdate=false` | Official | [Zoom auto-update policy](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058493) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/zoom/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/zoom.sh) | [X](https://formulae.brew.sh/cask/zoom) |
<!-- APPS_TABLE:END -->

## Caveats

<!-- These footnotes are generated by scripts/render_readme.py. Do not edit by hand. -->
<!-- FOOTNOTES:BEGIN -->
[^1password]: `updates.autoUpdate` applies to the direct-download `.app` build. For PKG/MDM deployments 1Password expects updates to be pushed via your MDM, and this key does not apply there. Source: [1Password MDM](https://support.1password.com/mobile-device-management/).
[^rogueamoeba]: **Untested.** Audio Hijack and Loopback use Rogue Amoeba's own periodic version check (`com.rogueamoeba.ptappcontroller.versionCheck`), not standard Sparkle scheduling — so `SUEnableAutomaticChecks` does not stop it. `versionCheckEnabled=false` is the observed native preference (from binary inspection) but has **not** been verified to hold as a forced managed preference. Test before relying on it.
[^fleet-cleanshot]: Fleet ships a CleanShot X package, but its detection query checks bundle ID `com.getcleanshot.app` while current builds are `pl.maketheweb.cleanshotx` — so Fleet's install/patch **detection** may be unreliable even though a package exists. (Upstream Fleet issue, not this profile.)
[^codex]: The shared OpenAI updater backs both the standalone **Codex** app and the current **ChatGPT** desktop app — both report bundle ID `com.openai.codex`, so this one payload covers both. The older ChatGPT "Classic" build used a different ID and is not covered.
[^keystone]: Keystone is Google's **shared updater**, not an app — this payload disables auto-updates for every Keystone-managed app (Chrome, Earth, Drive, …). The coverage links point to Google Chrome as the representative catalog entry.
[^mau]: `HowToCheck=Manual` is **current and documented** — the *deprecated* value is `Automatic` (replaced by `AutomaticCheck`). In `Manual` mode MAU still updates **itself**, but stops auto-updating the Office apps. The undocumented `StartDaemonOnAppLaunch` key was removed; the remaining keys (`AcknowledgedDataCollectionPolicy`, `DisableOptInNotification`, `EnableCheckForUpdatesButton`, `IgnoreUIOpenAfterInstall`) are documented MAU preferences. Source: [MAU preferences](https://learn.microsoft.com/en-us/microsoft-365-apps/mac/mau-preferences).
[^omnifocus]: OmniFocus uses Omni's own `OmniSoftwareUpdate` framework (not Sparkle). `OSUCheckEnabled=false` is the master toggle that stops both the launch-time and the periodic (~24h) check; `OSUSoftwareUpdateAtLaunch=false` alone only stops the launch check. Keys are confirmed from Omni's [open-source framework](https://github.com/omnigroup/OmniGroup/blob/main/Frameworks/OmniSoftwareUpdate/OSUPreferences.m), not vendor MDM docs, and are not live-tested here.
[^opera]: `OPDisableAutoUpdate` comes from an Opera-**staff forum post**, not an official enterprise deployment doc, and has not been re-verified on current Opera (v133).
[^orion]: Covers the stable Orion build (`com.kagi.kagimacOS`). Orion **RC** uses `com.kagi.kagimacOS.RC` and is **not** covered by this payload.
[^direct-build]: Applies to the **direct-download** build only. The Mac App Store build updates through the App Store and ignores these managed preferences.
[^fleet-unarchiver]: Fleet's detection query checks bundle ID `cx.c3.theunarchiver`, while the direct-download build is `com.macpaw.site.theunarchiver` — Fleet detection may not match the direct build. (Upstream Fleet issue.)
[^tunnelblick]: Uses Tunnelblick's documented forced preference `updateCheckAutomatically=false`, which replaces the earlier `SUFeedURL=https://localhost` hack. `updateFeedURL` is not needed to disable checks. Source: [Tunnelblick preferences](https://tunnelblick.net/cPreferences.html).
<!-- FOOTNOTES:END -->

## Entries that still need live testing

Statuses above are based on documentation, the Sparkle framework, or source code — **not** on installing this profile and confirming the updater actually stops. The ones most worth verifying on your own builds:

- **Audio Hijack, Loopback** (Untested) — Rogue Amoeba's custom updater; `versionCheckEnabled=false` is a best guess.
- **OmniFocus** (Community) — `OSUCheckEnabled=false` is confirmed from Omni's source but not live-tested as a forced preference.
- **Opera** (Community) — staff-forum key, not confirmed on current Opera.
- **Tunnelblick** (Official) — documented preference, but not live-tested here.
- Everything else marked **Official/Sparkle** is evidence-based but has not been individually behavior-tested on every build.

## Removing the profile

`PayloadRemovalDisallowed` is set to **false**, so the profile can be removed normally (System Settings › Device Management, or `profiles`/MDM). This is deliberate while some payloads are experimental — do not set it back to `true` unless you specifically want to lock the profile in place.

## Cutting the profile down (`fupdaters.py`)

The full profile disables updaters for every app it knows about. Only disable an updater if something else patches the app, so trim the profile to the tools you actually run:

```
python3 fupdaters.py --fleet > MyFleet.mobileconfig          # you run Fleet
python3 fupdaters.py --cask --alectrona -o Subset.mobileconfig   # keep anything either one covers
python3 fupdaters.py --any -o Subset.mobileconfig            # anything covered by a known source
python3 fupdaters.py --list                                  # preview the coverage matrix
```

Source flags are OR'd (an app is kept if any selected tool covers it). Coverage data lives in `apps.json`. Python 3 only, no install.

## Contributing

PRs welcome — especially new apps and live-test results for anything marked **Untested** or **Community**.

**The pieces**

| File | Role |
|------|------|
| `FUpdaters.mobileconfig` | The profile. **Authoritative** for each payload's preference domain and the exact keys/values it sets. |
| `apps.json` | Per-app metadata: name, status, docs link, coverage, and footnote wiring. Source of truth for everything in the table *except* the keys. |
| `scripts/render_readme.py` | Regenerates the README table + footnotes from the profile + `apps.json`. |
| `scripts/validate_profile.py` | Lints the profile (valid plist, unique UUIDs/identifiers). |
| `fupdaters.py` | End-user filter tool (reads `apps.json`). |

**Do not hand-edit the table** between the `APPS_TABLE`/`FOOTNOTES` markers in this file. It is generated from `apps.json`.

### Adding or changing an app

1. **Edit the profile.** Add (or change) a `com.apple.ManagedClient.preferences` payload. Give it a unique `PayloadUUID` (`uuidgen`) and a `PayloadIdentifier` of the form `com.fupdaters.disable-updaters.<slug>`. Put the real preference keys under `mcx_preference_settings`.

2. **Add the matching entry to `apps.json`** (the `<slug>` must match the payload identifier's suffix):

   ```json
   {
     "slug": "transmit",
     "name": "Transmit",
     "bundleId": "com.panic.Transmit",
     "status": "Sparkle",
     "coverage": {
       "alectrona": true,
       "fleet": "transmit",
       "installomator": "transmit5",
       "cask": "transmit"
     }
   }
   ```

   - **`status`**: one of `Official`, `Sparkle`, `Community`, `Untested` (see the Status legend). Don't claim `Official` without a vendor doc, or `Sparkle` without confirming the app bundles Sparkle.
   - **`docs`** (optional): a full markdown link, e.g. `"[Vendor doc](https://…)"`. Omit it for `Sparkle` apps (the Sparkle link is added automatically) or when there's no doc.
   - **`coverage`**: for `fleet` / `installomator` / `cask`, use the catalog's **slug/token** (string) so the `X` becomes a link — the Fleet output dir name, the Installomator label file name, or the Homebrew cask token. Use `true` if it's covered but has no per-app page (Alectrona is always `true`/`false`), or `false` if not covered. **Verify the link resolves (HTTP 200)** — some Installomator labels are aliases without their own file, and some Fleet records detect a different bundle ID than the app actually ships (see the CleanShot/Unarchiver footnotes).
   - **Footnotes** (optional): `"statusFootnotes": ["direct-build"]` adds a `[^direct-build]` marker to the Status cell; `"coverageFootnotes": {"fleet": ["fleet-cleanshot"]}` adds one to a coverage cell. Define the footnote text once in the top-level `"footnotes"` map in `apps.json`.

3. **Regenerate the README, then run the linter locally.** Regenerate first, then run the checks below — these are exactly what the **`Validate profile`** GitHub workflow ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)) runs on your PR, so if they pass locally the CI linter will pass too:

   ```
   # regenerate the generated README regions after editing apps.json / the profile
   python3 scripts/render_readme.py

   # --- the linter (same checks CI runs, in order) ---
   plutil -lint FUpdaters.mobileconfig          # profile is a well-formed plist (CI uses xmllint; same effect)
   python3 scripts/validate_profile.py          # valid plist + unique PayloadUUIDs / identifiers
   python3 scripts/render_readme.py --check      # apps.json <-> profile parity + README up to date
   ```

   All three are Python 3 / built-in macOS tools — nothing to install. `python3 scripts/render_readme.py --check` exits non-zero (and tells you what to fix) if `apps.json` and the profile disagree or the committed README is stale.

   **Commit the regenerated `README.md` alongside your `apps.json`/profile change.** `main` is protected and requires signed commits, so the README is part of your own (signed) PR — nothing is auto-committed by a bot. Only the two marked regions of the README change; leave the prose alone.

A PR fails if the profile is an invalid plist, has a duplicate `PayloadUUID`/`PayloadIdentifier`, if `apps.json` and the profile reference different sets of apps, or if the committed README is out of date (run `render_readme.py` and commit).

## License / usage

Open source. Review the payloads before deploying, and only push updater-disable payloads for apps you are actually patching another way.
