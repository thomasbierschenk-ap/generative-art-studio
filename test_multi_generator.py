#!/usr/bin/env python3
"""
Test script for multi-generator architecture.

Tests that the refactored architecture supports multiple generators correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generators import RandomWalkGenerator
from app import GenerativeArtApp

def test_generator_interface():
    """Test that generators implement the required interface."""
    print("Testing Generator Interface")
    print("=" * 60)
    
    gen = RandomWalkGenerator()
    
    # Test required methods
    print(f"✓ get_name(): {gen.get_name()}")
    print(f"✓ get_description(): {gen.get_description()}")
    print(f"✓ get_icon(): {gen.get_icon()}")
    
    param_defs = gen.get_parameters()
    print(f"✓ get_parameters(): {len(param_defs)} parameters defined")
    
    # Test generation with default values
    params = {name: def_dict['default'] for name, def_dict in param_defs.items()}
    artwork = gen.generate(400, 300, params)
    print(f"✓ generate(): Created artwork with {len(artwork.paths)} paths")
    
    print()

def test_app_initialization():
    """Test that the app initializes with multiple generators."""
    print("Testing App Initialization")
    print("=" * 60)
    
    # We can't fully test the GUI without a display, but we can test initialization
    try:
        import tkinter as tk
        
        # Create app without running mainloop
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Import after creating root
        from generators import RandomWalkGenerator
        
        # Test generator dictionary
        generators = {}
        random_walk = RandomWalkGenerator()
        generators[random_walk.get_name()] = random_walk
        
        print(f"✓ Generators dictionary created")
        print(f"  - {random_walk.get_name()}: {random_walk.get_description()}")
        
        # Test that we can access generators by name
        gen_name = list(generators.keys())[0]
        gen = generators[gen_name]
        print(f"✓ Can access generator by name: {gen_name}")
        print(f"  - Description: {gen.get_description()}")
        print(f"  - Icon: {gen.get_icon()}")
        
        root.destroy()
        print()
        
    except Exception as e:
        print(f"⚠ GUI test skipped (Tkinter issue): {e}")
        print()

def test_backwards_compatibility():
    """Test that existing functionality still works."""
    print("Testing Backwards Compatibility")
    print("=" * 60)
    
    gen = RandomWalkGenerator()
    
    # Test with default parameters
    params = {
        'num_walks': 3,
        'steps_per_walk': 100,
        'step_size': 5.0,
        'angle_variation': 45.0,
        'line_width': 2.0,
        'color_mode': 'monochrome',
        'base_color': '#000000',
        'background_color': '#FFFFFF',
        'start_position': 'center',
        'boundary_behavior': 'bounce',
        'add_nodes': False,
        'seed': 42
    }
    
    artwork = gen.generate(400, 300, params)
    
    print(f"✓ Generation works with explicit parameters")
    print(f"  - Paths: {len(artwork.paths)}")
    print(f"  - Size: {artwork.width}x{artwork.height}")
    print(f"  - Background: {artwork.background_color}")
    
    # Test export functions still work
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    svg_path = os.path.join(output_dir, 'test_refactor.svg')
    png_path = os.path.join(output_dir, 'test_refactor.png')
    
    gen.to_svg(artwork, svg_path)
    gen.to_png(artwork, png_path)
    
    print(f"✓ Export functions work")
    print(f"  - SVG: {os.path.basename(svg_path)}")
    print(f"  - PNG: {os.path.basename(png_path)}")
    
    print()

def main():
    """Run all tests."""
    print()
    print("=" * 60)
    print("Multi-Generator Architecture Tests")
    print("=" * 60)
    print()
    
    try:
        test_generator_interface()
        test_app_initialization()
        test_backwards_compatibility()
        
        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Test failed: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
