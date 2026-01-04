# Lesson 02  -  Giving the Model a Role

## What Question Are We Answering?

**"Why does the same model behave differently?"**

You've probably noticed that LLMs can act like different personas - technical expert, creative writer, helpful assistant. How does that work?

## What You Will Build

A script that uses **system prompts** to:
- Assign the model a specific role
- Stabilize its behavior
- Control tone and format

## New Concepts Introduced

### 1. System Prompts

A **system prompt** is an instruction that shapes how the model responds. It's like giving someone a role before a conversation.

Example system prompts:
```
"You are a calm, precise teacher who explains concepts simply."
```

```
"You are a creative writer who uses vivid imagery."
```

```
"You are a code reviewer who finds bugs and suggests improvements."
```

### 2. Instruction Hierarchy

Most models understand this hierarchy:
1. **System prompt** - Overall behavior and role
2. **User prompt** - The actual question or request

The system prompt has higher "priority" - it guides how the model interprets the user prompt.

### 3. Behavior Shaping

Behavior ≠ intelligence. Behavior = instructions.

The same model can:
- Be technical or casual (tone)
- Be verbose or concise (length)
- Be creative or factual (style)

All based on the system prompt.

## What We Are NOT Doing (Yet)

- No structured outputs ([Lesson 03](03_structured_output.md))
- No decisions ([Lesson 04](04_decision_making.md))
- No tools ([Lesson 05](05_tools.md))
- No memory ([Lesson 07](07_memory.md))

## The Code

Look at `agent/agent.py` → `generate_with_role()` method:

```python
def generate_with_role(self, user_input: str) -> str:
    """
    Generate with a system prompt to shape behavior.
    """
    # Use a format that doesn't confuse the model
    prompt = f"""{self.system_prompt}

User: {user_input}
Assistant:"""
    
    response = self.llm.generate(prompt)
    # Clean up any potential tag artifacts
    response = response.replace('<SYSTEM>', '').replace('</SYSTEM>', '')
    response = response.replace('<USER>', '').replace('</USER>', '')
    return response.strip()
```

Notice we've added:
- The system prompt at the beginning
- A simple "User:" / "Assistant:" format for the conversation
- Cleanup code to remove any tag artifacts that might appear

## How to Run

Look at `complete_example.py` → `lesson_02_with_role()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

# The agent has a default system prompt:
# "You are a calm, precise, and helpful AI assistant..."

response = agent.generate_with_role("What is an AI agent?")
print(response)
```

## Compare to Lesson 01

**Without system prompt ([Lesson 01](01_basic_llm_chat.md)):**
```
Input: "What is an AI agent?"
Output: "An AI agent is a system that perceives its environment and acts autonomously to achieve specified goals. It processes information, makes decisions, and can adapt to changing conditions using machine learning algorithms..."
```

**With system prompt:**
```
Input: "What is an AI agent?"
Output: "Think of an AI agent as a helpful assistant that can observe what's happening around it and take actions to help you accomplish tasks. Like how a thermostat watches the temperature and adjusts heating automatically - but much more sophisticated."
```

Same question. Same model. Different behavior.

## The Power of System Prompts

### Example 1: Technical Expert
```python
agent.system_prompt = "You are a senior software engineer who explains concepts with code examples."
```

### Example 2: ELI5 (Explain Like I'm 5)
```python
agent.system_prompt = "You explain complex topics using simple words and everyday analogies."
```

### Example 3: Concise Responder
```python
agent.system_prompt = "You give accurate answers in 1-2 sentences maximum. No elaboration unless asked."
```

## Key Insights

### Behavior is Configurable

You're not changing the model - you're changing the **constraints** on its output. The model still predicts tokens; the system prompt just shifts probabilities.

### Consistency Improves

Without a system prompt, the model might be:
- Formal one response, casual the next
- Verbose sometimes, terse other times
- Inconsistent in tone

A system prompt creates **behavioral consistency**.

### Still Probabilistic

Even with a system prompt, responses vary. But they vary **within the constraints** you set.

## Common System Prompt Patterns

### 1. Role Definition
```
You are a [role] who [behavior].
```

### 2. Constraint Setting
```
You must [requirement]. You never [prohibition].
```

### 3. Output Format
```
Always respond with [format]. Use [style].
```

### 4. Combination
```
You are a helpful assistant. 
You explain concepts clearly using examples.
You keep responses under 100 words unless asked to elaborate.
```

## Common Issues

**"The model ignores my system prompt"**
- Some models follow system prompts better than others
- Try being more explicit and specific
- Use stronger language ("You MUST..." instead of "Try to...")

**"Responses are still inconsistent"**
- This is normal - LLMs are probabilistic
- Lower the `temperature` for more consistency
- We'll add validation in [Lesson 03](03_structured_output.md)

**"The system prompt is too long"**
- Keep it under 100-200 words
- More tokens = less room for user input + response

## Exercises

1. Try different system prompts and observe behavior changes
2. Create a system prompt that makes responses extremely concise
3. Create a system prompt that makes responses highly detailed
4. Experiment with conflicting instructions (what wins?)

## What's Next?

In [Lesson 03](03_structured_output.md), we'll add **structured outputs** to make responses reliable and parseable. Instead of free text, we'll get validated JSON.

---

**Key Takeaway:** Behavior is not intelligence. It's constraints. System prompts turn a general model into a specific assistant.
