# Lesson 09  -  Atomic Steps & Safe Execution

## What Question Are We Answering?

**"How do I make plans safe and predictable?"**

Plan steps like "Write article" are vague and hard to validate. Atomic actions break steps into the smallest possible, well-defined operations that can be validated and executed safely.

## What You Will Build

An atomic action system that:
- Converts vague plan steps into specific, typed actions
- Validates actions before execution
- Uses schemas to ensure correct parameters
- Makes execution predictable and debuggable

## New Concepts Introduced

### 1. Atomicity

**Atomicity** means breaking actions into the smallest possible units. Instead of "Write article," you get "generate_text" with specific parameters like topic and length.

Atomic actions are indivisible - they either succeed completely or fail completely, with no partial states.

### 2. Determinism

**Determinism** means predictable outcomes. Given the same atomic action with the same inputs, you should get similar results (accounting for LLM randomness).

Atomic actions make execution deterministic by removing ambiguity.

### 3. Typed Execution

**Typed execution** means actions have validated schemas. Each action specifies:
- Action name (e.g., "generate_text")
- Required inputs (e.g., {"topic": string, "length": string})
- Validation rules

This catches errors before execution.

## What We Are NOT Doing (Yet)

- No dependency handling between actions ([Lesson 10](10_atom_of_thought.md))
- No parallel execution
- No action execution implementation - just conversion and validation

## The Code

Look at `agent/planner.py`, see `create_atomic_action()` function:

```python
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
```

And in `agent/agent.py`:

```python
def create_atomic_action(self, step: str) -> dict | None:
    """
    Convert a plan step into an atomic action.
    
    Lesson 09 version.
    
    Args:
        step: A step from a plan (e.g., "Write an explanation of AI agents")
        
    Returns:
        Atomic action dictionary with "action" and "inputs", or None if generation failed
    """
    return create_atomic_action(self.llm, step)
```

Notice:
- **Step conversion** - Vague steps become specific actions with parameters
- **Schema validation** - Actions must have "action" and "inputs" fields
- **Structured output** - Uses the same JSON pattern from previous lessons
- **Retry logic** - Multiple attempts to get valid atomic actions

## How to Run

Look at `complete_example.py`, see `lesson_09_atomic_actions()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

# Convert a plan step into an atomic action
step = "Write an explanation of AI agents"
atomic_action = agent.create_atomic_action(step)
print(f"Step: {step}")
print(f"Atomic action: {atomic_action}")

# Example with a step from a plan
plan = agent.create_plan("Create a tutorial about Python")
if plan and "steps" in plan and plan["steps"]:
    first_step = plan["steps"][0]
    atomic_action_from_plan = agent.create_atomic_action(first_step)
    print(f"\nPlan step: {first_step}")
    print(f"Atomic action from plan step: {atomic_action_from_plan}")
```

## Compare to Lesson 08

**Lesson 08 (Planning):**
```
Goal -> Plan: ["Research topic", "Create outline", "Write draft"]
```
Plans are lists of vague step descriptions.

**Lesson 09 (Atomic Actions):**
```
Step: "Write draft" -> Atomic: {"action": "generate_text", "inputs": {"topic": "...", "length": "..."}}
```
Steps become specific, typed actions with validated parameters.

## Key Insights

### Small Steps = Safe Systems

The smaller the action, the safer the system. Atomic actions are:
- Easier to validate - you can check parameters before execution
- Easier to test - each action can be tested independently
- Easier to debug - failures are isolated to specific actions
- Harder to fail catastrophically - small actions have limited blast radius

### Vague vs Specific

"Write article" is vague. "generate_text(topic='AI agents', length='1000 words')" is specific. Specificity enables validation and predictable execution.

### Validation Happens Early

By validating actions before execution, you catch errors early. A plan with invalid actions can be rejected before any work is done.

### Building Blocks

Atomic actions are building blocks. Complex workflows are built from many simple atomic actions, each validated and safe.

## Common Issues

**"Atomic action is still vague"**
- Provide clearer instructions in the prompt
- Give examples of good atomic actions
- Consider constraining the action names to a predefined set

**"Validation fails"**
- Check that the action has both "action" and "inputs" fields
- Verify the JSON structure is correct
- Consider adding schema validation for inputs

**"Conversion fails"**
- Some steps might not map cleanly to atomic actions
- Consider multiple retry attempts (already implemented)
- Provide more context about what makes a good atomic action

## Exercises

1. Convert different types of plan steps to atomic actions
2. Compare atomic actions for similar steps
3. Try to validate atomic actions before execution
4. Experiment with different input parameter structures

## What's Next?

In [Lesson 10](10_atom_of_thought.md), we'll combine planning, atomic actions, and **dependencies** to create execution graphs that can run actions in the correct order and even in parallel.

---

**Key Takeaway:** Small steps = safe systems. Atomic actions make execution predictable, debuggable, and safe by breaking vague plans into specific, validated operations.