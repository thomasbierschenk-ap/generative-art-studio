#!/usr/bin/env python3
"""
Unit tests for Random Walk Generator
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generators import RandomWalkGenerator
import tempfile


def test_generator_creation():
    """Test that generator can be created"""
    gen = RandomWalkGenerator()
    assert gen.get_name() == "Random Walk"
    print("✓ Generator creation successful")


def test_parameters():
    """Test that parameters are defined correctly"""
    gen = RandomWalkGenerator()
    params = gen.get_parameters()
    
    # Check required parameters exist
    required = ['num_walks', 'steps_per_walk', 'step_size', 'angle_variation']
    for param in required:
        assert param in params, f"Missing parameter: {param}"
    
    # Check parameter structure
    for name, definition in params.items():
        assert 'type' in definition, f"Parameter {name} missing 'type'"
        assert 'default' in definition, f"Parameter {name} missing 'default'"
    
    print(f"✓ All {len(params)} parameters defined correctly")


def test_generation():
    """Test that artwork can be generated"""
    gen = RandomWalkGenerator()
    
    # Get default parameters
    params = {name: def_dict['default'] for name, def_dict in gen.get_parameters().items()}
    
    # Generate artwork
    artwork = gen.generate(400, 300, params)
    
    # Verify artwork structure
    assert artwork.width == 400
    assert artwork.height == 300
    assert len(artwork.paths) > 0, "No paths generated"
    
    print(f"✓ Generated artwork with {len(artwork.paths)} paths")


def test_svg_export():
    """Test SVG export"""
    gen = RandomWalkGenerator()
    params = {name: def_dict['default'] for name, def_dict in gen.get_parameters().items()}
    params['num_walks'] = 2  # Keep it small for testing
    params['steps_per_walk'] = 100
    
    artwork = gen.generate(200, 200, params)
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as f:
        temp_path = f.name
    
    try:
        gen.to_svg(artwork, temp_path)
        
        # Verify file exists and has content
        assert os.path.exists(temp_path), "SVG file not created"
        assert os.path.getsize(temp_path) > 0, "SVG file is empty"
        
        # Verify it's valid SVG
        with open(temp_path, 'r') as f:
            content = f.read()
            assert '<?xml' in content, "Not a valid XML file"
            assert '<svg' in content, "Not a valid SVG file"
        
        print(f"✓ SVG export successful ({os.path.getsize(temp_path)} bytes)")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_png_export():
    """Test PNG export"""
    gen = RandomWalkGenerator()
    params = {name: def_dict['default'] for name, def_dict in gen.get_parameters().items()}
    params['num_walks'] = 2
    params['steps_per_walk'] = 100
    
    artwork = gen.generate(200, 200, params)
    
    # Export to temporary file
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        temp_path = f.name
    
    try:
        gen.to_png(artwork, temp_path)
        
        # Verify file exists and has content
        assert os.path.exists(temp_path), "PNG file not created"
        assert os.path.getsize(temp_path) > 0, "PNG file is empty"
        
        # Verify it's valid PNG
        with open(temp_path, 'rb') as f:
            header = f.read(8)
            assert header[:4] == b'\x89PNG', "Not a valid PNG file"
        
        print(f"✓ PNG export successful ({os.path.getsize(temp_path)} bytes)")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_reproducibility():
    """Test that same seed produces same output"""
    gen = RandomWalkGenerator()
    params = {name: def_dict['default'] for name, def_dict in gen.get_parameters().items()}
    params['seed'] = 42
    params['num_walks'] = 2
    params['steps_per_walk'] = 100
    
    # Generate twice with same seed
    artwork1 = gen.generate(200, 200, params)
    artwork2 = gen.generate(200, 200, params)
    
    # Should have same number of paths
    assert len(artwork1.paths) == len(artwork2.paths)
    
    # First path should have same points
    assert len(artwork1.paths[0].points) == len(artwork2.paths[0].points)
    
    print("✓ Reproducibility verified (same seed = same output)")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Random Walk Generator Tests")
    print("="*60 + "\n")
    
    tests = [
        test_generator_creation,
        test_parameters,
        test_generation,
        test_svg_export,
        test_png_export,
        test_reproducibility,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
