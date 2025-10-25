#!/usr/bin/env python3
"""
Test script for Mathematical Patterns Generator
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generators.mathematical import MathematicalPatternsGenerator

def test_generator():
    """Test the mathematical patterns generator."""
    print("Testing Mathematical Patterns Generator...")
    print("=" * 60)
    
    gen = MathematicalPatternsGenerator()
    
    # Test basic properties
    print(f"\n✓ Generator Name: {gen.get_name()}")
    print(f"✓ Description: {gen.get_description()}")
    print(f"✓ Icon: {gen.get_icon()}")
    
    # Test parameters
    params = gen.get_parameters()
    print(f"\n✓ Parameters defined: {len(params)}")
    for param_name, param_def in params.items():
        print(f"  - {param_name}: {param_def.get('label', param_name)}")
    
    # Test each pattern type
    pattern_types = ['spiral', 'wave', 'lissajous', 'fractal_tree', 'circle_pack']
    
    for pattern_type in pattern_types:
        print(f"\n✓ Testing pattern: {pattern_type}")
        
        # Build parameters with defaults
        test_params = {}
        for param_name, param_def in params.items():
            test_params[param_name] = param_def.get('default')
        
        # Override pattern type
        test_params['pattern_type'] = pattern_type
        test_params['density'] = 50  # Lower density for faster testing
        
        # Progress callback
        def progress_callback(artwork, progress, status):
            if int(progress) % 25 == 0:
                print(f"    Progress: {progress:.0f}% - {status}")
        
        # Generate artwork
        try:
            artwork = gen.generate(800, 600, test_params, progress_callback)
            print(f"    ✓ Generated {len(artwork.paths)} paths, {len(artwork.circles)} circles")
        except Exception as e:
            print(f"    ✗ Error: {e}")
            return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    return True

if __name__ == '__main__':
    success = test_generator()
    sys.exit(0 if success else 1)
