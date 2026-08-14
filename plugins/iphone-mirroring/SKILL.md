---
name: iphone-mirroring
description: Drive the iPhone from this Mac through the iPhone Mirroring app - launch it, check whether it is locked, screenshot the mirrored screen, and map coordinates for taps. Use when the user asks to do something on their phone from the laptop, change an iOS setting, assign a Back Tap, install or configure a Shortcut on the phone, or read something that only exists on the phone. Also use when a task needs a phone-side step that cannot be done from macOS.
---

# iPhone Mirroring control

Verified on macOS 26.5.1, 2026-08-04. Facts below marked VERIFIED were tested
directly on this machine. Do not silently upgrade UNVERIFIED claims.

## Authentication: there is no PIN to type

VERIFIED: when locked, the window shows **"iPhone Mirroring Is Locked — Touch ID
or enter the Mac login for '\<your Mac account name\>' to continue."**

CONFIRMED by Apple docs (support.apple.com/en-us/120421 and the Apple Platform
Security guide, sec6ab47ebfc): this recurring "Ask every time" prompt is
satisfied by the **Mac's own credential** - Mac login password, Touch ID, or
Apple Watch - brokered through the Secure Enclave over the same protocol as
Apple Watch unlock. The iPhone passcode is a *different*, one-time device-trust
step that the phone itself asks for on first pairing or after a restart. If the
user insists "it uses the iPhone PIN", they are remembering that one-time
prompt, not this one.

Three things follow, and they kill any plan to automate this:

1. The secret it wants is the **Mac login password**, not the iPhone passcode.
2. VERIFIED: `System Events keystroke` into that field does nothing. The
   placeholder never becomes dots. macOS secure event input blocks synthetic
   keystrokes in auth fields by design.
3. VERIFIED: the Claude Code permission classifier refuses this in auto mode.
   It blocked (a) clicking the field then keystroking, (b) keystroking the
   secret read from the env file, and (c) *writing a shell script* that would
   do it. Typing a stored credential into an auth prompt is indistinguishable
   from credential stuffing, so it is denied outright rather than prompted.
   **Do not attempt to work around this.** No `cliclick` install, no CGEvent
   helper, no AppleScript variant, no helper script, no retry after the user
   says "I'll approve it" - in auto mode there is no approval prompt to hit.
   Tell the user to enable automatic authentication instead.

**Never store the Mac login password in a dotfile to feed this prompt.** It is
the key to the whole machine, the keychain, and sudo. If the user has already
put it in one, say so and offer to blank it.

One honest counter-report, ANECDOTAL and unreproduced here
(macscripter.net/t/iphone-mirroring/77733): Nigel Garvey claims that targeting
the element directly, `text field 1 of group 1` rather than blind
coordinate-clicking, did accept a typed credential plus Return. It may be
version or config dependent. It does not change the guidance, because the
classifier refuses the attempt either way and the settings fix is strictly
better. Recorded only so nobody thinks this avenue went unexamined.

CONFIRMED context on how everyone else dodges this: none of the community
projects solve the lock in-band. `mirroir-mcp` and `kae-builds/iphone-mirror-mcp`
both list "iPhone Mirroring already configured and working" as a prerequisite and
punt. `blitzdotdev/iPhone-mcp` (Developer Mode + trusted USB pairing) and
`lakr233/iphone-mcp` (Appium + WebDriverAgent) are not mirroring-based at all,
which is how they avoid the problem entirely.

### What to do instead

Ordered best to worst:

1. **One-time setting.** This is the fix. VERIFIED end to end on this Mac,
   including that the Settings window opens *even while the mirror is locked*.

   Menu path: **iPhone Mirroring menu > Settings…** > *"Require Mac login to
   access iPhone:"* > choose **"Authenticate automatically"** (the other option
   is **"Ask every time"**, which is the default and the thing causing the
   prompt).

   Open it programmatically, and read the current state:

   ```bash
   open -a "iPhone Mirroring"
   osascript -e 'tell application "System Events" to tell process "iPhone Mirroring" to click menu item "Settings…" of menu 1 of menu bar item 2 of menu bar 1'
   ```

   VERIFIED accessibility path to the radio group (titles are `missing value`
   because it is SwiftUI, so identify by index and by `value`, where 1 = selected):

   ```
   radio button 1 of radio group 1 of group 1 of scroll area 1 of group 1 of window "iPhone Mirroring Settings"
     -> "Ask every time"
   radio button 2 of ... -> "Authenticate automatically"
   ```

   Also in that window: a "Revoke Access to <device>" button (group 2, button 1).
   Never click that.

   VERIFIED: **clicking radio button 2 is blocked by the permission classifier**,
   because it weakens the machine's security posture. Do not retry it. Screenshot
   the open Settings window, tell the user which option to click, and let them
   do it. Selecting it also requires one Touch ID or password entry.

   CONFIRMED tradeoff to disclose before recommending it (Apple support 120421):
   choosing "Authenticate automatically" forces Lock Screen's *"Require password
   after screen saver begins or display is turned off"* to **Immediately**.

   Relevant prefs live in `com.apple.ScreenContinuity` (`isAuthFrequencySet`,
   `onenessPairedDeviceID`). The chosen value is not exposed there in plaintext,
   so read the radio button `value` via accessibility instead of `defaults`.
2. **Ask the user for Touch ID.** One finger, zero secrets stored. Say
   "iPhone Mirroring is locked, please Touch ID" and wait.
3. Nothing else. If it is locked and the user is away, the phone-side task is
   blocked. Report that plainly instead of improvising.

## Launch and locate the window

```bash
open -a "iPhone Mirroring"
# window 1 geometry, in logical points
osascript -e 'tell application "System Events" to tell process "iPhone Mirroring" to get position of window 1'
osascript -e 'tell application "System Events" to tell process "iPhone Mirroring" to get size of window 1'
```

VERIFIED typical values: position `241, 158`, size `348, 766`.

Gotchas learned the hard way:

- `tell process "iPhone Mirroring" to set frontmost to true` fails with error
  -10006. Use `open -a "iPhone Mirroring"` to raise it.
- `get {item 1 of position, ...} of window 1` fails with -1700. Fetch
  `position` and `size` as separate calls and parse the `"X, Y"` strings.

## Screenshot the mirrored screen

```bash
screencapture -x -R "$X,$Y,$W,$H" /path/out.png
```

VERIFIED: `-R` captures whatever is **topmost** in that screen region, not the
window. If the terminal overlaps the window you will screenshot your own
terminal. Raise iPhone Mirroring with `open -a` first, then capture.

VERIFIED: `Quartz` (pyobjc) is NOT installed, so window-ID capture via
`CGWindowListCopyWindowInfo` is unavailable without installing it. `screencapture
-l <windowid>` captures even when occluded and avoids the focus-stealing dance,
so it is the better path once you can get the ID. CONFIRMED that the iPhone
Mirroring window is a normal window to macOS windowing APIs with no special
obstruction, so either `pip install pyobjc-framework-Quartz` or the `GetWindowID`
utility (github.com/gsbabil/GetWindowID) unlocks this. Prefer that over `-R`.

Output is Retina 2x: a 348x766 point window yields a 696x1532 px image.

### Coordinate mapping

To convert a feature found in the screenshot to a screen point for clicking:

```
screen_x = window_X + (pixel_x / 2)
screen_y = window_Y + (pixel_y / 2)
```

Crop before reading an image when you only need one region. `PIL` is available:

```python
from PIL import Image
Image.open("out.png").crop((100, 850, 600, 1050)).save("crop.png")
```

## Interacting with the phone

UNVERIFIED here: taps via
`osascript -e 'tell application "System Events" to click at {x, y}'` and text
entry via `keystroke`. Neither was confirmed working inside the mirrored screen
in this session.

What the community actually does, and it is worth copying:

- **Taps via CGEvent**, not System Events `click at`. Both `mirroir-mcp` and
  `iphone-mirror-mcp` went this route.
- **Text via clipboard paste** (`pbcopy` then Cmd-V), not `keystroke`. Reported
  as materially more reliable, and it bypasses IME interference. Use this first
  for any text entry inside the phone.
- **Swipes as gesture curves**, otherwise the phone reads them as drags.
- ANECDOTAL but encouraging (macscripter.net/t/iphone-mirroring/77733):
  `keystroke` does reach normal iOS text fields through mirroring even though
  the UI tree is not inspectable. So keystroke unreliability is a quality issue
  inside the phone, not a blanket OS block. The auth field is the exception,
  and that one is a hard block.

### Consider an existing MCP server instead

Before hand-rolling coordinate automation, check these - they already implement
screenshot/tap/swipe/type as MCP tools: `jfarcand/mirroir-mcp`,
`kae-builds/iphone-mirror-mcp`, `blitzdotdev/iPhone-mcp`. None of them solve the
auth prompt either.

### If the goal is real device automation, skip mirroring

CONFIRMED as the preferred stack when you need reliable control rather than a
mirrored screen: `pymobiledevice3` (pure Python, iOS 17+ tunneling), `go-ios`,
`idb`, and Apple's `xcrun devicectl`. None of these need a live unlocked
mirrored window. Reach for these for anything repeated or scripted.

Hard limits that are certain:

- The mirrored area is a **video stream**. There is no accessibility tree for
  anything on the phone, so element queries return nothing. Every interaction
  is blind coordinate work against a screenshot.
- `cliclick` is NOT installed.
- Coordinates shift whenever the window moves or resizes. Re-read geometry and
  re-screenshot before every interaction. Never reuse coordinates across turns.

Because of this fragility: prefer a macOS-side path whenever one exists. Only
fall back to mirroring for things that genuinely only live on the phone, for
example Settings > Accessibility > Touch > Back Tap.

## Do not use mirroring for Shortcuts

Shortcuts sync from this Mac to the iPhone over iCloud. Build the shortcut on
the Mac and let it sync — if you have a script-based shortcut-build pipeline,
reuse that pattern here. Note that `shortcuts sign` rejects any input file not
named `*.shortcut`.
