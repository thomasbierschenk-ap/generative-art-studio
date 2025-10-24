# Installation Guide

## Recommended: Using venv with Public PyPI

If you're on a corporate network (like Square) with SSL/Artifactory issues, use this method:

```bash
cd generative-art-studio

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR on Windows: venv\Scripts\activate

# Install using public PyPI (bypasses corporate Artifactory)
./install_public_pypi.sh

# OR manually:
pip install --index-url https://pypi.org/simple \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# Verify installation
./verify_setup.sh  # On macOS/Linux
# OR: python tests/test_random_walk.py

# Test it works
python test_generator.py
```

## Alternative: Standard Installation (If No Corporate Network Issues)

```bash
cd generative-art-studio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Alternative: Using uv (May Have Issues on Corporate Networks)

If you're on a corporate network (like Square), `uv` may have issues with internal PyPI mirrors. If you want to try:

```bash
cd generative-art-studio

# Try uv sync
uv sync

# If it fails with Artifactory/TLS errors, use venv instead (see above)
```

### Troubleshooting uv on Corporate Networks

If you get errors like:
```
error: Failed to fetch: `https://artifactory.global.square/...`
Caused by: tls handshake eof
```

**Solution 1: Use venv instead (recommended)**
Follow the venv instructions above.

**Solution 2: Configure uv to use public PyPI**
```bash
# Tell uv to use public PyPI instead of corporate mirror
export UV_INDEX_URL=https://pypi.org/simple
uv sync
```

**Solution 3: Use pip in the uv venv**
```bash
uv venv  # Create venv only
source .venv/bin/activate
pip install -r requirements.txt
```

## Verifying Installation

After installation with either method:

```bash
# Run verification script
./verify_setup.sh

# Or manually run tests
python tests/test_random_walk.py

# Or generate test artwork
python test_generator.py
```

You should see:
- ✓ All 6 tests passing
- ✓ Test output files created in `output/`

## What Gets Installed

### Core Dependencies (Required)
- **Pillow** (10.0.0+): Image processing and PNG export
- **svgwrite** (1.4.3+): SVG generation
- **numpy** (1.24.0+): Numerical operations

### Optional Dependencies
- **psutil** (5.9.0+): For Method 3 (System Metrics) - install when needed
- **pyaudio** (0.2.13+): For Method 4 (Audio-Reactive) - install when needed
- **scipy** (1.10.0+): For Method 4 (Audio-Reactive) - install when needed

## Quick Start After Installation

```bash
# Make sure venv is activated
source venv/bin/activate  # if using venv

# Generate test artwork
python test_generator.py

# Check the output
ls -lh output/

# Try the GUI (may not work on all systems)
python src/main.py
```

## Common Issues

### Issue: "command not found: pip"
**Solution:** Use `python3 -m pip` instead:
```bash
python3 -m pip install -r requirements.txt
```

### Issue: "No module named 'PIL'"
**Solution:** Make sure venv is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: GUI doesn't work
**Solution:** Use command-line generation instead:
```bash
python test_generator.py
# or write your own script using the examples in docs/EXAMPLES.md
```

### Issue: Corporate network blocks PyPI
**Solution:** 
1. Use venv + pip (usually works through corporate proxy)
2. Or ask IT for PyPI access
3. Or download wheels manually and install offline

## Next Steps

Once installed:
1. Read `docs/QUICKSTART.md` for usage guide
2. Try examples from `docs/EXAMPLES.md`
3. Explore parameters in the GUI or scripts
4. Start creating art! 🎨
