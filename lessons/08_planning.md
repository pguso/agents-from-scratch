# Lesson 08  -  Planning as Data (Not Thoughts)

## What Question Are We Answering?

**"How can an agent solve multi-step tasks?"**

Complex tasks require multiple steps. Planning breaks down a goal into a sequence of actions that can be executed step by step.

## What You Will Build

A planning system that:
- Generates a step-by-step plan from a goal
- Separates planning from execution
- Stores plans as data structures
- Executes plans sequentially

## New Concepts Introduced

### 1. Planning vs Execution

**Planning** is generating the steps needed to achieve a goal. **Execution** is actually doing those steps. By separating them, you can:
- Inspect the plan before executing
- Modify the plan if needed
- Debug planning separately from execution

This separation is powerful - you can see what the agent "thinks" it should do before it does it.

### 2. Step Ordering

**Step ordering** determines the sequence of actions. Steps might depend on each other (step 2 needs step 1's output), or they might be independent.

For now, we execute steps in order. Later lessons will handle dependencies more explicitly.

### 3. Validation

**Validation** checks plans before execution. Is the plan valid JSON? Does it have the required structure? Are the steps reasonable?

Validating plans catches errors before wasting time on execution.

## What We Are NOT Doing (Yet)

- No dependency handling ([Lesson 10](10_atom_of_thought.md))
- No atomic action validation ([Lesson 09](09_atomic_actions.md))
- No parallel execution - steps run sequentially

## The Code

Look at `agent/agent.py`, see `create_plan()` and `execute_plan()` methods:

```python
def create_plan(self, goal: str) -> dict | None:
    """
    Generate a plan to achieve a goal.
    
    Lesson 08 version.
    
    Args:
        goal: The goal to achieve
        
    Returns:
        Plan with steps
    """
    plan = create_plan(self.llm, goal)
    
    if plan:
        self.state.current_plan = plan
    
    return plan

def execute_plan(self, plan: dict) -> list:
    """
    Execute a plan step by step.
    
    Args:
        plan: Plan dictionary with "steps" list
        
    Returns:
        List of execution results
    """
    if not plan or "steps" not in plan:
        return []
    
    results = []
    
    for step in plan["steps"]:
        # Simple execution - in reality you'd call tools, etc.
        result = {
            "step": step,
            "executed": True
        }
        results.append(result)
        self.state.increment_step()
    
    return results
```

And the planner implementation in `agent/planner.py`:

```python
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
```

Notice:
- **Structured output** - Plans are JSON data structures
- **Validation** - We check that plans have the expected structure
- **Retry logic** - Multiple attempts to get a valid plan
- **Simple execution** - Steps are executed in order (actual execution logic comes later)

## How to Run

Look at `complete_example.py`, see `lesson_08_planning()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

plan = agent.create_plan("Write a blog post about AI agents")
print(f"Plan: {plan}")

if plan:
    results = agent.execute_plan(plan)
    print(f"Execution results: {results}")
```

## Compare to Lesson 07

**Lesson 07 (Memory):**
```
User: "My name is Alice" -> Save to memory
User: "What's my name?" -> Retrieve from memory
```
Stores and retrieves facts.

**Lesson 08 (Planning):**
```
Goal: "Write article" -> Plan: ["Research", "Outline", "Write", "Review"]
Plan -> Execute each step -> Results
```
Generates and executes a sequence of steps.

## Key Insights

### Plans Aren't Thoughts

Plans aren't thoughts - they're **data structures**. This makes them inspectable, modifiable, and safe. You can see, edit, and validate them before execution.

### Planning = Data Generation

Planning is not sophisticated reasoning - it's structured data generation. The model generates a list of steps, just like it generates any other structured output.

### Separate Phases

Separating planning from execution lets you:
- Debug plans without executing
- Modify plans before running
- Reuse plans for similar goals
- Test planning independently

### Simple Execution

For now, execution is simple - just iterate through steps. Later lessons will add more sophisticated execution with dependencies and validation.

## Common Issues

**"The plan is too vague"**
- Make the goal more specific
- Provide examples of good plans in the prompt
- Consider breaking down very general goals

**"Steps are in wrong order"**
- The model determines order - validate if needed
- Consider adding dependency information
- Review and reorder steps before execution if necessary

**"Execution doesn't do anything"**
- This lesson's execution is a placeholder
- In practice, you'd call tools or other functions
- The pattern is more important than the implementation

## Exercises

1. Generate plans for different types of goals
2. Modify plans manually before executing
3. Compare plans for the same goal across multiple runs
4. Try to validate plans for completeness

## What's Next?

In [Lesson 09](09_atomic_actions.md), we'll make execution safer by converting plan steps into **atomic actions** with validated schemas.

---

**Key Takeaway:** Planning = data generation, not reasoning. Plans are inspectable data structures that enable multi-step execution.
