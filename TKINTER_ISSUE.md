# Tkinter Compatibility Issue

## Problem

The GUI application (`run_gui.sh` / `src/main.py`) crashes on macOS Sequoia (26.0.1) with the following error:

```
Tcl_Panic: TkpInit
macOS 26 (2600) or later required, have instead 16 (1600)
```

## Root Cause

Your system has Tk framework version 8.5.9, which is incompatible with macOS Sequoia. The crash occurs when Tkinter tries to initialize the Tk framework:

```
Thread 0 Crashed:
3   Tcl    0x23768c068 Tcl_PanicVA + 232
4   Tcl    0x23768c088 Tcl_Panic + 32
5   Tk     0x237987730 TkpInit + 452
```

## Why This Happens

- macOS Sequoia (26.x) requires Tk 8.6 or later
- Your system's Python 3.9.6 (at `/Library/Developer/CommandLineTools/...`) includes Tk 8.5.9
- Tk 8.5.9 was released before macOS Sequoia existed and doesn't support it

## Solution: Use the Command-Line Interface

We've created an **interactive command-line interface** that provides all the functionality of the GUI without requiring Tkinter:

```bash
./create_art.sh
```

This interface:
- ✅ Works on your system (no Tkinter required)
- ✅ Guides you through all parameters interactively
- ✅ Generates both SVG and PNG output
- ✅ Supports all the same features as the GUI

## Alternative Solutions (If You Need the GUI)

### Option 1: Install Python from python.org

Download and install Python 3.11+ from <https://www.python.org/downloads/>. This version includes Tk 8.6.

```bash
# After installation, update the shebang in run_gui.sh to use the new Python
# Or run directly:
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 src/main.py
```

### Option 2: Install Python via Homebrew

```bash
brew install python-tk@3.11
# Then use:
/opt/homebrew/bin/python3.11 src/main.py
```

### Option 3: Use pyenv with tkinter

```bash
brew install tcl-tk
brew install pyenv

# Set environment variables for tcl-tk
export PATH="/opt/homebrew/opt/tcl-tk/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/tcl-tk/lib"
export CPPFLAGS="-I/opt/homebrew/opt/tcl-tk/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk/lib/pkgconfig"

# Install Python with tkinter support
pyenv install 3.11.6
pyenv local 3.11.6

# Verify tkinter works
python -m tkinter
```

## Recommendation

**For now, use the command-line interface** (`./create_art.sh`). It's:
- Immediately available
- Fully functional
- Actually quite pleasant to use!

The GUI can be added later if needed, but the CLI provides everything you need to create generative art.

## Files Affected

- **Working**: `create_art.sh`, `generate_art.py`, `run_test.sh`, `test_generator.py`
- **Not Working**: `run_gui.sh`, `src/main.py`, `src/gui/*`

## Testing

To verify the CLI works:

```bash
# Interactive mode
./create_art.sh

# Quick test
./run_test.sh

# Check output
ls -lh output/
```

## References

- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Tk/Tcl on macOS](https://www.tcl.tk/software/mac/)
- [Python.org Downloads](https://www.python.org/downloads/)
