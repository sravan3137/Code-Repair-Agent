# Code-Repair-Agent 🤖☕

An autonomous, agentic system designed to iteratively analyze, repair, and validate Java repositories. This agent uses a **ReAct** (Reasoning + Acting) loop to localize failures, traverse dependency graphs, and apply surgical code patches.

## 🚀 Overview

The Java-Repair-Agent is built to handle the complexities of multi-file Java projects where a single bug might have ripple effects across the codebase. Unlike standard LLM code editors, this agent:
- **Builds a Symbol Graph**: Understands the repository as a network of functions and dependencies, not just a folder of files.
- **Surgical Patching**: Uses `apply_symbol_patch` to modify specific methods without corrupting the surrounding class structure.
- **Propagation Awareness**: Detects when a signature change in one file requires updates in its callers across the repository.

## 🛠 Features

- **Autonomous Debugging Loop**: Iterates through `Localize -> Retrieve -> Patch -> Update Graph -> Validate`.
- **Dependency Traversal**: Tools to perform incoming/outgoing call graph analysis.
- **Multi-Model Support**: Confirmed compatibility with:
  - **Cloud**: Groq (Llama 3 70B) for high-reasoning tasks.
  - **Local**: Ollama (Qwen 2.5 Coder 7B) for privacy and local execution.
- **Robust Tooling**: Includes AST-based symbol extraction, cross-file failure localization, and automated validation (compilation checks).

## 📂 Project Structure

- `agent/`: Core agent logic, memory management, and system prompts.
- `tools/`: Deterministic Python tools for repository manipulation (AST parsing, graph building, patching).
- `utils/`: Logging, security scanning, and shared utilities.
- `repositories/`: Target Java repositories for the agent to repair.
- `main.py`: Entry point for launching the repair cycle.

## 🚦 Getting Started

### Prerequisites
- Python 3.10+
- Java (JDK) installed and in your PATH (for `javac` validation)
- Ollama (optional, for local model support)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sravan3137/Code-Repair-Agent.git
   cd Code-Repair-Agent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your environment:
   Create a `.env` file with your API keys (if using Groq/OpenAI).

### Running a Repair Task
Configure the `REPO_PATH` in `main.py` and run:
```bash
python main.py
```

## 🧠 Model Insights

This project has been tested with varying model scales:
- **7B Models (e.g., Qwen 2.5 Coder)**: Effective for syntax fixes and single-file repairs. May require "Loop Detection" or prompted "Chain of Thought" for complex multi-file logic.
- **70B Models (e.g., Llama 3)**: Highly capable of cross-file dependency reasoning and global state awareness.

## 🛡 Security
The agent includes a `security.py` layer that scans proposed code changes for common vulnerabilities and token-based risks before applying patches.

---
*Created by [sravan3137](https://github.com/sravan3137)*
