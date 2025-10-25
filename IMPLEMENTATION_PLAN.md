# Implementation Plan: Multi-Method Support + Mathematical Patterns

## Overview

This document outlines the step-by-step implementation plan for adding multi-method support and the Mathematical Patterns generator.

## Goals

1. ✅ Refactor architecture to support multiple generators
2. ✅ Add method selector to GUI
3. ✅ Implement dynamic parameter panel
4. ✅ Create Mathematical Patterns generator
5. ✅ Enable method switching and layering
6. ✅ Maintain clean, intuitive UX

## Phase 1: Architecture Refactoring

### Step 1.1: Update BaseGenerator
**File:** `src/generators/base.py`

Add new methods for UI integration:
```python
def get_description(self) -> str:
    """Return brief description of the generator."""
    return ""

def get_icon(self) -> str:
    """Return emoji/icon for UI display."""
    return "🎨"
```

### Step 1.2: Update RandomWalkGenerator
**File:** `src/generators/random_walk.py`

Add description and icon:
```python
def get_description(self) -> str:
    return "Organic flowing patterns using random walk algorithms"

def get_icon(self) -> str:
    return "🚶"
```

### Step 1.3: Update App Class
**File:** `src/app.py`

Change from single generator to generator dictionary:
```python
def _initialize_generators(self) -> Dict[str, BaseGenerator]:
    generators = {}
    
    # Random Walk (Method 2)
    random_walk = RandomWalkGenerator()
    generators[random_walk.get_name()] = random_walk
    
    # Mathematical Patterns (Method 1) - NEW
    math_patterns = MathematicalPatternsGenerator()
    generators[math_patterns.get_name()] = math_patterns
    
    return generators

def __init__(self):
    # ...
    self.generators = self._initialize_generators()
    
    # Pass all generators to MainWindow
    self.main_window = MainWindow(self.root, self.generators, self.output_dir)
```

### Step 1.4: Update MainWindow Constructor
**File:** `src/gui/main_window.py`

Accept multiple generators:
```python
def __init__(self, root: tk.Tk, generators: Dict[str, BaseGenerator], output_dir: str):
    self.root = root
    self.generators = generators
    self.current_generator_name = list(generators.keys())[0]
    self.current_generator = generators[self.current_generator_name]
    self.output_dir = output_dir
    
    # State
    self.param_widgets: Dict[str, Any] = {}
    self.current_artwork = None
    self.layer_history = []  # Track method names used
    # ... rest of state
```

## Phase 2: GUI Updates for Method Selection

### Step 2.1: Add Method Selector
**File:** `src/gui/main_window.py`

Add method selector dropdown in `_create_control_panel()`:
```python
def _create_control_panel(self, parent):
    # ... existing scrollable frame setup ...
    
    # Title
    title_label = ttk.Label(...)
    title_label.pack(pady=10)
    
    # METHOD SELECTOR - NEW
    method_frame = ttk.LabelFrame(scrollable_frame, text="Generator Method", padding=10)
    method_frame.pack(fill=tk.X, padx=5, pady=5)
    
    self.method_var = tk.StringVar(value=self.current_generator_name)
    method_dropdown = ttk.Combobox(
        method_frame,
        textvariable=self.method_var,
        values=list(self.generators.keys()),
        state='readonly',
        width=30
    )
    method_dropdown.pack(fill=tk.X, padx=5, pady=5)
    method_dropdown.bind('<<ComboboxSelected>>', self._on_method_changed)
    
    # Add description label
    self.method_desc_var = tk.StringVar(value=self.current_generator.get_description())
    desc_label = ttk.Label(
        method_frame,
        textvariable=self.method_desc_var,
        wraplength=400,
        font=("Arial", 9),
        foreground="gray"
    )
    desc_label.pack(fill=tk.X, padx=5, pady=(0, 5))
    
    # Output size section
    # ... rest of existing code ...
```

### Step 2.2: Implement Method Change Handler
**File:** `src/gui/main_window.py`

```python
def _on_method_changed(self, event=None):
    """Handle method selection change."""
    new_method = self.method_var.get()
    
    if new_method == self.current_generator_name:
        return  # No change
    
    # Update current generator
    self.current_generator_name = new_method
    self.current_generator = self.generators[new_method]
    
    # Update description
    self.method_desc_var.set(self.current_generator.get_description())
    
    # Update window title
    self.root.title(f"Generative Art Studio - {new_method}")
    
    # Rebuild parameter panel
    self._rebuild_parameter_panel()
    
    # Update status
    self.status_var.set(f"Switched to {new_method}")
```

### Step 2.3: Implement Dynamic Parameter Panel
**File:** `src/gui/main_window.py`

```python
def _rebuild_parameter_panel(self):
    """Rebuild parameter controls for current generator."""
    # Clear existing parameter widgets
    for widget in self.params_frame.winfo_children():
        widget.destroy()
    
    self.param_widgets.clear()
    
    # Recreate parameter controls for current generator
    self._create_parameter_controls(self.params_frame)
    
    # Force update
    self.params_frame.update_idletasks()
```

Note: Need to store `params_frame` as instance variable in `_create_control_panel()`:
```python
# Generator parameters
self.params_frame = ttk.LabelFrame(scrollable_frame, text="Parameters", padding=10)
self.params_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

self._create_parameter_controls(self.params_frame)
```

### Step 2.4: Update Layer Mode Label
**File:** `src/gui/main_window.py`

Change checkbox text:
```python
layer_checkbox = ttk.Checkbutton(
    layer_frame,
    text="Keep & layer with previous artwork",  # Updated text
    variable=self.layer_mode_var
)
```

### Step 2.5: Track Layer History
**File:** `src/gui/main_window.py`

Update `_generate_artwork()` to track methods:
```python
def _generate_artwork(self):
    try:
        # ... existing code ...
        
        if previous_artwork:
            # Merge and track layer
            merged_artwork = ArtworkData(...)
            # Add to layer history
            if not hasattr(self, 'layer_history'):
                self.layer_history = []
            self.layer_history.append(self.current_generator_name)
            self.current_artwork = merged_artwork
        else:
            # New artwork - reset layer history
            self.layer_history = [self.current_generator_name]
            self.current_artwork = new_artwork
        
        # ... rest of code ...
```

Update status to show layer info:
```python
def _on_generation_complete(self):
    # ... existing code ...
    
    # Update status with layer info
    layer_count = len(self.layer_history)
    if layer_count == 1:
        status = f"Complete! (took {time_str})"
    else:
        methods = ", ".join(self.layer_history)
        status = f"Complete! {layer_count} layers ({methods}) (took {time_str})"
    
    self.status_var.set(status)
```

### Step 2.6: Clear Layer History on Clear
**File:** `src/gui/main_window.py`

```python
def _on_clear(self):
    # ... existing code ...
    self.layer_history = []
    self.status_var.set("Canvas cleared")
```

## Phase 3: Mathematical Patterns Generator

### Step 3.1: Create Generator File
**File:** `src/generators/mathematical.py`

```python
"""
Mathematical Patterns Generator

Creates artwork using mathematical equations and geometric patterns.
"""

import math
import random
from typing import Dict, Any, List, Tuple
from .base import BaseGenerator, ArtworkData, PathElement, CircleElement


class MathematicalPatternsGenerator(BaseGenerator):
    """
    Generates art using mathematical patterns.
    
    Supports various pattern types:
    - Spirals (Archimedean, logarithmic, Fibonacci)
    - Fractals (Mandelbrot, Julia, Sierpinski)
    - Waves (sine, cosine, combined)
    - Lissajous curves
    - Geometric patterns
    """
    
    def get_name(self) -> str:
        return "Mathematical Patterns"
    
    def get_description(self) -> str:
        return "Geometric patterns from mathematical equations and fractals"
    
    def get_icon(self) -> str:
        return "📐"
    
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            'pattern_type': {
                'type': 'choice',
                'default': 'spiral',
                'choices': ['spiral', 'fractal', 'wave', 'lissajous', 'circle_pack'],
                'label': 'Pattern Type',
                'help': 'Type of mathematical pattern to generate'
            },
            # Spiral parameters
            'spiral_type': {
                'type': 'choice',
                'default': 'archimedean',
                'choices': ['archimedean', 'logarithmic', 'fibonacci'],
                'label': 'Spiral Type',
                'help': 'Type of spiral (when pattern_type is spiral)'
            },
            'spiral_turns': {
                'type': 'int',
                'default': 5,
                'min': 1,
                'max': 20,
                'label': 'Spiral Turns',
                'help': 'Number of complete rotations'
            },
            'spiral_spacing': {
                'type': 'float',
                'default': 10.0,
                'min': 1.0,
                'max': 50.0,
                'step': 1.0,
                'label': 'Spiral Spacing',
                'help': 'Distance between spiral arms'
            },
            # Wave parameters
            'wave_type': {
                'type': 'choice',
                'default': 'sine',
                'choices': ['sine', 'cosine', 'combined', 'damped'],
                'label': 'Wave Type',
                'help': 'Type of wave pattern'
            },
            'wave_frequency': {
                'type': 'float',
                'default': 2.0,
                'min': 0.1,
                'max': 10.0,
                'step': 0.1,
                'label': 'Wave Frequency',
                'help': 'Number of wave cycles'
            },
            'wave_amplitude': {
                'type': 'float',
                'default': 50.0,
                'min': 10.0,
                'max': 200.0,
                'step': 5.0,
                'label': 'Wave Amplitude',
                'help': 'Height of waves'
            },
            'wave_count': {
                'type': 'int',
                'default': 5,
                'min': 1,
                'max': 20,
                'label': 'Wave Count',
                'help': 'Number of parallel waves'
            },
            # Fractal parameters
            'fractal_type': {
                'type': 'choice',
                'default': 'mandelbrot',
                'choices': ['mandelbrot', 'julia', 'sierpinski'],
                'label': 'Fractal Type',
                'help': 'Type of fractal pattern'
            },
            'fractal_iterations': {
                'type': 'int',
                'default': 50,
                'min': 10,
                'max': 200,
                'label': 'Fractal Iterations',
                'help': 'Detail level (higher = more detail)'
            },
            'fractal_zoom': {
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'step': 0.1,
                'label': 'Fractal Zoom',
                'help': 'Zoom level into fractal'
            },
            # Lissajous parameters
            'lissajous_a': {
                'type': 'int',
                'default': 3,
                'min': 1,
                'max': 10,
                'label': 'Lissajous A',
                'help': 'Frequency parameter A'
            },
            'lissajous_b': {
                'type': 'int',
                'default': 4,
                'min': 1,
                'max': 10,
                'label': 'Lissajous B',
                'help': 'Frequency parameter B'
            },
            'lissajous_delta': {
                'type': 'float',
                'default': 90.0,
                'min': 0.0,
                'max': 360.0,
                'step': 15.0,
                'label': 'Phase Shift',
                'help': 'Phase difference in degrees'
            },
            # Circle packing parameters
            'circle_count': {
                'type': 'int',
                'default': 50,
                'min': 5,
                'max': 500,
                'label': 'Circle Count',
                'help': 'Number of circles to pack'
            },
            'circle_min_radius': {
                'type': 'float',
                'default': 5.0,
                'min': 1.0,
                'max': 50.0,
                'step': 1.0,
                'label': 'Min Circle Radius',
                'help': 'Minimum circle size'
            },
            'circle_max_radius': {
                'type': 'float',
                'default': 50.0,
                'min': 10.0,
                'max': 200.0,
                'step': 5.0,
                'label': 'Max Circle Radius',
                'help': 'Maximum circle size'
            },
            # Common parameters
            'line_width': {
                'type': 'float',
                'default': 2.0,
                'min': 0.1,
                'max': 10.0,
                'step': 0.1,
                'label': 'Line Width',
                'help': 'Thickness of drawn lines'
            },
            'color_mode': {
                'type': 'choice',
                'default': 'monochrome',
                'choices': ['monochrome', 'gradient', 'rainbow', 'depth'],
                'label': 'Color Mode',
                'help': 'How to color the pattern'
            },
            'base_color': {
                'type': 'color',
                'default': '#000000',
                'label': 'Base Color',
                'help': 'Primary color'
            },
            'background_color': {
                'type': 'color',
                'default': '#FFFFFF',
                'label': 'Background Color',
                'help': 'Canvas background color'
            },
            'rotation': {
                'type': 'float',
                'default': 0.0,
                'min': 0.0,
                'max': 360.0,
                'step': 15.0,
                'label': 'Rotation',
                'help': 'Rotate pattern (degrees)'
            },
            'symmetry': {
                'type': 'int',
                'default': 1,
                'min': 1,
                'max': 12,
                'label': 'Symmetry',
                'help': 'Radial symmetry count (1 = none)'
            },
            'seed': {
                'type': 'int',
                'default': 0,
                'min': 0,
                'max': 999999,
                'label': 'Random Seed',
                'help': 'Seed for reproducibility (0 = random)'
            }
        }
    
    def generate(self, width: int, height: int, params: Dict[str, Any],
                 progress_callback=None) -> ArtworkData:
        """Generate mathematical pattern artwork."""
        # Validate parameters
        params = self.validate_parameters(params)
        
        # Set random seed if specified
        if params['seed'] > 0:
            random.seed(params['seed'])
        
        # Create artwork container
        bg_color = self._hex_to_rgb(params['background_color'])
        artwork = ArtworkData(width=width, height=height, background_color=bg_color)
        
        # Generate based on pattern type
        pattern_type = params['pattern_type']
        
        if pattern_type == 'spiral':
            self._generate_spiral(width, height, params, artwork, progress_callback)
        elif pattern_type == 'wave':
            self._generate_wave(width, height, params, artwork, progress_callback)
        elif pattern_type == 'fractal':
            self._generate_fractal(width, height, params, artwork, progress_callback)
        elif pattern_type == 'lissajous':
            self._generate_lissajous(width, height, params, artwork, progress_callback)
        elif pattern_type == 'circle_pack':
            self._generate_circle_pack(width, height, params, artwork, progress_callback)
        
        return artwork
    
    # Implementation methods will be added in next steps
    def _generate_spiral(self, width, height, params, artwork, progress_callback):
        """Generate spiral patterns."""
        pass  # To be implemented
    
    def _generate_wave(self, width, height, params, artwork, progress_callback):
        """Generate wave patterns."""
        pass  # To be implemented
    
    def _generate_fractal(self, width, height, params, artwork, progress_callback):
        """Generate fractal patterns."""
        pass  # To be implemented
    
    def _generate_lissajous(self, width, height, params, artwork, progress_callback):
        """Generate Lissajous curves."""
        pass  # To be implemented
    
    def _generate_circle_pack(self, width, height, params, artwork, progress_callback):
        """Generate circle packing patterns."""
        pass  # To be implemented
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
```

### Step 3.2: Implement Spiral Generation
(Will implement in detail in next step)

### Step 3.3: Implement Other Pattern Types
(Will implement in detail in subsequent steps)

### Step 3.4: Register Generator
**File:** `src/generators/__init__.py`

```python
from .base import BaseGenerator, ArtworkData, PathElement, CircleElement
from .random_walk import RandomWalkGenerator
from .mathematical import MathematicalPatternsGenerator

__all__ = [
    'BaseGenerator',
    'ArtworkData',
    'PathElement',
    'CircleElement',
    'RandomWalkGenerator',
    'MathematicalPatternsGenerator',
]
```

## Phase 4: Testing & Documentation

### Step 4.1: Test Method Switching
- Switch between methods
- Verify parameter panel updates
- Check that each method generates correctly

### Step 4.2: Test Layering
- Generate with Random Walk
- Keep and switch to Mathematical Patterns
- Generate spiral
- Verify both are visible
- Test with 3+ layers

### Step 4.3: Update Documentation
- Update README with new method
- Add examples of method combinations
- Document best practices

### Step 4.4: Create Example Workflows
Document common use cases:
- Abstract backgrounds
- Geometric overlays
- Mixed media compositions

## Implementation Order

1. ✅ Phase 1: Architecture (Steps 1.1-1.4)
2. ✅ Phase 2: GUI Updates (Steps 2.1-2.6)
3. ✅ Phase 3: Mathematical Patterns (Steps 3.1-3.4)
   - Start with spiral implementation
   - Add other patterns incrementally
4. ✅ Phase 4: Testing & Docs

## Next Steps

Start with Phase 1, Step 1.1: Update BaseGenerator with new methods.

Would you like me to proceed with the implementation?
