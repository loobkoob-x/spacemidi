# SpaceMIDI 🎛️

Control Ableton Live (or any DAW) with a **3Dconnexion SpaceNavigator** using all 6 axes and 2 buttons as MIDI CC messages.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What it does

The SpaceNavigator is a 6-DOF input device (push, pull, tilt, rotate in every direction). SpaceMIDI bridges it to MIDI, letting you use it as an expressive controller in your DAW.

Each physical axis maps to a MIDI CC:

| Axis | Direction | Default CC |
|------|-----------|-----------|
| X | Left / Right | CC 1 |
| Y | Forward / Backward | CC 7 |
| Z | Up / Down | CC 74 |
| RX | Tilt left / right | CC 10 |
| RY | Tilt forward / backward | CC 71 |
| RZ | Rotate | CC 91 |
| Button 1 | Press | CC 80 |
| Button 2 | Press | CC 81 |

All mappings are fully configurable in `config.json`.

---

## Requirements

### Hardware
- 3Dconnexion SpaceNavigator (tested on SpaceNavigator NB USB, model 3DX-600036)

### Software
- Windows 10 or 11
- Python 3.11 or 3.13
- [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) — creates a virtual MIDI port

> ⚠️ The official **3DxWare** driver from 3Dconnexion may conflict with SpaceMIDI. If the device is not detected, try uninstalling it.

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/spacemidi.git
cd spacemidi
```

**2. Create a virtual environment**
```bash
py -3.13 -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Install hidapi.dll**

Download the latest Windows release from [hidapi releases](https://github.com/libusb/hidapi/releases), extract `x64/hidapi.dll` and place it in `venv\Scripts\`.

**5. Create a virtual MIDI port**

Open loopMIDI, click **+** and name the port `SpaceMIDI`.

**6. Configure**
```bash
cp config.example.json config.json
```
Edit `config.json` if needed (see [Configuration](#configuration)).

---

## Usage

**1. Activate the virtual environment**
```bash
venv\Scripts\activate
```

**2. Run SpaceMIDI**
```bash
python spacemidi.py
```

**3. Configure Ableton**

In Ableton: *Preferences → MIDI* → enable **Track** and **Remote** for the `SpaceMIDI` input port.

**4. Map axes to parameters**

- Press **F9** to switch to **MAPPING mode** (one axis at a time)
- In Ableton, press **Ctrl+M** to enter MIDI Map mode
- Click a parameter, then move one axis on the SpaceNavigator
- Press **F9** again to switch back to **LIVE mode** (all axes simultaneously)

---

## Configuration

All settings live in `config.json`:

```json
{
    "midi_output_id": 5,
    "midi_channel": 0,
    "max_val": 500,
    "dead_zone": 20,
    "lock_ms": 400,
    "axis_mapping": {
        "x":  1,
        "y":  7,
        "z":  74,
        "rx": 10,
        "ry": 71,
        "rz": 91
    },
    "btn_mapping": {
        "1": 80,
        "2": 81
    },
    "hotkey_toggle_mode": "F9"
}
```

| Key | Description |
|-----|-------------|
| `midi_output_id` | ID of the loopMIDI output port (run `python list_ports.py` to find it) |
| `midi_channel` | MIDI channel (0 = channel 1) |
| `max_val` | Expected maximum axis value — adjust for sensitivity |
| `dead_zone` | Ignore axis values below this threshold |
| `lock_ms` | How long (ms) to lock onto one axis in mapping mode |
| `axis_mapping` | Axis → CC number |
| `btn_mapping` | Button → CC number |
| `hotkey_toggle_mode` | Keyboard shortcut to toggle mapping/live mode |

---

## Utilities

List available MIDI output ports:
```bash
python list_ports.py
```

---

## Troubleshooting

**Device not found**
- Make sure the SpaceNavigator is plugged in
- Uninstall 3DxWare if installed
- Check that `hidapi.dll` is in `venv\Scripts\`

**No MIDI in Ableton**
- Check that loopMIDI is running and the `SpaceMIDI` port exists
- Verify Track + Remote are enabled in Ableton MIDI preferences
- Confirm `midi_output_id` in `config.json` matches your loopMIDI port

**Axes oscillate during mapping**
- Make sure you are in **MAPPING mode** (press F9)
- Increase `lock_ms` in `config.json` (e.g. 600)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](LICENSE).
