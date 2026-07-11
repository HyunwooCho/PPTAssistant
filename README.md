# PPT Assistant

PowerPoint cleanup and style utility for Windows.

**Author:** tenace  
**Version:** 3.0.0

## Current features

- PPTX drag-and-drop GUI
- Remove proofing metadata and red-underlining markers
- Set Korean proofing language
- Normalize fonts
- Remove speaker notes
- Process multiple files
- Style profile framework with built-in ETRI profile placeholder
- Processing log and progress indicator

## Development setup (Windows / VS Code)

```powershell
cd C:\project\PPTAssistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
python -m pptassistant
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Build EXE

Run:

```text
build_exe_on_windows.bat
```

Output:

```text
dist\PPTAssistant.exe
```

The EXE is built with `--onefile`; other users normally need only the EXE.

## Tests

```powershell
pytest
```

## Repository layout

```text
src/pptassistant/gui       GUI
src/pptassistant/engine    PPTX processing engines
src/pptassistant/profiles  company style profiles
src/pptassistant/resources icons and bundled assets
tests                      automated tests
```
