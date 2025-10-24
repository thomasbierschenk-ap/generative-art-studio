# Generative Art Studio

A Python-based application for creating computer-generated art through various algorithmic methods.

## Overview

Generative Art Studio provides a GUI interface for experimenting with different art generation techniques, including mathematical patterns, random processes, system visualization, and audio-reactive graphics.

## Features

- **Multiple Generation Methods**:
  - Method 1: Mathematical Patterns (sine waves, spirals, fractals)
  - Method 2: Random Walks with controlled parameters
  - Method 3: System Metrics Visualization (CPU, memory, network)
  - Method 4: Audio-Reactive Art (frequency and amplitude driven)

- **Flexible Output**:
  - Vector graphics (SVG)
  - Raster graphics (PNG)
  - Configurable output dimensions
  - Color modes: monochrome, grayscale, full color

- **Interactive GUI**:
  - Real-time parameter adjustment
  - Method selection
  - Preview and export capabilities

## Installation

The project requires Python 3.9+ with the following packages:
- `Pillow` (PIL)
- `svgwrite`
- `numpy`

**If you already have these packages installed globally, you can skip the installation step.**

**Quick Start:**

```bash
cd generative-art-studio

# Test if dependencies are already available
./run_test.sh

# If that works, you're ready to go!
# Otherwise, install dependencies:
python3 -m pip install --user Pillow svgwrite numpy
```

**For detailed installation instructions, troubleshooting, and alternative methods (including venv/uv), see [INSTALL.md](INSTALL.md)**

## Usage

**Run the test generator (no GUI):**
```bash
./run_test.sh
```

**Run the GUI application:**
```bash
./run_gui.sh
```

**Or set PYTHONPATH manually:**
```bash
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
python3 test_generator.py  # For testing
python3 src/main.py        # For GUI
```

### Basic Workflow

1. Select a generation method from the dropdown
2. Configure output size (width x height)
3. Adjust method-specific parameters
4. Click "Generate" to create the artwork
5. Save as SVG or PNG

## Project Structure

```
generative-art-studio/
├── src/
│   ├── main.py                 # Application entry point
│   ├── app.py                  # Main application class
│   ├── generators/             # Generation method modules
│   │   ├── __init__.py
│   │   ├── base.py            # Base generator class
│   │   ├── random_walk.py     # Random walk implementation
│   │   ├── mathematical.py    # Mathematical patterns
│   │   ├── system_viz.py      # System metrics visualization
│   │   └── audio_reactive.py  # Audio-reactive generation
│   └── gui/                    # GUI components
│       ├── __init__.py
│       ├── main_window.py     # Main window layout
│       └── controls.py        # Parameter controls
├── output/                     # Generated artwork output
├── docs/                       # Additional documentation
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Development

### Adding a New Generator

1. Create a new class inheriting from `BaseGenerator` in `src/generators/`
2. Implement the `generate()` method
3. Define parameters in `get_parameters()`
4. Register the generator in `src/app.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document classes and methods with docstrings
- Keep methods focused and modular

## Technical Details

### Dependencies

- **tkinter**: GUI framework (included with Python)
- **Pillow (PIL)**: Image processing and PNG export
- **svgwrite**: SVG generation
- **numpy**: Numerical operations
- **psutil**: System metrics (for Method 3)
- **pyaudio**: Audio capture (for Method 4)
- **scipy**: Signal processing (for Method 4)

### Architecture

The application follows a modular architecture:

- **App Layer**: Manages application state and coordinates components
- **GUI Layer**: Handles user interface and interactions
- **Generator Layer**: Implements art generation algorithms
- **Export Layer**: Handles output to various formats

## Future Enhancements

- Animation and sequence generation
- Preset saving/loading
- Batch generation
- Additional export formats (PDF, EPS)
- Plugin system for custom generators
- Gallery view of generated works

## License

MIT License (or your preferred license)

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## Credits

Created as an exploration of generative art and algorithmic creativity.
