# Lesson 06  -  The Agent Loop (Without ReAct)

## What Question Are We Answering?

**"How does this become an agent instead of a chatbot?"**

Answer: When it can **observe → decide → act → repeat**, with state.

## New Concepts Introduced

- **Agent loop** - The observe/decide/act cycle
- **State transitions** - How state changes with each step
- **Termination conditions** - When to stop

## The Loop

```
while not done:
    observation = perceive(environment)
    decision = decide(observation, state)
    state = act(decision, state)
```

## The Code

```python
results = agent.run_loop("Help me analyze this document", max_steps=5)
# Runs multiple steps until done or max_steps reached
```

## Key Insight

An agent is not a clever prompt. It's a **loop with state**.

---

**Key Takeaway:** Agent = loop + state. That's it.
