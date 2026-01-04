# Lesson 05  -  Introducing Tools (Carefully)

## What Question Are We Answering?

**"Can the model ask me to do something?"**

Tools extend the agent's capabilities beyond text generation.

## New Concepts Introduced

- **Tool interfaces** - APIs the agent can request
- **Structured tool calls** - JSON specifications for function calls  
- **Model-chosen actions** - Agent decides WHICH tool to use

## Important Rule

The model **requests** tools. The system **executes** them. No autonomy yet.

## The Code

```python
# Agent requests a tool
tool_call = agent.request_tool("What is 42 * 7?")
# Returns: {"tool": "calculator", "arguments": {"a": 42, "b": 7, "operation": "multiply"}}

# Human/system executes it
result = agent.execute_tool_call(tool_call)
# Returns: 294
```

## Key Insight

Tools are **interfaces**, not abilities. The agent describes what it needs; you provide it.

---

**Key Takeaway:** Tool calling = expanding capabilities without retraining.
