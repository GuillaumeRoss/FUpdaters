---
name: add-app
description: Add a macOS app's auto-updater-disable payload to the FUpdaters repo (the profile + apps.json), then regenerate the README and open a PR. Use when someone wants to add, contribute, or fix an app in FUpdaters — it covers finding the correct disable key, editing FUpdaters.mobileconfig and apps.json, verifying catalog coverage, running the linter, and opening a signed PR.
---

# Add an app to FUpdaters

## What this repo is

FUpdaters is a single macOS **configuration profile** (`FUpdaters.mobileconfig`) that disables the built-in auto-updater of third-party Mac apps, using `com.apple.ManagedClient.preferences` (managed/forced preferences) payloads.

**The goal — and the one rule you must respect:** only disable an app's self-updater if **something else keeps it patched**. An app is eligible only if it has an *available* patching/install source in at least one of these catalogs: **Alectrona Patch, Fleet-maintained apps, Installomator, or Homebrew Cask**. Disabling an updater for an app with no coverage means it silently goes stale and vulnerable — don't do it. If the requested app has zero coverage, say so and stop (or add it only with the user's explicit acknowledgement of the risk).

Note: "coverage" means the app is *patchable* by that tool, not that the user is actually running it. And these payloads are mostly **not live-tested** — be honest about confidence via the Status field (below).

## How the repo fits together

| File | Role | Edit by hand? |
|------|------|----------------|
| `FUpdaters.mobileconfig` | The profile. **Authoritative** for each payload's preference domain + exact keys/values. | Yes |
| `apps.json` | Per-app metadata: name, status, docs, coverage, footnotes. Source of truth for the README table **except** the keys. | Yes |
| `README.md` | The App table + footnotes between the `APPS_TABLE`/`FOOTNOTES` markers are **generated**. Everything else is prose. | Only the prose |
| `scripts/render_readme.py` | Regenerates the README table + footnotes from the profile + `apps.json`. | — |
| `scripts/validate_profile.py` | Lints the profile (well-formed plist, unique UUIDs/identifiers). | — |
| `fupdaters.py` | End-user filter tool (reads `apps.json`). | — |

The `apps.json` `slug` and the profile `PayloadIdentifier` suffix (`com.fupdaters.disable-updaters.<slug>`) must match 1:1 — CI fails otherwise.

## Steps to add an app

### 1. Find the app's bundle ID and the correct disable mechanism

```bash
defaults read "/Applications/<App>.app/Contents/Info" CFBundleIdentifier
```

Then figure out **how** the app updates, and pick a Status. Prefer inspecting the installed bundle over guessing:

```bash
# Does it use the Sparkle framework? (the common indie-app updater)
find "/Applications/<App>.app" -name "Sparkle.framework" -o -name "Autoupdate" 2>/dev/null
# Any SU* keys / custom updater strings the app already writes?
defaults read <bundleId> 2>/dev/null | grep -iE 'SU|update|version|check'
```

Choose the Status honestly:

- **Official** — the vendor documents a managed preference to disable updates. You must have the doc URL. (e.g. Firefox `DisableAppUpdate`, VS Code `UpdateMode=none`, Slack `AutoUpdate=false`.)
- **Sparkle** — you confirmed the bundle ships `Sparkle.framework`. Use `SUEnableAutomaticChecks=false` (and usually `SUAutomaticallyUpdate=false`). Direct-download builds only — the Mac App Store build ignores these.
- **Community** — a real preference that works but the vendor doesn't document it (reverse-engineered, staff-forum, or open-source-derived). Name the source.
- **Untested** — you found a candidate key but can't confirm it stops the updater (e.g. a custom, non-Sparkle updater like Rogue Amoeba's `versionCheckEnabled`). Mark it Untested rather than overclaiming.

Do **not** label something Official without a vendor doc, or Sparkle without confirming the framework is present. When unsure, use Community or Untested. Never treat "the coverage link returns HTTP 200" as evidence the disable payload works.

### 2. Add the payload to `FUpdaters.mobileconfig`

Add a `dict` to the top-level `PayloadContent` array. Generate a fresh UUID with `uuidgen`. Use identifier `com.fupdaters.disable-updaters.<slug>`. Put the real keys under `mcx_preference_settings`. Example (Sparkle app):

```xml
<dict>
    <key>PayloadContent</key>
    <dict>
        <key>com.panic.Transmit</key>
        <dict>
            <key>Forced</key>
            <array>
                <dict>
                    <key>mcx_preference_settings</key>
                    <dict>
                        <key>SUAutomaticallyUpdate</key>
                        <false/>
                        <key>SUEnableAutomaticChecks</key>
                        <false/>
                    </dict>
                </dict>
            </array>
        </dict>
    </dict>
    <key>PayloadDisplayName</key>
    <string>Transmit - Disable Auto-Updates</string>
    <key>PayloadIdentifier</key>
    <string>com.fupdaters.disable-updaters.transmit</string>
    <key>PayloadType</key>
    <string>com.apple.ManagedClient.preferences</string>
    <key>PayloadUUID</key>
    <string>PASTE-A-FRESH-UUIDGEN-VALUE</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
</dict>
```

### 3. Verify coverage, then add the `apps.json` entry

Find the app's slug/token in each catalog and **confirm the URL resolves (HTTP 200)** before using it — don't assume:

- **Cask** — token → `https://formulae.brew.sh/api/cask/<token>.json`. Use the token in the entry.
- **Installomator** — label → `https://raw.githubusercontent.com/Installomator/Installomator/main/fragments/labels/<label>.sh`. ⚠️ Some labels are aliases with **no** `.sh` file (e.g. `camtasia`, `visualstudiocode` 404 — use `camtasia2026`, `microsoftvisualstudiocode`). Verify the exact file exists.
- **Fleet** — output dir → `https://raw.githubusercontent.com/fleetdm/fleet/main/ee/maintained-apps/outputs/<slug>/darwin.json`. Match by bundle ID. ⚠️ Fleet's detection query sometimes targets a **different** bundle ID than the app ships (see the CleanShot/Unarchiver footnotes) — if so, note it via a `coverageFootnotes` entry.
- **Alectrona** — check the [catalog](https://www.alectrona.com/patch-catalog); it has no per-app URL, so this is just `true`/`false`.

Add the entry to the `apps` array in `apps.json` (`slug` must equal the profile identifier suffix):

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

- **`docs`** (optional): a full markdown link, e.g. `"[Vendor doc](https://…)"`. Omit for Sparkle apps (the Sparkle link is added automatically) or when there is no doc.
- **`coverage`** values: the catalog **slug/token string** (→ becomes a linked `X`), `true` (covered but no per-app page — Alectrona is always `true`/`false`), or `false`/omit (not covered).
- **Footnotes** (optional): `"statusFootnotes": ["direct-build"]` adds `[^direct-build]` to the Status cell; `"coverageFootnotes": {"fleet": ["fleet-cleanshot"]}` adds one to a coverage cell. Define new footnote text once in the top-level `"footnotes"` map.

### 4. Regenerate the README and run the linter (same checks as CI)

```bash
python3 scripts/render_readme.py           # rewrite the generated table + footnotes
python3 scripts/validate_profile.py        # well-formed plist + unique UUIDs/identifiers
python3 scripts/render_readme.py --check    # apps.json <-> profile parity + README up to date
```

Fix anything they flag. Do **not** hand-edit the table between the markers.

### 5. Commit and open a PR

`main` is protected and requires signed commits (merge via **squash**), and PRs are required. Commit the profile, `apps.json`, and the regenerated `README.md` together, then open a PR:

```bash
git checkout -b add-<app>
git add FUpdaters.mobileconfig apps.json README.md
git commit -m "Add <App> updater-disable payload"
git push -u origin add-<app>
gh pr create --base main --fill
```

## Quick checklist

- [ ] Real bundle ID confirmed from the installed app.
- [ ] Status is honest (Official needs a doc; Sparkle needs the framework confirmed).
- [ ] App has ≥1 real coverage source; every coverage link returns HTTP 200.
- [ ] Fresh `uuidgen` UUID; identifier suffix == `apps.json` slug.
- [ ] `render_readme.py` run; `validate_profile.py` and `render_readme.py --check` both pass.
- [ ] Profile + `apps.json` + regenerated README committed together.
