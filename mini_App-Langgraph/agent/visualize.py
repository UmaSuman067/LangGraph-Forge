import os
from pathlib import Path


def save_graph_visualization(graph, output_filename="agent_graph.png"):
    """
    Save the LangGraph visualization to the resources directory.
    
    Args:
        graph: The compiled LangGraph instance
        output_filename: Name of the output image file (default: agent_graph.png)
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    resources_dir = project_root / "resources"
    
    # Create resources directory if it doesn't exist
    resources_dir.mkdir(exist_ok=True)
    
    # Full path for the output image
    output_path = resources_dir / output_filename
    
    try:
        # Generate and save the graph visualization
        graph_image = graph.get_graph().draw_mermaid_png()
        
        with open(output_path, "wb") as f:
            f.write(graph_image)
        
        print(f"[visualize] Graph saved to: {output_path}")
        return str(output_path)
    except Exception as e:
        print(f"[visualize] Failed to save graph: {e}")
        return None
