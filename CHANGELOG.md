# Changelog

All notable changes to the Generative Art Studio project.

## [Unreleased]

### Fixed - Pause Button Save Buttons (2025-10-26)

#### Issue
- Save buttons remained disabled/greyed out when pausing generation
- Users couldn't save in-progress artwork while paused

#### Solution
- Removed conditional check that was preventing save buttons from enabling
- Save buttons now **always enabled when paused** (since artwork always exists during generation)
- Status message confirms: "Paused - You can save the current artwork"

#### Impact
- Users can now save intermediate artwork at any point during generation
- Better workflow for capturing interesting partial generations
- Consistent with the pause/continue feature's purpose

### Added - Pause/Continue Feature (2025-10-26)

#### New Functionality
- **Replaced Abort with Pause/Continue**: More flexible generation control
  - Pause generation at any point without losing progress
  - Save current artwork while paused
  - Resume generation from where it left off
  - Create multiple saved versions from a single generation run
  - Button dynamically changes between "Pause" and "Continue"

#### User Workflow Improvements
- **Save Intermediate States**: Pause to save interesting partial generations
- **Create Variations**: Save at 25%, 50%, 75%, and 100% completion
- **Layer Mode Compatible**: Pause/save works with layered artwork
- **No Work Lost**: All progress preserved when pausing

#### Technical Implementation
- **Pause State Management**:
  - Added `is_paused` flag for pause state tracking
  - Added `paused_time` to track time spent paused
  - Added `pause_start_time` for current pause timing
- **Smart Time Tracking**:
  - Generation time excludes paused periods
  - Accurate time estimates when resuming
  - Completion message shows actual generation time
- **Thread-Safe Pause Loop**:
  - Generator thread waits in polling loop when paused
  - GUI remains responsive via `update_idletasks()`
  - No complex synchronization needed
- **UI State Management**:
  - Save buttons enabled while paused
  - Save buttons disabled while generating
  - Status messages reflect pause state
  - Progress bar freezes/resumes correctly

#### Benefits
- **More Control**: Stop and examine artwork at any point
- **Multiple Versions**: Create variations from single run
- **Happy Accidents**: Save interesting intermediate states
- **Better Workflow**: Pause to save, then continue adding complexity
- **Layer Friendly**: Works seamlessly with layer mode

#### Documentation
- Created comprehensive `PAUSE_CONTINUE_FEATURE.md`
- Detailed user workflows and examples
- Technical implementation notes
- Future enhancement ideas

### Fixed - User Experience Improvements (2025-10-26)

#### New Feature - Start Angle Parameter
- **Added `start_angle` parameter** to Mathematical Patterns Generator (0-360 degrees)
  - Allows rotation of spiral and Lissajous pattern starting positions
  - Enables more varied compositions and precise pattern orientation
  - Works seamlessly with symmetry parameter
  - Perfect for layering patterns at different angles
  - Default: 0.0 (maintains backward compatibility)

#### Fixed - Save After Abort
- **Save buttons now stay enabled** after aborting generation
  - Previously, save buttons were disabled when aborting incomplete generation
  - Now, if artwork exists, save buttons remain enabled
  - Allows saving interesting partial generations ("happy accidents")
  - Provides more flexibility in the creative process
  - No loss of work when aborting

#### Fixed - Random Walk Wrap Boundary
- **Eliminated straight lines** when using wrap boundary behavior
  - Previously created bizarre horizontal/vertical lines from edge to edge
  - Now breaks path into separate segments when wrapping occurs
  - No visual connection between segments
  - Cleaner, more professional-looking wrap behavior
  - Preserves organic flow of random walk
- **Technical changes**:
  - `_handle_boundary()` now returns wrap detection flag
  - `_generate_walk()` returns list of path segments
  - Segments created automatically when wrap event detected
  - Progress updates handle multiple segments correctly

#### Documentation
- Created comprehensive `FIXES_2025-10-26.md` documenting all three improvements
- Updated CHANGELOG with detailed fix descriptions
- All changes maintain backward compatibility

### Enhanced - Mathematical Patterns Generator (2025-10-26)

#### Bug Fixes
- **Fixed Lissajous straight lines**: Changed `closed=False` to prevent unwanted line connecting end to start
- **Improved visual quality**: Patterns now look more natural and less "computer-generated"

#### New Parameters - Color System
- **color_scheme** (replaces use_gradient): 6 color schemes
  - `gradient`: Smooth hue transition (default)
  - `monochrome`: Brightness variation only
  - `complementary`: Alternates between base and opposite colors
  - `analogous`: Colors within 60° of base hue
  - `triadic`: Three colors 120° apart
  - `random`: Random colors within variation range
- **color_variation** (0-100): Control how much colors vary from base
  - 0 = uniform color
  - 100 = maximum variation
  - Default: 30

#### New Parameters - Organic Variation
- **organic_factor** (0-1): Add controlled randomness and imperfection
  - 0 = perfect mathematical patterns (default)
  - 1 = highly organic, natural-looking
  - Effects:
    - Spirals: wobble, radius variation, position jitter
    - Waves: phase shifts, offset variation, jitter
    - Lissajous: parameter variation, jitter
    - Fractal Trees: random angles, 2-4 branches, asymmetric growth
    - Circle Packing: radius variation, organic clustering
- **completeness** (0.3-1.0): Control how complete the pattern is
  - 1.0 = full pattern (default)
  - 0.3 = only 30% drawn
  - Creates partial/incomplete aesthetics
  - For trees: randomly skips branches

#### Technical Improvements
- **Proper HSV color system**: Accurate RGB ↔ HSV conversion
- **Enhanced color manipulation**: Independent hue, saturation, value control
- **Pattern-specific organic variation**: Each pattern type has tailored randomness
- **Variable branch counts**: Fractal trees now generate 2-4 branches (not fixed at 2)
- **Backward compatible**: All new parameters have sensible defaults

#### User Experience
- **More interesting patterns**: Less regular, more organic feel
- **Greater creative control**: Fine-tune randomness and color schemes
- **Partial patterns**: Create sketch-like, incomplete aesthetics
- **Rich color options**: 6 different color distribution schemes

### Added - Mathematical Patterns Generator (2025-10-25) - Phase 3

#### New Generator Type
- **Mathematical Patterns Generator**: Create geometric art using mathematical formulas
- **5 Pattern Types**:
  - **Spiral**: Archimedean spirals with configurable complexity
  - **Wave**: Harmonic wave patterns with multiple frequencies
  - **Lissajous**: Beautiful parametric curves
  - **Fractal Tree**: Recursive branching structures
  - **Circle Pack**: Organic circle packing algorithms

#### Configurable Parameters
- **Density**: Control number of elements (10-500)
- **Complexity**: Adjust pattern intricacy (0.5-5.0)
- **Symmetry**: Create radial symmetry (1-12 repetitions)
- **Line Width**: Customize stroke width (0.5-10.0)
- **Primary Color**: Choose main pattern color
- **Color Gradient**: Enable dynamic color transitions
- **Background Color**: Set canvas background

#### Technical Features
- Progress tracking for each pattern type
- Abort support during generation
- Gradient color generation algorithm
- Optimized circle packing with collision detection
- Recursive fractal tree generation with depth limiting
- Full integration with layer mode for pattern mixing

#### User Experience
- Available in method selector dropdown (📐 Mathematical Patterns)
- Dynamic parameters update when selected
- Can be layered with Random Walk patterns
- Real-time preview during generation
- Export to PNG and SVG formats

### Added - GUI Method Selector (2025-10-25) - Phase 2

#### Method Selection UI
- **Method selector dropdown**: Choose between available generators
- **Method description display**: Shows description below selector
- **Dynamic parameter panel**: Parameters update when method changes
- **Window title updates**: Shows current method name
- **Smooth transitions**: Clean UI updates when switching methods

#### Layer History Tracking
- **Track methods used**: Records which generators created each layer
- **Display layer info**: Status shows "2 layers (Random Walk + Random Walk)"
- **Clear on reset**: Layer history cleared when canvas is cleared
- **Informative feedback**: Users see what methods were combined

#### Enhanced UX
- **Method change handler**: Smoothly switches between generators
- **Parameter rebuilding**: Automatic UI updates for new method
- **Status messages**: Clear feedback on method switching
- **Title updated**: "Generative Art Studio" + current method in window title

#### Technical Implementation
- Method selector with ComboboxSelected event binding
- Dynamic parameter panel rebuilding
- Layer history list tracking
- Enhanced status messages with layer information

### Added - Multi-Generator Architecture (2025-10-25) - Phase 1

#### Architecture Refactoring
- **BaseGenerator enhancements**: Added `get_description()` and `get_icon()` methods
- **Multi-generator support**: App now manages multiple generators in a dictionary
- **Dynamic generator selection**: Foundation for method selector dropdown
- **Layer history tracking**: Track which methods were used in layered artwork
- **Improved modularity**: Easy to add new generator types

#### Generator Updates
- RandomWalkGenerator now provides description and icon
- All generators implement consistent interface
- Backwards compatible with existing code

#### Testing
- Created comprehensive test suite for multi-generator architecture
- Verified backwards compatibility
- Tested generator interface methods
- Validated export functions

### Fixed - UI Layout Issues (2025-10-25)

#### Window Size and Layout
- **Increased window size** from 1400x900 to 1500x1000 for better content fit
- **Fixed control panel width** - increased from 450px to 480px
- **Fixed inner canvas width** - increased from 400px to 460px (key fix for cut-off borders)
- **Reduced horizontal padding** on all sections from 10px to 5px
- **Result**: All LabelFrame borders now fully visible, no scrolling needed

#### Layer Mode Fixes
- **Fixed layer mode functionality** - previous artwork now stays visible during new generation
- **Fixed import error** - changed from relative to absolute imports to work in threaded context
- **Fixed real-time preview** - both old and new artwork visible during generation
- **Result**: Layer mode works perfectly, allowing multiple generations to be layered

### Added - Progress Tracking & Control Features (2025-10-25)

#### New Features
- **Progress Indicator with Time Estimation**: Real-time display showing:
  - Current progress percentage
  - Estimated time remaining (dynamically calculated)
  - Total time taken upon completion
- **Abort Button**: Stop generation in progress at any time
- **Clear Canvas Button**: Clear the preview and reset the workspace
- **Enhanced Progress Display**: Formatted time display (seconds, minutes, hours)

#### UI Improvements
- Progress section with labeled frame
- Abort and Clear buttons in a convenient row layout
- Progress information label showing percentage and time estimates
- Proper button state management (enabled/disabled based on context)
- Status messages for all actions (generating, complete, aborted, cleared)

#### Technical Enhancements
- Time tracking from generation start
- Dynamic time estimation based on progress rate
- Abort handling with proper cleanup
- Thread-safe abort mechanism
- Graceful error handling for interrupted generation

### Added - Live Preview Feature (2025-10-25)

#### Major Features
- **Live Preview Canvas**: Watch artwork being created in real-time as the algorithm runs
- **Real-time Progress Updates**: Visual feedback showing generation progress with progress bar
- **Responsive Preview**: Canvas automatically scales and adjusts to window size
- **Thread-based Generation**: Non-blocking generation keeps UI responsive

#### Technical Improvements
- Updated `BaseGenerator` to support progress callbacks
- Modified `RandomWalkGenerator` to send incremental updates during generation
- Completely rewrote `MainWindow` with modern layout and preview panel
- Added threading support for background generation
- Implemented PIL-based rendering for preview canvas

#### UI Enhancements
- Split-pane layout with controls on left, preview on right
- Improved parameter controls with better visual feedback
- Save buttons enabled only after generation completes
- Status messages and progress tracking
- Color picker with visual preview

#### Documentation
- Added comprehensive `GUI_GUIDE.md` with detailed instructions
- Updated `README.md` to highlight live preview feature
- Enhanced `QUICK_START.md` with GUI section
- Documented workflow, tips, and troubleshooting

### Fixed
- Tkinter 9.0 compatibility issue (trace -> trace_add)
- Preview scaling maintains aspect ratio
- Thread safety for UI updates

### Removed
- Obsolete installation workaround scripts
- Unused pip configuration files

---

## [0.1.0] - Initial Release (2025-10-24)

### Added
- Random Walk generator with extensive parameters
- CLI interface with interactive prompts
- GUI interface with parameter controls
- SVG and PNG export capabilities
- Comprehensive documentation
- Test suite
- Multiple color modes (monochrome, grayscale, color, rainbow)
- Boundary behaviors (bounce, wrap, stop, ignore)
- Configurable output dimensions

### Documentation
- README.md with overview and usage
- INSTALL.md with detailed installation instructions
- QUICK_START.md for immediate usage
- CLI_GUIDE.md for command-line interface
- ARCHITECTURE.md explaining system design
- DEVELOPMENT.md for contributors
- EXAMPLES.md with sample configurations
- TROUBLESHOOTING.md for common issues
- TKINTER_ISSUE.md for GUI compatibility
- SQUARE_NETWORK_README.md for corporate network issues
- BLOCK_SETUP_NOTES.md for Block/Square Python setup

### Technical
- Modular architecture with base generator class
- Type hints throughout codebase
- Comprehensive parameter validation
- Support for venv and uv package managers
- Git repository with proper .gitignore
- Automated test scripts

---

## Version History

- **v0.2.0** (Unreleased): Live preview feature
- **v0.1.0** (2025-10-24): Initial release with Random Walk generator

---

## Future Plans

### Short Term
- Add more generator types (fractals, mathematical patterns)
- Implement preset saving/loading
- Add keyboard shortcuts to GUI
- Export animation sequences

### Long Term
- Plugin system for custom generators
- Gallery view of generated works
- Batch generation capabilities
- Additional export formats (PDF, EPS)
- Web-based interface
- Cloud rendering for complex generations
