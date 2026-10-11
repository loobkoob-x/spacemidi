=====================================================================
                      SPACEMIDI CONTROLLER SURFACE
=====================================================================

SpaceMIDI transforms your 3Dconnexion SpaceNavigator 6-axis puck into 
a highly expressive, multi-parameter MIDI controller for Ableton Live.

---------------------------------------------------------------------
0. NEW SYSTEM INSTALLATION & DEPLOYMENT GUIDE
---------------------------------------------------------------------
When moving this folder to a brand new computer:

1. Verify Core Folder Requirements (Do not delete these!):
   * Ensure the 'easyhid' folder remains in this directory.
   * Ensure the 'hidapi.dll' file remains in this directory.
   (The automated script needs both to bridge your USB hardware).

2. Download & Install External Software:
   * Python 3.13: Ensure you check the box that says "Add python.exe to 
     PATH" during the setup installer wizard.
   * loopMIDI: Install it, launch it, and click [+] to create a virtual 
     port named exactly 'SpaceMIDI'. Leave it running in the background.

3. Run the Master Launcher & Connect Ableton:
   * Double-click 'SpaceMIDI_Launcher.bat'. It will detect the new PC,
     automatically install all library modules, and inject your 
     'hidapi.dll' straight into the environment path automatically.
   * Open Ableton Live's Preferences (Ctrl + ,) -> Link, Tempo, MIDI.
   * Find 'In: SpaceMIDI' and toggle TRACK and REMOTE to ON.

---------------------------------------------------------------------
1. ACTIVE HARDWARE HOTKEYS (Global Keyboard Controls)
---------------------------------------------------------------------
[F9]  - TOGGLE MAPPING MODE vs LIVE MODE
        * Mapping Mode: Isolates only the dominant axis you are moving. 
          Use this inside Ableton's MIDI Map mode (Ctrl+M) to prevent 
          other axes from accidentally binding to the same knob.
        * Live Mode: Enables all 6 axes simultaneously for highly 
          expressive, fluid performances.

[F10] - MASTER LATCH OVERRIDE TOGGLE
        * Flips all 6 axes globally to match the same mode instantly.
          It forces a total swap between a pure SPRING setup and a 
          pure LATCH setup on the fly.

---------------------------------------------------------------------
2. INTERACTIVE CONSOLE COMMANDS (Type in Terminal & Press Enter)
---------------------------------------------------------------------
* latch [axis]  - Lock a specific axis into sticky dial behavior.
                  Example: Type 'latch z' so vertical movement stays put.

* spring [axis] - Turn an axis back into a center-snapping joystick.
                  Example: Type 'spring rx' so tilt resets when let go.

* [number]      - Set all axes globally to a single speed percentage.
                  Example: Type '15' to set all axes to 15% speed.
                  
* [axis speed]  - Isolate a single axis and change its tracking speed.
                  Available axes: x, y, z, rx, ry, rz
                  Example: Type 'z 25' to make vertical movements fast.
                  Example: Type 'rz 3' to make twisting ultra-fine.
                  
* status / show - Prints a live snapshot report showing your current 
                  operational profile map grid and active speeds.
                  
* readme / help - Displays this reference manual (skipping installation setup).
                  
* reset         - Instantly discards manual speed or mode tweaks and 
                  reloads your initial fallback presets saved inside config.json.
                  
* quit          - Safely unhooks the USB thread and shuts down the app.

---------------------------------------------------------------------
3. HOW TO TWEAK DEFAULTS PERMANENTLY
---------------------------------------------------------------------
If you want to permanently alter your starting parameters on boot, 
open 'config.json' in Notepad:
* Adjust values under "axis_modes" ("latch" or "spring") to change behavior.
* Adjust values under "axis_sensitivity" to alter your tracking speeds.
=====================================================================
