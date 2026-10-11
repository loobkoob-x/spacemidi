# Changelog

All notable changes to SpaceMIDI will be documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0-fork-1.0] - 2026-10-10

### Added
- **Interactive live terminal**: Added console commands to view values and adjust parameters on the fly.
- **Multi-threaded architecture**: Separated HID hardware polling loop into a background thread to keep the console interactive.
- **2 different control response behaviours**: `spring` and `latch`. Spring was the original behaviour; latch increments over time as a parameter is adjusted and holds its position when released.
- **Independent per-axis sensitivity and response behaviours**: Default sensitivity percentages and control response behaviours can be set in `config.json`, or they can be adjusted in the console.
- **Automatic MIDI port mapping**: Integrated `mido` dynamic port lookup to automatically scan and lock onto the virtual "SpaceMIDI" name.
- **Launcher batch file**: Checks for dependencies, downloads them if missing, creates venv if necessary. If everything is already set up, opens loopMIDI (if necessary) then runs `spacemidi.py`.

### Changed
- **Optimized polling rate**: increased polling frequency to 1000Hz (1ms) for reduced latency and more responsive tracking.
- Refactored code.

### Removed
- requirements.txt: this is now handled by the batch file
- config.example.json
- list_ports.py: automatic port mapping is handled by spacemidi.py

---

## [1.0.0] - 2026-05-15

### Added
- 6-axis MIDI CC output from 3Dconnexion SpaceNavigator NB USB
- 2-button MIDI CC output
- Dead zone filtering
- Axis lock in mapping mode (prevents axis bleed)
- Live mode: all axes simultaneously
- Mapping mode: single dominant axis
- F9 hotkey to toggle between modes (configurable)
- External JSON configuration file
- `list_ports.py` utility to identify MIDI output port IDs
