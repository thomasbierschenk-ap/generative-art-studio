"""
Base generator class for all art generation methods.

This module defines the interface that all generators must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional
import svgwrite
from PIL import Image, ImageDraw


@dataclass
class PathElement:
    """Represents a path (line, curve, etc.) in the artwork."""
    points: List[Tuple[float, float]]
    color: Tuple[int, int, int]  # RGB
    width: float = 1.0
    closed: bool = False


@dataclass
class CircleElement:
    """Represents a circle in the artwork."""
    center: Tuple[float, float]
    radius: float
    color: Tuple[int, int, int]  # RGB
    fill: bool = True
    stroke_width: float = 1.0


@dataclass
class ArtworkData:
    """
    Container for generated artwork data.
    
    This structure allows generators to create artwork in a format-agnostic way,
    which can then be exported to SVG, PNG, or other formats.
    """
    width: int
    height: int
    background_color: Tuple[int, int, int] = (255, 255, 255)
    paths: List[PathElement] = field(default_factory=list)
    circles: List[CircleElement] = field(default_factory=list)
    # Future: Add more shape types (rectangles, polygons, text, etc.)


class BaseGenerator(ABC):
    """
    Abstract base class for all art generators.
    
    Subclasses must implement:
    - get_name(): Return the display name
    - get_parameters(): Define configurable parameters
    - generate(): Create the artwork
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the display name of this generator."""
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, Dict[str, Any]]:
        """
        Return parameter definitions for this generator.
        
        Format:
        {
            'param_name': {
                'type': 'int' | 'float' | 'color' | 'choice' | 'bool',
                'default': value,
                'min': min_value,      # for int/float
                'max': max_value,      # for int/float
                'step': step_value,    # for int/float
                'choices': [...],      # for choice
                'label': 'Display Name',
                'help': 'Description'
            }
        }
        """
        pass
    
    @abstractmethod
    def generate(self, width: int, height: int, params: Dict[str, Any], 
                 progress_callback: Optional[callable] = None) -> ArtworkData:
        """
        Generate artwork with the given dimensions and parameters.
        
        Args:
            width: Output width in pixels
            height: Output height in pixels
            params: Dictionary of parameter values
            progress_callback: Optional callback function(artwork_data, progress_pct) 
                             called during generation for live preview
            
        Returns:
            ArtworkData object containing the generated artwork
        """
        pass
    
    def to_svg(self, artwork: ArtworkData, filename: str) -> None:
        """
        Export artwork to SVG format.
        
        Args:
            artwork: The artwork data to export
            filename: Output filename (should end in .svg)
        """
        dwg = svgwrite.Drawing(filename, size=(artwork.width, artwork.height))
        
        # Set background
        bg_color = f'rgb({artwork.background_color[0]},{artwork.background_color[1]},{artwork.background_color[2]})'
        dwg.add(dwg.rect(insert=(0, 0), size=(artwork.width, artwork.height), fill=bg_color))
        
        # Draw paths
        for path in artwork.paths:
            if len(path.points) < 2:
                continue
            
            color = f'rgb({path.color[0]},{path.color[1]},{path.color[2]})'
            
            if path.closed:
                # Create a polygon
                dwg.add(dwg.polygon(
                    points=path.points,
                    fill=color,
                    stroke=color,
                    stroke_width=path.width
                ))
            else:
                # Create a polyline
                dwg.add(dwg.polyline(
                    points=path.points,
                    fill='none',
                    stroke=color,
                    stroke_width=path.width,
                    stroke_linecap='round',
                    stroke_linejoin='round'
                ))
        
        # Draw circles
        for circle in artwork.circles:
            color = f'rgb({circle.color[0]},{circle.color[1]},{circle.color[2]})'
            dwg.add(dwg.circle(
                center=circle.center,
                r=circle.radius,
                fill=color if circle.fill else 'none',
                stroke=color if not circle.fill else 'none',
                stroke_width=circle.stroke_width
            ))
        
        dwg.save()
    
    def to_png(self, artwork: ArtworkData, filename: str) -> None:
        """
        Export artwork to PNG format.
        
        Args:
            artwork: The artwork data to export
            filename: Output filename (should end in .png)
        """
        # Create image with background color
        img = Image.new('RGB', (artwork.width, artwork.height), artwork.background_color)
        draw = ImageDraw.Draw(img)
        
        # Draw paths
        for path in artwork.paths:
            if len(path.points) < 2:
                continue
            
            if path.closed:
                # Draw as polygon
                draw.polygon(path.points, fill=path.color, outline=path.color)
            else:
                # Draw as line
                if path.width <= 1:
                    draw.line(path.points, fill=path.color, width=int(path.width))
                else:
                    # For thicker lines, draw multiple segments
                    for i in range(len(path.points) - 1):
                        draw.line(
                            [path.points[i], path.points[i + 1]],
                            fill=path.color,
                            width=int(path.width)
                        )
        
        # Draw circles
        for circle in artwork.circles:
            x, y = circle.center
            r = circle.radius
            bbox = [(x - r, y - r), (x + r, y + r)]
            
            if circle.fill:
                draw.ellipse(bbox, fill=circle.color, outline=circle.color)
            else:
                draw.ellipse(
                    bbox,
                    fill=None,
                    outline=circle.color,
                    width=int(circle.stroke_width)
                )
        
        img.save(filename)
    
    def validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize parameters against the parameter definitions.
        
        Args:
            params: User-provided parameters
            
        Returns:
            Validated parameters with defaults filled in
        """
        param_defs = self.get_parameters()
        validated = {}
        
        for name, definition in param_defs.items():
            value = params.get(name, definition.get('default'))
            
            # Type-specific validation
            param_type = definition.get('type')
            
            if param_type == 'int':
                value = int(value)
                if 'min' in definition:
                    value = max(value, definition['min'])
                if 'max' in definition:
                    value = min(value, definition['max'])
            
            elif param_type == 'float':
                value = float(value)
                if 'min' in definition:
                    value = max(value, definition['min'])
                if 'max' in definition:
                    value = min(value, definition['max'])
            
            elif param_type == 'choice':
                if value not in definition.get('choices', []):
                    value = definition.get('default')
            
            elif param_type == 'bool':
                value = bool(value)
            
            validated[name] = value
        
        return validated
