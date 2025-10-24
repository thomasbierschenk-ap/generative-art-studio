"""
Main window for Generative Art Studio.

Provides the primary user interface for the application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from typing import Dict, Any, Callable, List
import os


class MainWindow:
    """Main application window."""
    
    def __init__(self, root: tk.Tk, generators: Dict[str, Any]):
        """
        Initialize the main window.
        
        Args:
            root: The root Tk window
            generators: Dictionary of generator name -> generator instance
        """
        self.root = root
        self.generators = generators
        self.current_generator = None
        self.parameter_widgets = {}
        
        self.root.title("Generative Art Studio")
        self.root.geometry("900x700")
        
        self._setup_ui()
        
        # Select first generator by default
        if generators:
            first_gen = list(generators.keys())[0]
            self.generator_var.set(first_gen)
            self._on_generator_change()
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Generative Art Studio",
            font=('Helvetica', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Controls
        self._setup_control_panel(main_frame)
        
        # Right panel - Preview/Info
        self._setup_info_panel(main_frame)
        
        # Bottom panel - Action buttons
        self._setup_action_panel(main_frame)
    
    def _setup_control_panel(self, parent):
        """Set up the control panel on the left side."""
        control_frame = ttk.LabelFrame(parent, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Generator selection
        ttk.Label(control_frame, text="Generation Method:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.generator_var = tk.StringVar()
        generator_combo = ttk.Combobox(
            control_frame,
            textvariable=self.generator_var,
            values=list(self.generators.keys()),
            state='readonly',
            width=25
        )
        generator_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        generator_combo.bind('<<ComboboxSelected>>', lambda e: self._on_generator_change())
        
        # Output dimensions
        ttk.Label(control_frame, text="Output Size:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        size_frame = ttk.Frame(control_frame)
        size_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(size_frame, text="Width:").grid(row=0, column=0, sticky=tk.W)
        self.width_var = tk.StringVar(value="800")
        ttk.Entry(size_frame, textvariable=self.width_var, width=10).grid(row=0, column=1, padx=(5, 15))
        
        ttk.Label(size_frame, text="Height:").grid(row=0, column=2, sticky=tk.W)
        self.height_var = tk.StringVar(value="600")
        ttk.Entry(size_frame, textvariable=self.height_var, width=10).grid(row=0, column=3, padx=(5, 0))
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').grid(
            row=4, column=0, sticky=(tk.W, tk.E), pady=10
        )
        
        # Parameters section (will be populated dynamically)
        ttk.Label(control_frame, text="Parameters:", font=('Helvetica', 10, 'bold')).grid(
            row=5, column=0, sticky=tk.W, pady=(0, 10)
        )
        
        # Scrollable frame for parameters
        self.params_canvas = tk.Canvas(control_frame, highlightthickness=0)
        params_scrollbar = ttk.Scrollbar(control_frame, orient="vertical", command=self.params_canvas.yview)
        self.params_frame = ttk.Frame(self.params_canvas)
        
        self.params_frame.bind(
            "<Configure>",
            lambda e: self.params_canvas.configure(scrollregion=self.params_canvas.bbox("all"))
        )
        
        self.params_canvas.create_window((0, 0), window=self.params_frame, anchor="nw")
        self.params_canvas.configure(yscrollcommand=params_scrollbar.set)
        
        self.params_canvas.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        params_scrollbar.grid(row=6, column=1, sticky=(tk.N, tk.S))
        
        control_frame.rowconfigure(6, weight=1)
        control_frame.columnconfigure(0, weight=1)
    
    def _setup_info_panel(self, parent):
        """Set up the info panel on the right side."""
        info_frame = ttk.LabelFrame(parent, text="Information", padding="10")
        info_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Info text
        self.info_text = tk.Text(info_frame, wrap=tk.WORD, height=10, width=40)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        info_scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        info_frame.rowconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
        
        # Initial info
        self._update_info("Welcome to Generative Art Studio!\n\n"
                         "Select a generation method, adjust parameters, "
                         "and click Generate to create your artwork.")
    
    def _setup_action_panel(self, parent):
        """Set up the action buttons at the bottom."""
        action_frame = ttk.Frame(parent, padding="10")
        action_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Generate button
        self.generate_btn = ttk.Button(
            action_frame,
            text="Generate Artwork",
            command=self._on_generate,
            style='Accent.TButton'
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save buttons
        ttk.Button(
            action_frame,
            text="Save as SVG",
            command=lambda: self._on_save('svg')
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            action_frame,
            text="Save as PNG",
            command=lambda: self._on_save('png')
        ).pack(side=tk.LEFT)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(action_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT)
    
    def _on_generator_change(self):
        """Handle generator selection change."""
        generator_name = self.generator_var.get()
        self.current_generator = self.generators.get(generator_name)
        
        if self.current_generator:
            self._update_parameters()
            self._update_info(f"Selected: {generator_name}\n\n"
                            "Adjust parameters and click Generate to create artwork.")
    
    def _update_parameters(self):
        """Update the parameter controls based on selected generator."""
        # Clear existing widgets
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        self.parameter_widgets.clear()
        
        if not self.current_generator:
            return
        
        # Get parameter definitions
        params = self.current_generator.get_parameters()
        
        row = 0
        for param_name, param_def in params.items():
            # Label
            label_text = param_def.get('label', param_name)
            ttk.Label(self.params_frame, text=f"{label_text}:").grid(
                row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10)
            )
            
            # Widget based on type
            widget = self._create_parameter_widget(self.params_frame, param_name, param_def)
            widget.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
            
            self.parameter_widgets[param_name] = {
                'widget': widget,
                'definition': param_def
            }
            
            # Help text
            if 'help' in param_def:
                help_label = ttk.Label(
                    self.params_frame,
                    text=param_def['help'],
                    foreground='gray',
                    font=('Helvetica', 8)
                )
                help_label.grid(row=row+1, column=0, columnspan=2, sticky=tk.W, padx=(10, 0))
                row += 2
            else:
                row += 1
        
        self.params_frame.columnconfigure(1, weight=1)
    
    def _create_parameter_widget(self, parent, param_name: str, param_def: Dict[str, Any]):
        """Create appropriate widget for parameter type."""
        param_type = param_def.get('type')
        default = param_def.get('default')
        
        if param_type == 'int' or param_type == 'float':
            # Scale widget for numeric values
            var = tk.DoubleVar(value=default) if param_type == 'float' else tk.IntVar(value=default)
            
            frame = ttk.Frame(parent)
            
            scale = ttk.Scale(
                frame,
                from_=param_def.get('min', 0),
                to=param_def.get('max', 100),
                variable=var,
                orient=tk.HORIZONTAL
            )
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Value label
            value_label = ttk.Label(frame, text=str(default), width=8)
            value_label.pack(side=tk.LEFT, padx=(5, 0))
            
            # Update label when scale changes
            def update_label(*args):
                if param_type == 'float':
                    value_label.config(text=f"{var.get():.2f}")
                else:
                    value_label.config(text=f"{int(var.get())}")
            
            var.trace('w', update_label)
            
            frame.var = var  # Store reference
            return frame
        
        elif param_type == 'bool':
            var = tk.BooleanVar(value=default)
            widget = ttk.Checkbutton(parent, variable=var)
            widget.var = var
            return widget
        
        elif param_type == 'choice':
            var = tk.StringVar(value=default)
            widget = ttk.Combobox(
                parent,
                textvariable=var,
                values=param_def.get('choices', []),
                state='readonly'
            )
            widget.var = var
            return widget
        
        elif param_type == 'color':
            frame = ttk.Frame(parent)
            var = tk.StringVar(value=default)
            
            entry = ttk.Entry(frame, textvariable=var, width=10)
            entry.pack(side=tk.LEFT, padx=(0, 5))
            
            def choose_color():
                color = colorchooser.askcolor(initialcolor=var.get())
                if color[1]:
                    var.set(color[1])
            
            ttk.Button(frame, text="Choose...", command=choose_color).pack(side=tk.LEFT)
            
            frame.var = var
            return frame
        
        # Default: text entry
        var = tk.StringVar(value=str(default))
        widget = ttk.Entry(parent, textvariable=var)
        widget.var = var
        return widget
    
    def _get_parameter_values(self) -> Dict[str, Any]:
        """Extract current parameter values from widgets."""
        values = {}
        for param_name, widget_info in self.parameter_widgets.items():
            widget = widget_info['widget']
            param_def = widget_info['definition']
            param_type = param_def.get('type')
            
            var = widget.var
            value = var.get()
            
            # Type conversion
            if param_type == 'int':
                value = int(value)
            elif param_type == 'float':
                value = float(value)
            elif param_type == 'bool':
                value = bool(value)
            
            values[param_name] = value
        
        return values
    
    def _on_generate(self):
        """Handle generate button click."""
        if not self.current_generator:
            messagebox.showerror("Error", "Please select a generation method.")
            return
        
        try:
            # Get dimensions
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive")
            
            # Get parameters
            params = self._get_parameter_values()
            
            # Update status
            self.status_var.set("Generating...")
            self.root.update()
            
            # Generate artwork
            self.artwork = self.current_generator.generate(width, height, params)
            
            # Update status
            self.status_var.set("Generation complete! Ready to save.")
            self._update_info(f"Artwork generated successfully!\n\n"
                            f"Size: {width} x {height}\n"
                            f"Method: {self.generator_var.get()}\n\n"
                            f"Click 'Save as SVG' or 'Save as PNG' to export.")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            self.status_var.set("Error")
        except Exception as e:
            messagebox.showerror("Generation Error", f"An error occurred:\n{str(e)}")
            self.status_var.set("Error")
    
    def _on_save(self, format_type: str):
        """Handle save button click."""
        if not hasattr(self, 'artwork'):
            messagebox.showwarning("No Artwork", "Please generate artwork first.")
            return
        
        # File dialog
        extension = f".{format_type}"
        filetypes = [(f"{format_type.upper()} files", f"*{extension}")]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=extension,
            filetypes=filetypes,
            initialdir=os.path.join(os.path.dirname(__file__), '..', '..', 'output')
        )
        
        if not filename:
            return
        
        try:
            self.status_var.set(f"Saving {format_type.upper()}...")
            self.root.update()
            
            if format_type == 'svg':
                self.current_generator.to_svg(self.artwork, filename)
            elif format_type == 'png':
                self.current_generator.to_png(self.artwork, filename)
            
            self.status_var.set(f"Saved: {os.path.basename(filename)}")
            messagebox.showinfo("Success", f"Artwork saved to:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save:\n{str(e)}")
            self.status_var.set("Save failed")
    
    def _update_info(self, text: str):
        """Update the info text area."""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, text)
