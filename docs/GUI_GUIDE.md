# GUI Guide - Generative Art Studio

## Overview

The Generative Art Studio GUI provides an intuitive interface for creating algorithmic art with real-time visual feedback. The interface is split into two main panels: a control panel on the left and a live preview canvas on the right.

## Features

### Live Preview Canvas

The most exciting feature of the GUI is the **live preview canvas** that shows your artwork being created in real-time:

- **Real-time Visualization**: Watch each random walk being drawn step-by-step as the algorithm runs
- **Progress Tracking**: A progress bar shows the overall completion percentage
- **Automatic Scaling**: The preview automatically scales to fit the canvas while maintaining aspect ratio
- **Responsive**: Resizes smoothly when you adjust the window size

### Control Panel

The left panel provides all the controls you need to customize your artwork:

#### Action Buttons

- **Generate**: Start creating artwork with current parameters
- **Abort**: Stop generation in progress (enabled during generation)
- **Clear Canvas**: Clear the preview and reset workspace
- **Save as PNG**: Export finished artwork as raster image
- **Save as SVG**: Export finished artwork as vector graphics

#### Progress Tracking

The progress section shows real-time information during generation:
- **Progress Bar**: Visual indicator of completion percentage
- **Progress Info**: Displays:
  - Current percentage (e.g., "45%")
  - Estimated time remaining (e.g., "Est. time remaining: 2m 15s")
  - Time format adjusts based on duration (seconds, minutes, hours)
- **Status Messages**: Current operation status
  - "Ready" - Waiting to generate
  - "Generating..." - Creation in progress
  - "Generation complete! (took 3.2s)" - Finished with total time
  - "Generation aborted by user" - Stopped by user
  - "Canvas cleared" - Workspace reset

#### Output Size
- **Width**: Set the output width in pixels (default: 800)
- **Height**: Set the output height in pixels (default: 600)

#### Generator Parameters

Each parameter is presented with an appropriate control:

**Sliders** (for numeric values):
- Drag the slider to adjust values
- Current value is displayed next to the slider
- Supports both integer and floating-point values

**Dropdowns** (for choices):
- Click to see available options
- Select from predefined choices

**Checkboxes** (for boolean options):
- Click to toggle on/off

**Color Pickers**:
- Visual preview of the current color
- Click "Pick" to open a color chooser dialog
- Or manually enter hex color codes (e.g., #FF0000)

### Random Walk Parameters

When using the Random Walk generator, you can adjust:

- **Number of Walks**: How many separate walks to generate (1-50)
- **Steps per Walk**: Length of each walk (10-10,000 steps)
- **Step Size**: Distance of each step in pixels (0.5-50)
- **Angle Variation**: Maximum angle change between steps (0-360°)
  - 0° = straight line
  - 180° = smooth curves
  - 360° = completely random direction
- **Line Width**: Thickness of the drawn lines (0.1-10)
- **Color Mode**: Choose from:
  - Monochrome: Single color
  - Grayscale: Varying shades of gray
  - Color: Random colors
  - Rainbow: HSV spectrum
- **Base Color**: Primary color (used in monochrome mode)
- **Background Color**: Canvas background
- **Start Position**: Where walks begin:
  - Center: All walks start from the center
  - Random: Random starting positions
  - Edges: Start from canvas edges
  - Corners: Start from canvas corners
- **Boundary Behavior**: What happens at edges:
  - Bounce: Reflect off boundaries
  - Wrap: Wrap around to opposite side
  - Stop: End the walk
  - Ignore: Continue beyond boundaries
- **Show Nodes**: Draw circles at walk endpoints
- **Random Seed**: For reproducible results (0 = random)

## Workflow

### Basic Usage

1. **Launch the GUI**:
   ```bash
   ./run_gui_modern.sh
   ```

2. **Set Output Size**: Enter desired width and height

3. **Adjust Parameters**: Use the sliders and controls to customize your artwork

4. **Generate**: Click the "Generate" button

5. **Watch**: The preview canvas will show the artwork being created in real-time
   - You'll see each random walk being drawn
   - The progress bar updates as generation proceeds
   - Progress info shows percentage and estimated time remaining
   - Status messages keep you informed

6. **Control Generation** (optional):
   - Click "Abort" to stop generation at any time
   - Click "Clear Canvas" to reset and start fresh
   - Time estimates update dynamically as generation progresses

7. **Save**: Once complete, use the save buttons:
   - "Save as PNG" for raster graphics
   - "Save as SVG" for vector graphics

### Tips for Best Results

**For Interesting Patterns:**
- Try multiple walks (5-20) with different color modes
- Experiment with angle variation:
  - 30-90° for flowing, organic shapes
  - 120-180° for more chaotic patterns
- Use "bounce" boundary behavior for contained compositions

**For Performance:**
- Start with fewer steps (100-500) while experimenting
- Increase to 1000-5000 for final artwork
- The live preview updates every ~50 steps to maintain responsiveness

**For Reproducibility:**
- Set a specific random seed (any number > 0)
- Save your parameter settings by noting them down
- Use the same seed to recreate the exact same artwork

### Color Schemes

**Monochrome:**
- Clean, minimalist look
- Great for printing
- Try black on white or white on black

**Grayscale:**
- Creates depth through value variation
- Each walk gets a different shade
- Works well with many walks

**Color:**
- Vibrant, energetic compositions
- Each walk gets a random color
- Best with 5-15 walks

**Rainbow:**
- Smooth color transitions
- Walks progress through the spectrum
- Beautiful with many walks (10-30)

## Technical Details

### Performance

The GUI runs generation in a background thread to keep the interface responsive:
- The main UI thread handles user interactions
- A worker thread performs the generation
- Progress callbacks update the preview without blocking

### Preview Rendering

The preview canvas uses PIL (Pillow) for rendering:
- Artwork is rendered to an in-memory image
- Image is scaled to fit the canvas
- Updates occur periodically during generation
- Final render happens when generation completes

### Threading Model

```
Main Thread (GUI)          Worker Thread (Generation)
     |                              |
     |-- Click Generate ----------->|
     |                              |-- Start generation
     |<-- Progress Update ----------|-- Send progress
     |-- Update canvas              |
     |<-- Progress Update ----------|
     |-- Update canvas              |
     |                              |
     |<-- Complete ----------------|-- Finish
     |-- Enable save buttons        |
```

## Troubleshooting

### GUI Won't Launch

**Error: "macOS 26 (2600) or later required"**
- Your system Python's Tkinter is too old
- Use `./run_gui_modern.sh` instead of `./run_gui.sh`
- Or use the CLI interface: `./create_art.sh`

**Error: "No module named '_tkinter'"**
- Tkinter is not installed
- Install with: `brew install python-tk@3.13`
- Or use the CLI interface

### Preview Not Updating

- Check that generation is running (progress bar should be moving)
- Try with fewer steps to see updates more clearly
- Ensure the window is visible and not minimized

### Slow Performance

- Reduce steps per walk
- Reduce number of walks
- Use thinner lines (line width < 2)
- Close other applications

### Save Button Disabled

- Wait for generation to complete
- Progress bar should reach 100%
- Status should say "Generation complete!"

## Keyboard Shortcuts

Currently, the GUI uses mouse-based interaction. Future versions may include:
- Ctrl+G: Generate
- Ctrl+S: Save PNG
- Ctrl+Shift+S: Save SVG
- Ctrl+R: Randomize parameters

## Future Enhancements

Planned improvements for the GUI:
- Multiple generator selection
- Parameter presets
- Undo/redo functionality
- Animation export
- Batch generation
- Gallery view of previous works
- Parameter randomization
- Export settings (DPI, quality)

## Comparison: GUI vs CLI

**Use the GUI when:**
- You want to see the artwork being created
- You're experimenting with parameters
- You want immediate visual feedback
- You enjoy the interactive experience

**Use the CLI when:**
- You know exactly what you want
- You're generating multiple artworks
- You're on a system without GUI support
- You're automating generation

Both interfaces use the same underlying generator code, so the output quality is identical.
