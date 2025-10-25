"""
Random Walk Generator

Creates artwork based on random walk algorithms with various parameters
for controlling the behavior and appearance.
"""

import random
import math
from typing import Dict, Any, List, Tuple
from .base import BaseGenerator, ArtworkData, PathElement, CircleElement


class RandomWalkGenerator(BaseGenerator):
    """
    Generates art using random walk algorithms.
    
    A random walk is a path where each step is taken in a random direction.
    Various parameters control the walk behavior, creating different visual effects.
    """
    
    def get_name(self) -> str:
        return "Random Walk"
    
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        return {
            'num_walks': {
                'type': 'int',
                'default': 5,
                'min': 1,
                'max': 50,
                'label': 'Number of Walks',
                'help': 'How many separate random walks to generate'
            },
            'steps_per_walk': {
                'type': 'int',
                'default': 1000,
                'min': 10,
                'max': 10000,
                'label': 'Steps per Walk',
                'help': 'Number of steps in each walk'
            },
            'step_size': {
                'type': 'float',
                'default': 5.0,
                'min': 0.5,
                'max': 50.0,
                'step': 0.5,
                'label': 'Step Size',
                'help': 'Length of each step in pixels'
            },
            'angle_variation': {
                'type': 'float',
                'default': 180.0,
                'min': 0.0,
                'max': 360.0,
                'step': 5.0,
                'label': 'Angle Variation (degrees)',
                'help': 'Maximum angle change between steps (0=straight, 360=any direction)'
            },
            'line_width': {
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'step': 0.1,
                'label': 'Line Width',
                'help': 'Thickness of the drawn lines'
            },
            'color_mode': {
                'type': 'choice',
                'default': 'monochrome',
                'choices': ['monochrome', 'grayscale', 'color', 'rainbow'],
                'label': 'Color Mode',
                'help': 'How to color the walks'
            },
            'base_color': {
                'type': 'color',
                'default': '#000000',
                'label': 'Base Color',
                'help': 'Primary color (used in monochrome mode)'
            },
            'background_color': {
                'type': 'color',
                'default': '#FFFFFF',
                'label': 'Background Color',
                'help': 'Canvas background color'
            },
            'start_position': {
                'type': 'choice',
                'default': 'center',
                'choices': ['center', 'random', 'edges', 'corners'],
                'label': 'Start Position',
                'help': 'Where walks begin'
            },
            'boundary_behavior': {
                'type': 'choice',
                'default': 'bounce',
                'choices': ['bounce', 'wrap', 'stop', 'ignore'],
                'label': 'Boundary Behavior',
                'help': 'What happens at canvas edges'
            },
            'add_nodes': {
                'type': 'bool',
                'default': False,
                'label': 'Show Nodes',
                'help': 'Draw circles at walk endpoints'
            },
            'seed': {
                'type': 'int',
                'default': 0,
                'min': 0,
                'max': 999999,
                'label': 'Random Seed',
                'help': 'Seed for reproducibility (0 = random)'
            }
        }
    
    def generate(self, width: int, height: int, params: Dict[str, Any],
                 progress_callback=None) -> ArtworkData:
        """Generate random walk artwork with optional progress updates."""
        # Validate parameters
        params = self.validate_parameters(params)
        
        # Set random seed if specified
        if params['seed'] > 0:
            random.seed(params['seed'])
        
        # Create artwork container
        bg_color = self._hex_to_rgb(params['background_color'])
        artwork = ArtworkData(width=width, height=height, background_color=bg_color)
        
        # Generate each walk
        for i in range(params['num_walks']):
            walk_color = self._get_walk_color(i, params)
            path = self._generate_walk(width, height, params, walk_color, 
                                       artwork, progress_callback, i)
            artwork.paths.append(path)
            
            # Add endpoint node if requested
            if params['add_nodes'] and len(path.points) > 0:
                last_point = path.points[-1]
                node = CircleElement(
                    center=last_point,
                    radius=params['line_width'] * 2,
                    color=walk_color,
                    fill=True
                )
                artwork.circles.append(node)
            
            # Update progress after each walk completes
            if progress_callback:
                progress = ((i + 1) / params['num_walks']) * 100
                progress_callback(artwork, progress)
        
        return artwork
    
    def _generate_walk(
        self,
        width: int,
        height: int,
        params: Dict[str, Any],
        color: Tuple[int, int, int],
        artwork: ArtworkData,
        progress_callback,
        walk_index: int
    ) -> PathElement:
        """Generate a single random walk with progress updates."""
        points = []
        
        # Determine starting position
        x, y = self._get_start_position(width, height, params['start_position'])
        current_angle = random.uniform(0, 2 * math.pi)
        
        points.append((x, y))
        
        # Calculate update frequency (update every N steps for performance)
        update_interval = max(1, params['steps_per_walk'] // 50)
        
        # Perform the walk
        for step in range(params['steps_per_walk']):
            # Calculate angle change
            angle_var_rad = math.radians(params['angle_variation'])
            angle_change = random.uniform(-angle_var_rad / 2, angle_var_rad / 2)
            current_angle += angle_change
            
            # Calculate new position
            dx = math.cos(current_angle) * params['step_size']
            dy = math.sin(current_angle) * params['step_size']
            
            new_x = x + dx
            new_y = y + dy
            
            # Handle boundaries
            new_x, new_y, should_continue = self._handle_boundary(
                new_x, new_y, width, height, params['boundary_behavior']
            )
            
            if not should_continue:
                break
            
            x, y = new_x, new_y
            points.append((x, y))
            
            # Send progress updates during walk generation
            if progress_callback and step % update_interval == 0:
                # Create a temporary path with current points
                temp_path = PathElement(
                    points=points.copy(),
                    color=color,
                    width=params['line_width'],
                    closed=False
                )
                # Calculate overall progress
                walk_progress = walk_index / params['num_walks']
                step_progress = (step / params['steps_per_walk']) / params['num_walks']
                total_progress = (walk_progress + step_progress) * 100
                
                # Create temporary artwork with current path
                temp_artwork = ArtworkData(
                    width=width,
                    height=height,
                    background_color=artwork.background_color,
                    paths=artwork.paths + [temp_path],
                    circles=artwork.circles.copy()
                )
                progress_callback(temp_artwork, total_progress)
        
        return PathElement(
            points=points,
            color=color,
            width=params['line_width'],
            closed=False
        )
    
    def _get_start_position(
        self,
        width: int,
        height: int,
        mode: str
    ) -> Tuple[float, float]:
        """Determine starting position based on mode."""
        if mode == 'center':
            return (width / 2, height / 2)
        
        elif mode == 'random':
            return (random.uniform(0, width), random.uniform(0, height))
        
        elif mode == 'edges':
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top':
                return (random.uniform(0, width), 0)
            elif edge == 'bottom':
                return (random.uniform(0, width), height)
            elif edge == 'left':
                return (0, random.uniform(0, height))
            else:  # right
                return (width, random.uniform(0, height))
        
        elif mode == 'corners':
            corner = random.choice([
                (0, 0), (width, 0), (0, height), (width, height)
            ])
            return corner
        
        return (width / 2, height / 2)
    
    def _handle_boundary(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        behavior: str
    ) -> Tuple[float, float, bool]:
        """
        Handle boundary conditions.
        
        Returns:
            (new_x, new_y, should_continue)
        """
        if behavior == 'ignore':
            return (x, y, True)
        
        should_continue = True
        
        if behavior == 'stop':
            if x < 0 or x > width or y < 0 or y > height:
                should_continue = False
            return (x, y, should_continue)
        
        elif behavior == 'bounce':
            if x < 0:
                x = -x
            elif x > width:
                x = 2 * width - x
            
            if y < 0:
                y = -y
            elif y > height:
                y = 2 * height - y
        
        elif behavior == 'wrap':
            x = x % width
            y = y % height
        
        return (x, y, should_continue)
    
    def _get_walk_color(self, index: int, params: Dict[str, Any]) -> Tuple[int, int, int]:
        """Determine color for a walk based on color mode."""
        mode = params['color_mode']
        
        if mode == 'monochrome':
            return self._hex_to_rgb(params['base_color'])
        
        elif mode == 'grayscale':
            # Vary brightness
            num_walks = params['num_walks']
            if num_walks == 1:
                value = 0
            else:
                value = int(255 * index / (num_walks - 1))
            return (value, value, value)
        
        elif mode == 'color':
            # Random colors
            return (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
        
        elif mode == 'rainbow':
            # HSV to RGB conversion for rainbow effect
            num_walks = params['num_walks']
            hue = (index / num_walks) if num_walks > 1 else 0
            return self._hsv_to_rgb(hue, 1.0, 1.0)
        
        return (0, 0, 0)
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
        """Convert HSV to RGB."""
        import colorsys
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))
