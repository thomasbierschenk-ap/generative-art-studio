# Changelog

All notable changes to the Generative Art Studio project.

## [Unreleased]

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
