# Mathematical Patterns Guide

A visual guide to the 5 pattern types available in the Mathematical Patterns Generator.

## Pattern Types Overview

| Pattern | Best For | Complexity | Speed |
|---------|----------|------------|-------|
| **Spiral** | Hypnotic, flowing designs | Low-Medium | Fast |
| **Wave** | Rhythmic, harmonic patterns | Medium | Fast |
| **Lissajous** | Elegant mathematical curves | Medium | Fast |
| **Fractal Tree** | Organic, natural structures | High | Medium |
| **Circle Pack** | Textural, bubble-like art | Medium-High | Slow |

---

## 1. Spiral Patterns

### Description
Archimedean spirals that grow outward from the center. The complexity parameter controls how tightly the spiral winds.

### Visual Characteristics
- Smooth, continuous curves
- Radiates from center point
- Can create galaxy-like or shell-like patterns
- Symmetry creates flower-like designs

### Best Parameters
```
Density: 150-300
Complexity: 1.0-3.0
Symmetry: 1 (single), 3-6 (flower), 8-12 (mandala)
```

### Use Cases
- Hypnotic backgrounds
- Mandala-like designs
- Galaxy simulations
- Shell patterns
- Vortex effects

### Tips
- Complexity = 1.618 (golden ratio) for natural spirals
- High symmetry (6-12) creates beautiful mandalas
- Try gradient colors for depth
- Layer with Random Walk for organic contrast

---

## 2. Wave Patterns

### Description
Harmonic wave patterns created by combining multiple sine waves at different frequencies. Creates flowing, rhythmic designs.

### Visual Characteristics
- Horizontal flowing lines
- Multiple frequency harmonics
- Wave interference patterns
- Can create ocean-like or sound-like visuals

### Best Parameters
```
Density: 100-200
Complexity: 2.0-4.0 (number of harmonics)
Symmetry: 1-4
```

### Use Cases
- Ocean waves
- Sound visualization
- Rhythmic backgrounds
- Textile patterns
- Abstract landscapes

### Tips
- Complexity controls number of harmonics (higher = more complex)
- Symmetry creates multiple wave layers
- Works great with blue/teal colors for ocean themes
- Try layering waves with different complexities

---

## 3. Lissajous Curves

### Description
Beautiful parametric curves created by combining two perpendicular sine waves. Named after Jules Antoine Lissajous.

### Visual Characteristics
- Closed loop curves
- Figure-8 and infinity-like shapes
- Elegant mathematical beauty
- Smooth, flowing lines

### Best Parameters
```
Density: 100-300
Complexity: 1.0-4.0
Symmetry: 1-4
```

### Use Cases
- Elegant logos
- Mathematical art
- Oscilloscope-like patterns
- Abstract designs
- Scientific visualization

### Tips
- Complexity controls the frequency ratio
- Integer complexity values create closed curves
- Non-integer values create more complex patterns
- Beautiful with gradient colors
- Try symmetry = 1 for classic Lissajous curves

---

## 4. Fractal Tree

### Description
Recursive branching structures that mimic natural tree growth. Each branch splits into two smaller branches.

### Visual Characteristics
- Organic, natural branching
- Self-similar at different scales
- Tree-like or root-like structures
- Dense, intricate patterns

### Best Parameters
```
Density: 50-150 (controls starting branch length)
Complexity: 2.0-4.5 (controls recursion depth)
Symmetry: 1-4
```

### Use Cases
- Tree and forest scenes
- Root systems
- Vein patterns
- Lightning bolts
- Natural organic structures

### Tips
- Complexity controls depth (higher = more branches)
- Keep complexity < 5.0 to avoid slowdown
- Symmetry creates multiple trees
- Green/brown colors for natural look
- Black background with white/gold trees is striking
- Gradient creates depth effect

### Warning
- High complexity (>4.5) generates many branches and may be slow
- Maximum depth is limited to 12 to prevent stack overflow

---

## 5. Circle Pack

### Description
Organic circle packing algorithm that fills space with non-overlapping circles of varying sizes.

### Visual Characteristics
- Bubble-like appearance
- Organic, natural spacing
- Varied circle sizes
- Textural quality

### Best Parameters
```
Density: 100-400 (target number of circles)
Complexity: 1.0-3.0 (affects size variation)
Symmetry: 1-8
```

### Use Cases
- Bubble art
- Organic textures
- Cell-like patterns
- Foam structures
- Abstract backgrounds

### Tips
- Higher density = more circles (but slower)
- Complexity affects size variation
- Symmetry creates radial repetition
- May not achieve full density if canvas is crowded
- Works beautifully with pastel colors
- Try layering with other patterns for texture

### Warning
- Can be slow with density > 400
- May terminate early if no space for more circles

---

## Combining Patterns (Layer Mode)

### Recommended Combinations

#### 1. Geometric + Organic
```
Layer 1: Spiral (symmetry=6, complexity=2.0)
Layer 2: Random Walk (organic flow)
Result: Structured geometry with organic overlay
```

#### 2. Double Spirals
```
Layer 1: Spiral (complexity=1.0, color=#FF6B6B)
Layer 2: Spiral (complexity=2.0, color=#4ECDC4)
Result: Interwoven spirals with color contrast
```

#### 3. Waves + Trees
```
Layer 1: Wave (complexity=3.0, color=#2E86AB)
Layer 2: Fractal Tree (complexity=3.5, color=#A23B72)
Result: Natural elements combined
```

#### 4. Lissajous + Circle Pack
```
Layer 1: Lissajous (complexity=3.14, color=#F18F01)
Layer 2: Circle Pack (density=200, color=#C73E1D)
Result: Elegant curves with textural overlay
```

#### 5. Mathematical Mandala
```
Layer 1: Spiral (symmetry=8, color=#6A4C93)
Layer 2: Wave (symmetry=8, color=#1982C4)
Layer 3: Lissajous (symmetry=8, color=#FF595E)
Result: Complex symmetrical mandala
```

---

## Parameter Deep Dive

### Density
- **Spiral/Wave/Lissajous**: Number of points in the path
  - Low (50-100): Rough, angular
  - Medium (100-200): Smooth
  - High (200-500): Very smooth
  
- **Fractal Tree**: Starting branch length
  - Low (50-100): Short, compact trees
  - High (150-200): Tall, expansive trees
  
- **Circle Pack**: Target number of circles
  - Low (50-100): Sparse, large circles
  - High (300-500): Dense, varied sizes

### Complexity
- **Spiral**: How tightly wound (0.5 = loose, 5.0 = tight)
- **Wave**: Number of harmonic frequencies (1.0 = simple, 5.0 = complex)
- **Lissajous**: Frequency ratio (1.0-5.0, integers create closed curves)
- **Fractal Tree**: Recursion depth (2.0 = shallow, 4.5 = deep)
- **Circle Pack**: Size variation factor (1.0 = uniform, 3.0 = varied)

### Symmetry
Creates radial repetition of the pattern:
- **1**: Single pattern
- **2**: Mirror symmetry
- **3**: Triangular
- **4**: Square/cross
- **6**: Hexagonal (honeycomb)
- **8**: Octagonal
- **12**: Dodecagonal (mandala-like)

### Color Gradient
When enabled:
- Colors shift smoothly across the pattern
- Based on element index or depth
- Creates sense of depth and flow
- Works with any base color

---

## Performance Guide

### Fast Patterns (< 1 second)
- Spiral with density < 200
- Wave with density < 200
- Lissajous with density < 200

### Medium Speed (1-3 seconds)
- Spiral with high density (300-500)
- Fractal Tree with complexity < 4.0
- Circle Pack with density < 200

### Slower Patterns (3-10 seconds)
- Fractal Tree with complexity > 4.0
- Circle Pack with density > 300
- High symmetry (>8) with complex patterns

### Optimization Tips
1. Start with low density/complexity
2. Increase gradually to find sweet spot
3. Use abort button if it's taking too long
4. Lower symmetry for faster generation
5. Circle pack is slowest - be patient!

---

## Color Palette Suggestions

### Natural
```
Spiral: #228B22 (forest green)
Wave: #4682B4 (steel blue)
Tree: #8B4513 (saddle brown)
Background: #F0F8FF (alice blue)
```

### Vibrant
```
Spiral: #FF1493 (deep pink)
Wave: #00CED1 (dark turquoise)
Tree: #FFD700 (gold)
Background: #000000 (black)
```

### Pastel
```
Spiral: #FFB6C1 (light pink)
Wave: #B0E0E6 (powder blue)
Circle Pack: #DDA0DD (plum)
Background: #FFFAF0 (floral white)
```

### Monochrome
```
All patterns: #FFFFFF (white)
Background: #000000 (black)
Enable gradient: Yes
```

### Sunset
```
Spiral: #FF6B6B (coral)
Wave: #FFA500 (orange)
Tree: #FFD700 (gold)
Background: #4A0E4E (deep purple)
```

---

## Troubleshooting

### Pattern looks rough/angular
- **Solution**: Increase density

### Pattern is too simple
- **Solution**: Increase complexity

### Generation is too slow
- **Solution**: Decrease density or complexity

### Circles aren't filling the canvas
- **Solution**: Increase density or decrease complexity

### Fractal tree is too dense
- **Solution**: Decrease complexity

### Colors look flat
- **Solution**: Enable "Use Color Gradient"

### Pattern is cut off
- **Solution**: Decrease complexity or adjust symmetry

---

## Advanced Techniques

### 1. Gradient Mastery
- Use gradient to show depth in fractals
- Create rainbow effects with high symmetry
- Combine gradient patterns in layers

### 2. Symmetry Exploration
- Try prime numbers (3, 5, 7, 11) for unique patterns
- Even numbers (4, 6, 8, 12) for traditional mandalas
- Symmetry = 1 for asymmetric, organic feel

### 3. Layer Blending
- Start with low-complexity base layer
- Add high-complexity detail layer
- Finish with accent elements (circles, etc.)

### 4. Color Theory
- Complementary colors for vibrant contrast
- Analogous colors for harmony
- Monochrome with gradient for elegance

### 5. Negative Space
- Use white patterns on black background
- Leave areas empty for visual breathing room
- Balance dense and sparse regions

---

## Inspiration Gallery

### Suggested Experiments

1. **Cosmic Spiral**: Spiral, complexity=2.0, symmetry=1, purple gradient on black
2. **Ocean Waves**: Wave, complexity=3.0, symmetry=2, blue gradient on light blue
3. **Sacred Geometry**: Lissajous, complexity=3.0, symmetry=6, gold on deep blue
4. **Forest**: Fractal Tree, complexity=4.0, symmetry=3, green gradient on cream
5. **Bubble Bath**: Circle Pack, density=300, symmetry=1, pastel pink on white
6. **Mandala**: Spiral, symmetry=12, complexity=1.5, rainbow gradient on black
7. **Sound Waves**: Wave, complexity=4.0, symmetry=1, turquoise gradient on dark
8. **Flower of Life**: Lissajous, symmetry=6, complexity=2.0, purple on white
9. **Lightning**: Fractal Tree, complexity=4.5, symmetry=1, white on black
10. **Cells**: Circle Pack, density=400, symmetry=4, various colors

---

## Conclusion

The Mathematical Patterns Generator offers endless creative possibilities. Experiment with different combinations, layer patterns, and explore the parameter space to discover unique artworks!

**Remember**: There are no wrong settings - only different artistic expressions! 🎨

Happy creating!
