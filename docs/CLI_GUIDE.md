# Command-Line Interface Guide

This guide covers using the interactive command-line interface for the Generative Art Studio.

## Quick Start

```bash
./create_art.sh
```

This launches an interactive session that guides you through creating artwork.

## Parameters Explained

### Number of Walks
- **What it does**: Controls how many separate random walk paths are drawn
- **Typical range**: 1-20
- **Effect**: More walks = denser, more complex patterns

### Steps Per Walk
- **What it does**: How many line segments each walk contains
- **Typical range**: 50-500
- **Effect**: More steps = longer, more intricate paths

### Step Size
- **What it does**: Length of each line segment in pixels
- **Typical range**: 5-20
- **Effect**: Larger steps = bolder, more angular patterns

### Angle Variation
- **What it does**: Maximum angle change between steps (in degrees)
- **Typical range**: 15-90
- **Effect**: 
  - Small angles (15-30°) = smooth, flowing curves
  - Large angles (60-90°) = sharp, chaotic patterns

### Line Width
- **What it does**: Thickness of the drawn lines in pixels
- **Typical range**: 1-5
- **Effect**: Thicker lines = bolder, more visible patterns

## Color Modes

### 1. Monochrome
- Single color (black) on white background
- Clean, minimalist aesthetic
- Best for: Print-ready art, simple designs

### 2. Grayscale
- Random shades of gray for each walk
- Subtle variation without color distraction
- Best for: Professional looks, texture studies

### 3. Color
- Random colors for each walk
- Vibrant and varied
- Best for: Playful, energetic compositions

### 4. Rainbow
- Smooth color gradient across the spectrum
- Colors transition through the rainbow
- Best for: Psychedelic effects, gradient studies

## Start Positions

### 1. Center
- All walks begin from the canvas center
- Creates radial, explosive patterns
- Best for: Mandala-like designs, focal compositions

### 2. Random
- Each walk starts from a random location
- Distributed patterns across the canvas
- Best for: Abstract textures, scattered compositions

### 3. Grid
- Walks start from evenly-spaced grid points
- Organized, structured starting points
- Best for: Systematic explorations, tiled patterns

## Boundary Behaviors

### 1. Wrap
- Walks that leave one edge reappear on the opposite edge
- Creates seamless, tileable patterns
- Best for: Wallpapers, repeating patterns

### 2. Bounce
- Walks reflect off edges like a ball
- Keeps all content within bounds
- Best for: Contained compositions, framed art

### 3. Stop
- Walks end when they hit an edge
- Natural termination at boundaries
- Best for: Organic, realistic movement

## Canvas Size

### Standard Sizes
- **Square**: 800x800, 1000x1000
- **Landscape**: 1920x1080 (HD), 1600x900
- **Portrait**: 1080x1920, 900x1600
- **Wide**: 2560x1080, 3440x1440

### Tips
- Larger canvases need more steps or walks to fill
- Consider your output medium (screen, print)
- SVG scales infinitely; PNG is fixed resolution

## Example Configurations

### Smooth Flowing Lines
```
Number of walks: 5
Steps per walk: 200
Step size: 8
Angle variation: 20
Line width: 2
Color mode: Rainbow
Start position: Center
Boundary: Wrap
Canvas: 800x800
```

### Chaotic Energy
```
Number of walks: 15
Steps per walk: 100
Step size: 15
Angle variation: 75
Line width: 3
Color mode: Color
Start position: Random
Boundary: Bounce
Canvas: 1200x800
```

### Minimalist Elegance
```
Number of walks: 3
Steps per walk: 300
Step size: 5
Angle variation: 30
Line width: 1
Color mode: Monochrome
Start position: Center
Boundary: Stop
Canvas: 1000x1000
```

### Textured Abstract
```
Number of walks: 20
Steps per walk: 150
Step size: 10
Angle variation: 45
Line width: 2
Color mode: Grayscale
Start position: Grid
Boundary: Wrap
Canvas: 1600x1200
```

## Tips for Experimentation

1. **Start Simple**: Begin with default values and change one parameter at a time
2. **Iterate**: Generate multiple versions with slight variations
3. **Save Your Favorites**: Use descriptive filenames to remember settings
4. **Combine Techniques**: Generate multiple images and layer them in an image editor
5. **Print Test**: If printing, generate at higher resolutions (2000x2000+)

## Output Files

Your artwork is saved in the `output/` directory:
- `yourname.svg` - Vector format (scalable, editable)
- `yourname.png` - Raster format (ready to use)

## Troubleshooting

### "Invalid input" errors
- Make sure to enter numbers for numeric parameters
- Press Enter to accept default values

### Artwork looks empty
- Increase number of walks or steps
- Increase step size
- Check canvas size isn't too large for your parameters

### Lines go off canvas
- Use "bounce" or "stop" boundary behavior
- Reduce step size
- Start from center instead of random

### Colors not showing
- Make sure you selected a color mode other than monochrome
- Try "rainbow" mode for guaranteed visible colors

## Advanced Usage

### Batch Generation
Create a simple script to generate multiple variations:

```bash
#!/bin/bash
for i in {1..10}; do
    echo "5
100
10
45
2
4
1
1
800
600
artwork_$i" | ./create_art.sh
done
```

### Scripted Generation
Call the generator directly from Python:

```python
from generators.random_walk import RandomWalkGenerator

gen = RandomWalkGenerator(
    num_walks=5,
    num_steps=100,
    step_size=10,
    angle_variation=45,
    line_width=2,
    color_mode="rainbow",
    start_position="center",
    boundary_behavior="wrap"
)

gen.generate(800, 600)
gen.save_svg("output/my_art.svg")
gen.save_png("output/my_art.png")
```

## Next Steps

- Experiment with different parameter combinations
- Try the same settings with different random seeds (just regenerate)
- Combine multiple outputs in an image editor
- Share your creations!

For more information, see the main [README.md](../README.md) and [ARCHITECTURE.md](ARCHITECTURE.md).
