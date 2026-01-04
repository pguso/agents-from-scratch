# Lesson 03  -  Making Output Reliable

## What Question Are We Answering?

**"How do I stop parsing free-text?"**

Free-text responses are unpredictable. Sometimes the model adds explanations, sometimes it uses different formats, sometimes it hallucinates. We need **structure**.

## What You Will Build

A system that:
- Forces JSON output
- Validates the response
- Retries on failure

## New Concepts Introduced

### 1. Output Contracts

An **output contract** is a specification for what the model must return. Instead of "answer the question," we say "return JSON matching this schema."

```json
{
  "answer": string,
  "confidence": "high" | "medium" | "low"
}
```

### 2. Trust Boundaries

Never trust LLM output directly. Always:
1. Parse it
2. Validate it
3. Handle failures

This is the first "engineering" moment - treating the LLM as a fallible component.

### 3. Validation

Validation ensures the output matches your contract:
- Is it valid JSON?
- Does it have required fields?
- Are the values the right type?

## The Code

Look at `agent/agent.py`, see `generate_structured()` method:

```python
def generate_structured(self, user_input: str, schema: str) -> dict | None:
    """
    Generate structured JSON output with validation and retries.
    
    Lesson 03 version.
    
    Args:
        user_input: The user's question or request
        schema: JSON schema description
        
    Returns:
        Parsed JSON dictionary or None if all retries failed
    """
    prompt = f"""{self.system_prompt}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no extra text before or after the JSON
3. Start your response with {{ and end with }}

Schema you must follow:
{schema}

User request: {user_input}

Response (JSON only):"""
    
    # Try up to 3 times
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed is not None:
            return parsed
    
    return None
```

Notice we've added:
- **Strong instructions** - "CRITICAL INSTRUCTIONS" with explicit JSON-only requirements
- **Temperature control** - `temperature=0.0` for more deterministic, consistent output
- **JSON extraction** - `extract_json_from_text()` handles cases where the model adds extra text
- **Retry logic** - Up to 3 attempts to get valid JSON, turning probabilistic behavior into reliable results

## How to Run

Look at `complete_example.py`, see `lesson_03_structured()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

schema = '''
{
  "topic": string,
  "difficulty": "beginner" | "intermediate" | "advanced"
}
'''

result = agent.generate_structured(
    "Explain quantum computing",
    schema
)

print(result)
# {"topic": "'quantum computing", "difficulty": "advanced"}
```

## Why This Matters

### Before (Free Text)
```
Output: "Okay! This task is medium difficulty. I'd suggest building..."
```
- Can't parse
- Inconsistent
- Unreliable

### After (Structured)
```
Output: {'topic': 'quantum computing', 'difficulty': 'advanced'}
```
- Parseable
- Predictable
- Validated

## Key Insights

### LLMs Are Probabilistic

They don't always output valid JSON on the first try. Retries turn probabilistic behavior into reliable behavior.

### Structure Beats Cleverness

A simple prompt with validation beats a clever prompt without it.

### This is Engineering

You're treating the LLM as a component in a system:
- Input: prompt + schema
- Output: validated data or error
- Retry: if validation fails

## Common Issues

**"The model adds explanations before JSON"**
- Use `extract_json_from_text()` helper (finds JSON in text)
- Emphasize "ONLY valid JSON" in prompt

**"Still getting invalid responses"**
- Lower temperature for more deterministic output
- Be more specific about the schema
- Use models trained for structured output

**"Retries use too many tokens"**
- 3 retries is usually enough
- Track retry counts to monitor model quality

## What's Next?

In [Lesson 04](04_decision_making.md), we add **decision making** - the model chooses actions, not just answers questions.

---

**Key Takeaway:** Structured outputs + validation = reliable agents.