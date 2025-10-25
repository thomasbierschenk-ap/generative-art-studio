"""
Main window for the Generative Art Studio GUI.

Provides an interface for configuring parameters and generating artwork with live preview.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from typing import Dict, Any, Optional
import threading
import time
from PIL import Image, ImageTk, ImageDraw
import os


class MainWindow:
    """Main application window with live preview canvas."""
    
    def __init__(self, root: tk.Tk, generators: Dict[str, Any], output_dir: str):
        """
        Initialize the main window.
        
        Args:
            root: Tkinter root window
            generators: Dictionary of available generators {name: instance}
            output_dir: Directory for saving output files
        """
        self.root = root
        self.generators = generators
        self.current_generator_name = list(generators.keys())[0]
        self.current_generator = generators[self.current_generator_name]
        self.output_dir = output_dir
        
        # State
        self.param_widgets: Dict[str, Any] = {}
        self.current_artwork = None
        self.is_generating = False
        self.preview_image = None
        self.abort_generation = False
        self.generation_start_time = None
        self.layer_history = []  # Track which methods were used
        
        # Set up the window
        self.root.title(f"Generative Art Studio - {self.current_generator_name}")
        self.root.geometry("1500x1000")
        
        # Create the UI
        self._create_ui()
        
    def _create_ui(self):
        """Create the user interface layout."""
        # Main container - use grid for better control
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0, minsize=480)  # Left panel fixed - increased width
        self.root.grid_columnconfigure(1, weight=1)  # Right panel expands
        
        # Left panel: Controls (fixed width)
        left_panel = ttk.Frame(self.root, width=480)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(5, 2), pady=5)
        left_panel.grid_propagate(False)  # Maintain fixed width
        
        # Right panel: Preview canvas (takes remaining space)
        right_panel = ttk.Frame(self.root)
        right_panel.grid(row=0, column=1, sticky='nsew', padx=(2, 5), pady=5)
        
        # Build left panel
        self._create_control_panel(left_panel)
        
        # Build right panel
        self._create_preview_panel(right_panel)
        
    def _create_control_panel(self, parent):
        """Create the control panel with parameters."""
        # Scrollable frame for parameters
        canvas = tk.Canvas(parent, width=460)  # Increased from 400 to 460
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(
            scrollable_frame,
            text="Generative Art Studio",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Method Selector
        method_frame = ttk.LabelFrame(scrollable_frame, text="Generator Method", padding=10)
        method_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.method_var = tk.StringVar(value=self.current_generator_name)
        method_dropdown = ttk.Combobox(
            method_frame,
            textvariable=self.method_var,
            values=list(self.generators.keys()),
            state='readonly',
            width=35
        )
        method_dropdown.pack(fill=tk.X, padx=5, pady=5)
        method_dropdown.bind('<<ComboboxSelected>>', self._on_method_changed)
        
        # Method description
        self.method_desc_var = tk.StringVar(value=self.current_generator.get_description())
        desc_label = ttk.Label(
            method_frame,
            textvariable=self.method_desc_var,
            wraplength=420,
            font=("Arial", 9),
            foreground="gray"
        )
        desc_label.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Output size section
        size_frame = ttk.LabelFrame(scrollable_frame, text="Output Size", padding=10)
        size_frame.pack(fill=tk.X, padx=5, pady=5)  # Reduced padx from 10 to 5
        
        ttk.Label(size_frame, text="Width:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.width_var = tk.IntVar(value=800)
        width_entry = ttk.Entry(size_frame, textvariable=self.width_var, width=10)
        width_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(size_frame, text="Height:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.height_var = tk.IntVar(value=600)
        height_entry = ttk.Entry(size_frame, textvariable=self.height_var, width=10)
        height_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Generator parameters
        self.params_frame = ttk.LabelFrame(scrollable_frame, text="Parameters", padding=10)
        self.params_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Reduced padx from 10 to 5
        
        self._create_parameter_controls(self.params_frame)
        
        # Action buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)  # Reduced padx from 10 to 5
        
        # Layer mode checkbox
        layer_frame = ttk.Frame(button_frame)
        layer_frame.pack(fill=tk.X, pady=2)
        
        self.layer_mode_var = tk.BooleanVar(value=False)
        layer_checkbox = ttk.Checkbutton(
            layer_frame,
            text="Keep previous artwork (layer mode)",
            variable=self.layer_mode_var
        )
        layer_checkbox.pack(side=tk.LEFT)
        
        self.generate_btn = ttk.Button(
            button_frame,
            text="Generate",
            command=self._on_generate,
            style="Accent.TButton"
        )
        self.generate_btn.pack(fill=tk.X, pady=2)
        
        # Abort and Clear buttons in a row
        control_row = ttk.Frame(button_frame)
        control_row.pack(fill=tk.X, pady=2)
        
        self.abort_btn = ttk.Button(
            control_row,
            text="Abort",
            command=self._on_abort,
            state=tk.DISABLED
        )
        self.abort_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        self.clear_btn = ttk.Button(
            control_row,
            text="Clear Canvas",
            command=self._on_clear
        )
        self.clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        
        self.save_png_btn = ttk.Button(
            button_frame,
            text="Save as PNG",
            command=lambda: self._on_save('png'),
            state=tk.DISABLED
        )
        self.save_png_btn.pack(fill=tk.X, pady=2)
        
        self.save_svg_btn = ttk.Button(
            button_frame,
            text="Save as SVG",
            command=lambda: self._on_save('svg'),
            state=tk.DISABLED
        )
        self.save_svg_btn.pack(fill=tk.X, pady=2)
        
        # Progress section
        progress_frame = ttk.LabelFrame(button_frame, text="Progress", padding=5)
        progress_frame.pack(fill=tk.X, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=2)
        
        # Progress info (percentage and time)
        self.progress_info_var = tk.StringVar(value="0% - Estimated time: --")
        progress_info_label = ttk.Label(progress_frame, textvariable=self.progress_info_var, font=("Arial", 9))
        progress_info_label.pack(pady=2)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(button_frame, textvariable=self.status_var)
        status_label.pack(pady=2)
        
        # Pack scrollbar and canvas
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _create_preview_panel(self, parent):
        """Create the preview canvas panel."""
        # Title
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(
            title_frame,
            text="Live Preview",
            font=("Arial", 14, "bold")
        ).pack(side=tk.LEFT)
        
        # Canvas for preview
        canvas_frame = ttk.Frame(parent, relief=tk.SUNKEN, borderwidth=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.preview_canvas = tk.Canvas(
            canvas_frame,
            bg='white',
            highlightthickness=0
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind resize event
        self.preview_canvas.bind('<Configure>', self._on_canvas_resize)
        
    def _create_parameter_controls(self, parent):
        """Create controls for generator parameters."""
        params = self.current_generator.get_parameters()
        
        row = 0
        for param_name, param_def in params.items():
            param_type = param_def.get('type')
            label_text = param_def.get('label', param_name)
            help_text = param_def.get('help', '')
            
            # Label
            label = ttk.Label(parent, text=f"{label_text}:")
            label.grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
            
            # Create appropriate control based on type
            if param_type == 'int' or param_type == 'float':
                self._create_numeric_control(parent, row, param_name, param_def)
            
            elif param_type == 'bool':
                self._create_bool_control(parent, row, param_name, param_def)
            
            elif param_type == 'choice':
                self._create_choice_control(parent, row, param_name, param_def)
            
            elif param_type == 'color':
                self._create_color_control(parent, row, param_name, param_def)
            
            row += 1
    
    def _create_numeric_control(self, parent, row, param_name, param_def):
        """Create a numeric slider control."""
        is_float = param_def.get('type') == 'float'
        min_val = param_def.get('min', 0)
        max_val = param_def.get('max', 100)
        default = param_def.get('default', min_val)
        
        # Variable
        if is_float:
            var = tk.DoubleVar(value=default)
        else:
            var = tk.IntVar(value=default)
        
        self.param_widgets[param_name] = var
        
        # Frame for slider and value
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Slider
        slider = ttk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            variable=var,
            orient=tk.HORIZONTAL
        )
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Value label
        value_label = ttk.Label(frame, text=str(default), width=8)
        value_label.pack(side=tk.LEFT, padx=5)
        
        # Update label when slider changes
        def update_label(*args):
            if is_float:
                value_label.config(text=f"{var.get():.2f}")
            else:
                value_label.config(text=str(int(var.get())))
        
        var.trace_add('write', update_label)
    
    def _create_bool_control(self, parent, row, param_name, param_def):
        """Create a checkbox control."""
        default = param_def.get('default', False)
        var = tk.BooleanVar(value=default)
        self.param_widgets[param_name] = var
        
        checkbox = ttk.Checkbutton(parent, variable=var)
        checkbox.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
    
    def _create_choice_control(self, parent, row, param_name, param_def):
        """Create a dropdown control."""
        choices = param_def.get('choices', [])
        default = param_def.get('default', choices[0] if choices else '')
        
        var = tk.StringVar(value=default)
        self.param_widgets[param_name] = var
        
        dropdown = ttk.Combobox(
            parent,
            textvariable=var,
            values=choices,
            state='readonly',
            width=20
        )
        dropdown.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
    
    def _create_color_control(self, parent, row, param_name, param_def):
        """Create a color picker control."""
        default = param_def.get('default', '#000000')
        var = tk.StringVar(value=default)
        self.param_widgets[param_name] = var
        
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Color preview
        color_preview = tk.Canvas(frame, width=30, height=20, bg=default, relief=tk.SUNKEN, borderwidth=1)
        color_preview.pack(side=tk.LEFT, padx=5)
        
        # Pick button
        def pick_color():
            color = colorchooser.askcolor(initialcolor=var.get())[1]
            if color:
                var.set(color)
                color_preview.config(bg=color)
        
        pick_btn = ttk.Button(frame, text="Pick", command=pick_color, width=8)
        pick_btn.pack(side=tk.LEFT)
        
        # Entry for manual input
        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side=tk.LEFT, padx=5)
        
        def update_preview(*args):
            try:
                color_preview.config(bg=var.get())
            except:
                pass
        
        var.trace_add('write', update_preview)
    
    def _get_parameters(self) -> Dict[str, Any]:
        """Get current parameter values from widgets."""
        params = {}
        for name, var in self.param_widgets.items():
            params[name] = var.get()
        return params
    
    def _on_generate(self):
        """Handle generate button click."""
        if self.is_generating:
            return
        
        self.is_generating = True
        self.abort_generation = False
        self.generation_start_time = time.time()
        
        self.generate_btn.config(state=tk.DISABLED)
        self.abort_btn.config(state=tk.NORMAL)
        self.save_png_btn.config(state=tk.DISABLED)
        self.save_svg_btn.config(state=tk.DISABLED)
        self.status_var.set("Generating...")
        self.progress_var.set(0)
        self.progress_info_var.set("0% - Estimated time: calculating...")
        
        # Run generation in a separate thread
        thread = threading.Thread(target=self._generate_artwork)
        thread.daemon = True
        thread.start()
    
    def _on_abort(self):
        """Handle abort button click."""
        if self.is_generating:
            self.abort_generation = True
            self.status_var.set("Aborting...")
            self.abort_btn.config(state=tk.DISABLED)
    
    def _on_clear(self):
        """Handle clear canvas button click."""
        self.preview_canvas.delete("all")
        self.current_artwork = None
        self.preview_image = None
        self.layer_history = []
        self.save_png_btn.config(state=tk.DISABLED)
        self.save_svg_btn.config(state=tk.DISABLED)
        self.status_var.set("Canvas cleared")
        self.progress_var.set(0)
        self.progress_info_var.set("0% - Estimated time: --")
    
    def _on_method_changed(self, event=None):
        """Handle method selection change."""
        new_method = self.method_var.get()
        
        if new_method == self.current_generator_name:
            return  # No change
        
        # Update current generator
        self.current_generator_name = new_method
        self.current_generator = self.generators[new_method]
        
        # Update description
        self.method_desc_var.set(self.current_generator.get_description())
        
        # Update window title
        self.root.title(f"Generative Art Studio - {new_method}")
        
        # Rebuild parameter panel
        self._rebuild_parameter_panel()
        
        # Update status
        self.status_var.set(f"Switched to {new_method}")
    
    def _rebuild_parameter_panel(self):
        """Rebuild parameter controls for current generator."""
        # Clear existing parameter widgets
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        self.param_widgets.clear()
        
        # Recreate parameter controls for current generator
        self._create_parameter_controls(self.params_frame)
        
        # Force update
        self.params_frame.update_idletasks()
    
    def _generate_artwork(self):
        """Generate artwork in background thread."""
        try:
            width = self.width_var.get()
            height = self.height_var.get()
            params = self._get_parameters()
            
            # Check if we should keep previous artwork (layer mode)
            previous_artwork = None
            if self.layer_mode_var.get() and self.current_artwork:
                # Store previous artwork to merge later
                previous_artwork = self.current_artwork
            
            # Generate with progress callback - use wrapper to handle layering
            if previous_artwork:
                # Create a wrapper callback that merges artwork during generation
                def layer_progress_callback(new_artwork, progress):
                    # Import here to avoid circular imports
                    from generators.base import ArtworkData
                    # Merge with previous artwork
                    merged_artwork = ArtworkData(
                        width=width,
                        height=height,
                        background_color=previous_artwork.background_color,
                        paths=previous_artwork.paths + new_artwork.paths,
                        circles=previous_artwork.circles + new_artwork.circles
                    )
                    self._on_progress(merged_artwork, progress)
                
                new_artwork = self.current_generator.generate(
                    width, height, params,
                    progress_callback=layer_progress_callback
                )
                
                # Final merge
                from generators.base import ArtworkData
                self.current_artwork = ArtworkData(
                    width=width,
                    height=height,
                    background_color=previous_artwork.background_color,
                    paths=previous_artwork.paths + new_artwork.paths,
                    circles=previous_artwork.circles + new_artwork.circles
                )
            else:
                new_artwork = self.current_generator.generate(
                    width, height, params,
                    progress_callback=self._on_progress
                )
                self.current_artwork = new_artwork
                # Reset layer history for new artwork
                self.layer_history = [self.current_generator_name]
            
            # Track layer if in layer mode
            if previous_artwork:
                self.layer_history.append(self.current_generator_name)
            
            # Final update
            self.root.after(0, self._on_generation_complete)
            
        except Exception as e:
            import traceback
            error_msg = str(e)
            traceback.print_exc()  # Print full traceback for debugging
            self.root.after(0, lambda: self._on_generation_error(error_msg))
    
    def _on_progress(self, artwork, progress):
        """Handle progress updates from generator."""
        # Check if abort was requested
        if self.abort_generation:
            raise InterruptedError("Generation aborted by user")
        
        # Calculate estimated time remaining
        if self.generation_start_time and progress > 0:
            elapsed = time.time() - self.generation_start_time
            total_estimated = elapsed / (progress / 100.0)
            remaining = total_estimated - elapsed
            
            if remaining < 60:
                time_str = f"{int(remaining)}s"
            elif remaining < 3600:
                time_str = f"{int(remaining / 60)}m {int(remaining % 60)}s"
            else:
                hours = int(remaining / 3600)
                minutes = int((remaining % 3600) / 60)
                time_str = f"{hours}h {minutes}m"
            
            progress_text = f"{int(progress)}% - Est. time remaining: {time_str}"
        else:
            progress_text = f"{int(progress)}% - Est. time remaining: calculating..."
        
        # Update UI - use update_idletasks to force immediate GUI update
        self.progress_var.set(progress)
        self.progress_info_var.set(progress_text)
        self._update_preview(artwork)
        
        # Force GUI to process pending events
        self.root.update_idletasks()
        
        # Small sleep to allow GUI thread to breathe
        time.sleep(0.01)
    
    def _update_preview(self, artwork):
        """Update the preview canvas with current artwork."""
        if not artwork:
            return
        
        # Convert artwork to PIL Image
        img = Image.new('RGB', (artwork.width, artwork.height), artwork.background_color)
        draw = ImageDraw.Draw(img)
        
        # Draw paths
        for path in artwork.paths:
            if len(path.points) >= 2:
                if path.width <= 1:
                    draw.line(path.points, fill=path.color, width=1)
                else:
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
                draw.ellipse(bbox, fill=None, outline=circle.color, width=int(circle.stroke_width))
        
        # Scale to fit canvas
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            # Calculate scaling to fit
            scale_x = canvas_width / artwork.width
            scale_y = canvas_height / artwork.height
            scale = min(scale_x, scale_y, 1.0)  # Don't scale up
            
            new_width = int(artwork.width * scale)
            new_height = int(artwork.height * scale)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.preview_image = ImageTk.PhotoImage(img)
            
            # Clear canvas and draw image
            self.preview_canvas.delete("all")
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            self.preview_canvas.create_image(x, y, anchor=tk.NW, image=self.preview_image)
    
    def _on_canvas_resize(self, event):
        """Handle canvas resize event."""
        if self.current_artwork:
            self._update_preview(self.current_artwork)
    
    def _on_generation_complete(self):
        """Handle successful generation completion."""
        self.is_generating = False
        self.abort_generation = False
        
        self.generate_btn.config(state=tk.NORMAL)
        self.abort_btn.config(state=tk.DISABLED)
        self.save_png_btn.config(state=tk.NORMAL)
        self.save_svg_btn.config(state=tk.NORMAL)
        
        # Calculate total time and show layer info
        if self.generation_start_time:
            elapsed = time.time() - self.generation_start_time
            if elapsed < 60:
                time_str = f"{elapsed:.1f}s"
            else:
                time_str = f"{int(elapsed / 60)}m {int(elapsed % 60)}s"
            
            # Add layer info if multiple layers
            layer_count = len(self.layer_history)
            if layer_count > 1:
                methods = " + ".join(self.layer_history)
                status = f"Complete! {layer_count} layers ({methods}) - {time_str}"
            else:
                status = f"Generation complete! (took {time_str})"
            
            self.status_var.set(status)
        else:
            self.status_var.set("Generation complete!")
        
        self.progress_var.set(100)
        self.progress_info_var.set("100% - Complete")
        
        # Update preview with final artwork
        self._update_preview(self.current_artwork)
    
    def _on_generation_error(self, error_msg):
        """Handle generation error."""
        self.is_generating = False
        self.abort_generation = False
        
        self.generate_btn.config(state=tk.NORMAL)
        self.abort_btn.config(state=tk.DISABLED)
        
        # Check if it was an abort
        if "aborted" in error_msg.lower() or "interrupted" in error_msg.lower():
            self.status_var.set("Generation aborted by user")
            self.progress_info_var.set("Aborted")
        else:
            self.status_var.set("Error!")
            self.progress_info_var.set("Error occurred")
            messagebox.showerror("Generation Error", f"Failed to generate artwork:\n{error_msg}")
    
    def _on_save(self, format_type):
        """Handle save button click."""
        if not self.current_artwork:
            return
        
        # Ask for filename
        if format_type == 'png':
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialdir=self.output_dir
            )
            if filename:
                self.current_generator.to_png(self.current_artwork, filename)
                self.status_var.set(f"Saved: {os.path.basename(filename)}")
        
        elif format_type == 'svg':
            filename = filedialog.asksaveasfilename(
                defaultextension=".svg",
                filetypes=[("SVG files", "*.svg"), ("All files", "*.*")],
                initialdir=self.output_dir
            )
            if filename:
                self.current_generator.to_svg(self.current_artwork, filename)
                self.status_var.set(f"Saved: {os.path.basename(filename)}")
