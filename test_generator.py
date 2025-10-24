#!/usr/bin/env python3
"""
Test script to verify generator functionality without GUI.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generators import RandomWalkGenerator

def main():
    print("Testing Generative Art Studio - Random Walk Generator")
    print("=" * 60)
    
    # Create generator
    generator = RandomWalkGenerator()
    print(f"\nGenerator: {generator.get_name()}")
    
    # Show parameters
    print("\nAvailable parameters:")
    params = generator.get_parameters()
    for name, definition in params.items():
        print(f"  - {definition.get('label', name)}: {definition.get('help', 'No description')}")
    
    # Generate with default parameters
    print("\nGenerating artwork with default parameters...")
    print("  Size: 800 x 600")
    
    # Get default values
    default_params = {name: def_dict['default'] for name, def_dict in params.items()}
    
    artwork = generator.generate(800, 600, default_params)
    
    print(f"\nGeneration complete!")
    print(f"  Paths created: {len(artwork.paths)}")
    print(f"  Circles created: {len(artwork.circles)}")
    
    # Save outputs
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    svg_path = os.path.join(output_dir, 'test_output.svg')
    png_path = os.path.join(output_dir, 'test_output.png')
    
    print(f"\nSaving outputs...")
    generator.to_svg(artwork, svg_path)
    print(f"  SVG saved: {svg_path}")
    
    generator.to_png(artwork, png_path)
    print(f"  PNG saved: {png_path}")
    
    print("\n✓ Test completed successfully!")
    print(f"\nCheck the output directory to see your generated art:")
    print(f"  {output_dir}")

if __name__ == '__main__':
    main()
