from easyhid import Enumeration
import pygame.midi
import struct
import time
import keyboard
import json


# --- Config ---
with open('config.json', 'r') as f:
    cfg = json.load(f)

MIDI_OUTPUT_ID = cfg['midi_output_id']
MIDI_CHANNEL   = cfg['midi_channel']
MAX_VAL        = cfg['max_val']
DEAD_ZONE      = cfg['dead_zone']
LOCK_MS        = cfg['lock_ms']
AXIS_MAPPING   = cfg['axis_mapping']
BTN_MAPPING    = {int(k): v for k, v in cfg['btn_mapping'].items()}
HOTKEY         = cfg['hotkey_toggle_mode']

MODE = 'live'  # 'live' ou 'mapping'


AXIS_MAPPING = {
    'x':  1,
    'y':  7,
    'z':  74,
    'rx': 10,
    'ry': 71,
    'rz': 91,
}
BTN_MAPPING = {1: 80, 2: 81}

# --- État ---
last_sent  = {k: -1 for k in AXIS_MAPPING}
btn_state  = {1: -1, 2: -1}

def toggle_mode():
    global MODE
    MODE = 'mapping' if MODE == 'live' else 'live'
    print(f"\n>>> MODE : {MODE.upper()} <<<\n")

keyboard.add_hotkey(HOTKEY, toggle_mode)

def scale(value):
    return max(0, min(127, int((value + MAX_VAL) / (2 * MAX_VAL) * 127)))

# --- État ---
last_sent    = {k: -1 for k in AXIS_MAPPING}
btn_state    = {1: -1, 2: -1}
locked_axis  = None
lock_until   = 0


def send_group(raw_axes):
    global locked_axis, lock_until

    all_at_rest = all(abs(v) < DEAD_ZONE for v in raw_axes.values())

    if all_at_rest:
        locked_axis = None
        for key in raw_axes:
            if last_sent[key] != 64:
                last_sent[key] = 64
                output.write_short(0xB0 | MIDI_CHANNEL, AXIS_MAPPING[key], 64)
        return

    now = time.time() * 1000

    if MODE == 'mapping':
        dominant_key, dominant_val = max(raw_axes.items(), key=lambda kv: abs(kv[1]))

        # Nouveau dominant ou verrou expiré ou axe pas dans ce groupe → on verrouille
        if locked_axis is None or now > lock_until or locked_axis not in raw_axes:
            locked_axis = dominant_key
            lock_until  = now + LOCK_MS

        # N'envoie que l'axe verrouillé
        val = raw_axes[locked_axis]
        cc  = scale(val) if abs(val) >= DEAD_ZONE else 64
        if cc != last_sent[locked_axis]:
            last_sent[locked_axis] = cc
            output.write_short(0xB0 | MIDI_CHANNEL, AXIS_MAPPING[locked_axis], cc)

    else:
        locked_axis = None
        for key, val in raw_axes.items():
            cc = scale(val) if abs(val) >= DEAD_ZONE else 64
            if cc != last_sent[key]:
                last_sent[key] = cc
                output.write_short(0xB0 | MIDI_CHANNEL, AXIS_MAPPING[key], cc)

# --- Init ---
pygame.midi.init()
output = pygame.midi.Output(MIDI_OUTPUT_ID)
print("MIDI OK")

e = Enumeration()
device = e.find(vid=0x046d, pid=0xc628)[0]
device.open()
print("SpaceNavigator OK")
print("En écoute... (Ctrl+C pour quitter)\n")

try:
    while True:
        data = device.read(13, timeout=100)
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
                    output.write_short(0xB0 | MIDI_CHANNEL, BTN_MAPPING[1], 127 if b1 else 0)
                if b2 != btn_state[2]:
                    btn_state[2] = b2
                    output.write_short(0xB0 | MIDI_CHANNEL, BTN_MAPPING[2], 127 if b2 else 0)

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nArrêt.")

finally:
    output.close()
    pygame.midi.quit()
    device.close()