=====================================================================
                      SPACEMIDI PERFORMANCE MANUAL
=====================================================================

SpaceMIDI lets you use a 3Dconnexion SpaceNavigator puck as a fluid, 
6-axis MIDI controller inside Ableton Live or any other DAW. 

---------------------------------------------------------------------
0. NEW INSTALLATION
---------------------------------------------------------------------
If you move this project folder to a new computer:

1. Run the Launcher: Double-click 'SpaceMIDI_Launcher.bat'. The script 
   will automatically detect a fresh install, prompt you to install 
   Python and loopMIDI if necessary, and download any missing 
   dependencies.
2. When installing Python 3.13: Make sure you tick the checkbox that says 
   "Add python.exe to PATH" during setup.
3. Setup loopMIDI: Run it, click the [+] button, and create a virtual 
   port named "SpaceMIDI".


In Ableton, open Preferences -> MIDI, find the 'SpaceMIDI' input, and
turn both TRACK and REMOTE to ON.

---------------------------------------------------------------------
1. HARDWARE SHORTCUTS
---------------------------------------------------------------------
[F9]  - TOGGLE MAPPING MODE vs LIVE MODE
        * Mapping Mode isolates whatever axis you move the hardest. 
          Use this inside Ableton's MIDI Learn menu (Ctrl+M) so other 
          axes don't accidentally override your knob assignments.
        * Live Mode opens all 6 axes up at once for performing.

[F10] - MASTER AXIS OVERRIDE
        * Toggles all 6 control response behaviours back and forth 
		between SPRING and LATCH modes.

---------------------------------------------------------------------
2. LIVE TERMINAL COMMANDS
---------------------------------------------------------------------
Type these directly into your active console screen while jamming:

* latch [axis]  - Lock an axis into sticky volume dial behavior.
				  Axes: x, y, z, rx, ry, rz
                  Example: 'latch z' stops the vertical axis snapping.

* spring [axis] - Reset an axis to center-snapping joystick behavior.
                  Example: 'spring rx' makes tilt snap back to 64.

* [number]      - Instantly change all axes to one global speed.
                  Example: '15' sets everything to 15% speed.
                  
* [axis speed]  - Fine-tune the velocity multiplier of one specific axis.
                  Example: 'z 25' makes vertical adjustments highly sensitive.
                  Example: 'rz 3' makes twisting incredibly fine.
                  
* status / show - Prints a clean table tracking your current layout.
                  
* readme / help - Pulls up this guide inside the terminal window.
                  
* reset         - Wipes out all live modifications and reloads the
                  saved default behaviors from your config.json file.
                  
* quit          - Safely closes the USB stream and shuts down the app.

---------------------------------------------------------------------
3. EDITING FIXED STARTUP DEFAULTS
---------------------------------------------------------------------
To change default startup settings, open 'config.json' in a text editor:
* Edit the "axis_modes" list to assign permanent 'latch' or 'spring' defaults.
* Edit the "axis_sensitivity" values to assign preferred tracking speeds.
=====================================================================
