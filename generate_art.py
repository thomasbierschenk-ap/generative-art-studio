#!/usr/bin/env python3
"""
Simple command-line interface for the Generative Art Studio.
This bypasses the GUI to avoid Tkinter compatibility issues.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from generators.random_walk import RandomWalkGenerator


def print_banner():
    print("\n" + "="*60)
    print("  GENERATIVE ART STUDIO - Command Line Interface")
    print("="*60 + "\n")


def get_input(prompt, default=None, type_func=str):
    """Get user input with optional default value."""
    if default is not None:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    value = input(prompt).strip()
    
    if not value and default is not None:
        return default
    
    if not value:
        return get_input(prompt, default, type_func)
    
    try:
        return type_func(value)
    except ValueError:
        print(f"Invalid input. Please enter a valid {type_func.__name__}.")
        return get_input(prompt, default, type_func)


def main():
    print_banner()
    
    print("Random Walk Generator")
    print("-" * 60)
    print("This generator creates organic, flowing patterns using")
    print("random walk algorithms.\n")
    
    # Get parameters from user
    print("Configuration:")
    print("-" * 60)
    
    num_walks = get_input("Number of walks", 5, int)
    num_steps = get_input("Steps per walk", 100, int)
    step_size = get_input("Step size", 10, int)
    angle_variation = get_input("Angle variation (degrees)", 45, int)
    line_width = get_input("Line width", 2, int)
    
    print("\nColor modes:")
    print("  1. Monochrome (single color)")
    print("  2. Grayscale")
    print("  3. Color (random colors)")
    print("  4. Rainbow")
    color_choice = get_input("Choose color mode (1-4)", 1, int)
    
    color_modes = {1: "monochrome", 2: "grayscale", 3: "color", 4: "rainbow"}
    color_mode = color_modes.get(color_choice, "monochrome")
    
    print("\nStart positions:")
    print("  1. Center")
    print("  2. Random")
    print("  3. Grid")
    start_choice = get_input("Choose start position (1-3)", 1, int)
    
    start_positions = {1: "center", 2: "random", 3: "grid"}
    start_position = start_positions.get(start_choice, "center")
    
    print("\nBoundary behaviors:")
    print("  1. Wrap (continue from opposite side)")
    print("  2. Bounce (reflect off edges)")
    print("  3. Stop (end walk at boundary)")
    boundary_choice = get_input("Choose boundary behavior (1-3)", 1, int)
    
    boundary_behaviors = {1: "wrap", 2: "bounce", 3: "stop"}
    boundary_behavior = boundary_behaviors.get(boundary_choice, "wrap")
    
    width = get_input("\nCanvas width", 800, int)
    height = get_input("Canvas height", 600, int)
    
    output_name = get_input("\nOutput filename (without extension)", "artwork")
    
    # Create generator with parameters
    print("\n" + "="*60)
    print("Generating artwork...")
    print("="*60 + "\n")
    
    generator = RandomWalkGenerator()
    
    # Prepare parameters
    params = {
        'num_walks': num_walks,
        'steps_per_walk': num_steps,
        'step_size': step_size,
        'angle_variation': angle_variation,
        'line_width': line_width,
        'color_mode': color_mode,
        'start_position': start_position,
        'boundary_behavior': boundary_behavior,
        'base_color': '#000000',
        'background_color': '#FFFFFF',
        'add_nodes': False,
        'seed': 0
    }
    
    # Generate and save
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    svg_path = output_dir / f"{output_name}.svg"
    png_path = output_dir / f"{output_name}.png"
    
    try:
        artwork = generator.generate(width, height, params)
        generator.to_svg(artwork, str(svg_path))
        generator.to_png(artwork, str(png_path))
        
        print(f"✓ SVG saved to: {svg_path}")
        print(f"✓ PNG saved to: {png_path}")
        print("\nArtwork generated successfully!\n")
        
    except Exception as e:
        print(f"\n✗ Error generating artwork: {e}\n")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user.\n")
        sys.exit(1)
