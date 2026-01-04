# Lesson 01  -  Talking to a Model

## What Question Are We Answering?

**"How do I talk to a language model at all?"**

This is the absolute foundation. Before we can build agents, we need to understand the simplest possible interaction: text in, text out.

## What You Will Build

A minimal interaction that:
- Loads a local LLM
- Sends text to it
- Receives text back

That's it. No magic. No frameworks. Just the basics.

## New Concepts Introduced

### 1. Prompts

A **prompt** is just text you send to the model. It can be a question like "What is an AI agent?", an instruction like "Explain quantum computing", or a request like "Write a poem about the ocean". The model completes or responds to this text based on patterns it learned during training.

### 2. Tokens

Models don't see text as words - they see **tokens**. Tokens are pieces of text (often words or subwords). For example, "Hello world" might be 2 tokens, while "artificial intelligence" could be 2-4 tokens depending on the model.

This matters because models have token limits (context windows), generation is measured in tokens per second, and longer prompts use more tokens, leaving less room for responses.

### 3. Context

The **context** is everything the model can "see" at once. It includes your prompt, any previous conversation, and system instructions. Models have a **context window** (e.g., 2048 tokens). If you exceed it, the model can't see the earlier text.

## What We Are NOT Doing (Yet)

- No system prompts ([Lesson 02](02_system_prompt.md))
- No structured outputs ([Lesson 03](03_structured_output.md))
- No tools ([Lesson 05](05_tools.md))
- No agents ([Lesson 06](06_agent_loop.md))
- No memory ([Lesson 07](07_memory.md))

This lesson is intentionally minimal.

## The Code

Look at `agent/agent.py`, see `simple_generate()` method:

```python
def simple_generate(self, user_input: str) -> str:
    """
    Simplest possible interaction - just pass text to the LLM.
    """
    return self.llm.generate(user_input)
```

That's it. One line. No complexity.

## How to Run

Look at `complete_example.py`, see `lesson_01_basic_chat()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

response = agent.simple_generate("What is an AI agent?")
print(response)
```

## What's Happening Internally?

1. Your text is converted to tokens
2. Tokens are sent to the model
3. The model predicts the next token
4. Repeat until a stop condition (end token, max length, etc.)
5. Tokens are converted back to text
6. Text is returned to you

## Key Insights

### There is No "Understanding"

The model doesn't "understand" your question. Instead, it recognizes patterns in the tokens, predicts likely continuations, and generates probabilistic text. This is important: **models are pattern matchers, not minds.**

### It's Probabilistic

Run the same prompt twice and you might get different responses. This happens because models use randomness (temperature) in generation, and multiple plausible continuations exist. There's no single "correct" answer - just probabilistic outputs.

### Text In = Text Out

That's all this is. Everything else we build (agents, tools, memory) is built on top of this simple foundation.

## Common Issues

**"The response is cut off"**
- Increase `max_tokens` in `shared/llm.py`

**"The model repeats itself"**
- This is normal for completion models
- We'll fix it with better prompting in [Lesson 02](02_system_prompt.md)

**"The response doesn't match the prompt"**
- Some models need specific formatting
- We'll add structure in [Lesson 02](02_system_prompt.md) and [Lesson 03](03_structured_output.md)

## Exercises

1. Try different prompts and observe the responses
2. Change the `temperature` in `shared/llm.py` (0.0 = deterministic, 1.0 = creative)
3. Use `max_tokens` to control response length

## What's Next?

In [Lesson 02](02_system_prompt.md), we'll add a **system prompt** to shape the model's behavior. This turns random completions into consistent, useful responses.

---

**Key Takeaway:** An LLM is just a text completion engine. Everything we build is structured interaction with this simple mechanism.
