# Lesson 05  -  Introducing Tools 

## What Question Are We Answering?

**"Can the model ask me to do something?"**

Tools extend the agent's capabilities beyond text generation. Instead of only generating text, the agent can request actions like calculations, API calls, or file operations.

## What You Will Build

A tool-calling system that:
- Lets the agent request specific tools with structured parameters
- Validates tool requests before execution
- Separates tool requests from tool execution
- Extends agent capabilities without retraining the model

## New Concepts Introduced

### 1. Tool Interfaces

A **tool interface** is a defined API the agent can request. Tools have names and parameters, like `calculator(a, b, operation)`. The agent requests the tool, but the system executes it.

This separation is critical - the agent **describes** what it needs, but you **control** what actually happens.

### 2. Structured Tool Calls

Tool calls are **structured JSON specifications** for function calls. The model outputs JSON like `{"tool": "calculator", "arguments": {"a": 42, "b": 7, "operation": "multiply"}}`, and your code validates and executes it.

This is similar to Lesson 04's decision making, but instead of choosing an action, the agent is specifying a function call.

### 3. Model-Chosen Actions

The agent decides **which tool to use** and **what parameters to pass**. You define available tools, but the agent chooses which one fits the situation.

This is agency at work - the agent is selecting and configuring actions.

## Important Rule

The model **requests** tools. The system **executes** them. No autonomy yet. This separation gives you control and safety.

## What We Are NOT Doing (Yet)

- No agent loop ([Lesson 06](06_agent_loop.md))
- No memory ([Lesson 07](07_memory.md))
- No automatic tool execution - you still manually execute tool calls

## The Code

Look at `agent/agent.py`, see `request_tool()` method:

```python
def request_tool(self, user_input: str) -> dict | None:
    """
    Have the model request a tool call.
    
    Lesson 05 version.
    
    Args:
        user_input: The user's request
        
    Returns:
        Tool call specification or None if request failed
    """
    prompt = f"""{self.system_prompt}

You are a tool-calling assistant. When asked a math question, you must respond with ONLY valid JSON.

Available tool: calculator
- Parameters: a (number), b (number), operation ("add", "subtract", "multiply", or "divide")

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Example format:
{{"tool": "calculator", "arguments": {{"a": 42, "b": 7, "operation": "multiply"}}}}

User request: {user_input}

Response (JSON only):"""
    
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed and "tool" in parsed and "arguments" in parsed:
            return parsed
    
    return None

def execute_tool_call(self, tool_call: dict) -> Any:
    """
    Execute a tool call requested by the model.
    
    Args:
        tool_call: Dictionary with "tool" and "arguments"
        
    Returns:
        Result of the tool execution
    """
    return execute_tool(tool_call["tool"], tool_call["arguments"])
```

Notice:
- **Structured output** - The tool call is validated JSON, similar to Lesson 03
- **Validation** - We check that both "tool" and "arguments" are present
- **Separation of concerns** - Request and execution are separate methods
- **Extensibility** - Easy to add new tools without changing the model

## How to Run

Look at `complete_example.py`, see `lesson_05_tools()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

tool_call = agent.request_tool("What is 42 * 7?")
print(f"Tool request: {tool_call}")

if tool_call:
    result = agent.execute_tool_call(tool_call)
    print(f"Tool result: {result}")
```

## Compare to Lesson 04

**Lesson 04 (Decision Making):**
```
Input: "What should I do?"
Choices: ["answer", "calculate", "translate"]
Output: "calculate"
```
The agent picks from a list of actions.

**Lesson 05 (Tool Calling):**
```
Input: "What is 42 * 7?"
Tool: calculator
Arguments: {"a": 42, "b": 7, "operation": "multiply"}
Result: 294
```
The agent specifies a tool call with parameters and gets a result.

## Key Insights

### Tools Are Interfaces, Not Abilities

The agent doesn't have the ability - you do. The agent describes what it needs through a structured interface, and you provide the implementation. This keeps you in control.

### No Retraining Required

To add new capabilities, you add new tools. The model doesn't need retraining - it just needs to understand the tool interface. This is powerful.

### Safety Through Separation

By separating tool requests from execution, you can validate, log, and control what actually happens. The agent can't execute dangerous operations without your code allowing it.

### Structured = Reliable

Using the same structured JSON pattern from Lessons 03 and 04 makes tool calls reliable and parseable. The model outputs structured data, you validate it, then execute.

## Common Issues

**"The model requests a tool that doesn't exist"**
- Validate the tool name against your available tools
- Provide clear examples of available tools in the prompt
- Handle invalid tool names gracefully

**"The arguments are the wrong type"**
- Validate argument types before execution
- Make the expected types clear in the tool description
- Consider using schema validation for complex tools

**"The model doesn't request a tool when it should"**
- Make it clear when tools should be used
- Provide examples in the prompt
- Consider making tool use mandatory for certain request types

## Exercises

1. Add a new tool (e.g., "weather" or "search") and test it
2. Try invalid tool calls and see how validation handles them
3. Modify the tool interface and see how the model adapts
4. Create tools with different parameter types (strings, numbers, booleans)

## What's Next?

In [Lesson 06](06_agent_loop.md), we'll create the **agent loop** - putting decision making and tool calling together into a repeating cycle.

---

**Key Takeaway:** Tool calling = expanding capabilities without retraining. Tools are interfaces you control, not abilities the agent has.
