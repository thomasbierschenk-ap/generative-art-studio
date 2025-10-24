# Development Guide

## Project Overview

Generative Art Studio is a modular Python application for creating algorithmic art. The current implementation includes a fully functional Random Walk generator with plans to add three more generation methods.

## Current Status

### ✅ Completed
- Project structure and organization
- Git repository with proper .gitignore
- Base generator framework (extensible architecture)
- Random Walk generator (Method 2) - fully functional
- GUI with dynamic parameter controls
- SVG and PNG export
- Comprehensive documentation
- Command-line generation capability

### 🚧 In Progress
Nothing currently in progress

### 📋 Planned
- Method 1: Mathematical Patterns
- Method 3: System Metrics Visualization
- Method 4: Audio-Reactive Art
- Additional features (see TODO.md)

## Architecture

### Core Components

1. **Base Generator** (`src/generators/base.py`)
   - Abstract base class for all generators
   - Defines common interface
   - Handles SVG/PNG export
   - Parameter validation

2. **Generators** (`src/generators/`)
   - Each generator is a separate module
   - Inherits from `BaseGenerator`
   - Implements `generate()`, `get_name()`, `get_parameters()`

3. **GUI** (`src/gui/`)
   - `MainWindow`: Main application window
   - Dynamic parameter controls based on generator definitions
   - File save dialogs

4. **Application** (`src/app.py`)
   - Coordinates GUI and generators
   - Manages application state
   - Registers available generators

### Data Flow

```
User Input (GUI) → Parameter Collection → Generator.generate() → ArtworkData → Export (SVG/PNG)
```

### ArtworkData Structure

The `ArtworkData` class is format-agnostic and contains:
- Dimensions (width, height)
- Background color
- List of `PathElement` objects (lines, curves)
- List of `CircleElement` objects
- Future: More shape types can be added

## Adding a New Generator

### Step 1: Create Generator Class

Create a new file in `src/generators/` (e.g., `mathematical.py`):

```python
from .base import BaseGenerator, ArtworkData, PathElement
from typing import Dict, Any

class MathematicalGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "Mathematical Patterns"
    
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            'pattern_type': {
                'type': 'choice',
                'default': 'spiral',
                'choices': ['spiral', 'sine_wave', 'lissajous'],
                'label': 'Pattern Type',
                'help': 'Type of mathematical pattern to generate'
            },
            'complexity': {
                'type': 'int',
                'default': 100,
                'min': 10,
                'max': 1000,
                'label': 'Complexity',
                'help': 'Number of points in the pattern'
            },
            # ... more parameters
        }
    
    def generate(self, width: int, height: int, params: Dict[str, Any]) -> ArtworkData:
        params = self.validate_parameters(params)
        artwork = ArtworkData(width=width, height=height)
        
        # Your generation logic here
        # Create PathElement and CircleElement objects
        # Add them to artwork.paths and artwork.circles
        
        return artwork
```

### Step 2: Register Generator

Update `src/generators/__init__.py`:

```python
from .mathematical import MathematicalGenerator

__all__ = ['BaseGenerator', 'ArtworkData', 'RandomWalkGenerator', 'MathematicalGenerator']
```

Update `src/app.py` in `_initialize_generators()`:

```python
def _initialize_generators(self) -> Dict[str, any]:
    generators = {}
    
    random_walk = RandomWalkGenerator()
    generators[random_walk.get_name()] = random_walk
    
    mathematical = MathematicalGenerator()
    generators[mathematical.get_name()] = mathematical
    
    return generators
```

### Step 3: Test

Run the application or use command-line testing:

```python
from generators import MathematicalGenerator

gen = MathematicalGenerator()
params = {param: def_dict['default'] for param, def_dict in gen.get_parameters().items()}
artwork = gen.generate(800, 600, params)
gen.to_svg(artwork, 'test.svg')
```

## Parameter Types

The GUI automatically creates appropriate controls based on parameter type:

### Integer (`'type': 'int'`)
- Creates a slider with value display
- Requires: `min`, `max`, `default`
- Optional: `step`

### Float (`'type': 'float'`)
- Creates a slider with decimal value display
- Requires: `min`, `max`, `default`
- Optional: `step`

### Boolean (`'type': 'bool'`)
- Creates a checkbox
- Requires: `default`

### Choice (`'type': 'choice'`)
- Creates a dropdown/combobox
- Requires: `choices` (list), `default`

### Color (`'type': 'color'`)
- Creates a color picker
- Requires: `default` (hex color string)

## Best Practices

### Code Organization
- Keep generators self-contained
- Use helper methods for complex logic
- Document complex algorithms
- Add type hints

### Performance
- For large numbers of elements, consider optimization
- Test with various parameter ranges
- Profile if generation is slow

### Testing
- Create a test script for each generator
- Test edge cases (min/max values)
- Verify output files are created correctly

### Documentation
- Update README.md with new features
- Add examples to EXAMPLES.md
- Document any new parameters thoroughly

## Common Patterns

### Creating Paths

```python
points = []
for i in range(num_points):
    x = calculate_x(i)
    y = calculate_y(i)
    points.append((x, y))

path = PathElement(
    points=points,
    color=(0, 0, 0),
    width=2.0,
    closed=False
)
artwork.paths.append(path)
```

### Creating Circles

```python
circle = CircleElement(
    center=(x, y),
    radius=10.0,
    color=(255, 0, 0),
    fill=True,
    stroke_width=1.0
)
artwork.circles.append(circle)
```

### Color Utilities

```python
# Hex to RGB
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# HSV to RGB (for rainbow effects)
import colorsys
def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))
```

## Debugging

### Command-Line Testing
The fastest way to test is without the GUI:

```python
python test_generator.py
```

Or create a custom test script.

### GUI Issues
If GUI doesn't work:
1. Check Tkinter version compatibility
2. Test on different Python version
3. Use command-line generation as fallback

### Output Verification
- Open SVG in browser or vector editor
- Check PNG in image viewer
- Verify file sizes are reasonable

## Git Workflow

### Making Changes
```bash
# Create feature branch (optional)
git checkout -b feature/new-generator

# Make changes, test, commit
git add .
git commit -m "Add new generator: [description]"

# Merge back to main
git checkout main
git merge feature/new-generator
```

### Commit Messages
Follow this format:
```
[Component] Brief description

- Detailed change 1
- Detailed change 2
- Detailed change 3
```

Example:
```
Add Mathematical Patterns generator

- Implement spiral pattern generation
- Add sine wave patterns
- Create parameter controls for frequency and amplitude
- Add comprehensive tests
```

## Future Enhancements

### Priority 1: Core Generators
Complete the four planned generation methods.

### Priority 2: User Experience
- Preset system (save/load parameter sets)
- Real-time preview (scaled down)
- Progress indicators for long generations
- Undo/redo for parameters

### Priority 3: Advanced Features
- Animation support (generate sequences)
- Batch generation with parameter sweeps
- Export to additional formats (PDF, EPS)
- Plugin system for community generators

### Priority 4: Polish
- Better error handling
- Input validation improvements
- Tooltips and help system
- Gallery view of generated art

## Resources

### Python Libraries
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [svgwrite Documentation](https://svgwrite.readthedocs.io/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

### Generative Art Inspiration
- [Tyler Hobbs](https://tylerxhobbs.com/) - Flow fields, plotting
- [Inconvergent](https://inconvergent.net/) - Differential growth
- [Matt DesLauriers](https://www.mattdesl.com/) - Creative coding
- [r/generative](https://reddit.com/r/generative) - Community

### Algorithms
- Random walks and Brownian motion
- Perlin/Simplex noise
- L-systems (Lindenmayer systems)
- Cellular automata
- Fractals (Mandelbrot, Julia, IFS)
- Voronoi diagrams
- Delaunay triangulation

## Getting Help

If you're continuing this project in a new session:

1. Read this document first
2. Check TODO.md for current status
3. Review ARCHITECTURE.md for system design
4. Look at EXAMPLES.md for usage patterns
5. Examine existing code in `src/generators/random_walk.py`

## Contact

This is an open-source project. Feel free to:
- Fork and modify
- Submit pull requests
- Share your generated art
- Suggest new features

Happy coding! 🎨
