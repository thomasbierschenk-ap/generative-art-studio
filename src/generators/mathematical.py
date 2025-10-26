"""
Mathematical Patterns Generator - Enhanced Version

Generates artwork using mathematical formulas and geometric patterns with organic variation.
Includes spirals, waves, fractals, Lissajous curves, and circle packing.
"""

import math
import random
from typing import Dict, Any, Callable, Tuple
import numpy as np

from .base import BaseGenerator, ArtworkData, PathElement, CircleElement


class MathematicalPatternsGenerator(BaseGenerator):
    """Generator for mathematical and geometric patterns with organic variation."""
    
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
            'color_scheme': {
                'type': 'choice',
                'default': 'gradient',
                'choices': ['gradient', 'monochrome', 'complementary', 'analogous', 'triadic', 'random'],
                'label': 'Color Scheme',
                'help': 'How colors are distributed across the pattern'
            },
            'color_variation': {
                'type': 'float',
                'default': 30.0,
                'min': 0.0,
                'max': 100.0,
                'label': 'Color Variation',
                'help': 'Amount of color variation (0 = uniform, 100 = maximum)'
            },
            'organic_factor': {
                'type': 'float',
                'default': 0.0,
                'min': 0.0,
                'max': 1.0,
                'label': 'Organic Factor',
                'help': 'Add randomness and imperfection (0 = perfect, 1 = very organic)'
            },
            'completeness': {
                'type': 'float',
                'default': 1.0,
                'min': 0.3,
                'max': 1.0,
                'label': 'Completeness',
                'help': 'How complete the pattern is (0.3 = partial, 1.0 = full)'
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
        progress_callback: Callable[[ArtworkData, float], None] = None
    ) -> ArtworkData:
        """Generate mathematical pattern artwork."""
        
        # Extract parameters
        pattern_type = params.get('pattern_type', 'spiral')
        density = params.get('density', 100)
        complexity = params.get('complexity', 1.5)
        symmetry = params.get('symmetry', 1)
        line_width = params.get('line_width', 2.0)
        color = params.get('color', '#2E86AB')
        color_scheme = params.get('color_scheme', 'gradient')
        color_variation = params.get('color_variation', 30.0)
        organic_factor = params.get('organic_factor', 0.0)
        completeness = params.get('completeness', 1.0)
        bg_color = params.get('background_color', '#FFFFFF')
        
        # Store parameters for helper methods
        self._current_color = color
        self._color_scheme = color_scheme
        self._color_variation = color_variation / 100.0
        self._organic_factor = organic_factor
        self._completeness = completeness
        
        # Initialize artwork
        artwork = ArtworkData(
            width=width,
            height=height,
            background_color=self._hex_to_rgb(bg_color)
        )
        
        # Generate pattern based on type
        if pattern_type == 'spiral':
            self._generate_spiral(artwork, density, complexity, symmetry, 
                                line_width, progress_callback)
        elif pattern_type == 'wave':
            self._generate_wave(artwork, density, complexity, symmetry,
                              line_width, progress_callback)
        elif pattern_type == 'lissajous':
            self._generate_lissajous(artwork, density, complexity, symmetry,
                                   line_width, progress_callback)
        elif pattern_type == 'fractal_tree':
            self._generate_fractal_tree(artwork, density, complexity, symmetry,
                                      line_width, progress_callback)
        elif pattern_type == 'circle_pack':
            self._generate_circle_pack(artwork, density, complexity, symmetry,
                                     line_width, progress_callback)
        
        return artwork
    
    def _generate_spiral(self, artwork: ArtworkData, density: int, complexity: float,
                        symmetry: int, line_width: float,
                        progress_callback: Callable):
        """Generate spiral patterns with organic variation."""
        cx, cy = artwork.width / 2, artwork.height / 2
        max_radius = min(artwork.width, artwork.height) * 0.4
        
        # Apply completeness to density
        actual_density = int(density * self._completeness)
        
        for sym in range(symmetry):
            # Add organic variation to symmetry
            angle_offset = (2 * math.pi * sym) / symmetry
            if self._organic_factor > 0:
                angle_offset += random.uniform(-0.1, 0.1) * self._organic_factor
            
            path_points = []
            
            for i in range(actual_density):
                t = i / density  # Use original density for t calculation
                
                # Add organic wobble to angle and radius
                angle = t * complexity * 2 * math.pi + angle_offset
                if self._organic_factor > 0:
                    angle += random.uniform(-0.05, 0.05) * self._organic_factor * math.pi
                
                radius = t * max_radius
                if self._organic_factor > 0:
                    radius *= (1 + random.uniform(-0.1, 0.1) * self._organic_factor)
                
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                
                # Add position jitter
                if self._organic_factor > 0:
                    jitter = 5 * self._organic_factor
                    x += random.uniform(-jitter, jitter)
                    y += random.uniform(-jitter, jitter)
                
                path_points.append((x, y))
                
                # Progress update
                if progress_callback and i % 10 == 0:
                    progress = ((sym * actual_density + i) / (symmetry * actual_density)) * 100
                    progress_callback(artwork, progress)
            
            # Add path to artwork
            if len(path_points) > 1:
                path_color = self._get_color_for_element(sym, symmetry)
                artwork.paths.append(PathElement(
                    points=path_points,
                    color=path_color,
                    width=line_width,
                    closed=False
                ))
    
    def _generate_wave(self, artwork: ArtworkData, density: int, complexity: float,
                      symmetry: int, line_width: float,
                      progress_callback: Callable):
        """Generate wave patterns with organic variation."""
        num_waves = symmetry
        actual_density = int(density * self._completeness)
        
        for wave_idx in range(num_waves):
            path_points = []
            y_offset = (artwork.height / (num_waves + 1)) * (wave_idx + 1)
            
            # Add organic variation to y_offset
            if self._organic_factor > 0:
                y_offset += random.uniform(-10, 10) * self._organic_factor
            
            for i in range(actual_density):
                t = i / density
                x = t * artwork.width
                
                # Multiple sine waves with different frequencies
                y = y_offset
                for freq in range(1, int(complexity) + 1):
                    amplitude = (artwork.height / (num_waves + 1)) * 0.3 / freq
                    phase = wave_idx + (random.random() * self._organic_factor if self._organic_factor > 0 else 0)
                    y += amplitude * math.sin(2 * math.pi * freq * t + phase)
                
                # Add position jitter
                if self._organic_factor > 0:
                    jitter = 3 * self._organic_factor
                    x += random.uniform(-jitter, jitter)
                    y += random.uniform(-jitter, jitter)
                
                path_points.append((x, y))
                
                # Progress update
                if progress_callback and i % 10 == 0:
                    progress = ((wave_idx * actual_density + i) / (num_waves * actual_density)) * 100
                    progress_callback(artwork, progress)
            
            # Add path to artwork
            if len(path_points) > 1:
                path_color = self._get_color_for_element(wave_idx, num_waves)
                artwork.paths.append(PathElement(
                    points=path_points,
                    color=path_color,
                    width=line_width,
                    closed=False
                ))
    
    def _generate_lissajous(self, artwork: ArtworkData, density: int, complexity: float,
                          symmetry: int, line_width: float,
                          progress_callback: Callable):
        """Generate Lissajous curves with organic variation."""
        cx, cy = artwork.width / 2, artwork.height / 2
        scale_x = artwork.width * 0.4
        scale_y = artwork.height * 0.4
        
        actual_density = int(density * self._completeness)
        
        for sym in range(symmetry):
            path_points = []
            a = 1 + sym * 0.5
            b = complexity
            delta = (math.pi / 4) * sym
            
            # Add organic variation to parameters
            if self._organic_factor > 0:
                a += random.uniform(-0.1, 0.1) * self._organic_factor
                b += random.uniform(-0.1, 0.1) * self._organic_factor
                delta += random.uniform(-0.1, 0.1) * self._organic_factor
            
            for i in range(actual_density):
                t = (i / density) * 2 * math.pi
                x = cx + scale_x * math.sin(a * t + delta)
                y = cy + scale_y * math.sin(b * t)
                
                # Add position jitter
                if self._organic_factor > 0:
                    jitter = 5 * self._organic_factor
                    x += random.uniform(-jitter, jitter)
                    y += random.uniform(-jitter, jitter)
                
                path_points.append((x, y))
                
                # Progress update
                if progress_callback and i % 10 == 0:
                    progress = ((sym * actual_density + i) / (symmetry * actual_density)) * 100
                    progress_callback(artwork, progress)
            
            # Add path to artwork (NOT closed - this fixes the straight line bug!)
            if len(path_points) > 1:
                path_color = self._get_color_for_element(sym, symmetry)
                artwork.paths.append(PathElement(
                    points=path_points,
                    color=path_color,
                    width=line_width,
                    closed=False  # Changed from True to False!
                ))
    
    def _generate_fractal_tree(self, artwork: ArtworkData, density: int, complexity: float,
                              symmetry: int, line_width: float,
                              progress_callback: Callable):
        """Generate fractal tree patterns with organic variation."""
        max_depth = min(int(complexity * 3), 12)
        
        for sym in range(symmetry):
            # Starting position and angle
            angle_offset = (2 * math.pi * sym) / symmetry
            start_x = artwork.width / 2
            start_y = artwork.height * 0.8
            start_angle = -math.pi / 2 + angle_offset
            branch_length = min(artwork.width, artwork.height) * 0.15
            
            # Add organic variation to starting position
            if self._organic_factor > 0:
                start_x += random.uniform(-20, 20) * self._organic_factor
                start_angle += random.uniform(-0.2, 0.2) * self._organic_factor
            
            # Recursive tree generation
            branches_drawn = [0]
            
            def draw_branch(x, y, angle, length, depth):
                if depth > max_depth or length < 2:
                    return
                
                # Apply completeness - randomly skip some branches
                if random.random() > self._completeness:
                    return
                
                # Add organic variation to angle
                if self._organic_factor > 0:
                    angle += random.uniform(-0.1, 0.1) * self._organic_factor
                
                # Calculate end point
                end_x = x + length * math.cos(angle)
                end_y = y + length * math.sin(angle)
                
                # Add branch as path
                branch_color = self._get_color_for_element(depth, max_depth + 1)
                artwork.paths.append(PathElement(
                    points=[(x, y), (end_x, end_y)],
                    color=branch_color,
                    width=line_width * (1 - depth / (max_depth + 1)),
                    closed=False
                ))
                
                branches_drawn[0] += 1
                
                # Progress update
                if progress_callback and branches_drawn[0] % 5 == 0:
                    progress = ((sym + branches_drawn[0] / 100) / symmetry) * 100
                    progress_callback(artwork, min(progress, 99))
                
                # Recursively draw child branches with organic variation
                length_factor = 0.7 + (random.uniform(-0.1, 0.1) * self._organic_factor if self._organic_factor > 0 else 0)
                new_length = length * length_factor
                
                # Vary angle spread
                angle_spread = math.pi / 6  # 30 degrees base
                if self._organic_factor > 0:
                    angle_spread += random.uniform(-0.2, 0.2) * self._organic_factor
                
                # Randomly add 2-4 branches instead of always 2
                num_branches = 2
                if self._organic_factor > 0.5:
                    num_branches = random.choice([2, 2, 2, 3])  # Weighted towards 2
                
                for i in range(num_branches):
                    branch_angle = angle + (i - (num_branches - 1) / 2) * angle_spread
                    draw_branch(end_x, end_y, branch_angle, new_length, depth + 1)
            
            draw_branch(start_x, start_y, start_angle, branch_length, 0)
    
    def _generate_circle_pack(self, artwork: ArtworkData, density: int, complexity: float,
                            symmetry: int, line_width: float,
                            progress_callback: Callable):
        """Generate circle packing patterns with organic variation."""
        circles = []
        max_radius = min(artwork.width, artwork.height) * 0.1
        min_radius = max_radius * 0.1
        attempts_per_circle = 50
        
        actual_density = int(density * self._completeness)
        
        for i in range(actual_density):
            # Try to place a circle
            placed = False
            for attempt in range(attempts_per_circle):
                # Random position
                x = random.uniform(0, artwork.width)
                y = random.uniform(0, artwork.height)
                
                # Start with max radius and shrink if overlapping
                radius = max_radius / (1 + complexity * random.random())
                
                # Add organic variation to radius
                if self._organic_factor > 0:
                    radius *= (1 + random.uniform(-0.2, 0.2) * self._organic_factor)
                
                # Check for overlaps with more tolerance for organic look
                overlap_tolerance = line_width * (1 - self._organic_factor * 0.5)
                valid = True
                for cx, cy, cr in circles:
                    dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    if dist < radius + cr + overlap_tolerance:
                        # Try smaller radius
                        radius = max(min_radius, dist - cr - overlap_tolerance)
                        if radius < min_radius:
                            valid = False
                            break
                
                if valid and radius >= min_radius:
                    circles.append((x, y, radius))
                    placed = True
                    break
            
            # Progress update
            if progress_callback and i % 5 == 0:
                progress = (i / actual_density) * 100
                progress_callback(artwork, progress)
            
            if not placed:
                break
        
        # Add circles to artwork with symmetry
        for sym in range(symmetry):
            angle_offset = (2 * math.pi * sym) / symmetry
            if self._organic_factor > 0:
                angle_offset += random.uniform(-0.05, 0.05) * self._organic_factor
            
            cx_center = artwork.width / 2
            cy_center = artwork.height / 2
            
            for idx, (x, y, radius) in enumerate(circles):
                # Rotate around center for symmetry
                dx = x - cx_center
                dy = y - cy_center
                rotated_x = cx_center + dx * math.cos(angle_offset) - dy * math.sin(angle_offset)
                rotated_y = cy_center + dx * math.sin(angle_offset) + dy * math.cos(angle_offset)
                
                circle_color = self._get_color_for_element(idx, len(circles))
                artwork.circles.append(CircleElement(
                    center=(rotated_x, rotated_y),
                    radius=radius,
                    color=circle_color,
                    fill=False,
                    stroke_width=line_width
                ))
    
    # Color helper methods
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color string to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        )
    
    def _rgb_to_hsv(self, r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Convert RGB to HSV."""
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        diff = max_c - min_c
        
        if max_c == min_c:
            h = 0
        elif max_c == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif max_c == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360
        
        s = 0 if max_c == 0 else (diff / max_c)
        v = max_c
        
        return h, s, v
    
    def _hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV to RGB."""
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (
            int((r + m) * 255),
            int((g + m) * 255),
            int((b + m) * 255)
        )
    
    def _get_color_for_element(self, index: int, total: int) -> Tuple[int, int, int]:
        """Get color for an element based on color scheme."""
        base_rgb = self._hex_to_rgb(self._current_color)
        h, s, v = self._rgb_to_hsv(*base_rgb)
        
        t = index / max(total - 1, 1)  # Normalized position 0-1
        
        if self._color_scheme == 'monochrome':
            # Vary only brightness
            new_v = v * (0.5 + 0.5 * t)
            new_h, new_s = h, s
        
        elif self._color_scheme == 'gradient':
            # Smooth hue shift
            hue_shift = self._color_variation * 120  # Up to 120 degrees
            new_h = (h + t * hue_shift) % 360
            new_s = s
            new_v = v
        
        elif self._color_scheme == 'complementary':
            # Alternate between base and complement
            if index % 2 == 0:
                new_h = h
            else:
                new_h = (h + 180) % 360
            new_s = s
            new_v = v
        
        elif self._color_scheme == 'analogous':
            # Stay within 60 degrees
            hue_shift = self._color_variation * 60
            new_h = (h + (t - 0.5) * hue_shift) % 360
            new_s = s
            new_v = v
        
        elif self._color_scheme == 'triadic':
            # Use three colors 120 degrees apart
            offset = (index % 3) * 120
            new_h = (h + offset) % 360
            new_s = s
            new_v = v
        
        elif self._color_scheme == 'random':
            # Completely random within variation range
            hue_shift = self._color_variation * 360
            new_h = (h + random.uniform(-hue_shift, hue_shift)) % 360
            new_s = s * (1 + random.uniform(-0.3, 0.3) * self._color_variation)
            new_v = v * (1 + random.uniform(-0.3, 0.3) * self._color_variation)
            new_s = max(0, min(1, new_s))
            new_v = max(0, min(1, new_v))
        
        else:
            new_h, new_s, new_v = h, s, v
        
        return self._hsv_to_rgb(new_h, new_s, new_v)
