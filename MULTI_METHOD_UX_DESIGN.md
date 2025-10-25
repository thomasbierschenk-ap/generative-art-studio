# Multi-Method UX Design

## Overview

Design for supporting multiple art generation methods with a clean, intuitive interface that allows users to:
1. Select one method at a time
2. Generate artwork with that method
3. Layer multiple generations using different methods
4. Switch between methods without overwhelming the UI

## UI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  Generative Art Studio                                    [×]    │
├─────────────────────┬───────────────────────────────────────────┤
│                     │                                           │
│  Method Selection   │         Live Preview                      │
│  ┌───────────────┐  │                                           │
│  │ Random Walk  ▼│  │                                           │
│  └───────────────┘  │                                           │
│                     │                                           │
│  Output Size        │                                           │
│  ┌───────────────┐  │                                           │
│  │ Width:  800   │  │                                           │
│  │ Height: 600   │  │                                           │
│  └───────────────┘  │                                           │
│                     │                                           │
│  Parameters         │                                           │
│  ┌───────────────┐  │                                           │
│  │ [Dynamic      │  │                                           │
│  │  controls     │  │                                           │
│  │  based on     │  │                                           │
│  │  selected     │  │                                           │
│  │  method]      │  │                                           │
│  │               │  │                                           │
│  │               │  │                                           │
│  └───────────────┘  │                                           │
│                     │                                           │
│  ☐ Keep & layer     │                                           │
│     with previous   │                                           │
│                     │                                           │
│  [Generate]         │                                           │
│  [Abort] [Clear]    │                                           │
│  [Save PNG]         │                                           │
│  [Save SVG]         │                                           │
│                     │                                           │
│  Progress           │                                           │
│  ▓▓▓▓▓▓░░░░ 60%     │                                           │
│  Ready              │                                           │
└─────────────────────┴───────────────────────────────────────────┘
```

## User Workflows

### Workflow 1: Single Method Generation
1. Select method from dropdown (e.g., "Random Walk")
2. Adjust parameters for that method
3. Click "Generate"
4. Watch live preview
5. Save result

### Workflow 2: Multi-Method Layering
1. Select "Random Walk" method
2. Generate artwork (black lines)
3. Check ☑ "Keep & layer with previous"
4. Switch to "Mathematical Patterns" method
5. Select "Spiral" pattern
6. Generate again
7. See spiral layered on top of random walk
8. Optionally: Switch to another method and layer again
9. Save final composite

### Workflow 3: Experimenting with Methods
1. Generate with Method A
2. Don't like it → Clear canvas
3. Switch to Method B
4. Generate again
5. Like it → Keep it
6. Switch to Method C
7. Layer Method C on top
8. Save result

## UI Components

### 1. Method Selector (Dropdown)
```
┌─────────────────────────┐
│ Random Walk            ▼│
├─────────────────────────┤
│ Random Walk             │
│ Mathematical Patterns   │
│ System Metrics          │ (grayed out if not available)
│ Audio Reactive          │ (grayed out if not available)
└─────────────────────────┘
```

**Behavior:**
- Dropdown at the top of control panel
- Shows all available methods
- Grays out methods that aren't implemented yet
- When changed, updates the parameter panel below

### 2. Dynamic Parameter Panel
**Behavior:**
- Content changes based on selected method
- Smoothly transitions between different parameter sets
- Maintains scroll position when possible
- Each method has its own parameter configuration

**Example - Random Walk Parameters:**
- Number of Walks
- Steps per Walk
- Step Size
- Angle Variation
- Line Width
- Color Mode
- Base Color
- Background Color
- Start Position
- Boundary Behavior
- Show Nodes
- Random Seed

**Example - Mathematical Patterns Parameters:**
- Pattern Type (Spiral, Fractal, Wave, etc.)
- Iterations/Depth
- Scale/Size
- Rotation
- Color Mode
- Symmetry
- etc.

### 3. Layer Mode Checkbox
**New Label:** "Keep & layer with previous"
**Behavior:**
- When checked, next generation adds to existing artwork
- When unchecked, next generation replaces artwork
- Allows mixing different methods
- Background color from first generation is preserved

### 4. Status Indicators
**Show current state:**
- "Ready" - No artwork generated
- "Generating... (Method: Random Walk)" - Shows which method is running
- "Complete - 1 layer" - Shows number of layers
- "Complete - 3 layers (Random Walk, Spiral, Fractal)" - Shows method history

## Technical Implementation

### Architecture Changes

#### 1. App Class Updates (`src/app.py`)
```python
class GenerativeArtApp:
    def __init__(self):
        self.generators = {
            'Random Walk': RandomWalkGenerator(),
            'Mathematical Patterns': MathematicalPatternsGenerator(),
            # 'System Metrics': SystemMetricsGenerator(),  # Future
            # 'Audio Reactive': AudioReactiveGenerator(),  # Future
        }
        self.current_generator = 'Random Walk'
```

#### 2. MainWindow Updates (`src/gui/main_window.py`)
```python
class MainWindow:
    def __init__(self, root, generators, output_dir):
        self.generators = generators  # Dict of all generators
        self.current_generator_name = list(generators.keys())[0]
        self.current_generator = generators[self.current_generator_name]
        self.layer_history = []  # Track which methods were used
        
    def _create_method_selector(self):
        """Create dropdown for method selection"""
        
    def _on_method_changed(self, method_name):
        """Handle method selection change"""
        self.current_generator_name = method_name
        self.current_generator = self.generators[method_name]
        self._rebuild_parameter_panel()
        
    def _rebuild_parameter_panel(self):
        """Rebuild parameter controls for current generator"""
        # Clear existing parameters
        # Create new parameters for current generator
```

#### 3. Layer History Tracking
```python
class ArtworkData:
    def __init__(self, ...):
        self.layers = []  # List of (method_name, timestamp) tuples
        
    def add_layer(self, method_name):
        self.layers.append((method_name, time.time()))
```

### Method Registration System

**Each generator registers itself:**
```python
class BaseGenerator:
    def get_name(self) -> str:
        """Return display name for UI"""
        
    def get_description(self) -> str:
        """Return brief description"""
        
    def get_icon(self) -> str:
        """Return emoji or icon identifier"""
```

**Example:**
```python
class RandomWalkGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "Random Walk"
        
    def get_description(self) -> str:
        return "Organic flowing patterns using random walk algorithms"
        
    def get_icon(self) -> str:
        return "🚶"

class MathematicalPatternsGenerator(BaseGenerator):
    def get_name(self) -> str:
        return "Mathematical Patterns"
        
    def get_description(self) -> str:
        return "Geometric patterns from mathematical equations"
        
    def get_icon(self) -> str:
        return "📐"
```

## Enhanced Features

### 1. Layer Information Display
Show layer count and methods used:
```
Status: Complete - 3 layers
  1. Random Walk (5 walks, rainbow)
  2. Spiral (golden ratio, blue)
  3. Fractal (Mandelbrot, depth 100)
```

### 2. Method Hints
When hovering over method selector, show tooltip:
```
Random Walk
Create organic, flowing patterns using random walk algorithms.
Perfect for: Natural textures, backgrounds, abstract art
```

### 3. Suggested Combinations
After first generation, show suggestions:
```
💡 Try layering with:
  • Spiral (for structured overlay)
  • Fractal (for detailed texture)
  • Wave Pattern (for rhythmic elements)
```

### 4. Quick Switch
After generation, show quick method switch buttons:
```
[Generate]
[Keep & Switch to: Spiral | Fractal | Wave]
```

## Benefits of This Design

✅ **Clean Interface**
- Only shows controls for selected method
- No overwhelming number of parameters visible at once

✅ **Intuitive Workflow**
- Natural progression: Generate → Keep → Switch → Layer
- Clear visual feedback on what's happening

✅ **Powerful Combinations**
- Mix any methods together
- Create unique composite artworks
- Experiment freely

✅ **Scalable**
- Easy to add new methods
- Each method is self-contained
- No UI clutter as methods are added

✅ **Discoverable**
- Method selector makes all options visible
- Descriptions help users understand each method
- Suggestions guide experimentation

## Implementation Plan

### Phase 1: Refactor for Multi-Method Support
1. Update `App` class to manage multiple generators
2. Update `MainWindow` to accept generator dictionary
3. Add method selector dropdown
4. Implement dynamic parameter panel rebuilding
5. Update layer mode to track method history

### Phase 2: Implement Mathematical Patterns Generator
1. Create `MathematicalPatternsGenerator` class
2. Implement pattern types (spiral, fractal, wave)
3. Define parameters for each pattern type
4. Test with existing UI

### Phase 3: Polish & Enhancement
1. Add method descriptions and tooltips
2. Implement layer history display
3. Add suggested combinations
4. Create method icons/emojis
5. Add quick switch buttons

### Phase 4: Documentation & Testing
1. Update user documentation
2. Create example workflows
3. Test all method combinations
4. Document best practices for layering

## Example Use Cases

### Use Case 1: Abstract Background
1. Generate Random Walk (low variation, many walks) → flowing background
2. Keep & switch to Spiral
3. Generate golden ratio spiral → focal point
4. Save composite

### Use Case 2: Fractal Texture
1. Generate Mandelbrot fractal (high iteration) → detailed texture
2. Keep & switch to Random Walk
3. Generate few walks (high variation) → organic overlay
4. Save composite

### Use Case 3: Geometric Art
1. Generate Spiral (Archimedean) → structured base
2. Keep & switch to Wave Pattern
3. Generate sine waves → rhythmic element
4. Keep & switch to Random Walk
5. Generate subtle walks → organic touch
6. Save composite

## Future Enhancements

- **Preset Combinations**: Save favorite method combinations
- **Layer Opacity**: Control transparency of each layer
- **Layer Reordering**: Drag to reorder layers
- **Layer Visibility**: Toggle individual layers on/off
- **Blend Modes**: Different ways layers combine (multiply, screen, etc.)
- **Animation**: Animate between different method generations
- **Batch Generation**: Generate multiple variations automatically

---

This design provides a clean, intuitive interface while enabling powerful creative workflows through method combination and layering.
