# Prototype Scripts - Development History

This directory contains early prototypes and experimental implementations of YouTube data collection workflows. Each script represents different approaches and iterations in developing the autonomous data collection system.

---

## Script Overview

### 📹 `youtube.py` - Single Video Automation
**Purpose**: Basic YouTube automation for single video data collection

**Features**:
- Random search term selection from multi-language noun list (200+ terms)
- First video result selection and playback
- "Stats for Nerds" activation via right-click context menu
- Basic telemetry monitoring and display
- Firefox browser automation using Playwright

**Approach**: Simplified single-video workflow focusing on core telemetry extraction functionality.

**Key Learning**: Established basic Playwright patterns for YouTube interaction and stats panel access.

---

### 🔄 `workflow.py` - Multi-Video Collection Engine
**Purpose**: Advanced multi-video data collection with comprehensive telemetry logging

**Features**:
- **Batch Processing**: Configurable number of videos (user input)
- **Smart Sampling**: Random watch time selection (0 to full duration)
- **Continuous Monitoring**: Real-time stats collection during playback
- **Structured Output**: JSON telemetry export with metadata
- **Error Handling**: Graceful handling of missing videos or stats panel

**Data Collected**:
- Video URL and search query
- Full video duration vs. actual watch time
- Timestamped telemetry data throughout playback
- Complete stats panel snapshots

**Innovation**: First implementation of realistic viewing patterns with randomized watch times.

---

### 🤖 `gen-youtube.py` - Pure Playwright Recording
**Purpose**: Raw Playwright codegen output for YouTube interaction

**Characteristics**:
- **Generated Code**: Direct output from `playwright codegen`
- **Hardcoded Actions**: Specific element targeting and fixed interactions
- **Sequential Operations**: Linear workflow without randomization
- **Manual Triggers**: Requires specific video availability

**Historical Context**: Represents the baseline automation before AI enhancement and generalization.

**Limitations**: 
- Brittle element selectors
- No error handling
- Fixed search terms and interactions
- Not suitable for production use

---

### 🎯 `add_grid_to_screenshot.py` - PyAutoGUI Development Tool
**Purpose**: Coordinate identification helper for PyAutoGUI-based automation

**Functionality**:
- **Grid Overlay**: Draws coordinate grid on screenshots
- **Large Font Labels**: Clearly marked X/Y coordinates
- **Visual Debugging**: Helps identify click targets
- **Direct Clicking**: Includes example coordinate-based clicking

**Development Role**: 
- Facilitated early PyAutoGUI experiments
- Provided visual debugging for coordinate-based automation
- Bridged gap between visual inspection and programmatic interaction

**Note**: Later superseded by Playwright's more robust element targeting.

---

## Development Evolution

### Phase 1: Manual Recording (`gen-youtube.py`)
- **Approach**: Playwright's built-in recording functionality
- **Output**: Basic but brittle automation script
- **Learning**: Understanding of YouTube's DOM structure and interaction patterns

### Phase 2: Basic Automation (`youtube.py`)
- **Enhancement**: Added randomization and multi-language support
- **Improvement**: Proper error handling and browser management
- **Foundation**: Established core telemetry extraction workflow

### Phase 3: Production Ready (`workflow.py`)
- **Scaling**: Multi-video batch processing
- **Intelligence**: Realistic viewing patterns and smart sampling
- **Data Quality**: Comprehensive telemetry logging with metadata

### Phase 4: AI Enhancement (Main Directory)
- **Integration**: LLM-powered script generation and improvement
- **Generalization**: Framework for multiple platforms
- **Production**: Robust, scalable, and maintainable system

---

## Key Technical Insights

### Browser Choice Evolution
- **Firefox**: Chosen for stability and consistent "Stats for Nerds" behavior
- **Chrome Alternative**: Investigated but rejected due to DOM inconsistencies
- **Headless Mode**: Avoided to maintain full JavaScript execution context

### Telemetry Access Strategies
1. **Context Menu Approach**: Right-click → "Stats for Nerds" (most reliable)
2. **Keyboard Shortcuts**: Considered but platform-dependent
3. **DevTools Protocol**: Future enhancement for direct access

### Randomization Strategies
- **Search Terms**: 200+ nouns across 10+ languages for content diversity
- **Watch Time**: Uniform random distribution (0, video_duration)
- **Interaction Timing**: Realistic delays between actions

### Data Structure Design
```json
{
  "video_url": "https://youtube.com/watch?v=...",
  "query": "search_term_used",
  "duration": 180.5,
  "watched": 45.2,
  "stats": ["telemetry_snapshot_1", "telemetry_snapshot_2", ...]
}
```

---

## Lessons Learned

### ✅ What Worked
- **Playwright Reliability**: More stable than PyAutoGUI for web automation
- **Multi-language Content**: Effective strategy for dataset diversity
- **Stats Panel Access**: Context menu approach most reliable across updates
- **JSON Structured Output**: Facilitates downstream analysis

### ⚠️ Challenges Encountered
- **Element Selector Brittleness**: YouTube's frequent DOM changes
- **Timing Dependencies**: Network conditions affecting page load states
- **Content Availability**: Some search terms yield no results
- **Platform Variations**: macOS vs. Linux browser behavior differences

### 🔄 Iterative Improvements
1. **Error Recovery**: Added fallbacks for missing elements
2. **State Verification**: Wait conditions for reliable element interaction
3. **Resource Management**: Proper browser cleanup and memory management
4. **Logging Enhancement**: Progress indicators and debug information

---

## File Dependencies

### External Libraries
```python
playwright>=1.40.0    # Web automation framework
google-generativeai   # AI script enhancement (main directory)
pyautogui            # Legacy coordinate-based automation
pillow               # Screenshot processing
```

### Shared Resources
- **Multi-language noun list**: Common across `youtube.py` and `workflow.py`
- **Telemetry patterns**: Consistent stats panel interaction methods
- **Error handling**: Similar timeout and retry strategies

---

## Usage Instructions

### Running Individual Prototypes

```bash
# Single video collection
python prototype/youtube.py

# Multi-video batch collection
python prototype/workflow.py
# (Follow prompt for number of videos)

# Coordinate debugging tool
python prototype/add_grid_to_screenshot.py

# Raw Playwright recording
python prototype/gen-youtube.py
```

### Integrating with Main System

The patterns and lessons from these prototypes are incorporated into the main `workflow_generator.py` system. Use these scripts as:

1. **Reference implementations** for understanding core workflows
2. **Testing grounds** for new automation strategies
3. **Baseline comparisons** for AI-enhanced scripts
4. **Educational examples** for Playwright automation techniques

---

## Future Development

These prototypes serve as the foundation for:
- **Multi-platform support** (Netflix, Prime Video, etc.)
- **Advanced telemetry collection** (network packet capture)
- **Machine learning integration** (anomaly detection, content classification)
- **Distributed deployment** (netUnicorn pipeline integration)

The evolutionary approach demonstrated here provides a robust methodology for extending automation to new platforms and use cases.
