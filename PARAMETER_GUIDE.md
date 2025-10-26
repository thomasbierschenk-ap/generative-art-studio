# Mathematical Patterns - Parameter Guide

## Quick Reference

### Pattern Types
- **spiral**: Archimedean spirals radiating from center
- **wave**: Harmonic sine waves across canvas
- **lissajous**: Parametric curves (figure-8 patterns)
- **fractal_tree**: Recursive branching structures
- **circle_pack**: Collision-based circle placement

### Core Parameters

#### Density (10-500)
- **Low (10-50)**: Sparse, minimal elements
- **Medium (50-150)**: Balanced detail
- **High (150-500)**: Dense, intricate patterns

#### Complexity (0.5-5.0)
- **Low (0.5-1.0)**: Simple, clean patterns
- **Medium (1.0-2.5)**: Moderate intricacy
- **High (2.5-5.0)**: Complex, detailed structures

#### Symmetry (1-12)
- **1**: Single pattern
- **2-4**: Subtle symmetry
- **5-8**: Strong radial symmetry
- **9-12**: Kaleidoscope effect

### New Parameters (2025-10-26)

#### Color Scheme
| Scheme | Effect | Best For |
|--------|--------|----------|
| **gradient** | Smooth hue transition | Flowing, organic patterns |
| **monochrome** | Brightness variation only | Minimalist, elegant |
| **complementary** | Alternating opposite colors | Bold, high contrast |
| **analogous** | Similar hues (±60°) | Harmonious, natural |
| **triadic** | Three colors 120° apart | Vibrant, balanced |
| **random** | Random within variation | Chaotic, energetic |

#### Color Variation (0-100)
- **0-20**: Subtle, cohesive
- **20-50**: Moderate variety
- **50-80**: High diversity
- **80-100**: Maximum variation

#### Organic Factor (0-1)
- **0.0**: Perfect mathematical precision
- **0.1-0.3**: Slight imperfection, hand-drawn feel
- **0.4-0.6**: Noticeably organic, natural
- **0.7-0.9**: Highly irregular, sketch-like
- **1.0**: Maximum randomness

**Effects by Pattern:**
- **Spirals**: Wobbles, uneven spacing
- **Waves**: Phase shifts, amplitude variation
- **Lissajous**: Parameter jitter, organic curves
- **Trees**: Random branch angles, 2-4 branches, asymmetry
- **Circles**: Size variation, organic clustering

#### Completeness (0.3-1.0)
- **0.3-0.5**: Partial, sketch-like
- **0.5-0.7**: Incomplete, artistic
- **0.7-0.9**: Mostly complete
- **1.0**: Full pattern

## Recommended Combinations

### Perfect Mathematical Beauty
```
Pattern: lissajous
Density: 200
Complexity: 2.5
Symmetry: 3
Organic Factor: 0.0
Completeness: 1.0
Color Scheme: gradient
Color Variation: 20
```

### Organic Nature-Inspired
```
Pattern: fractal_tree
Density: 150
Complexity: 2.0
Symmetry: 1
Organic Factor: 0.7
Completeness: 0.8
Color Scheme: analogous
Color Variation: 40
```

### Vibrant Abstract
```
Pattern: spiral
Density: 300
Complexity: 3.5
Symmetry: 6
Organic Factor: 0.3
Completeness: 1.0
Color Scheme: triadic
Color Variation: 70
```

### Minimalist Sketch
```
Pattern: wave
Density: 50
Complexity: 1.5
Symmetry: 2
Organic Factor: 0.5
Completeness: 0.6
Color Scheme: monochrome
Color Variation: 30
```

### Chaotic Energy
```
Pattern: circle_pack
Density: 200
Complexity: 3.0
Symmetry: 4
Organic Factor: 0.8
Completeness: 0.9
Color Scheme: random
Color Variation: 90
```

## Tips for Experimentation

1. **Start Simple**: Begin with default values, adjust one parameter at a time
2. **Organic Factor**: Try 0.0 first, then gradually increase to see effects
3. **Completeness**: Use < 1.0 for interesting partial patterns
4. **Color Schemes**: Match to your aesthetic:
   - Professional/Clean → monochrome, analogous
   - Bold/Modern → complementary, triadic
   - Artistic/Expressive → random
5. **Symmetry**: Higher values work well with lower complexity
6. **Layer Mode**: Combine different patterns and color schemes!

## Performance Notes

- **High Density + High Complexity**: May take longer to generate
- **Fractal Trees**: Complexity affects branch count exponentially
- **Circle Packing**: Higher density requires more collision checks
- **Organic Factor**: Minimal performance impact
- **Live Preview**: Updates every 10 iterations for smooth feedback

## Troubleshooting

**Pattern looks too regular?**
- Increase `organic_factor` to 0.3-0.7
- Try `completeness` < 1.0 for partial patterns

**Colors too similar?**
- Increase `color_variation` to 50-80
- Try different `color_scheme` (triadic, random)

**Pattern too dense/cluttered?**
- Reduce `density` to 50-100
- Reduce `complexity` to 1.0-2.0
- Reduce `symmetry` to 1-3

**Pattern too sparse?**
- Increase `density` to 200-400
- Increase `complexity` to 2.5-4.0
- Increase `symmetry` to 4-8

**Want hand-drawn look?**
- Set `organic_factor` to 0.5-0.8
- Set `completeness` to 0.6-0.8
- Use `monochrome` or `analogous` color scheme
