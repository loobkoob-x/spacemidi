# Contributing to SpaceMIDI

Thank you for your interest in contributing! Here's how to help.

---

## Ways to contribute

- **Report a bug** — open an Issue with as much detail as possible
- **Suggest a feature** — open an Issue tagged `enhancement`
- **Submit a fix or feature** — open a Pull Request
- **Improve documentation** — typos, clarity, translations

---

## Reporting a bug

Please include:
- Your OS and Python version
- Your 3Dconnexion device model
- The full error traceback
- Steps to reproduce

---

## Development setup

```bash
git clone https://github.com/yourusername/spacemidi.git
cd spacemidi
py -3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Submitting a Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test on a real device if possible
5. Commit with a clear message: `git commit -m "Add: support for SpaceMouse Pro"`
6. Push and open a PR against `main`

### Commit message conventions

| Prefix | Use for |
|--------|---------|
| `Add:` | New feature |
| `Fix:` | Bug fix |
| `Doc:` | Documentation only |
| `Refactor:` | Code change without behaviour change |
| `Config:` | Config file or defaults |

---

## Scope

SpaceMIDI is intentionally simple and focused. Before building a large feature, open an Issue first to discuss whether it fits the project.

Ideas that are welcome:
- Support for more 3Dconnexion models
- macOS / Linux support
- Additional MIDI message types (Note On/Off, Pitch Bend)
- GUI for configuration

---

## Code style

- Follow existing code conventions
- Keep functions small and commented
- No external dependencies beyond those in `requirements.txt` unless discussed first
