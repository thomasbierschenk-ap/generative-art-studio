#!/bin/bash
# Install dependencies using public PyPI (bypasses Square Artifactory)

echo "Installing from public PyPI (pypi.org)..."
echo ""

# Check if venv is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    echo "Then run this script again."
    exit 1
fi

echo "✓ Virtual environment detected: $VIRTUAL_ENV"
echo ""

# Install using public PyPI
echo "Installing dependencies..."
pip install --index-url https://pypi.org/simple \
    --trusted-host pypi.org \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Installation successful!"
    echo ""
    echo "Next steps:"
    echo "  1. Run tests: python tests/test_random_walk.py"
    echo "  2. Generate art: python test_generator.py"
    echo "  3. Try GUI: python src/main.py"
else
    echo ""
    echo "✗ Installation failed"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check your internet connection"
    echo "  2. Try running the command manually:"
    echo "     pip install --index-url https://pypi.org/simple -r requirements.txt"
    exit 1
fi
