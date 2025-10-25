# Bug Fix: Progress Callback Signature Mismatch

## Issue
When using the Mathematical Patterns Generator, the application crashed with:
```
TypeError: MainWindow._on_progress() takes 3 positional arguments but 4 were given
```

## Root Cause
The `MathematicalPatternsGenerator` internal methods were calling `progress_callback` with three arguments:
- `artwork` (ArtworkData)
- `progress` (float)
- `status` (str) ← **Extra argument causing the error**

However, `MainWindow._on_progress` and the `BaseGenerator` interface only expect two arguments:
- `artwork` (ArtworkData)
- `progress` (float)

Additionally, the internal methods had a `should_abort` parameter that was removed from the public `generate` method but not from the internal methods.

## Fix Applied
1. **Removed `should_abort` parameter** from all internal generation methods:
   - `_generate_spiral`
   - `_generate_wave`
   - `_generate_lissajous`
   - `_generate_fractal_tree`
   - `_generate_circle_pack`

2. **Removed status message argument** from all `progress_callback` calls:
   - Changed: `progress_callback(artwork, progress, "Status message")`
   - To: `progress_callback(artwork, progress)`

3. **Removed all `should_abort` checks** from internal methods since abort functionality is not currently implemented in the base architecture.

## Testing
Verified the fix with a test script that:
- Imports the `MathematicalPatternsGenerator`
- Creates a progress callback with the correct signature
- Generates a spiral pattern
- Confirms no errors occur

## Files Modified
- `src/generators/mathematical.py`

## Commit
```
b01c3dd Fix progress callback signature in MathematicalPatternsGenerator
```

## Status
✅ **RESOLVED** - The Mathematical Patterns Generator now works correctly with the GUI.
