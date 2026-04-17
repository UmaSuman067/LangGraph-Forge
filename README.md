# LangGraph-Forge
A multi-agent, LangGraph-driven AI system that transforms plain-language ideas into fully functional web applications, automating the entire project generation process from concept to code.

## System Architecture
The system operates on a state-based multi-agent workflow, ensuring a structured transition from a simple idea to a deployable project.

* **Planning Agent:** Analyzes requirements and defines the tech stack, features, and roadmap.
* **Architect Agent:** Decomposes the high-level plan into granular, executable implementation tasks.
* **Coding Agent:** Leverages specialized tools to execute tasks and generate the physical file structure.

## Quick Start
### Prerequisites
* Python 3.11+
* **uv** package manager (for faster dependency resolution)
* Google Gemini / Groq API Key

# Create and activate virtual environment
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
uv pip install -e .

# Setup environment
cp .sample_env .env
# Add your GEMINI_API_KEY or GROQ_API_KEY to .env

# Running the App
python agent/graph.py

## Project Structure
agent/
│── graph.py        # LangGraph workflow
│── prompts.py      # Agent instructions
│── states.py       # State models (Pydantic)
│── tools.py        # File operations
│── visualize.py    # Graph visualization

main.py             # Entry point
pyproject.toml      # Dependencies

Configuration & Model Support
The system is optimized for structured output and tool calling.

## Python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0.2
)

## Tested Models:
gemini-2.0-flash-exp: Best performance/latency balance.
gemini-1.5-pro: Recommended for complex multi-file architectures.
Groq (llama-3-70b): Ultra-fast inference for simple logic.

## Example Outputs
Calculator App
Login Page
Portfolio Website

## Troubleshooting
Issue: Tool choice is required error.
Solution: The selected model doesn't support the current tool schema. Upgrade to a model with native tool-calling support.
Issue: API Quota Exceeded.
Solution: Implement exponential backoff or switch to a higher-tier API key.
Issue: Generated project files are missing.
Solution: Check the generated_project/ root for logs; ensure the agent has write permissions.

