# Lesson 06  -  The Agent Loop

## What Question Are We Answering?

**"How does this become an agent instead of a chatbot?"**

Answer: When it can **observe, decide, act, and repeat**, with state. A chatbot responds once and stops. An agent takes multiple steps toward a goal.

## What You Will Build

An agent loop that:
- Runs multiple steps in sequence
- Maintains state across steps
- Decides actions based on current state
- Terminates when the goal is reached or max steps exceeded

## New Concepts Introduced

### 1. Agent Loop

The **agent loop** is the repeating cycle: observe, decide, act. Each iteration, the agent looks at the current situation, decides what to do, takes that action, and repeats until done.

This is what separates agents from simple chatbots - agents don't stop after one response.

### 2. State Transitions

**State transitions** track how the agent's state changes with each step. The state might include step count, completion status, accumulated results, or other tracking information.

State makes the loop aware of its progress and history.

### 3. Termination Conditions

**Termination conditions** determine when the loop stops. Common conditions include:
- The agent decides it's "done"
- Maximum steps reached
- A goal is achieved
- An error occurs

Without termination, the loop would run forever.

## What We Are NOT Doing (Yet)

- No memory across loops ([Lesson 07](07_memory.md))
- No planning ([Lesson 08](08_planning.md))
- No sophisticated reasoning - just simple step-by-step decisions

## The Code

Look at `agent/agent.py`, see `agent_step()` and `run_loop()` methods:

```python
def agent_step(self, user_input: str) -> dict | None:
    """
    Execute one step of the agent loop: observe, decide, act.
    
    Lesson 06 version.
    
    Args:
        user_input: User's input or system observation
        
    Returns:
        Action decision or None if step failed
    """
    state_dict = self.state.to_dict()
    
    prompt = f"""{self.system_prompt}

You are an agent. You must decide the next action and respond with ONLY valid JSON.

Current state: steps={state_dict.get('steps', 0)}, done={state_dict.get('done', False)}

Available actions: analyze, research, summarize, answer, done

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"action": "action_name", "reason": "explanation"}}

User input: {user_input}

Response (JSON only):"""
    
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed and "action" in parsed:
            if "reason" not in parsed:
                parsed["reason"] = f"Taking action: {parsed['action']}"
            self.state.increment_step()
            return parsed
    
    return None

def run_loop(self, user_input: str, max_steps: int = 5):
    """
    Run the agent loop for multiple steps.
    
    Args:
        user_input: Initial user input
        max_steps: Maximum number of steps to execute
        
    Returns:
        List of action results
    """
    self.state.reset()
    results = []
    
    while not self.state.done and self.state.steps < max_steps:
        action = self.agent_step(user_input)
        
        if action:
            results.append(action)
            
            # Simple termination condition
            if action.get("action") == "done":
                self.state.mark_done()
        else:
            break
    
    return results
```

Notice:
- **State tracking** - Each step increments the step counter and checks completion
- **Loop structure** - `while not done` continues until termination
- **Action accumulation** - Results are collected across steps
- **Safety limits** - `max_steps` prevents infinite loops

## How to Run

Look at `complete_example.py`, see `lesson_06_agent_loop()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

print("\nNote: Repetition in early iterations is expected.")
print("The agent refines its understanding step by step and may repeat analysis")
print("before converging on a clearer explanation.\n")

results = agent.run_loop("Help me understand loops", max_steps=3)

for i, result in enumerate(results, 1):
    print(f"Iteration {i}:")
    action = result.get("action", "unknown")
    reason = result.get("reason", "No reason provided")
    print(f"  Action: {action}")
    print(f"  Reason: {reason}")
    if i < len(results):
        print()
```

The output shows each iteration with the action taken and reason. Note that repetition in early iterations is expected - the agent refines its understanding step by step.

## Compare to Lesson 05

**Lesson 05 (Tool Calling):**
```
Request -> Tool call -> Result -> Done
```
Single interaction: request, execute, return.

**Lesson 06 (Agent Loop):**
```
Input -> Step 1 -> Step 2 -> Step 3 -> Done
          |        |        |
        Action   Action   Action
```
Multiple steps in sequence, each deciding what to do next.

![Agent Loop Flow](diagrams/lesson-06-agent-loop.png)

## Key Insights

### An Agent is Not a Clever Prompt

An agent is not a clever prompt. It's a **loop with state**. The magic isn't in the prompt - it's in the repeated cycle of observation, decision, and action.

### State Enables Continuity

Without state, each step would be independent. With state, steps can build on each other and track progress toward a goal.

### Termination is Critical

Always have termination conditions. Without them, loops can run forever or consume resources unnecessarily. `max_steps` is a simple but essential safety mechanism.

### Simple is Better

This loop is intentionally simple. Complex reasoning can come later - first, establish the pattern of repeated action.

## Common Issues

**"The loop runs forever"**
- Check that termination conditions are properly set
- Verify `max_steps` is being enforced
- Make sure the agent can signal "done"

**"Each step seems independent"**
- Include state information in the prompt
- Pass accumulated results to subsequent steps
- Make the state visible to the decision-making process

**"The agent doesn't make progress"**
- Check that actions actually change something
- Verify state is being updated correctly
- Ensure the agent sees relevant state information

## Exercises

1. Modify the available actions and see how the loop adapts
2. Change `max_steps` and observe how it affects behavior
3. Add state variables beyond step count
4. Experiment with different termination conditions

## What's Next?

In [Lesson 07](07_memory.md), we'll add **memory** so the agent can remember information across multiple interactions, not just within a single loop.

---

**Key Takeaway:** Agent = loop + state. That's it. The loop enables multi-step behavior, state enables continuity.