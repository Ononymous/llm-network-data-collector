# Agent-Based Data Collection Tool Using RAG/LLMs and PyAutoGUI

**Team Members:** Tim Qin, Adyah Rastogi, Wesley Truong, Gen Tamada

---

## Proposal
We propose developing an agent-based tool that leverages Retrieval-Augmented Generation (RAG) / Large Language Models (LLMs) combined with PyAutoGUI to automate data-collection workflows for various web-based applications. 

For example, this tool could:
- Start and stop a YouTube session
- Collect telemetry data using the "Stats-for-Nerds" tool
- Store session-specific data 

All without requiring manual programming or intervention.

---

## Motivation and Problem
There is a lack of robust, automated data collection methods for networking research. Current datasets, such as **CIC-IDS-2017**, are outdated and often lead to poorly trained models due to issues like shortcut learning.

Our goal is to leverage LLMs to:
- Dynamically determine which websites to visit
- Decide where to click
- Automate the steps necessary for accurate data collection 

All **without explicit human-defined instructions**.

---

## Existing Approaches
- **Manual Data Collection:**  
  Traditionally done in controlled environments, following rigid, predefined rules. Even partial automation still requires custom scripting for every new task.
  
- **Limitations:**  
  - Not reflective of real-world, dynamic network usage.
  - Time-consuming and inflexible.
  
- **Reinforcement Learning (RL):**  
  While RL could offer smarter automation, it suffers from:
  - Extensive reward engineering requirements.
  - Difficulty in avoiding biased or non-representative data.
  
---

## Existing Datasets
- **CIC-IDS-2017:**  
  Includes various attack types (Brute Force, Heartbleed, Botnet, DoS, DDoS, etc.).  
  Known for causing shortcut learning issues in ML models.

- **UNSW-NB15:**  
  A hybrid dataset combining real modern activities with synthetic attacks.  
  Better than older datasets, but still limited in adaptability and realism.

---

## Novelty and Implementation
Our approach introduces:
- A **fully autonomous data collection system** powered by LLMs and PyAutoGUI.
- The LLM will:
  - Make decisions throughout the data collection pipeline.
  - Generate new pipelines autonomously without human guidance.
  
This removes the need for manual programming when adapting to new data collection scenarios.

---

## Metrics and Evaluation
- **Success Criteria:**
  - Collection of high-quality, unbiased data suitable for networking research.
  - Data should minimize:
    - Shortcut learning
    - Out-of-distribution (OOD) sampling issues
    - Spurious correlations

- **Evaluation Method:**
  - Train a simple ML model using the collected data.
  - Validate the model's performance to assess data quality and generalizability.

---

