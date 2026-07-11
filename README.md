# PPT Assistant

PowerPoint cleanup, formatting, and company-style automation utility for Windows.

**Author:** tenace
**Current development version:** 3.0.0-alpha
**Supported Python:** 3.12+

---

## Project Overview

PPT Assistant automates repetitive PowerPoint editing tasks, including:

* cleaning text copied from ChatGPT
* removing proofing metadata and red-underlining markers
* applying company presentation styles
* normalizing fonts and language settings
* formatting tables
* optimizing images and backgrounds
* processing multiple PowerPoint files
* exporting presentation-ready output

The project is designed to work primarily by modifying the internal XML structure of `.pptx` files, without depending on Microsoft PowerPoint COM automation whenever possible.

---

## Current Features

* PPTX file selection and drag-and-drop GUI
* Multiple-file batch processing
* Remove proofing metadata
* Remove red-underlining markers
* Set Korean proofing language
* Normalize fonts
* Remove speaker notes
* Processing log
* Progress indicator
* Built-in ETRI style profile framework
* Custom style profile framework
* Modular processing-engine structure

---

## Planned Features

* ETRI style extraction and application
* Custom template style extraction
* Theme and master background extraction
* Background image optimization
* Modern default table style
* Table style extraction and application
* Image compression
* Unused slide-master cleanup
* PDF export
* Plugin system
* AI slide reviewer

---

## Development Environment

| Item                  | Requirement              |
| --------------------- | ------------------------ |
| Operating system      | Windows 10 or Windows 11 |
| Python                | 3.12 or later            |
| IDE                   | Visual Studio Code       |
| GUI framework         | PySide6                  |
| PowerPoint processing | python-pptx, lxml        |
| Image processing      | Pillow                   |
| Testing               | pytest                   |
| Formatting            | Black                    |
| Linting               | Ruff                     |
| Packaging             | PyInstaller              |

---

## Development Setup

Open the project folder in Visual Studio Code.

```cmd
cd C:\Projects\PPTAssistant
```

Create a virtual environment.

```cmd
python -m venv .venv
```

Activate the virtual environment in Command Prompt.

```cmd
.venv\Scripts\activate.bat
```

The terminal prompt should change to:

```text
(.venv) C:\Projects\PPTAssistant>
```

Upgrade pip.

```cmd
python -m pip install --upgrade pip
```

Install the project and development dependencies.

```cmd
pip install -e ".[dev]"
```

Run PPT Assistant.

```cmd
python -m pptassistant
```

---

## Visual Studio Code Setup

The project uses the `.vscode` directory for a consistent development environment.

```text
.vscode/
├── settings.json
├── launch.json
├── tasks.json
└── extensions.json
```

### Run with F5

After selecting the `.venv` Python interpreter, press:

```text
F5
```

This runs:

```cmd
python -m pptassistant
```

### Select the Python Interpreter

In Visual Studio Code:

```text
Ctrl + Shift + P
```

Select:

```text
Python: Select Interpreter
```

Then choose:

```text
.venv\Scripts\python.exe
```

---

## Build EXE

The target build output is a standalone Windows executable.

```text
dist\PPTAssistant.exe
```

The final build process will use:

```cmd
python build_release.py
```

The release script will be responsible for:

* validating the Python environment
* installing build dependencies
* running tests
* running Ruff
* running Black checks
* running PyInstaller
* creating the standalone executable
* creating a release package

Until `build_release.py` is finalized, development should be performed with:

```cmd
python -m pptassistant
```

---

## Tests

Run all tests:

```cmd
pytest
```

Run tests with verbose output:

```cmd
pytest -v
```

Run a specific test file:

```cmd
pytest tests\test_proofing.py
```

---

## Code Quality

Run Ruff:

```cmd
ruff check .
```

Automatically fix supported Ruff issues:

```cmd
ruff check . --fix
```

Run Black:

```cmd
black .
```

Check formatting without modifying files:

```cmd
black --check .
```

---

## Repository Layout

```text
PPTAssistant/
├── .vscode/
│   ├── extensions.json
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── DEVELOPMENT.md
│   └── ROADMAP.md
│
├── src/
│   └── pptassistant/
│       ├── gui/
│       ├── engine/
│       │   ├── cleanup/
│       │   ├── proofing/
│       │   ├── style/
│       │   ├── table/
│       │   └── optimizer/
│       ├── profiles/
│       ├── resources/
│       ├── main.py
│       └── __main__.py
│
├── tests/
├── build_release.py
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── LICENSE
```

---

# Development Principles

1. Never overwrite the original PowerPoint file.
2. Always create a separate output file.
3. Preserve user content whenever possible.
4. Prefer PPTX XML processing over PowerPoint COM automation.
5. Avoid requiring Microsoft Office for core processing.
6. Make processing features reusable from both GUI and CLI.
7. Keep modules independently testable.
8. Log all major processing operations.
9. Fail safely when unsupported PowerPoint structures are encountered.
10. Keep company style profiles separate from processing logic.

---

# Coding Convention

## Python

The project follows these Python coding rules:

* Python 3.12+
* UTF-8 source encoding
* Type hints required for public functions and methods
* Docstrings required for public modules, classes, functions, and methods
* Black formatting
* Ruff linting
* Small and independently testable modules
* Explicit exception handling
* `pathlib.Path` preferred over raw path strings
* Dataclasses preferred for structured configuration data

Example:

```python
from pathlib import Path

from pptassistant.profiles.models import StyleProfile


def extract_style(template: Path) -> StyleProfile:
    """Extract a reusable style profile from a PowerPoint template."""
```

---

# Git Convention

Commit messages follow a simplified Conventional Commits format.

```text
feat: Add style extractor

fix: Remove proofing metadata from grouped shapes

refactor: Improve PPTX XML parser

docs: Update README

test: Add proofing-engine tests

style: Apply Black formatting

chore: Update dependencies

build: Add PyInstaller release script

ci: Add GitHub Actions workflow
```

## Commit Types

| Type       | Purpose                        |
| ---------- | ------------------------------ |
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `refactor` | Internal code restructuring    |
| `docs`     | Documentation changes          |
| `test`     | Test additions or changes      |
| `style`    | Formatting-only changes        |
| `chore`    | Maintenance work               |
| `build`    | Build-system changes           |
| `ci`       | Continuous-integration changes |

---

# Branch Strategy

Primary branches:

```text
main
develop
```

Feature branches:

```text
feature/style-engine
feature/table-engine
feature/theme-extractor
feature/image-optimizer
feature/pdf-export
```

Bug-fix branches:

```text
bugfix/proofing
bugfix/gui
bugfix/template-parser
```

Release branches:

```text
release/v3.0
release/v3.1
```

## Branch Roles

* `main`: stable and releasable versions
* `develop`: integration branch for ongoing development
* `feature/*`: new features
* `bugfix/*`: bug fixes
* `release/*`: release preparation

---

# GitHub Project

The project uses a Kanban-style GitHub Project board.

```text
To Do
Doing
Review
Done
```

Suggested initial issues:

```text
ChatGPT Cleanup
Remove Proofing
ETRI Style
Theme Extractor
Table Engine
Image Optimizer
PDF Export
Plugin System
AI Slide Reviewer
```

Each feature should be tracked through a GitHub Issue before implementation.

Example issue titles:

```text
feat: Implement ETRI style extractor
```

```text
fix: Proofing metadata remains in table cells
```

```text
feat: Add modern fallback table style
```

---

# Roadmap

## v3.0-alpha

* [x] Project structure
* [x] PySide6 GUI foundation
* [x] Multiple-file processing foundation
* [x] Proofing cleanup engine
* [x] Korean proofing-language support
* [x] Notes-removal support
* [ ] ETRI style extraction
* [ ] ETRI style application
* [ ] Template style-summary panel
* [ ] Stable executable build

## v3.1

* [ ] Theme extractor
* [ ] Master background extractor
* [ ] Background image optimizer
* [ ] Table style extractor
* [ ] Modern fallback table style
* [ ] Font normalization improvements

## v3.2

* [ ] Image optimizer
* [ ] Unused master cleanup
* [ ] PDF export
* [ ] CLI interface
* [ ] Style-profile manager

## v4.0

* [ ] Plugin system
* [ ] AI slide reviewer
* [ ] Presentation-quality report
* [ ] 3GPP document formatter
* [ ] Citation checker

---

# License

MIT License
