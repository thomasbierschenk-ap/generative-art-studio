# Recent Updates - Generative Art Studio

## Version 1.1.0 - Live Preview Fix & Layering Feature

### Date: 2025-10-25

### Issues Fixed

#### 1. Live Preview Not Updating During Generation
**Problem:** The live preview and progress bar would only update to 100% after the entire generation was complete, rather than showing incremental progress.

**Root Cause:** The progress callback was being called from the worker thread, but the GUI wasn't processing the updates until the generation thread completed.

**Solution:**
- Changed from `root.after()` to direct updates with `update_idletasks()`
- Added a small `time.sleep(0.01)` to allow the GUI thread to process events
- This forces the GUI to update immediately when progress callbacks are received

**Result:** The preview canvas now updates smoothly during generation, showing each walk being drawn in real-time. The progress bar increments gradually, and time estimates update continuously.

### New Features

#### 2. Layer Mode - Build Complex Compositions
**Feature:** Added a "Keep previous artwork (layer mode)" checkbox that allows overlaying multiple generations.

**How It Works:**
- When **unchecked** (default): Each generation replaces the previous artwork
- When **checked**: New generations are added on top of existing artwork
- The background color from the first layer is preserved
- All paths and circles from previous layers are combined with new ones

**Use Cases:**
- Build up complex, multi-layered compositions iteratively
- Create depth by layering different densities and colors
- Experiment with complementary colors and contrasting styles
- Save intermediate results before adding more layers

**Implementation:**
- Added `layer_mode_var` checkbox to the GUI
- Modified `_generate_artwork()` to merge previous and new artwork when layer mode is enabled
- Uses `ArtworkData` to combine paths and circles from multiple generations

### Technical Changes

**File: `src/gui/main_window.py`**
- Added `keep_layers` state variable
- Added `layer_mode_var` checkbox widget
- Modified `_on_progress()` to use `update_idletasks()` and `time.sleep()`
- Modified `_generate_artwork()` to support artwork merging
- Improved progress callback handling for smoother updates

**File: `docs/GUI_GUIDE.md`**
- Added layer mode documentation
- Created "Layered Compositions (Advanced)" section
- Included three example workflows
- Added layering tips and best practices

### Usage Examples

#### Basic Layering Workflow:
```
1. Generate base layer (e.g., 10 green walks, bounce behavior)
2. Check "Keep previous artwork (layer mode)"
3. Adjust parameters (e.g., 5 red walks, different angle)
4. Click Generate to add new layer
5. Repeat steps 3-4 to add more layers
6. Save when satisfied, or Clear Canvas to start fresh
```

#### Example: Organic Landscape
```
Layer 1: 20 green walks, small steps → grass/foliage
Layer 2: 10 brown walks, medium steps → tree trunks
Layer 3: 5 yellow walks, small steps → sunlight rays
```

### Performance Notes

- Live preview updates occur approximately every 50 steps
- Small sleep (10ms) per update has minimal performance impact
- Layering has no performance penalty - it's just data merging
- Complex multi-layer compositions render at the same speed as single layers

### Backward Compatibility

- All existing functionality remains unchanged
- Layer mode is opt-in via checkbox (default: off)
- CLI and test scripts are unaffected
- Saved files (PNG/SVG) work exactly as before

### Testing

Tested scenarios:
- ✅ Live preview updates during generation
- ✅ Progress bar increments smoothly
- ✅ Time estimates update continuously
- ✅ Layer mode preserves previous artwork
- ✅ Layer mode combines paths and circles correctly
- ✅ Background color preserved from first layer
- ✅ Clear canvas resets everything properly
- ✅ Abort button works during generation
- ✅ Save buttons work with layered compositions

### Known Limitations

- Layer mode doesn't support undo (use Save incrementally)
- No layer visibility toggle (all layers always visible)
- No layer reordering (layers are added in generation order)
- Background color is always from the first layer

### Future Enhancements

Potential improvements for layering:
- Layer management panel (show/hide, reorder, delete)
- Opacity control per layer
- Blend modes (multiply, screen, overlay, etc.)
- Layer naming and organization
- Undo/redo for layer operations
- Export individual layers

### Documentation

Updated files:
- `docs/GUI_GUIDE.md` - Added layering section with examples
- `UPDATES.md` - This file
- Git commit messages with detailed change descriptions

### How to Use

**Launch the GUI:**
```bash
./run_gui_modern.sh
```

**Try the live preview:**
1. Set Steps per Walk to 5000+
2. Click Generate
3. Watch the preview update in real-time!

**Try layering:**
1. Generate first artwork
2. Check "Keep previous artwork (layer mode)"
3. Change colors/parameters
4. Generate again to overlay
5. Repeat to build complex compositions!

### Feedback Welcome

If you encounter any issues or have suggestions for improvements, please let us know!
