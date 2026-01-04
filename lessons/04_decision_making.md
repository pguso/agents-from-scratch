# Lesson 04  -  Decision Making with LLMs

## What Question Are We Answering?

**"Can the model decide what to do, not just answer?"**

This is the first moment of **agency**. Instead of responding, the model chooses actions.

## New Concepts Introduced

- **Decision schemas** - Finite choice spaces
- **Routing logic** - Directing execution based on decisions
- **Intent detection** - Understanding what the user wants

## The Code

```python
def decide(self, user_input: str, choices: list[str]) -> str | None:
    # Model picks ONE option from choices
    # Returns the chosen action
```

## Example

```python
decision = agent.decide(
    "Summarize this article about AI",
    choices=["answer_question", "summarize_text", "translate"]
)
# Returns: "summarize_text"
```

## Key Insight

The model is no longer generating content - it's **selecting from a finite action space**. This is how agents work.

---

**Key Takeaway:** Decisions = agency. Agents choose, not just respond.
