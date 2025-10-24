#!/bin/bash
# Verification script to test the setup

echo "=========================================="
echo "Generative Art Studio - Setup Verification"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "   ✗ Python 3 not found"
    exit 1
fi
echo "   ✓ Python 3 found"
echo ""

# Check if in project directory
if [ ! -f "pyproject.toml" ]; then
    echo "   ✗ Not in project directory"
    exit 1
fi

# Check for venv
echo "2. Checking for virtual environment..."
if [ -d "venv" ]; then
    echo "   ✓ venv directory exists"
    if [ -f "venv/bin/activate" ]; then
        echo "   ✓ venv is properly set up"
    else
        echo "   ✗ venv exists but not properly configured"
    fi
else
    echo "   ℹ No venv found (this is OK, you can create one)"
fi
echo ""

# Check if dependencies are installed
echo "3. Checking dependencies..."
python3 -c "import PIL" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ Pillow installed"
else
    echo "   ✗ Pillow not installed (run: pip install -r requirements.txt)"
fi

python3 -c "import svgwrite" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ svgwrite installed"
else
    echo "   ✗ svgwrite not installed (run: pip install -r requirements.txt)"
fi

python3 -c "import numpy" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ numpy installed"
else
    echo "   ✗ numpy not installed (run: pip install -r requirements.txt)"
fi
echo ""

# Run tests
echo "4. Running test suite..."
python3 tests/test_random_walk.py
if [ $? -eq 0 ]; then
    echo ""
    echo "   ✓ All tests passed!"
else
    echo ""
    echo "   ✗ Some tests failed"
    exit 1
fi
echo ""

# Check output directory
echo "5. Checking output directory..."
if [ -d "output" ]; then
    echo "   ✓ Output directory exists"
    file_count=$(ls -1 output/*.svg output/*.png 2>/dev/null | wc -l)
    if [ $file_count -gt 0 ]; then
        echo "   ✓ Found $file_count output files"
    else
        echo "   ℹ No output files yet (run test_generator.py to create some)"
    fi
else
    echo "   ✗ Output directory missing"
fi
echo ""

echo "=========================================="
echo "✓ Setup verification complete!"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  1. Create venv: python3 -m venv venv"
echo "  2. Activate:    source venv/bin/activate"
echo "  3. Install:     pip install -r requirements.txt"
echo "  4. Test:        python test_generator.py"
echo "  5. Run GUI:     python src/main.py"
echo ""
