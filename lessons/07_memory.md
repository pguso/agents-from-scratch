# Lesson 07  -  Memory (Short and Long)

## What Question Are We Answering?

**"How does an agent remember things?"**

## New Concepts Introduced

- **Context vs Memory** - What's in the prompt vs what's stored
- **Persistence** - Saving facts across turns
- **Retrieval** - Getting relevant memories when needed

## The Code

```python
# Agent can save facts to memory
response = agent.run_with_memory("My name is Alice")
# Internally: memory.add("User's name is Alice")

# Later...
response = agent.run_with_memory("What's my name?")
# Agent sees memory context and responds: "Your name is Alice"
```

## Key Insight

Memory is **explicit storage**, not consciousness. It's data you can inspect and modify.

---

**Key Takeaway:** Memory = data storage, not thoughts.
