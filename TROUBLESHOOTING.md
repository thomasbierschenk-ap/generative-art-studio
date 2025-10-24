# Troubleshooting Guide

## Common Issues and Solutions

### "ModuleNotFoundError: No module named 'svgwrite'" (or Pillow/numpy)

**Problem:** Python can't find the installed packages even though they're installed globally.

**Root Cause:** The project uses a `src/` directory structure, and the way Python's module resolution works, it needs to know to look in `src/` for local modules while still finding system packages.

**Solution:** Use the provided wrapper scripts that set `PYTHONPATH` correctly:

```bash
# For testing (no GUI)
./run_test.sh

# For GUI
./run_gui.sh
```

**Alternative:** Set `PYTHONPATH` manually before running:

```bash
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
python3 test_generator.py
python3 src/main.py
```

**Why This Happens:**

When `test_generator.py` does `sys.path.insert(0, 'src')`, it changes the import resolution order. The `PYTHONPATH` environment variable approach is cleaner because it:
1. Adds `src/` to the path for local modules
2. Preserves the normal Python path for system packages
3. Works consistently across different execution contexts

### Tkinter Version Issues

**Problem:** GUI fails to start with error about Tkinter version mismatch.

**Solution:** Use the command-line test script instead:

```bash
./run_test.sh
```

This generates artwork without requiring the GUI and is useful for:
- Testing the core generation logic
- Batch generation
- Automated workflows
- Systems where GUI isn't available

### Virtual Environment vs Global Packages

**When to Use a Virtual Environment:**

- You want isolated dependencies per project
- You're developing multiple Python projects
- You need specific package versions

**When Global Packages Are Fine:**

- You have the required packages already installed
- You're not concerned about version conflicts
- You want simpler project setup

**For This Project:**

If you have `Pillow`, `svgwrite`, and `numpy` installed globally, you don't need a virtual environment. Just use the wrapper scripts!

### Installation Issues on Square/Block Network

**Problem:** `pip install` or `uv sync` fails with SSL errors or hash mismatches.

**Root Cause:** Square's corporate network uses SSL inspection which modifies packages in transit, breaking hash verification.

**Solutions:**

1. **Use globally installed packages** (if you have them):
   ```bash
   python3 -c "import PIL, svgwrite, numpy; print('All dependencies available!')"
   ```

2. **Install to user site-packages** (may work):
   ```bash
   python3 -m pip install --user Pillow svgwrite numpy
   ```

3. **Use Hermit** (Block's recommended tool manager):
   See [BLOCK_SETUP_NOTES.md](BLOCK_SETUP_NOTES.md) for details

4. **Contact IT** for help with package installation on the corporate network

### Checking What's Installed

**Check if packages are available:**

```bash
python3 -c "import PIL; print('Pillow:', PIL.__version__)"
python3 -c "import svgwrite; print('svgwrite:', svgwrite.__version__)"
python3 -c "import numpy; print('numpy:', numpy.__version__)"
```

**List all installed packages:**

```bash
python3 -m pip list
```

**Check Python version:**

```bash
python3 --version
```

### Output Files Not Generated

**Problem:** Script runs but no files appear in `output/` directory.

**Check:**

1. Does the `output/` directory exist?
   ```bash
   ls -la output/
   ```

2. Are there any error messages in the console output?

3. Try with explicit paths:
   ```bash
   python3 test_generator.py
   ls -la output/test_output.*
   ```

### Permission Errors

**Problem:** Can't write to output directory or can't execute scripts.

**Solutions:**

```bash
# Make scripts executable
chmod +x run_test.sh run_gui.sh

# Check output directory permissions
ls -ld output/

# Create output directory if missing
mkdir -p output
```

## Getting Help

If you encounter issues not covered here:

1. Check the [README.md](README.md) for basic usage
2. Review [ARCHITECTURE.md](docs/ARCHITECTURE.md) for technical details
3. Look at [BLOCK_SETUP_NOTES.md](BLOCK_SETUP_NOTES.md) for Block-specific environment info
4. Check the Git history for recent changes: `git log --oneline`

## Reporting Issues

When reporting issues, please include:

- Python version: `python3 --version`
- Operating system
- Full error message and stack trace
- What you were trying to do
- Output of: `python3 -m pip list | grep -E "(Pillow|svgwrite|numpy)"`
