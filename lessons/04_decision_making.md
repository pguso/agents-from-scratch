# Lesson 04  -  Decision Making with LLMs

## What Question Are We Answering?

**"Can the model decide what to do, not just answer?"**

This is the first moment of **agency**. Instead of responding with generated text, the model chooses actions from a finite set of options.

## What You Will Build

A decision-making system that:
- Presents the model with a finite set of choices
- Forces the model to pick exactly one option
- Validates the decision and retries on failure
- Uses the decision to route execution

## New Concepts Introduced

### 1. Decision Schemas

A **decision schema** is a finite set of choices the model must pick from. Instead of generating free text, the model selects from predefined actions like "answer_question", "summarize_text", or "translate".

This constrains the output space dramatically - instead of infinite possible responses, there are only a few valid options.

### 2. Routing Logic

Once a decision is made, your code can **route** execution based on it. If the model chooses "summarize_text", you call the summarization function. If it chooses "translate", you call the translation function.

This is how agents take different paths based on what they "decide" to do.

### 3. Intent Detection

By framing user input as a decision problem, you're doing **intent detection**. The model analyzes what the user wants and maps it to one of your available actions.

This is simpler than trying to parse free text to understand intent.

## What We Are NOT Doing (Yet)

- No tools ([Lesson 05](05_tools.md))
- No agent loop ([Lesson 06](06_agent_loop.md))
- No memory ([Lesson 07](07_memory.md))
- No planning ([Lesson 08](08_planning.md))

## The Code

Look at `agent/agent.py`, see `decide()` method:

```python
def decide(self, user_input: str, choices: list[str]) -> str | None:
    """
    Make the model choose from a finite set of options.
    
    Lesson 04 version.
    
    Args:
        user_input: The input to make a decision about
        choices: List of possible actions/decisions
        
    Returns:
        The chosen action or None if decision failed
    """
    options = "\n".join(f"- {choice}" for choice in choices)
    
    prompt = f"""{self.system_prompt}

You must choose ONE of the following options. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Available choices:
{options}

Required JSON format:
{{"decision": "one_of_the_choices_above"}}

User request: {user_input}

Response (JSON only):"""
    
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed and "decision" in parsed:
            decision = parsed["decision"]
            if decision in choices:
                return decision
    
    return None
```

Notice we've added:
- **Finite choice space** - The model must pick from a predefined list, not generate anything
- **Validation** - We check that the decision is actually in the list of choices
- **Structured output** - Using the same JSON extraction pattern from Lesson 03
- **Retry logic** - Up to 3 attempts to get a valid decision

## How to Run

Look at `complete_example.py`, see `lesson_04_decisions()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

decision = agent.decide(
    "Can you summarize this article for me?",
    choices=["answer_question", "summarize_text", "translate"]
)

print(decision)
# Output: "summarize_text"
```

## Compare to Lesson 03

**Lesson 03 (Structured Output):**
```
Input: "What is AI?"
Output: {"answer": "AI is...", "confidence": "high"}
```
The model generates structured data with values it creates.

**Lesson 04 (Decision Making):**
```
Input: "Summarize this article"
Choices: ["answer_question", "summarize_text", "translate"]
Output: "summarize_text"
```
The model selects from predefined options - no generation, just selection.

## Key Insights

### Selection vs Generation

The model is no longer generating content - it's **selecting from a finite action space**. This is fundamentally different and much more predictable than free-text generation.

### Agency Begins Here

This is where the agent starts to feel "agent-like". It's not just responding - it's choosing what to do. The choices might be simple, but the pattern is important.

### Constrained = Reliable

By limiting choices to a small, well-defined set, you make the system more reliable. The model can't hallucinate new actions - it must pick from your list.

### Validation is Critical

Always validate that the decision is actually in your choices list. The model might return something that looks like a decision but isn't in your allowed set.

## Common Issues

**"The model returns a choice not in my list"**
- Validate against the choices list (the code does this)
- Make your choice names clear and unambiguous
- Consider adding a retry with more explicit instructions

**"All decisions seem random"**
- Check that your choices are semantically distinct
- Make sure the user input actually relates to the choices
- Lower temperature further for more deterministic selection

**"The model adds explanations"**
- The `extract_json_from_text()` helper handles this
- Stronger instructions help (already in the code)
- Consider rejecting responses with extra text

## Exercises

1. Create a decision with 5+ choices and test different inputs
2. Try ambiguous inputs and see which choice the model picks
3. Add a "none_of_the_above" choice and see when it's selected
4. Compare decisions with temperature 0.0 vs 0.5

## What's Next?

In [Lesson 05](05_tools.md), we'll introduce **tools** - capabilities the agent can request to extend beyond text generation.

---

**Key Takeaway:** Decisions = agency. Agents choose, not just respond. Constraining choices makes behavior predictable.