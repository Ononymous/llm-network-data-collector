Tim Qin, Adyah Rastogi, Wesley Truong, Gen Tamada
Proposal
We can develop an agent-based tool that employs RAG/LLMs combined with PyAutoGUI to automate data-collection workflows for different web-based applications. For example, this tool could start and stop a YouTube session, collect telemetry data using the Stats-for-Nerds tool, and store session-specific data without requiring any manual programming or intervention.
Motivation and Problem
The motivation for this project is that there are not many good automatic data collection methods for networking, and the current big datasets CIC-IDS-2017 for networking are not up to standard and result in incorrectly trained models. Ideally, the LLM can help us create new methods of data collection without explicitly told which website to visit, where to click, and what steps needs to be taken to correctly collect the data.
Existing Approaches
Data used to be collected manually, in a controlled lab environment, following rigid and static rules and steps. Even if some parts of the collection are automated, researchers still need to write new pipelines and steps for those automated scripts to collect something new. Manual data collection in these rigid environments also does not represent actual network usage from typical and malicious users, so these methods may be outdated.
Reinforcement learning could be used for a smarter and more natural automation to happen, but it requires extensive reward engineering for it to make the correct decisions. However, it is still difficult for the models to understand and avoid data that can be biased, or inaccurate to real-world scenarios.
Existing Datasets
CIC-IDS-2017: Created by the Canadian Institute for Cybersecurity for development and evaluation of intrusion detection systems (IDS). Includes many types of attacks: Brute Force, Heartbleed, Botnet, DoS, DDoS, Web Attack and Infiltration. However, there are known issues with training ML models on this dataset, especially with shortcut learning.
UNSW-NB15: Created by UNSW Sydney with the primary goal of creating a dataset with a hybrid of real modern normal activities and synthetic contemporary attack behaviours.
Novelty and Implementation
The novelty is that we are creating a new way of collecting with the use of LLMs and PyAutoGUI to create a program that can collect network data without any manual programming or human participation. Ideally, the LLM should be making decisions about the whole data collection pipeline, and or create new pipelines on its own without human input.
Metric and Evaluation
Successful collection of data that can be used for research, unbiased, and ideally lets models that use those data to avoid shortcut learning, out-of-distribution sampling, and spurious correlation.
We can train a simple model that uses those collected data and validate it to see its performance.
