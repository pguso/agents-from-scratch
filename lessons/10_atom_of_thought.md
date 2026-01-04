# Lesson 10  -  AoT (Atom of Thought)  -  Now It Makes Sense

## What Question Are We Answering?

**"How do I scale planning without losing control?"**

Complex tasks need many actions with dependencies. Some actions can run in parallel, others must wait. AoT (Atom of Thought) creates dependency graphs that enable safe, efficient execution of complex workflows.

## What You Will Build

An AoT system that:
- Creates dependency graphs with nodes and dependencies
- Validates graph structure before execution
- Executes actions respecting dependencies
- Enables parallel execution of independent actions

## New Concepts Introduced

### 1. Atomic Planning

**Atomic planning** means creating plans as dependency graphs where each node is an atomic action. Nodes can depend on other nodes, creating an explicit execution order.

This is the natural combination of Lesson 08's planning and Lesson 09's atomic actions, with added dependency tracking.

### 2. Dependency Resolution

**Dependency resolution** determines the correct execution order. Actions with no dependencies can run immediately. Actions with dependencies wait for their dependencies to complete.

This enables parallel execution of independent actions while respecting ordering constraints.

### 3. Validated Execution

**Validated execution** means checking the graph structure before running it. Are all dependencies valid? Is there a circular dependency? Are all required nodes present?

Validation catches structural errors before execution begins.

## The Code

Look at `agent/planner.py`, see `create_aot_graph()` function:

```python
def create_aot_graph(llm: LocalLLM, goal: str) -> dict | None:
    """
    Generate an AoT execution graph.
    
    Used in: Lesson 10
    
    Args:
        llm: The language model to use
        goal: The goal to achieve
        
    Returns:
        AoT graph with nodes and dependencies, or None if generation failed
    """
    from shared.utils import extract_json_from_text
    
    prompt = f"""Create an execution graph to achieve the goal. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{
  "nodes": [
    {{"id": "1", "action": "action_name", "depends_on": []}},
    {{"id": "2", "action": "action_name", "depends_on": ["1"]}}
  ]
}}

Each node must have:
- "id": unique identifier (string)
- "action": what to do (string)
- "depends_on": list of node IDs that must complete first (list of strings)

Goal: {goal}

Response (JSON only):"""
    
    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        graph = extract_json_from_text(response)
        
        if graph and "nodes" in graph and isinstance(graph["nodes"], list):
            # Validate node structure
            node_ids = set()
            for node in graph["nodes"]:
                if "id" not in node or "action" not in node or "depends_on" not in node:
                    break
                node_ids.add(node["id"])
            else:
                # All nodes valid, check dependencies reference valid nodes
                for node in graph["nodes"]:
                    for dep in node.get("depends_on", []):
                        if dep not in node_ids:
                            break
                    else:
                        continue
                    break
                else:
                    return graph
    
    return None
```

And in `agent/agent.py`:

```python
def create_aot_plan(self, goal: str) -> dict | None:
    """
    Generate an AoT execution graph.
    
    Lesson 10 version.
    
    Args:
        goal: The goal to achieve
        
    Returns:
        AoT graph with atomic nodes and dependencies
    """
    return create_aot_graph(self.llm, goal)

def execute_aot_plan(self, graph: dict) -> list:
    """
    Execute an AoT graph respecting dependencies.
    
    Args:
        graph: AoT graph
        
    Returns:
        List of execution results
    """
    def execute_action(action: str):
        # Placeholder for actual action execution
        return f"Executed: {action}"
    
    return execute_graph(graph, execute_action)
```

Notice:
- **Graph structure** - Nodes with IDs, actions, and dependencies
- **Validation** - Checks that all dependencies reference valid nodes
- **Dependency resolution** - The execute_graph function handles ordering
- **Extensibility** - Easy to add parallel execution later

## How to Run

Look at `complete_example.py`, see `lesson_10_aot()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

graph = agent.create_aot_plan("Research and write article")
print(f"AoT graph: {graph}")

if graph:
    results = agent.execute_aot_plan(graph)
    print(f"Execution results: {results}")
```

## Compare to Lesson 09

**Lesson 09 (Atomic Actions):**
```
Step -> Atomic action: {"action": "...", "inputs": {...}}
```
Single step converted to atomic action.

**Lesson 10 (AoT):**
```
Goal -> Graph: {
  nodes: [
    {id: "1", action: "...", depends_on: []},
    {id: "2", action: "...", depends_on: ["1"]}
  ]
}
```
Multiple atomic actions with explicit dependencies.

## Key Insights

### AoT is Inevitable

At this point, AoT feels **inevitable**, not advanced. It's the natural evolution of planning (Lesson 08), atomic actions (Lesson 09), and adding dependencies. Once you understand the pieces, the graph structure makes perfect sense.

### It's Not Advanced Reasoning

AoT isn't smarter thinking - it's **better structure**:
- Each node is validated (from Lesson 09)
- Dependencies are explicit (new in this lesson)
- Execution is deterministic (respecting order)
- Failures are contained (to individual nodes)

### Structure Enables Scale

By adding dependencies, you can handle complex workflows with many actions. Dependencies enable:
- Parallel execution of independent actions
- Clear execution order
- Easier debugging (know what depends on what)

### Validation is Key

The graph structure must be validated before execution. Circular dependencies, missing nodes, or invalid references must be caught early.

## Common Issues

**"Circular dependencies"**
- The validation should catch this
- Check that dependencies form a directed acyclic graph (DAG)
- Consider adding cycle detection to validation

**"Dependencies reference non-existent nodes"**
- Validation checks for this
- Ensure all node IDs in dependencies exist in the graph
- Consider generating IDs more systematically

**"Execution order seems wrong"**
- Verify dependencies are correctly specified
- Check that execute_graph respects dependencies
- Consider adding execution logging to see order

## Exercises

1. Create graphs with different dependency structures
2. Try to create a circular dependency and see if validation catches it
3. Compare execution order with and without dependencies
4. Experiment with parallel vs sequential execution

## Final Insight

You've now built an agent that:
1. Talks to an LLM ([Lesson 01](01_basic_llm_chat.md))
2. Has consistent behavior ([Lesson 02](02_system_prompt.md))
3. Produces validated outputs ([Lesson 03](03_structured_output.md))
4. Makes decisions ([Lesson 04](04_decision_making.md))
5. Uses tools ([Lesson 05](05_tools.md))
6. Runs in a loop ([Lesson 06](06_agent_loop.md))
7. Remembers things ([Lesson 07](07_memory.md))
8. Plans actions ([Lesson 08](08_planning.md))
9. Executes safely ([Lesson 09](09_atomic_actions.md))
10. Scales with dependencies ([Lesson 10](10_atom_of_thought.md))

And you understand **exactly how it all works**. No magic, no hidden reasoning - just structure, validation, and explicit execution.

---

**Key Takeaway:** AoT is structure, not magic. Agents are systems, not minds. Dependency graphs enable complex workflows while maintaining control and predictability.
