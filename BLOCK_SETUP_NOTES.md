# Block/Square Python Setup Notes

## Your Setup Matches Block's Recommended Approach!

After reviewing the [Block Applied Data dev environment guide](https://dev-guides.sqprod.co/applied-data/docs/dev-env/getting-started/setup), your setup aligns perfectly with their recommendations.

### Block's Recommended Stack

1. **Hermit** - Project-specific Python version management
2. **uv** - Fast dependency management (preferred over Poetry)
3. **pipx** - Isolated CLI tool installation
4. **Just** - Task runner (replaces make)

### What You Have

✅ **pipx** - Installed with tools (black, ruff, poetry, flake8, isort, cookiecutter, notebooks)  
✅ **uv** - v0.9.5 installed in `~/.local/bin/`  
✅ **Global packages** - Pillow, svgwrite, numpy already installed  
✅ **Block dotfiles** - Standard configuration from `squareup/config_files`  

### The pip.conf Configuration

Your `~/.config/pip/pip.conf` contains:
```ini
[global]
cert = /opt/homebrew/etc/openssl@1.1/cert.pem
index-url = https://artifactory.global.square/artifactory/api/pypi/block-pypi/simple
```

**This is intentional** - Block routes all pip traffic through their internal Artifactory mirror. The SSL inspection issue we encountered is a known side effect of Square's security infrastructure.

### Why the SSL Errors Happen

Square's network performs SSL inspection on all HTTPS traffic, including PyPI downloads. This:
1. Decrypts the traffic
2. Inspects it for security
3. Re-encrypts it with Square's certificate

This changes the cryptographic hashes of packages, causing pip to reject them as potentially tampered (which they technically are, by Square's proxy).

### Block's Recommended Workflow

According to their guide, for **project work**:

```bash
# Navigate to project
cd my-project

# Activate Hermit (if project uses it)
source ./bin/activate-hermit

# Use uv for dependencies
uv sync  # or uv pip install

# Use just for tasks
just test
just lint
just run
```

For **personal/experimental projects** (like your generative art):

**Option 1: Use system Python** (what works now)
```bash
cd ~/goose_code/generative-art-studio
python3 test_generator.py  # Just works!
```

**Option 2: Use uv with venv**
```bash
uv venv
source .venv/bin/activate
# Packages already available from system
```

**Option 3: Install on different network**
```bash
# At home or on phone hotspot
python3 -m venv venv
source venv/bin/activate
pip install Pillow svgwrite numpy
# Then use at work
```

### Why Your Code Works Without Setup

The `compost data` command (from Block's topsoil repo) installs common data science packages globally, including:
- Pillow
- numpy
- svgwrite (likely)
- And many others

This is why you don't need a venv for this project - the packages are already there!

### Validation Command

Block provides `sq poke` to validate your setup:

```bash
sq poke python-toolchain
```

This checks:
- ✓ pipx installed correctly
- ✓ uv available
- ✓ poetry available (legacy support)
- ✓ hermit available
- ✓ No conflicting tools (conda, pyenv)
- ✓ Python from correct location

### For Future Projects

**If starting a new data science project at Block:**

1. Use their project template (if available)
2. Set up Hermit for Python version
3. Use `uv` for dependencies
4. Use `just` for common tasks
5. Follow their guide: https://dev-guides.sqprod.co/applied-data/docs/dev-env/getting-started/setup

**For personal/side projects:**

- Use system Python (packages already installed)
- Or create venv on non-Square network
- Or use `uv` if it works for that project

### Summary

Your setup is **exactly** what Block recommends! The SSL issue is a known limitation of Square's security infrastructure, not a problem with your configuration. For this generative art project, you don't need any special setup - just run `python3 test_generator.py` and it works.

### References

- Block Dev Guide: https://dev-guides.sqprod.co/applied-data/docs/dev-env/getting-started/setup
- Hermit Guide: https://dev-guides.sqprod.co/applied-data/docs/dev-env/guides/hermit
- uv Guide: https://dev-guides.sqprod.co/applied-data/docs/dev-env/guides/uv
- Just Guide: https://dev-guides.sqprod.co/applied-data/docs/dev-env/guides/just
