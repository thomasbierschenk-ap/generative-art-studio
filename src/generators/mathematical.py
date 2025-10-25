"""
Mathematical Patterns Generator

Generates artwork using mathematical formulas and geometric patterns.
Includes spirals, waves, fractals, Lissajous curves, and circle packing.
"""

import math
import random
from typing import Dict, Any, Callable
import numpy as np

from .base import BaseGenerator, ArtworkData


class MathematicalPatternsGenerator(BaseGenerator):
    """Generator for mathematical and geometric patterns."""
    
    def get_name(self) -> str:
        return "Mathematical Patterns"
    
    def get_description(self) -> str:
        return "Geometric patterns using mathematical formulas: spirals, waves, fractals, and more"
    
    def get_icon(self) -> str:
        return "📐"
    
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            'pattern_type': {
                'type': 'choice',
                'default': 'spiral',
                'choices': ['spiral', 'wave', 'lissajous', 'fractal_tree', 'circle_pack'],
                'label': 'Pattern Type',
                'help': 'Type of mathematical pattern to generate'
            },
            'density': {
                'type': 'int',
                'default': 100,
                'min': 10,
                'max': 500,
                'label': 'Density',
                'help': 'Number of elements or iterations'
            },
            'complexity': {
                'type': 'float',
                'default': 1.5,
                'min': 0.5,
                'max': 5.0,
                'label': 'Complexity',
                'help': 'Pattern complexity factor'
            },
            'symmetry': {
                'type': 'int',
                'default': 1,
                'min': 1,
                'max': 12,
                'label': 'Symmetry',
                'help': 'Number of symmetrical repetitions'
            },
            'line_width': {
                'type': 'float',
                'default': 2.0,
                'min': 0.5,
                'max': 10.0,
                'label': 'Line Width',
                'help': 'Width of drawn lines'
            },
            'color': {
                'type': 'color',
                'default': '#2E86AB',
                'label': 'Primary Color',
                'help': 'Main color for the pattern'
            },
            'use_gradient': {
                'type': 'bool',
                'default': True,
                'label': 'Use Color Gradient',
                'help': 'Gradually shift colors through the pattern'
            },
            'background_color': {
                'type': 'color',
                'default': '#FFFFFF',
                'label': 'Background Color',
                'help': 'Canvas background color'
            }
        }
    
    def generate(
        self,
        width: int,
        height: int,
        params: Dict[str, Any],
        progress_callback: Callable[[ArtworkData, float, str], None] = None,
        should_abort: Callable[[], bool] = None
    ) -> ArtworkData:
        """Generate mathematical pattern artwork."""
        
        # Extract parameters
        pattern_type = params.get('pattern_type', 'spiral')
        density = params.get('density', 100)
        complexity = params.get('complexity', 1.5)
        symmetry = params.get('symmetry', 1)
        line_width = params.get('line_width', 2.0)
        color = params.get('color', '#2E86AB')
        use_gradient = params.get('use_gradient', True)
        bg_color = params.get('background_color', '#FFFFFF')
        
        # Initialize artwork
        artwork = ArtworkData(
            width=width,
            height=height,
            background_color=bg_color
        )
        
        # Generate pattern based on type
        if pattern_type == 'spiral':
            self._generate_spiral(artwork, density, complexity, symmetry, 
                                line_width, color, use_gradient, 
                                progress_callback, should_abort)
        elif pattern_type == 'wave':
            self._generate_wave(artwork, density, complexity, symmetry,
                              line_width, color, use_gradient,
                              progress_callback, should_abort)
        elif pattern_type == 'lissajous':
            self._generate_lissajous(artwork, density, complexity, symmetry,
                                   line_width, color, use_gradient,
                                   progress_callback, should_abort)
        elif pattern_type == 'fractal_tree':
            self._generate_fractal_tree(artwork, density, complexity, symmetry,
                                      line_width, color, use_gradient,
                                      progress_callback, should_abort)
        elif pattern_type == 'circle_pack':
            self._generate_circle_pack(artwork, density, complexity, symmetry,
                                     line_width, color, use_gradient,
                                     progress_callback, should_abort)
        
        return artwork
    
    def _generate_spiral(self, artwork: ArtworkData, density: int, complexity: float,
                        symmetry: int, line_width: float, color: str, use_gradient: bool,
                        progress_callback: Callable, should_abort: Callable):
        """Generate spiral patterns."""
        cx, cy = artwork.width / 2, artwork.height / 2
        max_radius = min(artwork.width, artwork.height) * 0.4
        
        for sym in range(symmetry):
            if should_abort and should_abort():
                break
                
            angle_offset = (2 * math.pi * sym) / symmetry
            path_points = []
            
            for i in range(density):
                if should_abort and should_abort():
                    break
                
                t = i / density
                angle = t * complexity * 2 * math.pi + angle_offset
                radius = t * max_radius
                
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                path_points.append((x, y))
                
                # Progress update
                if progress_callback and i % 10 == 0:
                    progress = ((sym * density + i) / (symmetry * density)) * 100
                    progress_callback(artwork, progress, f"Drawing spiral {sym + 1}/{symmetry}")
            
            # Add path to artwork
            if len(path_points) > 1:
                path_color = self._get_gradient_color(color, sym / max(symmetry - 1, 1)) if use_gradient else color
                artwork.paths.append({
                    'points': path_points,
                    'stroke': path_color,
                    'stroke_width': line_width,
                    'fill': 'none'
                })
    
    def _generate_wave(self, artwork: ArtworkData, density: int, complexity: float,
                      symmetry: int, line_width: float, color: str, use_gradient: bool,
                      progress_callback: Callable, should_abort: Callable):
        """Generate wave patterns."""
        num_waves = symmetry
        
        for wave_idx in range(num_waves):
            if should_abort and should_abort():
                break
            
            path_points = []
            y_offset = (artwork.height / (num_waves + 1)) * (wave_idx + 1)
            
            for i in range(density):
                if should_abort and should_abort():
                    break
                
                t = i / density
                x = t * artwork.width
                
                # Multiple sine waves with different frequencies
                y = y_offset
                for freq in range(1, int(complexity) + 1):
                    amplitude = (artwork.height / (num_waves + 1)) * 0.3 / freq
                    y += amplitude * math.sin(2 * math.pi * freq * t + wave_idx)
                
                path_points.append((x, y))
                
                # Progress update
                if progress_callback and i % 10 == 0:
                    progress = ((wave_idx * density + i) / (num_waves * density)) * 100
                    progress_callback(artwork, progress, f"Drawing wave {wave_idx + 1}/{num_waves}")
            
            # Add path to artwork
            if len(path_points) > 1:
                path_color = self._get_gradient_color(color, wave_idx / max(num_waves - 1, 1)) if use_gradient else color
                artwork.paths.append({
                    'points': path_points,
                    'stroke': path_color,
                    'stroke_width': line_width,
                    'fill': 'none'
                })
    
    def _generate_lissajous(self, artwork: ArtworkData, density: int, complexity: float,
                          symmetry: int, line_width: float, color: str, use_gradient: bool,
                          progress_callback: Callable, should_abort: Callable):
        """Generate Lissajous curves."""
        cx, cy = artwork.width / 2, artwork.height / 2
        scale_x = artwork.width * 0.4
        scale_y = artwork.height * 0.4
        
        for sym in range(symmetry):
            if should_abort and should_abort():
                break
            
            path_points = []
            a = 1 + sym * 0.5
            b = complexity
            delta = (math.pi / 4) * sym
            
            for i in range(density):
                if should_abort and should_abort():
                    break
                
                t = (i / density) * 2 * math.pi
                x = cx + scale_x * math.sin(a * t + delta)
                y = cy + scale_y * math.sin(b * t)
                path_points.append((x, y))
                
                # Progress update
                if progress_callback and i % 10 == 0:
                    progress = ((sym * density + i) / (symmetry * density)) * 100
                    progress_callback(artwork, progress, f"Drawing curve {sym + 1}/{symmetry}")
            
            # Close the curve
            if len(path_points) > 0:
                path_points.append(path_points[0])
            
            # Add path to artwork
            if len(path_points) > 1:
                path_color = self._get_gradient_color(color, sym / max(symmetry - 1, 1)) if use_gradient else color
                artwork.paths.append({
                    'points': path_points,
                    'stroke': path_color,
                    'stroke_width': line_width,
                    'fill': 'none'
                })
    
    def _generate_fractal_tree(self, artwork: ArtworkData, density: int, complexity: float,
                              symmetry: int, line_width: float, color: str, use_gradient: bool,
                              progress_callback: Callable, should_abort: Callable):
        """Generate fractal tree patterns."""
        max_depth = min(int(complexity * 3), 12)  # Limit depth to prevent exponential explosion
        total_branches = 0
        
        for sym in range(symmetry):
            if should_abort and should_abort():
                break
            
            # Starting position and angle
            angle_offset = (2 * math.pi * sym) / symmetry
            start_x = artwork.width / 2
            start_y = artwork.height * 0.8
            start_angle = -math.pi / 2 + angle_offset
            branch_length = min(artwork.width, artwork.height) * 0.15
            
            # Recursive tree generation
            branches_drawn = [0]  # Use list to allow modification in nested function
            
            def draw_branch(x, y, angle, length, depth):
                if should_abort and should_abort():
                    return
                if depth > max_depth or length < 2:
                    return
                
                # Calculate end point
                end_x = x + length * math.cos(angle)
                end_y = y + length * math.sin(angle)
                
                # Add branch as path
                branch_color = self._get_gradient_color(color, depth / max_depth) if use_gradient else color
                artwork.paths.append({
                    'points': [(x, y), (end_x, end_y)],
                    'stroke': branch_color,
                    'stroke_width': line_width * (1 - depth / (max_depth + 1)),
                    'fill': 'none'
                })
                
                branches_drawn[0] += 1
                
                # Progress update
                if progress_callback and branches_drawn[0] % 5 == 0:
                    progress = ((sym + branches_drawn[0] / 100) / symmetry) * 100
                    progress_callback(artwork, min(progress, 99), f"Growing tree {sym + 1}/{symmetry}")
                
                # Recursively draw child branches
                new_length = length * 0.7
                angle_spread = math.pi / 6  # 30 degrees
                
                draw_branch(end_x, end_y, angle - angle_spread, new_length, depth + 1)
                draw_branch(end_x, end_y, angle + angle_spread, new_length, depth + 1)
            
            draw_branch(start_x, start_y, start_angle, branch_length, 0)
            total_branches += branches_drawn[0]
    
    def _generate_circle_pack(self, artwork: ArtworkData, density: int, complexity: float,
                            symmetry: int, line_width: float, color: str, use_gradient: bool,
                            progress_callback: Callable, should_abort: Callable):
        """Generate circle packing patterns."""
        circles = []
        max_radius = min(artwork.width, artwork.height) * 0.1
        min_radius = max_radius * 0.1
        attempts_per_circle = 50
        
        for i in range(density):
            if should_abort and should_abort():
                break
            
            # Try to place a circle
            placed = False
            for attempt in range(attempts_per_circle):
                if should_abort and should_abort():
                    break
                
                # Random position
                x = random.uniform(0, artwork.width)
                y = random.uniform(0, artwork.height)
                
                # Start with max radius and shrink if overlapping
                radius = max_radius / (1 + complexity * random.random())
                
                # Check for overlaps
                valid = True
                for cx, cy, cr in circles:
                    dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if dist < radius + cr:
                        # Try smaller radius
                        radius = max(min_radius, dist - cr - line_width)
                        if radius < min_radius:
                            valid = False
                            break
                
                if valid and radius >= min_radius:
                    circles.append((x, y, radius))
                    placed = True
                    break
            
            # Progress update
            if progress_callback and i % 5 == 0:
                progress = (i / density) * 100
                progress_callback(artwork, progress, f"Packing circles: {len(circles)}/{density}")
            
            if not placed:
                # If we can't place more circles, we're done
                break
        
        # Add circles to artwork with symmetry
        for sym in range(symmetry):
            if should_abort and should_abort():
                break
            
            angle_offset = (2 * math.pi * sym) / symmetry
            cx_center = artwork.width / 2
            cy_center = artwork.height / 2
            
            for idx, (x, y, radius) in enumerate(circles):
                if should_abort and should_abort():
                    break
                
                # Rotate around center for symmetry
                dx = x - cx_center
                dy = y - cy_center
                rotated_x = cx_center + dx * math.cos(angle_offset) - dy * math.sin(angle_offset)
                rotated_y = cy_center + dx * math.sin(angle_offset) + dy * math.cos(angle_offset)
                
                circle_color = self._get_gradient_color(color, idx / len(circles)) if use_gradient else color
                artwork.circles.append({
                    'cx': rotated_x,
                    'cy': rotated_y,
                    'r': radius,
                    'stroke': circle_color,
                    'stroke_width': line_width,
                    'fill': 'none'
                })
    
    def _get_gradient_color(self, base_color: str, t: float) -> str:
        """Generate a color along a gradient from base_color."""
        # Parse hex color
        base_color = base_color.lstrip('#')
        r = int(base_color[0:2], 16)
        g = int(base_color[2:4], 16)
        b = int(base_color[4:6], 16)
        
        # Shift hue based on t
        # Convert to HSV-like manipulation
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        
        if max_val == min_val:
            # Gray, just vary brightness
            factor = 0.5 + 0.5 * t
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
        else:
            # Rotate hue
            hue_shift = t * 60  # Shift up to 60 degrees
            # Simple hue rotation approximation
            r = int(max(0, min(255, r + hue_shift * (g - b) / 255)))
            g = int(max(0, min(255, g + hue_shift * (b - r) / 255)))
            b = int(max(0, min(255, b + hue_shift * (r - g) / 255)))
        
        return f'#{r:02x}{g:02x}{b:02x}'
