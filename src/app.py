"""
Main application class for Generative Art Studio.

Coordinates between GUI and generators.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict
import os
from generators import RandomWalkGenerator
from gui import MainWindow


class GenerativeArtApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self._setup_style()
        
        # Set up output directory
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize generators
        self.generators = self._initialize_generators()
        
        # For now, use the first (and only) generator
        # In the future, we'll add a generator selection UI
        generator = list(self.generators.values())[0]
        
        # Create main window
        self.main_window = MainWindow(self.root, generator, self.output_dir)
    
    def _setup_style(self):
        """Configure application styling."""
        style = ttk.Style()
        
        # Try to use a modern theme if available
        available_themes = style.theme_names()
        if 'aqua' in available_themes:  # macOS
            style.theme_use('aqua')
        elif 'clam' in available_themes:
            style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Accent.TButton', font=('Helvetica', 11, 'bold'))
    
    def _initialize_generators(self) -> Dict[str, any]:
        """
        Initialize all available generators.
        
        Returns:
            Dictionary mapping generator names to instances
        """
        generators = {}
        
        # Method 2: Random Walk (our proof of concept)
        random_walk = RandomWalkGenerator()
        generators[random_walk.get_name()] = random_walk
        
        # Future generators will be added here:
        # Method 1: Mathematical Patterns
        # Method 3: System Visualization
        # Method 4: Audio Reactive
        
        return generators
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()


def main():
    """Application entry point."""
    app = GenerativeArtApp()
    app.run()


if __name__ == '__main__':
    main()
