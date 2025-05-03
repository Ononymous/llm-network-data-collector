# Autonomous Agent-Based Network Data Collection

**Team Members**: Tim Qin, Adyah Rastogi, Wesley Truong, Gen Tamada

---

## Project Overview

We are building an **autonomous agent-based framework** using RAG/LLMs and **PyAutoGUI** to automate data-collection workflows for various web-based applications. This system minimizes human involvement by enabling intelligent agents to dynamically interact with applications (like YouTube) to extract telemetry and network data without hardcoding steps or scripts.

---

## Motivation

- **Problem**: Networking ML models often suffer from poor generalizability due to outdated, static, or unrealistic datasets (e.g., CIC-IDS-2017).
- **Goal**: Enable real-world, flexible, and extensible data collection via autonomous agents, reducing manual scripting and making the process adaptive to new applications or environments.

---

## Updated Proof-of-Concept Roadmap

### Phase 1: YouTube Workflow Prototype

- Use PyAutoGUI + LLM agent to:
  - Start a YouTube session
  - Collect telemetry via "Stats-for-Nerds" using GUI scraping or Chrome DevTools protocol
  - Collect packet traces locally (e.g., via `tcpdump`)
- **Contact**: [@lkoduru@ucsb.edu](mailto:lkoduru@ucsb.edu) to identify unique YouTube workflows for automation

### Phase 2: Integration with netUnicorn

- Wrap the YouTube workflow as a netUnicorn **pipeline**:
  - Define self-contained tasks (e.g., launch browser, collect pcap, log telemetry)
  - Use `netUnicorn.Nodes` and `Pipeline` abstractions
- **Contact**: [@rbeltiukov@ucsb.edu](mailto:rbeltiukov@ucsb.edu) for assistance with netUnicorn integration and deployment

### Phase 3: Demonstrate Generalizability

- Extend the system to support other applications:
  - Amazon Prime
  - Netflix
  - Zoom (e.g., automated meeting, screen recording, telemetry scraping)
- Show that new workflows can be added with **minimal new code**, leveraging existing abstractions

---

## Key Technologies

- **PyAutoGUI**: GUI automation
- **RAG/LLM**: Smart decision making for UI interaction
- **tcpdump/Wireshark**: Packet trace capture
- **netUnicorn**: Deployment framework to modularize and scale data collection experiments

---

## Evaluation Metrics

- Successful autonomous collection of:
  - Application-specific telemetry (e.g., bitrate, resolution, buffering events)
  - Network packet traces
- Quality of datasets in downstream ML model performance:
  - Reduction in shortcut learning
  - Resistance to out-of-distribution (OOD) drift
  - Avoidance of spurious correlations

---

## References

- [netUnicorn Paper (ACM '23)](https://netunicorn.cs.ucsb.edu)
- CIC-IDS-2017 Dataset
- UNSW-NB15 Dataset
