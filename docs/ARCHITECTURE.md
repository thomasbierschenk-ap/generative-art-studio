# Architecture Documentation

## System Overview

Generative Art Studio is built with a modular, extensible architecture that separates concerns between UI, generation logic, and output handling.

## Core Components

### 1. Application Core (`app.py`)

The main application class that:
- Initializes the GUI
- Manages generator instances
- Coordinates between UI and generators
- Handles output operations

### 2. GUI Layer (`gui/`)

**Main Window** (`main_window.py`):
- Layout management
- Canvas for preview/display
- Method selector
- Output configuration

**Controls** (`controls.py`):
- Dynamic parameter controls based on selected generator
- Output size inputs
- Color mode selection
- Generate and save buttons

### 3. Generator Layer (`generators/`)

**Base Generator** (`base.py`):
- Abstract base class defining the generator interface
- Common functionality for all generators
- Parameter definition system

**Specific Generators**:
- `random_walk.py`: Random walk algorithms
- `mathematical.py`: Mathematical functions and patterns
- `system_viz.py`: System metrics visualization
- `audio_reactive.py`: Audio-driven generation

### 4. Output System

Handles export to multiple formats:
- **SVG**: Vector graphics using svgwrite
- **PNG**: Raster graphics using Pillow
- Maintains aspect ratio and resolution

## Data Flow

```
User Input (GUI)
    ↓
Parameter Collection
    ↓
Generator Selection
    ↓
Generation Process
    ↓
Canvas Display (optional)
    ↓
Export to File (SVG/PNG)
```

## Generator Interface

All generators implement:

```python
class BaseGenerator:
    def get_parameters(self) -> dict:
        """Return parameter definitions"""
        
    def generate(self, width: int, height: int, params: dict) -> ArtworkData:
        """Generate artwork with given dimensions and parameters"""
        
    def to_svg(self, artwork: ArtworkData, filename: str):
        """Export to SVG format"""
        
    def to_png(self, artwork: ArtworkData, filename: str):
        """Export to PNG format"""
```

## Parameter System

Parameters are defined as dictionaries:

```python
{
    'param_name': {
        'type': 'int' | 'float' | 'color' | 'choice',
        'default': value,
        'min': min_value,  # for numeric types
        'max': max_value,  # for numeric types
        'choices': [...],  # for choice type
        'label': 'Display Name'
    }
}
```

## Extension Points

### Adding New Generators

1. Inherit from `BaseGenerator`
2. Implement required methods
3. Register in app initialization

### Adding New Output Formats

1. Add export method to `BaseGenerator`
2. Update GUI with new export option
3. Implement format-specific rendering

### Adding New Parameter Types

1. Extend parameter definition schema
2. Add UI control in `controls.py`
3. Update parameter validation

## Design Decisions

### Why Tkinter?

- Built-in with Python (no extra dependencies)
- Sufficient for our needs
- Cross-platform
- Easy to learn and extend

### Why Separate Generators?

- Modularity: Each method is independent
- Extensibility: Easy to add new methods
- Maintainability: Changes don't affect other generators
- Testability: Can test each generator in isolation

### Why Both SVG and PNG?

- SVG: Scalable, editable, small file size
- PNG: Universal compatibility, exact pixel control
- Different use cases require different formats

## Performance Considerations

- Generation happens in main thread (simple for now)
- Future: Move to background thread for complex generations
- Canvas preview may be downscaled for performance
- Large outputs generated directly to file

## Error Handling

- Parameter validation before generation
- Graceful fallbacks for missing dependencies
- User-friendly error messages
- Logging for debugging

## Future Architecture Improvements

1. **Plugin System**: Dynamic generator loading
2. **Threading**: Background generation with progress
3. **Caching**: Parameter presets and templates
4. **Undo/Redo**: Generation history
5. **Batch Processing**: Multiple outputs from parameter ranges
