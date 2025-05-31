# Autonomous Agent-Based Network Data Collection

**Team Members**: Tim Qin, Adyah Rastogi, Wesley Truong, Gen Tamada

---

## Project Overview

We are building an **autonomous agent-based framework** using RAG/LLMs and **Playwright** to automate data-collection workflows for various web-based applications. This system minimizes human involvement by enabling intelligent agents to dynamically interact with applications (like YouTube) to extract telemetry and network data without hardcoding steps or scripts.

The project includes a sophisticated **AI-powered workflow generator** that creates, tests, and iteratively improves Playwright automation scripts using Google's Gemini LLM.

---

## Repository Structure

```
├── workflow_generator.py       # Main AI-powered workflow generator
├── prototype/                # Early prototypes and experiments
│   ├── workflow.py           # Multi-video YouTube data collection
│   ├── youtube.py            # Single video YouTube automation
│   ├── gen-youtube.py        # Basic Playwright generated script
│   ├── add_grid_to_screenshot.py # PyAutoGUI helper tool
│   └── telemetry.json        # Sample collected data
└── 293n/                     # Python virtual environment
```

---

## Current Features

### AI-Powered Workflow Generator
- **Interactive Setup**: Prompts for URLs and test specifications
- **Automated Test Generation**: Uses Playwright's codegen for initial recordings
- **AI Enhancement**: Leverages Gemini LLM to add robustness, error handling, and randomization
- **Iterative Improvement**: Continuous refinement based on test results and feedback

### YouTube Data Collection
- **Multi-language Search**: Uses diverse search terms in 10+ languages
- **Telemetry Extraction**: Collects "Stats for Nerds" data including bitrate, resolution, buffering
- **Random Sampling**: Watches random portions of videos for realistic usage patterns
- **JSON Export**: Structured data output for analysis

### Development Tools
- **Grid Screenshot**: PyAutoGUI helper for coordinate identification
- **Multiple Approaches**: Various automation strategies (Playwright, PyAutoGUI)

---

## Quick Start

### Prerequisites
1. **Python 3.8+** with virtual environment
2. **Playwright** with browser support:
   ```bash
   pip3 install playwright
   playwright install
   ```
3. **Google Generative AI** package:
   ```bash
   pip3 install google-generativeai
   ```
4. **Gemini API Key** from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation
```bash
# Clone and setup
git clone git@github.com:Ononymous/llm-network-data-collector.git
cd llm-network-data-collector

# Install dependencies
pip3 install -r requirements.txt
```

### Usage

#### AI Workflow Generator
```bash
python3 workflow_generator.py
```
Follow the interactive prompts to:
1. Specify target URL or existing script
2. Generate/record initial Playwright test
3. Apply AI enhancements with custom guidelines
4. Execute and refine the generated workflow

#### Direct YouTube Automation
```bash
# Single video collection
python3 youtube1.py

# Multi-video collection with telemetry
python3 prototype/workflow.py
```

---

## Motivation

- **Problem**: Networking ML models often suffer from poor generalizability due to outdated, static, or unrealistic datasets (e.g., CIC-IDS-2017).
- **Goal**: Enable real-world, flexible, and extensible data collection via autonomous agents, reducing manual scripting and making the process adaptive to new applications or environments.

---

## Roadmap

### Phase 1: YouTube Workflow Prototype (Current)
- Playwright-based automation for YouTube
- AI-powered script generation and enhancement
- Telemetry collection via "Stats-for-Nerds"
- Multi-language content diversity

### Phase 2: Integration with netUnicorn (In Progress)
- Wrap workflows as netUnicorn **pipelines**
- Define self-contained tasks (browser launch, data collection, packet capture)
- Use `netUnicorn.Nodes` and `Pipeline` abstractions

### Phase 3: Generalization (Planned)
- Extend to other streaming platforms:
  - Amazon Prime Video
  - Netflix
  - Twitch
- Add video conferencing platforms:
  - Zoom automated meetings
  - Microsoft Teams data collection
- Demonstrate **minimal new code** requirement for new platforms

---

## Key Technologies

- **Playwright**: Modern web automation framework
- **Google Gemini LLM**: AI-powered script generation and enhancement
- **PyAutoGUI**: GUI automation for fallback scenarios
- **tcpdump/Wireshark**: Packet trace capture (planned)
- **netUnicorn**: Deployment framework for scalable experiments

---

## Data Collection Capabilities

### YouTube Telemetry
- **Video Metadata**: Title, duration, URL
- **Playback Stats**: Current resolution, bitrate, codec
- **Network Performance**: Connection speed, dropped frames
- **Buffer Health**: Buffer size, rebuffering events
- **Viewport Info**: Video dimensions, framerate

### Sampling Strategy
- **Random Search Terms**: 200+ terms across 10+ languages
- **Randomized Watch Time**: Realistic viewing patterns
- **Diverse Content**: Multiple video types and lengths

---

## Evaluation Metrics

### Technical Success
- Successful autonomous collection of:
  - Application-specific telemetry (bitrate, resolution, buffering events)
  - Network packet traces
  - Cross-platform compatibility

### Data Quality
- **Diversity**: Multi-language, multi-genre content sampling
- **Realism**: Human-like interaction patterns
- **Completeness**: Full telemetry capture with minimal data loss

### ML Model Performance
- Reduction in shortcut learning
- Resistance to out-of-distribution (OOD) drift
- Avoidance of spurious correlations in downstream models

---

## Contributing

See the `prototype/` directory for experimental scripts and early development attempts. Each script represents different approaches to automation and data collection.

---

## References

- [netUnicorn Paper (ACM '23)](https://sites.cs.ucsb.edu/~arpitgupta/pdfs/netUnicorn.pdf)
- [Playwright Documentation](https://playwright.dev/)
- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)