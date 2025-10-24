# Quick Start Guide

## Installation

1. **Clone or navigate to the project:**
   ```bash
   cd generative-art-studio
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python src/main.py
```

Or make it executable:
```bash
chmod +x src/main.py
./src/main.py
```

## First Steps

1. **Select a Generation Method**
   - Open the dropdown at the top of the control panel
   - Currently available: "Random Walk"

2. **Set Output Size**
   - Enter desired width and height in pixels
   - Default: 800 x 600

3. **Adjust Parameters**
   - Use the sliders and controls to modify the generation
   - Each parameter has a description to help you understand its effect

4. **Generate**
   - Click "Generate Artwork"
   - Wait for the generation to complete

5. **Save Your Work**
   - Click "Save as SVG" for vector graphics (scalable)
   - Click "Save as PNG" for raster graphics (pixel-based)

## Random Walk Parameters Explained

- **Number of Walks**: How many separate paths to draw
- **Steps per Walk**: Length of each path (more steps = longer path)
- **Step Size**: Distance of each step in pixels
- **Angle Variation**: How much the direction can change (0° = straight line, 360° = any direction)
- **Line Width**: Thickness of the drawn lines
- **Color Mode**:
  - Monochrome: Single color
  - Grayscale: Gradient from black to white
  - Color: Random colors
  - Rainbow: Full spectrum
- **Start Position**: Where walks begin (center, random, edges, corners)
- **Boundary Behavior**: What happens at canvas edges
  - Bounce: Reflect back
  - Wrap: Continue from opposite side
  - Stop: End the walk
  - Ignore: Keep going off-canvas
- **Show Nodes**: Draw circles at walk endpoints
- **Random Seed**: Set to non-zero for reproducible results

## Tips for Interesting Results

### Organic, Natural Patterns
- Low angle variation (10-45°)
- Many steps (1000+)
- Small step size (2-5 pixels)
- Multiple walks from center

### Chaotic, Energetic Patterns
- High angle variation (120-180°)
- Medium steps (500-1000)
- Larger step size (10-20 pixels)
- Random start positions

### Geometric, Structured Patterns
- Very low angle variation (5-15°)
- Bounce boundary behavior
- Monochrome or grayscale
- Corners or edges start position

### Flowing, Ribbon-like Patterns
- Medium angle variation (30-60°)
- Many walks (10-30)
- Rainbow color mode
- Wrap boundary behavior

## Troubleshooting

**Application won't start:**
- Make sure all dependencies are installed
- Check that you're using Python 3.7 or later

**Generation is slow:**
- Reduce number of walks or steps
- Use smaller output dimensions for testing

**Saved files are too large:**
- PNG files can be large for complex artwork
- Use SVG for smaller file sizes
- Reduce line width or number of elements

## Next Steps

Once you're comfortable with Random Walk, stay tuned for:
- Method 1: Mathematical Patterns (fractals, spirals, waves)
- Method 3: System Visualization (CPU, memory, network)
- Method 4: Audio-Reactive Art (music visualization)

## Sharing Your Work

Generated artwork is saved to the `output/` directory by default.
Feel free to share your creations and experiment with different parameters!
