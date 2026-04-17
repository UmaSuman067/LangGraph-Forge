from dotenv import load_dotenv
from langchain_core.globals import set_verbose, set_debug
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.constants import END
from langgraph.graph import StateGraph
import json
import re

from prompts import *
from states import *
from tools import write_file, read_file, get_current_directory, list_files, init_project_root
from visualize import save_graph_visualization

# Load environment variables
_ = load_dotenv()

# Debugging settings
set_debug(True)
set_verbose(True)

# Using a more stable model for tool calling and structured output
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_retries=3)

# Initialize the generated_project directory
init_project_root()

def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan."""
    user_prompt = state["user_prompt"]
    
    # Explicit system instruction to prevent JSON schema nesting errors
    system_msg = SystemMessage(content="You are a project planner. Return ONLY the direct values for the schema. Do not wrap values in {'type':..., 'value':...} objects.")
    
    resp = llm.with_structured_output(Plan).invoke([
        system_msg,
        HumanMessage(content=planner_prompt(user_prompt))
    ])
    
    if resp is None:
        raise ValueError("Planner did not return a valid response.")
    
    print("[planner] completed")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan: Plan = state["plan"]
    
    system_msg = SystemMessage(content="You are a software architect. Create a detailed implementation plan. Do not use nested type/value structures in your JSON.")
    
    resp = llm.with_structured_output(TaskPlan).invoke([
        system_msg,
        HumanMessage(content=architect_prompt(plan=plan.model_dump_json()))
    ])
    
    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan
    print("[architect] completed")
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    existing_content = read_file.run(current_task.filepath)

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n\n"
        "IMPORTANT: Use write_file(path, content) to save your implementation."
    )

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    llm_with_tools = llm.bind_tools(coder_tools)

    tool_map = {t.name: t for t in coder_tools}
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm_with_tools.invoke(messages)

    # Execute tool calls
    max_iterations = 5
    iteration = 0
    while getattr(response, "tool_calls", None) and iteration < max_iterations:
        iteration += 1
        tool_results = []
        for call in response.tool_calls:
            tool = tool_map.get(call["name"])
            if tool is None:
                result = f"ERROR: Tool '{call['name']}' does not exist."
                continue
            else:
                try:
                    result = tool.invoke(call["args"])
                    print(f"[coder] executed {call['name']} -> success")
                except Exception as exc:
                    result = f"ERROR: {exc}"
            
            tool_results.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

        if not tool_results:
            break
            
        messages = messages + [response] + tool_results
        response = llm_with_tools.invoke(messages)

    coder_state.current_step_idx += 1
    print(f"[coder] completed step {coder_state.current_step_idx}/{len(steps)}")
    return {"coder_state": coder_state}


# Build the Graph
graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")
agent = graph.compile()

# Save graph visualization for documentation
save_graph_visualization(agent)

if __name__ == "__main__":
    description = input("Enter your project description: ")
    result = agent.invoke(
        {"user_prompt": description},
        {"recursion_limit": 50}
    )
    print("\n--- Execution Finished ---")
    print("Final Status:", result.get("status", "COMPLETED"))
    print("Your app files have been generated in the project root.")