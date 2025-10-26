# Pause Button Save Fix

**Date**: 2025-10-26

## Issue

When pausing generation, the save buttons (Save as PNG, Save as SVG) remained disabled/greyed out, preventing users from saving the current in-progress artwork.

## Root Cause

In the `_on_pause_continue` method, when pausing generation, the code was checking `if self.current_artwork:` before enabling the save buttons. During generation, artwork is always being created and updated via the progress callback, so this conditional check was preventing the buttons from being enabled.

## Solution

Removed the conditional check when pausing. The save buttons are now **always enabled when paused**, since there's always artwork during generation that can be saved.

### Code Change

**Before:**
```python
# Pause generation
self.is_paused = True
self.pause_start_time = time.time()
self.pause_btn.config(text="Continue")
self.status_var.set("Paused - You can save the current artwork")
# Enable save buttons while paused
if self.current_artwork:
    self.save_png_btn.config(state=tk.NORMAL)
    self.save_svg_btn.config(state=tk.NORMAL)
```

**After:**
```python
# Pause generation
self.is_paused = True
self.pause_start_time = time.time()
self.pause_btn.config(text="Continue")
self.status_var.set("Paused - You can save the current artwork")
# Enable save buttons while paused (there's always artwork during generation)
self.save_png_btn.config(state=tk.NORMAL)
self.save_svg_btn.config(state=tk.NORMAL)
```

## Testing

- Import test passed successfully
- Save buttons should now be enabled immediately when pausing generation
- Users can save in-progress artwork at any point during generation

## Files Modified

- `src/gui/main_window.py`: Updated `_on_pause_continue` method
