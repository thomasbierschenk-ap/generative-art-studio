# Usage Examples

## Command-Line Generation

If the GUI doesn't work on your system, you can generate art programmatically:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from generators import RandomWalkGenerator

# Create generator
gen = RandomWalkGenerator()

# Define parameters
params = {
    'num_walks': 10,
    'steps_per_walk': 2000,
    'step_size': 3.0,
    'angle_variation': 45.0,
    'line_width': 1.5,
    'color_mode': 'rainbow',
    'base_color': '#000000',
    'background_color': '#FFFFFF',
    'start_position': 'center',
    'boundary_behavior': 'bounce',
    'add_nodes': False,
    'seed': 42  # For reproducibility
}

# Generate artwork
artwork = gen.generate(1920, 1080, params)

# Save outputs
gen.to_svg(artwork, 'output/my_art.svg')
gen.to_png(artwork, 'output/my_art.png')
```

## Example Configurations

### Organic Flow

Creates smooth, flowing patterns reminiscent of natural forms:

```python
params = {
    'num_walks': 15,
    'steps_per_walk': 3000,
    'step_size': 2.0,
    'angle_variation': 30.0,
    'line_width': 1.0,
    'color_mode': 'rainbow',
    'background_color': '#FFFFFF',
    'start_position': 'center',
    'boundary_behavior': 'bounce',
    'add_nodes': False,
    'seed': 0
}
```

### Chaotic Energy

High variation creates energetic, unpredictable patterns:

```python
params = {
    'num_walks': 20,
    'steps_per_walk': 1000,
    'step_size': 10.0,
    'angle_variation': 180.0,
    'line_width': 2.0,
    'color_mode': 'color',
    'background_color': '#000000',
    'start_position': 'random',
    'boundary_behavior': 'wrap',
    'add_nodes': True,
    'seed': 0
}
```

### Minimalist Lines

Clean, geometric patterns with limited variation:

```python
params = {
    'num_walks': 5,
    'steps_per_walk': 5000,
    'step_size': 5.0,
    'angle_variation': 10.0,
    'line_width': 0.5,
    'color_mode': 'monochrome',
    'base_color': '#000000',
    'background_color': '#FFFFFF',
    'start_position': 'corners',
    'boundary_behavior': 'bounce',
    'add_nodes': False,
    'seed': 123
}
```

### Grayscale Depth

Multiple walks with varying shades create depth:

```python
params = {
    'num_walks': 30,
    'steps_per_walk': 1500,
    'step_size': 3.0,
    'angle_variation': 60.0,
    'line_width': 1.5,
    'color_mode': 'grayscale',
    'background_color': '#FFFFFF',
    'start_position': 'center',
    'boundary_behavior': 'bounce',
    'add_nodes': False,
    'seed': 0
}
```

### Edge Explosion

Walks starting from edges create outward expansion:

```python
params = {
    'num_walks': 25,
    'steps_per_walk': 800,
    'step_size': 8.0,
    'angle_variation': 90.0,
    'line_width': 2.5,
    'color_mode': 'rainbow',
    'background_color': '#000000',
    'start_position': 'edges',
    'boundary_behavior': 'stop',
    'add_nodes': True,
    'seed': 0
}
```

## Batch Generation

Generate multiple variations:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from generators import RandomWalkGenerator
import random

gen = RandomWalkGenerator()

# Base parameters
base_params = {
    'num_walks': 10,
    'steps_per_walk': 2000,
    'step_size': 3.0,
    'line_width': 1.5,
    'color_mode': 'rainbow',
    'background_color': '#FFFFFF',
    'start_position': 'center',
    'boundary_behavior': 'bounce',
    'add_nodes': False,
}

# Generate 10 variations with different angle variations
for i in range(10):
    params = base_params.copy()
    params['angle_variation'] = 10.0 + (i * 20.0)  # 10 to 190 degrees
    params['seed'] = i
    
    artwork = gen.generate(800, 600, params)
    gen.to_svg(artwork, f'output/variation_{i:02d}.svg')
    print(f"Generated variation {i} with angle_variation={params['angle_variation']}")
```

## Parameter Exploration

Systematically explore parameter space:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from generators import RandomWalkGenerator

gen = RandomWalkGenerator()

# Explore step size vs angle variation
step_sizes = [1.0, 3.0, 5.0, 10.0]
angle_vars = [15.0, 45.0, 90.0, 180.0]

for i, step_size in enumerate(step_sizes):
    for j, angle_var in enumerate(angle_vars):
        params = {
            'num_walks': 5,
            'steps_per_walk': 2000,
            'step_size': step_size,
            'angle_variation': angle_var,
            'line_width': 1.0,
            'color_mode': 'monochrome',
            'base_color': '#000000',
            'background_color': '#FFFFFF',
            'start_position': 'center',
            'boundary_behavior': 'bounce',
            'add_nodes': False,
            'seed': 42
        }
        
        artwork = gen.generate(400, 400, params)
        filename = f'output/explore_s{i}_a{j}.svg'
        gen.to_svg(artwork, filename)
        print(f"Generated: step={step_size}, angle={angle_var}")
```

## Tips for Interesting Results

### Balance Complexity and Clarity
- Too many walks can create visual clutter
- Too few may look sparse
- Start with 5-15 walks and adjust

### Step Size Matters
- Small steps (1-3px): Detailed, organic lines
- Medium steps (5-10px): Balanced, visible structure
- Large steps (15+px): Bold, geometric patterns

### Angle Variation Creates Character
- 0-30°: Smooth, flowing lines
- 30-90°: Natural curves with direction changes
- 90-180°: Chaotic, unpredictable paths
- 180-360°: Complete randomness

### Boundary Behavior Effects
- **Bounce**: Creates contained, reflected patterns
- **Wrap**: Seamless, infinite plane effect
- **Stop**: Organic edges, varying lengths
- **Ignore**: Extends beyond canvas (crops at edge)

### Color Mode Selection
- **Monochrome**: Focus on form and structure
- **Grayscale**: Adds depth through value
- **Color**: Vibrant, energetic
- **Rainbow**: Smooth color transitions

### Reproducibility
- Set `seed` to non-zero for reproducible results
- Same seed + same parameters = identical output
- Use seed=0 for random variation each time

## Advanced Techniques

### Creating Series
Generate a series with gradual parameter changes:

```python
for i in range(20):
    t = i / 19.0  # 0.0 to 1.0
    params['angle_variation'] = 10.0 + (t * 170.0)  # Gradually increase
    # ... generate and save
```

### Combining Multiple Outputs
Generate layers and combine in image editor:
1. Generate with transparent background
2. Create multiple variations
3. Layer in Photoshop/GIMP/etc.
4. Adjust opacity and blend modes

### High-Resolution Prints
For print quality:
```python
artwork = gen.generate(7200, 5400, params)  # 24x18 inches at 300 DPI
gen.to_svg(artwork, 'print.svg')  # SVG scales infinitely
```
