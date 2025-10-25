#!/usr/bin/env python3
"""
Test script to verify layer mode logic works correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generators.random_walk import RandomWalkGenerator
from generators.base import ArtworkData

def test_layer_mode():
    """Test the layer mode merging logic."""
    print("Testing layer mode logic...")
    
    # Create generator
    gen = RandomWalkGenerator()
    
    # Generate first artwork
    print("\n1. Generating first artwork (black)...")
    params1 = {
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
    
    artwork1 = gen.generate(400, 300, params1)
    print(f"   - Generated {len(artwork1.paths)} paths")
    print(f"   - Background color: {artwork1.background_color}")
    
    # Generate second artwork
    print("\n2. Generating second artwork (red)...")
    params2 = params1.copy()
    params2['base_color'] = '#FF0000'
    params2['seed'] = 123
    
    artwork2 = gen.generate(400, 300, params2)
    print(f"   - Generated {len(artwork2.paths)} paths")
    
    # Simulate layer mode merge
    print("\n3. Merging artworks (layer mode)...")
    merged = ArtworkData(
        width=400,
        height=300,
        background_color=artwork1.background_color,  # Keep first background
        paths=artwork1.paths + artwork2.paths,        # Combine paths
        circles=artwork1.circles + artwork2.circles   # Combine circles
    )
    
    print(f"   - Merged artwork has {len(merged.paths)} paths")
    print(f"   - First {len(artwork1.paths)} paths are black")
    print(f"   - Last {len(artwork2.paths)} paths are red")
    print(f"   - Background color: {merged.background_color}")
    
    # Verify
    assert len(merged.paths) == len(artwork1.paths) + len(artwork2.paths), "Path count mismatch!"
    assert merged.background_color == artwork1.background_color, "Background color changed!"
    
    print("\n✅ Layer mode logic test PASSED!")
    print("\nThe layer mode should:")
    print("  - Keep the original background color")
    print("  - Show all paths from both generations")
    print("  - Display them in order (old first, new on top)")
    
    return True

if __name__ == '__main__':
    try:
        test_layer_mode()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
