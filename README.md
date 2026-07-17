# FUpdaters

**F updaters.** A macOS configuration profile (`FUpdaters.mobileconfig`) that disables as many built-in third-party auto-updaters as possible.

I hate running a background service to update an app I rarely use (looking at you, Microsoft), but I find it equally annoying if less insulting to have apps constantly telling me an update is available when I have work to do, and tools to deal with those updates anyway.

The list of supported apps is heavily biased towards things I use, feel free to submit PRs for other apps, there isn't much downside to loading a profile blocking updaters for apps you do not have anyway. 

> [!IMPORTANT]
> Disabling an app's self-updater only makes sense if **something else** is keeping it patched. The goal here is to only disable updaters for apps that are covered by at least one patching source (currently **Alectrona** or **Fleet**, see Coverage columns below). More sources will be added over time. **Disabling updaters without alternative coverage will make your system vulnerable**. 

Customize the profile by deleting apps you don't have coverage for, or be aware they won't get updated.

## A cleaner alternative for per-app profiles

If you want individual, well-maintained, per-app profiles rather than one bundled config, use Alectrona's collection:

**https://github.com/alectrona/alectrona-patch-resources/tree/main/Disable-Built-In-Updaters**

## What this profile disables

Most payloads use a `com.apple.ManagedClient.preferences` (managed/forced preferences) payload to push settings into each app's preference domain.

### Method legend

| Method | Meaning |
|--------|---------|
| **Official** | Vendor-documented managed-preference / MDM key. Supported and stable. |
| **Sparkle** | Standard [Sparkle](https://sparkle-project.org/documentation/) auto-update framework keys. Documented by the Sparkle project (framework standard), not by the app vendor.  |
| **Community** | A real app preference, but not documented by the vendor — reverse-engineered / community-sourced. |
| **Hacky** | Unsupported technique (e.g. pointing `SUFeedURL` at `https://localhost` to break the update feed), or a key the app actively resets/ignores. |

Mac App Store apps are of course unsupported by this.

#### How the hacky (localhost) methods work

Some apps don't expose a real "disable updates" preference, but they *do* use [Sparkle](https://sparkle-project.org/) and read their update-feed URL from a preference key called `SUFeedURL`. The trick is to force that key to a dead address:

```
SUFeedURL = https://localhost
```

Sparkle then tries to fetch its appcast (the XML file that advertises new versions) from `https://localhost`, which on a normal Mac has nothing useful for it.

- It relies on the connection **failing**. If anything ever listens on `localhost:443` (a local dev server, a proxy), the behavior is undefined.
- It's not a vendor-supported switch, so an app update could change the feed key or ignore the override.
- It can produce silent network errors or log noise in the app.

Where a real key exists (`SUEnableAutomaticChecks=false`, or a vendor key like `NotionNoAutoUpdates`), that is always preferred over the localhost trick. In this profile the localhost override is only used as a belt-and-suspenders addition on **Cyberduck** and **Tunnelblick**, alongside the normal Sparkle keys. Other blunt variants of the same idea (not used here) include pointing `SUFeedURL` at `127.0.0.1`, `about:blank`, or an empty string.

### Coverage columns

- **Alectrona** — `X` if the app is in the [Alectrona Patch Catalog](https://www.alectrona.com/patch-catalog)
- **Fleet** — `X` if the app is a [Fleet-maintained app](https://fmalibrary.com/)
- **Installomator** — `X` if the app has an [Installomator](https://github.com/Installomator/Installomator) label (open-source, ~1,200 labels)
- **Cask** — `X` if the app ships as a [Homebrew Cask](https://formulae.brew.sh/cask/) (open-source, ~7,700 casks)

A `—` means the app is not in that catalog. Coverage is the point of this profile: every app disabled here is patched by at least one of these four sources.

### App table

| App | Preference domain | Key(s) set | Method | Docs | Alectrona | Fleet | Installomator | Cask |
|-----|-------------------|------------|--------|------|:---------:|:-----:|:------------:|:----:|
| 1Password 8 | `com.1password.1password` | `updates.autoUpdate=false` | Official | [1Password MDM](https://support.1password.com/mobile-device-management/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/1password/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/1password8.sh) | [X](https://formulae.brew.sh/cask/1password) |
| 1Password 7 | `com.agilebits.onepassword7` | `CheckForSoftwareUpdatesEnabled=false` | Community | — | X | — | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/1password7.sh) | [X](https://formulae.brew.sh/cask/1password@7) |
| Acorn | `com.flyingmeat.Acorn8` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/acorn/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/acorn.sh) | [X](https://formulae.brew.sh/cask/acorn) |
| Audio Hijack | `com.rogueamoeba.audiohijack` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/audio-hijack/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/rogueamoebaaudiohijack4.sh) | [X](https://formulae.brew.sh/cask/audio-hijack) |
| BetterTouchTool | `com.hegenberg.BetterTouchTool` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/bettertouchtool/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/bettertouchtool.sh) | [X](https://formulae.brew.sh/cask/bettertouchtool) |
| Camtasia | `com.techsmith.camtasia` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/camtasia/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/camtasia.sh) | [X](https://formulae.brew.sh/cask/camtasia) |
| Claude Desktop | `com.anthropic.claudefordesktop` | `disableAutoUpdates=true` | Official | [Claude enterprise config](https://support.claude.com/en/articles/12622667-enterprise-configuration-for-claude-desktop) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/claude/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/claudedesktop.sh) | [X](https://formulae.brew.sh/cask/claude) |
| CleanShot X | `pl.maketheweb.cleanshotx` | `automaticallyCheckForUpdates=false`, `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/cleanshot/darwin.json) | — | [X](https://formulae.brew.sh/cask/cleanshot) |
| Codex / ChatGPT | `com.openai.codex` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle [^codex] | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/codex-app/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/codex.sh) | [X](https://formulae.brew.sh/cask/codex-app) |
| Cursor | `com.todesktop.230313mzl4w4u92` | `UpdateMode=none` | Official | [Cursor deployment](https://cursor.com/docs/enterprise/deployment-patterns) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/cursor/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/cursorai.sh) | [X](https://formulae.brew.sh/cask/cursor) |
| Cyberduck | `ch.sudo.cyberduck` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false`, `SUFeedURL=https://localhost` | Sparkle + Hacky feed override | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/cyberduck/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/cyberduck.sh) | [X](https://formulae.brew.sh/cask/cyberduck) |
| DaisyDisk | `com.daisydiskapp.DaisyDiskStandAlone` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/daisydisk/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/daisydisk.sh) | [X](https://formulae.brew.sh/cask/daisydisk) |
| Firefox | `org.mozilla.firefox` | `DisableAppUpdate=true`, `AppAutoUpdate=false`, `EnterprisePoliciesEnabled=true` | Official | [Mozilla policies](https://mozilla.github.io/policy-templates/#disableappupdate) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/firefox/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/firefox.sh) | [X](https://formulae.brew.sh/cask/firefox) |
| Ghostty | `com.mitchellh.ghostty` | `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/ghostty/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/ghostty.sh) | [X](https://formulae.brew.sh/cask/ghostty) |
| Google Software Update (Keystone) | `com.google.Keystone` | `updatePolicies.global.UpdateDefault=2` | Official | [Chrome Enterprise update policy](https://support.google.com/chrome/a/answer/7591084) | X [^keystone] | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/google-chrome/darwin.json) [^keystone] | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/googlechrome.sh) [^keystone] | [X](https://formulae.brew.sh/cask/google-chrome) [^keystone] |
| HandBrake | `fr.handbrake.HandBrake` | `SUAllowsAutomaticUpdates=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/handbrake-app/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/handbrake.sh) | [X](https://formulae.brew.sh/cask/handbrake-app) |
| iMazing Profile Editor | `com.DigiDNA.iMazingProfileEditorMac` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/imazing-profile-editor/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/imazingprofileeditor.sh) | [X](https://formulae.brew.sh/cask/imazing-profile-editor) |
| iTerm2 | `com.googlecode.iterm2` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/iterm2/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/iterm2.sh) | [X](https://formulae.brew.sh/cask/iterm2) |
| Loopback | `com.rogueamoeba.Loopback` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/loopback/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/rogueamoebaloopback2.sh) | [X](https://formulae.brew.sh/cask/loopback) |
| Low Profile | `com.ninxsoft.lowprofile` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/low-profile/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/lowprofile.sh) | [X](https://formulae.brew.sh/cask/low-profile) |
| Microsoft AutoUpdate (MAU) | `com.microsoft.autoupdate2` | `HowToCheck=Manual` (+ telemetry/daemon keys) | Official [^mau] | [MAU preferences](https://learn.microsoft.com/en-us/microsoft-365-apps/mac/mau-preferences) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/microsoft-auto-update/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/microsoftautoupdate.sh) | [X](https://formulae.brew.sh/cask/microsoft-auto-update) |
| Microsoft OneDrive Updater | `com.microsoft.OneDriveUpdater` | `Tier=Enterprise` | Official [^onedrive] | [OneDrive update ring](https://learn.microsoft.com/en-us/sharepoint/sync-client-update-process) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/onedrive/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/microsoftonedrive.sh) | [X](https://formulae.brew.sh/cask/onedrive) |
| Mimestream | `com.mimestream.Mimestream` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/mimestream/darwin.json) | — | [X](https://formulae.brew.sh/cask/mimestream) |
| NetNewsWire | `com.ranchero.NetNewsWire-Evergreen` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/netnewswire/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/netnewswire.sh) | [X](https://formulae.brew.sh/cask/netnewswire) |
| NordVPN | `com.nordvpn.macos` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/nordvpn/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/nordvpn.sh) | [X](https://formulae.brew.sh/cask/nordvpn) |
| Notion | `notion.id` | `NotionNoAutoUpdates=true` | Official | [Notion macOS deployment](https://www.notion.com/help/deploy-notion-for-macos) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/notion/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/notion.sh) | [X](https://formulae.brew.sh/cask/notion) |
| OmniFocus | `com.omnigroup.OmniFocus4` | `OSUSoftwareUpdateAtLaunch=false` | Community [^omnifocus] | — | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/omnifocus/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/omnifocus4.sh) | [X](https://formulae.brew.sh/cask/omnifocus) |
| Opera | `com.operasoftware.Opera` | `OPDisableAutoUpdate=true` | Community | — | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/opera/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/opera.sh) | [X](https://formulae.brew.sh/cask/opera) |
| Orion | `com.kagi.kagimacOS` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | — | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/orion.sh) | [X](https://formulae.brew.sh/cask/orion) |
| Paw / RapidAPI | `com.luckymarmot.Paw` | `SUEnableAutomaticChecks=false`, `SUHasLaunchedBefore=true` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/rapidapi/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/rapidapi.sh) | [X](https://formulae.brew.sh/cask/rapidapi) |
| RingCentral | `com.ringcentral.glip` | `ZAutoUpdate=false` | Community | — | X | — | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/ringcentralapp.sh) | [X](https://formulae.brew.sh/cask/ringcentral) |
| RingCentral (pkg) | `com.ringcentral.glip.pkg` | `disableAutoLaunch=1` | Community [^rc-pkg] | — | X | — | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/ringcentralapp.sh) | [X](https://formulae.brew.sh/cask/ringcentral) |
| Slack | `com.tinyspeck.slackmacgap` | `AutoUpdate=false`, `SlackNoAutoUpdates=true` | Official [^slack] | [Slack app configuration](https://slack.com/help/articles/11906214948755-Manage-desktop-app-configurations) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/slack/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/slack.sh) | [X](https://formulae.brew.sh/cask/slack) |
| SwiftBar | `com.ameba.SwiftBar` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/swiftbar/darwin.json) | — | [X](https://formulae.brew.sh/cask/swiftbar) |
| Tailscale | `io.tailscale.ipn.macsys` | `SUEnableAutomaticChecks=false`, `SUHasLaunchedBefore=true` | Sparkle [^direct-build] | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/tailscale-app/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/tailscale.sh) | [X](https://formulae.brew.sh/cask/tailscale-app) |
| The Unarchiver | `com.macpaw.site.theunarchiver` | `SUEnableAutomaticChecks=false` | Sparkle [^direct-build] | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/the-unarchiver/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/theunarchiver.sh) | [X](https://formulae.brew.sh/cask/the-unarchiver) |
| Transmit | `com.panic.Transmit` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/transmit/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/transmit5.sh) | [X](https://formulae.brew.sh/cask/transmit) |
| Tunnelblick | `net.tunnelblick.tunnelblick` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false`, `SUFeedURL=https://localhost` | Sparkle + Hacky feed override [^tunnelblick] | [Tunnelblick forced prefs](https://tunnelblick.net/cPreferences.html) | — | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/tunnelblick/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/tunnelblick.sh) | [X](https://formulae.brew.sh/cask/tunnelblick) |
| VLC | `org.videolan.VLC` | `SUAllowsAutomaticUpdates=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/vlc/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/vlc.sh) | [X](https://formulae.brew.sh/cask/vlc) |
| Visual Studio Code | `com.microsoft.VSCode` | `UpdateMode=none` (+ telemetry keys) | Official | [VS Code enterprise policies](https://code.visualstudio.com/docs/enterprise/policies) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/visual-studio-code/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/visualstudiocode.sh) | [X](https://formulae.brew.sh/cask/visual-studio-code) |
| Wireshark | `org.wireshark.Wireshark` | `SUAutomaticallyUpdate=false`, `SUEnableAutomaticChecks=false` | Sparkle | [Sparkle](https://sparkle-project.org/documentation/) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/wireshark-app/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/wireshark.sh) | [X](https://formulae.brew.sh/cask/wireshark-app) |
| Zoom | `us.zoom.config` | `AU2_EnableAutoUpdate=false`, `ZAutoUpdate=false` | Official | [Zoom auto-update policy](https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0058493) | X | [X](https://github.com/fleetdm/fleet/blob/main/ee/maintained-apps/outputs/zoom/darwin.json) | [X](https://github.com/Installomator/Installomator/blob/main/fragments/labels/zoom.sh) | [X](https://formulae.brew.sh/cask/zoom) |

## Caveats

[^keystone]: Keystone is the **shared Google updater**, not an app — this one payload disables auto-updates for all Keystone-managed apps (Google Chrome, Earth, Drive, etc.). Those individual apps are what appear in the patching catalogs.
[^mau]: The `HowToCheck=Manual` value is documented but has been **deprecated by Microsoft** (still honored for now). Consider pairing with a channel/deferral policy for a longer-term approach.
[^onedrive]: `Tier` only selects the update **ring** — `Enterprise`/`Deferred` delays updates (~weeks), it does **not** fully disable the OneDrive updater. There is no officially documented key that fully stops it on macOS.
[^slack]: `AutoUpdate=false` is the current official (enforced-only) key. `SlackNoAutoUpdates=true` is the older community-discovered key that Slack deprecated on 2024-09-01 — kept for backward compatibility but no longer required.
[^rc-pkg]: `disableAutoLaunch` controls the auto-launch helper, not the updater directly; it's a community-sourced key.
[^direct-build]: Sparkle keys apply to the **direct-download** build only. The Mac App Store build updates through the App Store and ignores these keys.
[^tunnelblick]: The profile currently uses raw Sparkle keys plus a localhost feed override. Tunnelblick also exposes an **official "forced preferences"** mechanism (`updateCheckAutomatically`, `updateFeedURL`) which would be the cleaner supported approach — see the linked docs.

[^codex]: The same OpenAI updater backs both the standalone **Codex** app and the current **ChatGPT** desktop app — both report bundle ID `com.openai.codex`, so this one payload covers both. (The older ChatGPT "Classic" build used a different ID and is not covered here.)
[^omnifocus]: **Untested.** OmniFocus uses Omni's own `OmniSoftwareUpdate` framework (not Sparkle); `OSUSoftwareUpdateAtLaunch=false` is the observed check-at-launch key but has not been verified to hold as a forced preference — test on your build before relying on it.

## License / usage

Open source. Review the payloads before deploying, and only push updater-disable payloads for apps you are actually patching another way.
