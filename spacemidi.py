import os
# Force mido to use the stable, pre-installed pygame backend instead of looking for rtmidi
os.environ['MIDO_BACKEND'] = 'mido.backends.pygame'

from easyhid import Enumeration
import mido
import struct
import time
import keyboard
import json
import threading

# --- Config Loader ---
with open('config.json', 'r') as f:
    cfg = json.load(f)

USB_VID        = int(cfg['vendor_id'], 16)
USB_PID        = int(cfg['product_id'], 16)
MIDI_CHANNEL   = cfg['midi_channel']
MAX_VAL        = cfg['max_val']
DEAD_ZONE      = cfg['dead_zone']
LOCK_MS        = cfg['lock_ms']
AXIS_MAPPING   = cfg['axis_mapping']
BTN_MAPPING    = {int(k): v for k, v in cfg['btn_mapping'].items()}
HOTKEY_MAPPING = cfg['hotkey_mapping_mode']
HOTKEY_LATCH   = cfg['hotkey_latch_mode']

GLOBAL_FALLBACK = cfg.get('latch_sensitivity', 10)

# Dictionaries to manage live multi-profile tracking arrays
active_sensitivity = {}
active_modes = {}

def load_initial_speeds():
    """Reads initial per-axis speed values from config, falling back to global default."""
    global active_sensitivity
    config_axis_speeds = cfg.get('axis_sensitivity', {})
    for k in AXIS_MAPPING:
        percent = config_axis_speeds.get(k, GLOBAL_FALLBACK)
        active_sensitivity[k] = percent / 2000.0

def load_initial_modes():
    """Reads initial per-axis behavioral modes from config, falling back to spring."""
    global active_modes
    config_axis_modes = cfg.get('axis_modes', {})
    for k in AXIS_MAPPING:
        active_modes[k] = config_axis_modes.get(k, 'spring').lower()

def load_initial_profiles():
    """Full initialization wrapper to map all configuration settings."""
    load_initial_speeds()
    load_initial_modes()

# Initial load on script startup
load_initial_profiles()

MAPPING_MODE = 'live'    # Can be 'live' or 'mapping'
running      = True      # Control switch for background thread loop

# --- Controller State ---
last_sent    = {k: 64 for k in AXIS_MAPPING} 
accumulators = {k: 64.0 for k in AXIS_MAPPING} 
btn_state    = {1: -1, 2: -1}
locked_axis  = None
lock_until   = 0

# --- Hotkey Actions ---
def toggle_mapping_mode():
    global MAPPING_MODE
    MAPPING_MODE = 'mapping' if MAPPING_MODE == 'live' else 'live'
    print(f"\n>>> MAPPING MODE : {MAPPING_MODE.upper()} <<<\n")

def toggle_global_latch_override():
    """Flips all individual axis tracking parameters to match a unified toggle selection."""
    global active_modes
    current_latch_count = sum(1 for m in active_modes.values() if m == 'latch')
    target_mode = 'spring' if current_latch_count >= 3 else 'latch'
    
    for k in active_modes:
        active_modes[k] = target_mode
    print(f"\n>>> GLOBAL OVERRIDE ALL AXES TO : {target_mode.upper()} MODE <<<\n")
	
keyboard.add_hotkey(HOTKEY_MAPPING, toggle_mapping_mode)
keyboard.add_hotkey(HOTKEY_LATCH, toggle_global_latch_override)

# --- MIDI Value Processing ---
def calculate_value(key, val): 
    """Returns target MIDI values based on the axis mode and velocity settings."""
    if abs(val) >= DEAD_ZONE:
        if active_modes[key] == 'latch':
            accumulators[key] = max(0, min(127, accumulators[key] + (val * active_sensitivity[key])))
            return int(accumulators[key])
        else:
            return max(0, min(127, int((val + MAX_VAL) / (2 * MAX_VAL) * 127)))
    else:
        return int(accumulators[key]) if active_modes[key] == 'latch' else 64

def send_group(raw_axes):
    global locked_axis, lock_until

    all_at_rest = all(abs(v) < DEAD_ZONE for v in raw_axes.values())

    if all_at_rest:
        locked_axis = None
        for key in raw_axes:
            if active_modes[key] == 'spring':
                if last_sent[key] != 64:
                    last_sent[key] = 64
                    output.send(mido.Message('control_change', channel=MIDI_CHANNEL, control=AXIS_MAPPING[key], value=64))
        return

    now = time.time() * 1000

    if MAPPING_MODE == 'mapping':
        dominant_key, dominant_val = max(raw_axes.items(), key=lambda kv: abs(kv[1]))

        if locked_axis is None or now > lock_until or locked_axis not in raw_axes:
            locked_axis = dominant_key
            lock_until  = now + LOCK_MS

        val = raw_axes[locked_axis]
        cc  = calculate_value(locked_axis, val)
        if cc != last_sent[locked_axis]:
            last_sent[locked_axis] = cc
            output.send(mido.Message('control_change', channel=MIDI_CHANNEL, control=AXIS_MAPPING[locked_axis], value=cc))

    else:
        locked_axis = None
        for key, val in raw_axes.items():
            cc = calculate_value(key, val)
            if cc != last_sent[key]:
                last_sent[key] = cc
                output.send(mido.Message('control_change', channel=MIDI_CHANNEL, control=AXIS_MAPPING[key], value=cc))

# --- Background Hardware Processing Loop ---
def hardware_loop():
    global btn_state, running
    try:
        while running:
            data = device.read(13, timeout=1)
            if data:
                rid = data[0]

                if rid == 1:
                    x, y, z = struct.unpack_from('<3h', bytes(data), 1)
                    send_group({'x': x, 'y': y, 'z': z})

                elif rid == 2:
                    rx, ry, rz = struct.unpack_from('<3h', bytes(data), 1)
                    send_group({'rx': rx, 'ry': ry, 'rz': rz})

                elif rid == 3:
                    b1 = data[1] & 0x01
                    b2 = (data[1] >> 1) & 0x01
                    if b1 != btn_state[1]:
                        btn_state[1] = b1
                        if 1 in BTN_MAPPING:
                            output.send(mido.Message('control_change', channel=MIDI_CHANNEL, control=BTN_MAPPING[1], value=127 if b1 else 0))
                    if b2 != btn_state[2]:
                        btn_state[2] = b2
                        if 2 in BTN_MAPPING:
                            output.send(mido.Message('control_change', channel=MIDI_CHANNEL, control=BTN_MAPPING[2], value=127 if b2 else 0))

            time.sleep(0.001)
    except Exception as e:
        print(f"\nHardware Thread Error: {e}")

def print_status_report():
    """Outputs the complete multi-profile axis status configuration map layout data."""
    print("-" * 52)
    print("             CURRENT PROFILE MAP REPORT")
    print("-" * 52)
    print(f" Mapping Style : {MAPPING_MODE.upper()}")
    print("-" * 52)
    print("  AXIS   |  OPERATIONAL MODE  |  SPEED SENSITIVITY")
    print("-" * 52)
    for k in sorted(active_sensitivity.keys()):
        current_percent = active_sensitivity[k] * 2000.0
        mode_str = active_modes[k].upper()
        axis_str = f"[{k.upper()}]"
        print(f"  {axis_str:<6} |  {mode_str:<16}  |  {current_percent:g}%")
    print("-" * 52)

# --- Automated MIDI Scanning Init ---
available_outputs = mido.get_output_names()
target_port_name = None

for port in available_outputs:
    if "SpaceMIDI" in port:
        target_port_name = port
        break

if target_port_name is None:
    print("Error: Could not find an active loopMIDI port named 'SpaceMIDI'.")
    print(f"Ports detected: {available_outputs}")
    exit()

output = mido.open_output(target_port_name)
print(f"MIDI OK (Auto-locked onto port: '{target_port_name}')")

# --- Hardware Init ---
hid_scan = Enumeration()
found_devices = hid_scan.find(vid=USB_VID, pid=USB_PID)
if not found_devices:
    print(f"Error: No device found matching VID {hex(USB_VID)} and PID {hex(USB_PID)}.")
    exit()

device = found_devices[0]
device.open()
print("SpaceNavigator OK")

# --- Print Dashboard ---
print("=" * 52)
print("  SpaceMIDI Controller Active")
print("=" * 52)
print(f" SpaceNavigator Status : Connected OK")
print(f" MIDI Output Channel   : Channel {MIDI_CHANNEL + 1}")

print_status_report()

print(" ACTIVE CONTROLLER HOTKEYS:")
print(f" [{HOTKEY_MAPPING}]  - Toggle MAPPING mode vs LIVE mode")
print(f" [{HOTKEY_LATCH}] - Global OVERRIDE (Force all to SPRING vs LATCH)")
print("-" * 52)
print(" INTERACTIVE CONSOLE INPUTS:")
print(" * Type a general speed to update all axes (e.g. '15')")
print(" * Type an axis speed profile rewrite (e.g. 'z 25')")
print(" * Type a custom targeted mode rewrite (e.g. 'latch z' or 'spring rx')")
print(" * Type 'status' or 'show' to inspect current parameters")
print(" * Type 'readme' or 'help' to review documentation metrics")
print(" * Type 'reset modes' or 'reset latch' to reload default behaviors")
print(" * Type 'reset speeds' or 'reset speed' to reload default sensitivities")
print(" * Type 'reset' to completely restore all fallback config profiles")
print(" * Type 'quit' to terminate environment application thread")
print("=" * 52 + "\n")

# Start background parser task thread
controller_thread = threading.Thread(target=hardware_loop, daemon=True)
controller_thread.start()

# --- Interactive Terminal Interface ---
try:
    while True:
        user_input = input("SpaceMIDI> ").strip().lower()
        
        if user_input == 'quit':
            break
            
        if user_input == 'reset':
            load_initial_profiles()
            print(">> All modes and sensitivities restored to config baseline! <<\n")
            continue

        if user_input in ('reset modes', 'reset latch'):
            load_initial_modes()
            print(">> Axis operational modes restored to config defaults! <<\n")
            continue

        if user_input in ('reset speeds', 'reset speed', 'reset sensitivity', 'reset sensitivities'):
            load_initial_speeds()
            print(">> Axis sensitivities restored to config defaults! <<\n")
            continue

        if user_input in ('status', 'show'):
            print() 
            print_status_report()
            print()
            continue

        if user_input in ('readme', 'help'):
            print()
            try:
                with open('readme.txt', 'r') as readme_file:
                    full_text = readme_file.read()
                    marker = "1. ACTIVE HARDWARE HOTKEYS"
                    marker_position = full_text.find(marker)
                    
                    if marker_position != -1:
                        manual_content = full_text[marker_position:]
                        print("==========================================================")
                        print("               SPACEMIDI CONTROLLER SURFACE               ")
                        print("==========================================================")
                        print(manual_content)
                    else:
                        print(full_text)
            except FileNotFoundError:
                print("[!] Error: 'readme.txt' file was not found.")
            print()
            continue
            
        if user_input:
            parts = user_input.split()
            
            # Scenario A: User types a single global speed percentage (e.g., "15")
            if len(parts) == 1:
                try:
                    new_percent = float(parts[0])
                    if new_percent <= 0:
                        print("Sensitivity must be greater than 0%!")
                        continue
                    
                    for k in active_sensitivity:
                        active_sensitivity[k] = new_percent / 2000.0
                    print(f">> All axes updated to: {new_percent}% <<\n")
                except ValueError:
                    print("Invalid format. Use a number, 'axis number', 'status', 'reset' or 'quit'.")
            
            # Scenario B: User targets a parameter tuple pair (e.g., "latch z" or "z 25")
            elif len(parts) == 2:
                cmd_param_1 = parts[0]
                cmd_param_2 = parts[1]
                
                # Dynamic Mode Customization Routing
                if cmd_param_1 in ('latch', 'spring'):
                    target_axis = cmd_param_2
                    if target_axis not in active_modes:
                        print(f"Unknown axis: '{target_axis}'. Options: x, y, z, rx, ry, rz")
                        continue
                    active_modes[target_axis] = cmd_param_1
                    print(f">> Axis [{target_axis.upper()}] mode set to: {cmd_param_1.upper()} <<\n")
                
                # Dynamic Axis Velocity Customization Routing
                else:
                    target_axis = cmd_param_1
                    if target_axis not in active_sensitivity:
                        print(f"Unknown command or axis path: '{target_axis}'")
                        continue
                    try:
                        new_percent = float(cmd_param_2)
                        if new_percent <= 0:
                            print("Sensitivity must be greater than 0%!")
                            continue
                        active_sensitivity[target_axis] = new_percent / 2000.0
                        print(f">> Axis [{target_axis.upper()}] speed set to: {new_percent}% <<\n")
                    except ValueError:
                        print("Invalid number formatting.")

except KeyboardInterrupt:
    pass

except Exception as global_error:
    print(f"\nCore System Error: {global_error}")

finally:
    print("\nStopping application and closing connections...")
    running = False
    time.sleep(0.1)
    output.close()
    device.close()
    print("Goodbye.")
