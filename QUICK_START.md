# Quick Start Guide

## Create Your First Artwork (30 seconds)

```bash
cd generative-art-studio
./create_art.sh
```

Just press Enter to accept defaults, or customize the parameters!

## What You'll See

```
============================================================
  GENERATIVE ART STUDIO - Command Line Interface
============================================================

Random Walk Generator
------------------------------------------------------------
This generator creates organic, flowing patterns using
random walk algorithms.

Configuration:
------------------------------------------------------------
Number of walks [5]: 
Steps per walk [100]: 
Step size [10]: 
Angle variation (degrees) [45]: 
Line width [2]: 

Color modes:
  1. Monochrome (single color)
  2. Grayscale
  3. Color (random colors)
  4. Rainbow
Choose color mode (1-4) [1]: 4

Start positions:
  1. Center
  2. Random
  3. Grid
Choose start position (1-3) [1]: 

Boundary behaviors:
  1. Wrap (continue from opposite side)
  2. Bounce (reflect off edges)
  3. Stop (end walk at boundary)
Choose boundary behavior (1-3) [1]: 

Canvas width [800]: 
Canvas height [600]: 

Output filename (without extension) [artwork]: my_first_art

============================================================
Generating artwork...
============================================================

✓ SVG saved to: output/my_first_art.svg
✓ PNG saved to: output/my_first_art.png

Artwork generated successfully!
```

## Your Files

Check the `output/` directory:

```bash
ls -lh output/
```

You'll find:
- `my_first_art.svg` - Vector graphics (scalable, editable)
- `my_first_art.png` - Raster image (ready to share)

## Try Different Styles

### Smooth & Flowing
```
Number of walks: 5
Steps per walk: 200
Step size: 8
Angle variation: 20
Color mode: 4 (Rainbow)
```

### Chaotic & Energetic
```
Number of walks: 15
Steps per walk: 100
Step size: 15
Angle variation: 75
Color mode: 3 (Color)
Start position: 2 (Random)
```

### Minimalist
```
Number of walks: 3
Steps per walk: 300
Step size: 5
Angle variation: 30
Line width: 1
Color mode: 1 (Monochrome)
```

## Tips

1. **Press Enter** to use the default value shown in brackets `[like this]`
2. **Experiment!** Each generation is unique due to randomness
3. **Save favorites** with descriptive names
4. **Generate multiple** versions to find the perfect one

## Try the GUI (With Live Preview!)

If you have a compatible Tkinter installation, try the GUI to watch your artwork being created in real-time:

```bash
./run_gui_modern.sh
```

The GUI features:
- **Live preview canvas** - watch each random walk being drawn step-by-step
- **Real-time progress** - see the artwork evolve as it's generated
- **Interactive controls** - sliders and color pickers for easy parameter adjustment
- **Instant feedback** - see the results before saving

See [GUI_GUIDE.md](docs/GUI_GUIDE.md) for detailed GUI instructions.

## What's Next?

- Read [CLI_GUIDE.md](docs/CLI_GUIDE.md) for detailed parameter explanations
- Read [GUI_GUIDE.md](docs/GUI_GUIDE.md) for GUI features and tips
- Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand how it works
- See [DEVELOPMENT.md](docs/DEVELOPMENT.md) to add new generators

## Need Help?

- **Tkinter/GUI issues?** See [TKINTER_ISSUE.md](TKINTER_ISSUE.md)
- **Installation problems?** See [INSTALL.md](INSTALL.md)
- **General info?** See [README.md](README.md)

## One-Line Examples

```bash
# Accept all defaults (creates artwork.svg and artwork.png)
yes "" | ./create_art.sh

# Quick test with predefined settings
./run_test.sh

# View your creations
open output/*.png
```

---

**That's it! You're ready to create generative art. Have fun! 🎨**
