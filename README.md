# Autonomous Web Telemetry Collection Pipeline

**Team Members**: Tim Qin, Adyah Rastogi, Wesley Truong, Gen Tamada

This repository contains an agent‐based framework for automating frontend interactions and light telemetry collection from web applications—primarily demonstrated on YouTube. It evolved from early experiments with PyAutoGUI to a robust Playwright‐based workflow generator powered by Google’s Gemini API. The end goal is to support minimal‐human‐intervention data collection, with future plans to integrate packet‐capture tools like netUnicorn or Wireshark.

---

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Directory Structure](#directory-structure)  
5. [Usage](#usage)  
   - [PyAutoGUI Experiments](#pyautogui-experiments)  
   - [Playwright Examples](#playwright-examples)  
   - [Automated Workflow Generator](#automated-workflow-generator)  
6. [Sample Output](#sample-output)  
7. [Future Work](#future-work)  

---

## Project Overview

Early in this project, we experimented with [PyAutoGUI](https://github.com/asweigart/pyautogui) to script mouse clicks and keystrokes on a static screenshot grid. While PyAutoGUI is extremely simple to install and use, we found that:

- **Absolute coordinates** are brittle—every UI change (e.g., different browser window size or a slightly altered YouTube layout) required re‐generating a fresh high‐resolution screenshot.  
- **LLM assistance** (prompting with screenshots) was too inefficient and often failed to click the correct pixel when elements moved or the UI changed.  

Consequently, we pivoted to interacting with **raw HTML via a browser‐automation library**. We briefly considered Selenium, but encountered unpredictable race conditions (e.g., overlays, pop-up dialogs) and unreliable element locators. That led us to adopt **[Playwright](https://playwright.dev/)**—a modern, Microsoft-supported browser‐automation framework that:

- Launches Chromium, Firefox, or WebKit in headless/headful mode.  
- Locates elements by CSS selectors, `role` attributes, or text content.  
- Executes JavaScript and retrieves DOM information programmatically.  

On top of Playwright, we built:

1. **Playwright scripts** (`youtube1.py`, `youtube1_gen.py`) that navigate to YouTube, search for random videos (using “Stats for Nerds”), collect light telemetry (buffer health, resolution, network speed), and simulate random user actions (pause, skip, fast-forward).  
2. A **Workflow Generator** (`workflow_generator.py`) that uses Google’s Gemini API (via `google-generativeai`) to generate custom Playwright test code based on user‐provided prompts (e.g., “Navigate to this URL, click on X, collect Y”).  

The main focus today is on frontend‐interaction automation; future phases will integrate third-party data collection (e.g., netUnicorn pipelines for packet capture or Wireshark).

---

## Prerequisites

1. **Python 3.8+**  
2. **Node.js ≥ 14** (for Playwright’s `playwright install` step)  
3. **Google Gemini API Key** (for any functionality in `workflow_generator.py`)  
4. **Internet access** (to install dependencies and to run Playwright against live web pages)  

---

## Installation

1. **Clone the repository**  

    ```bash
    git clone git@github.com:Ononymous/llm-network-data-collector.git
    cd llm-network-data-collector
    ```

2. **Create and activate a virtual environment** (recommended)

    ```bash
    python3 -m venv venv
    source venv/bin/activate      # macOS/Linux
    venv\Scripts\activate.bat     # Windows
    ```

3. **Install Python dependencies**

    ```bash
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    ```

   The main dependencies are:

   * `playwright >= 1.40.0`
   * `google-generativeai >= 0.8.0`

4. **Install Playwright browsers**
   After installing the `playwright` Python package, you must install browser binaries:

   ```bash
   playwright install
   ```

   This will download Chromium, Firefox, and WebKit drivers so that Playwright can launch browsers programmatically.

---

## Directory Structure

```
├── README.md
├── requirements.txt           # Python dependencies
├── guidelines.txt             # Example guideline for collecting stats from random YouTube videos
├── feedback.txt               # Contains notes like “skip ads if any” for regenerating scripts
├── workflow_generator.py      # Gemini‐powered Playwright workflow generator
├── youtube1.py                # Hand‐recorded Playwright script (YouTube search + video navigation)
├── youtube1_gen.py            # Auto‐generated Playwright script from guidelines and feedback
└── youtube_telemetry.json     # Sample telemetry output from youtube1_gen.py
```
---

## Usage

### Automated Workflow Generator (`workflow_generator.py`)

This script leverages a language model (Gemini) to produce new Playwright test scripts based on user instructions. The high‐level flow:

1. **Check Playwright**
   The script verifies whether the `playwright` CLI is installed (`playwright --version`). If not found, it prints installation instructions and exits.

2. **Prompt for Inputs**

   * **Target URL** (e.g., `https://www.youtube.com/watch?v=<ID>`).
   * **Actions to perform** (e.g., “Right‐click, open Stats for Nerds, collect 10 samples of buffer health every second, then exit after a 5 second watch”).
   * **Output filename** (e.g., `my_youtube_test.py`).

3. **Generate Code via Gemini**
   Uses `google-generativeai` to send a prompt to the `gemini-2.5-flash-preview-05-20` model. The prompt is carefully structured to ask for a complete Playwright test in Python (including imports, browser launch, element locators, loops for stats collection, and JSON output).

4. **Write & Save**
   Receives the generated Python code from Gemini and writes it to disk under the provided filename.

5. **User Executes Generated Script**
   After generation, run:

   ```bash
   python3 <output_filename>.py
   ```

   Playwright will launch, perform the specified actions, collect telemetry, and save JSON.

#### How to Run

```bash
python3 workflow_generator.py
```

* Follow on‐screen prompts.
* Ensure your environment variable `GEMINI_API_KEY` (or the hardcoded `GEMINI_API_KEY` inside the script) is valid.
* After generation, run the newly created Python file with:

  ```bash
  python3 generated_script.py
  ```

---

### Playwright Examples

#### 1. `youtube1.py` (Manual Playwright Script)

This is a short example that:

1. Launches Firefox in a visible (`headful`) window.
2. Navigates to `https://www.youtube.com/`.
3. Searches for “timeless.”
4. Opens the first result and presses the Right‐Arrow keys several times to skip ads or advance playback.
5. Closes the browser.

To run:

```bash
python3 youtube1.py
```

* **Modify** the search term or add direct telemetry‐collection lines inside `run(...)`.
* You can change `playwright.firefox.launch(headless=False)` to `playwright.chromium.launch(headless=True)` for headless mode.

#### 2. `youtube1_gen.py` (Auto‐Generated Telemetry Collector)

This script has two main phases:

1. **Search Phase**:

   * Randomly choose a noun from a large multilingual list (English, Spanish, French, Chinese, Japanese, Hindi, Korean, Russian, Arabic, German, Portuguese, Italian).
   * Navigate to `https://www.youtube.com/results?search_query=<noun>`.
   * Click the first video result (if any).

2. **Telemetry + Interaction Phase**:

   * Right‐click on the video player → click “Stats for Nerds.”
   * Determine the full video duration via JavaScript (`document.querySelector('video').duration`).
   * Pick a random short watch time (e.g., 3–10 seconds), then collect \~10 stats samples at \~1 sec intervals.
   * Between collection loops, simulate random user actions (pause, fast‐forward, seek) to mimic realistic behavior.
   * Append `{ "video_url": …, "query": …, "duration": …, "watched": …, "stats_collections": […] }` to a Python list.

At the end, it:

* Prints the JSON to the console.
* Writes it to `telemetry.json` in the current directory.

To run:

```bash
python3 youtube1_gen.py
```

1. When prompted, enter the number of random videos to process (e.g., `5`).
2. The script will open a Firefox window (changeable to Chromium or WebKit by modifying `browser_type="firefox"`).
3. After completion, inspect `telemetry.json` for collected stats.

> **Tip**: If you want headless mode, set `headless=True` in the constructor:
>
> ```python
> test_runner = YouTubeVideoPlayerTest(headless=True, browser_type="chromium")
> ```

---


## Sample Output

A sample telemetry JSON (`youtube_telemetry.json`) is included for reference. It shows an array of telemetry objects, each containing:

* `video_url`: Full URL of the played video.
* `query`: The random noun used to search.
* `duration`: The full video duration in seconds.
* `watched`: How many seconds the test loop watched.
* `stats_collections`: A list of objects with:

  * `timestamp_watched` (relative playback time).
  * `stats` (multiline string from YouTube’s “Stats for Nerds” panel).

```jsonc
[
  {
    "video_url": "https://www.youtube.com/watch?v=RlT1jmMbNQQ",
    "query": "माता",
    "duration": 7205.0,
    "watched": 5.50,
    "stats_collections": [
      {
        "timestamp_watched": 1.03,
        "stats": "[X]\nVideo ID / sCPN RlT1jmMbNQQ / ZYVV GAZZ F13X N2B0 QBY0\nViewport / Frames 791×445*2.00 / –\n…"
      },
      {
        "timestamp_watched": 2.07,
        "stats": "[X]\nVideo ID / sCPN RlT1jmMbNQQ / ZYVV GAZZ F13X N2B0 QBY0\nViewport / Frames 791×445*2.00 / –\n…"
      },
      … (10 total samples)
    ]
  },
  … (one object per video)
]
```

---

## Future Work

1. **netUnicorn / Wireshark Integration**
   In Phase 2, wrap the Playwright telemetry steps in a netUnicorn pipeline:

   * Launch a browser node.
   * Start `tcpdump` on loopback or a specified interface.
   * Run the Playwright script concurrently.
   * Stop `tcpdump` and save a `.pcap`.
   * Associate telemetry JSON with packet trace files for downstream ML training.

2. **Extended Application Support**

   * Amazon Prime, Netflix: Navigate login flows, enable “Stats for Nerds” equivalents (if available).
   * Zoom: Automate meeting creation, join/leave, screen capture via an embedded Electron UI or PyAutoGUI fallback.

3. **Robust LLM Guidance**
   Improve `workflow_generator.py` to handle:

   * Dynamic error handling (e.g., pop-ups, age‐gates).
   * Conditional retries when elements are not found.
   * Modular code generation (e.g., separate “search → play → collect → exit” into functions).

4. **Data Quality & Evaluation**

   * Automate “out-of-distribution” drift detection by comparing network stats to known baselines.
   * Build a dashboard for visualizing buffer health distributions across random queries.

---

**Enjoy the repository! Feel free to modify the Playwright selectors, add new telemetry fields, or swap in headless execution for fully automated CI/CD tests.**