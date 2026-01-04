"""
Planning functionality for the agent.

Planning is data generation, not reasoning.
Plans are inspectable, modifiable data structures.
"""

from shared.llm import LocalLLM
from shared.utils import safe_json_parse


def create_plan(llm: LocalLLM, goal: str) -> dict | None:
    """
    Generate a plan to achieve a goal.
    
    Used in: Lesson 08
    
    Args:
        llm: The language model to use
        goal: The goal to achieve
        
    Returns:
        Plan as a dictionary with a "steps" list, or None if generation failed
    """
    from shared.utils import extract_json_from_text
    
    prompt = f"""Create a step-by-step plan to achieve the goal. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"steps": ["step1", "step2", "step3"]}}

Goal: {goal}

Response (JSON only):"""
    
    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        plan = extract_json_from_text(response)
        
        if plan and "steps" in plan and isinstance(plan["steps"], list):
            return plan
    
    return None


def create_atomic_action(llm: LocalLLM, step: str) -> dict | None:
    """
    Convert a plan step into an atomic action.
    
    Used in: Lesson 09
    
    Args:
        llm: The language model to use
        step: A step from a plan
        
    Returns:
        Atomic action as a dictionary, or None if generation failed
    """
    from shared.utils import extract_json_from_text
    
    prompt = f"""Convert this step into an atomic action. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{
  "action": "action_name",
  "inputs": {{"key": "value"}}
}}

The action should be a simple, atomic operation name.
The inputs should be a dictionary with the parameters needed for this action.

Step to convert:
{step}

Response (JSON only):"""
    
    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        action = extract_json_from_text(response)
        
        if action and "action" in action:
            return action
    
    return None


def create_aot_graph(llm: LocalLLM, goal: str) -> dict | None:
    """
    Generate an Atom of Thought (AoT) execution graph.
    
    Used in: Lesson 10
    
    Args:
        llm: The language model to use
        goal: The goal to achieve
        
    Returns:
        AoT graph with nodes and dependencies, or None if generation failed
    """
    from shared.utils import extract_json_from_text
    
    prompt = f"""Create an atomic execution graph for the goal. Each node is a single action. Dependencies are node IDs. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"nodes": [{{"id": "1", "action": "research", "depends_on": []}}, {{"id": "2", "action": "write", "depends_on": ["1"]}}]}}

Each node must have:
- id: unique string like "1", "2", "3"
- action: what to do (e.g., "research", "write", "review")
- depends_on: list of node IDs that must complete first (empty [] for first step)

Goal: {goal}

Response (JSON only):"""
    
    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        graph = extract_json_from_text(response)
        
        if graph and "nodes" in graph and isinstance(graph["nodes"], list):
            # Validate graph structure
            valid_nodes = []
            for node in graph["nodes"]:
                if isinstance(node, dict) and "id" in node and "action" in node and "depends_on" in node:
                    # Ensure depends_on is a list
                    if not isinstance(node["depends_on"], list):
                        continue
                    valid_nodes.append(node)
            
            if valid_nodes:
                return {"nodes": valid_nodes}
    
    return None


def execute_graph(graph: dict, executor_func) -> list:
    """
    Execute an AoT graph respecting dependencies.
    
    Args:
        graph: AoT graph with nodes and dependencies
        executor_func: Function to execute each action (takes action string)
        
    Returns:
        List of execution results in order
    """
    if not graph or "nodes" not in graph:
        return []
    
    nodes = graph["nodes"]
    executed = set()
    results = []
    
    # Simple topological execution
    # In a real implementation, this would be more sophisticated
    max_iterations = len(nodes) * 2
    iteration = 0
    
    while len(executed) < len(nodes) and iteration < max_iterations:
        iteration += 1
        
        for node in nodes:
            node_id = node["id"]
            
            # Skip if already executed
            if node_id in executed:
                continue
            
            # Check if all dependencies are met
            dependencies = node.get("depends_on", [])
            if all(dep in executed for dep in dependencies):
                # Execute the node
                try:
                    result = executor_func(node["action"])
                    results.append({
                        "node_id": node_id,
                        "action": node["action"],
                        "result": result,
                        "success": True
                    })
                    executed.add(node_id)
                except Exception as e:
                    results.append({
                        "node_id": node_id,
                        "action": node["action"],
                        "error": str(e),
                        "success": False
                    })
                    # Mark as executed even on failure to avoid infinite loops
                    executed.add(node_id)
    
    return results
