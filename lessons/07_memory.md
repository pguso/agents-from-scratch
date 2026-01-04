# Lesson 07  -  Memory (Short and Long)

## What Question Are We Answering?

**"How does an agent remember things?"**

Agents need to remember information across multiple interactions. Without memory, each conversation starts from scratch. Memory lets agents build on previous conversations and maintain context.

## What You Will Build

A memory system that:
- Stores facts across interactions
- Retrieves relevant memories when needed
- Integrates memory into the agent's context
- Allows explicit memory management

## New Concepts Introduced

### 1. Context vs Memory

**Context** is what's in the current prompt - everything the model can see right now. **Memory** is persistent storage that survives across interactions.

Context is temporary. Memory persists. Memory gets loaded into context when needed.

### 2. Persistence

**Persistence** means saving facts across turns. When a user says "My name is Alice," that fact should be stored and available in future interactions.

Without persistence, the agent forgets everything after each interaction.

### 3. Retrieval

**Retrieval** is getting relevant memories when needed. When the user asks "What's my name?", the agent retrieves "User's name is Alice" from memory and uses it to respond.

Simple retrieval might mean "get all memories." More sophisticated retrieval finds relevant memories based on the current query.

## What We Are NOT Doing (Yet)

- No planning ([Lesson 08](08_planning.md))
- No sophisticated memory retrieval - just simple "get all" retrieval
- No memory decay or prioritization

## The Code

Look at `agent/agent.py`, see `run_with_memory()` method:

```python
def run_with_memory(self, user_input: str) -> dict | None:
    """
    Run agent with memory context.
    
    Lesson 07 version.
    
    Args:
        user_input: User's input
        
    Returns:
        Response with potential memory update
    """
    memory_context = self.memory.get_all()
    
    # Build memory context string
    if memory_context:
        memory_str = "You remember the following:\n" + "\n".join(f"- {item}" for item in memory_context)
    else:
        memory_str = "You have no memories yet."
    
    prompt = f"""{self.system_prompt}

You are an agent with memory. You must respond with ONLY valid JSON.

{memory_str}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}
4. If the user tells you information (like their name), save it to memory
5. If the user asks about something you remember, USE YOUR MEMORY to answer

Required JSON format:
{{"reply": "your response text", "save_to_memory": "fact to remember" or null}}

Examples:
- User says "My name is Alice" -> {{"reply": "Nice to meet you, Alice!", "save_to_memory": "User's name is Alice"}}
- User asks "What's my name?" and you remember "User's name is Alice" -> {{"reply": "Your name is Alice", "save_to_memory": null}}

User input: {user_input}

Response (JSON only):"""
    
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed and "reply" in parsed:
            # Save to memory if requested
            if parsed.get("save_to_memory"):
                self.memory.add(parsed["save_to_memory"])
            
            self.state.increment_step()
            return parsed
    
    return None
```

Notice:
- **Memory retrieval** - `memory.get_all()` loads all stored memories
- **Context integration** - Memories are included in the prompt
- **Explicit storage** - The agent explicitly says what to save via JSON
- **Automatic persistence** - When `save_to_memory` is provided, it's automatically stored

## How to Run

Look at `complete_example.py`, see `lesson_07_memory()` method:

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

# First interaction - store name
response1 = agent.run_with_memory("My name is Alice")
if response1 and "reply" in response1:
    print(f"Response 1: {response1['reply']}")

# Second interaction - recall name
response2 = agent.run_with_memory("What's my name?")
if response2 and "reply" in response2:
    print(f"Response 2: {response2['reply']}")

print(f"Memory contents: {agent.memory.get_all()}")
```

![Memory System](diagrams/lesson-07-memory.png)

## Compare to Lesson 06

**Lesson 06 (Agent Loop):**
```
Loop -> Step 1 -> Step 2 -> Step 3 -> Done
         |         |        |
       Action   Action   Action
```
State persists within the loop but resets when the loop ends.

**Lesson 07 (Memory):**
```
Interaction 1 -> Save "name is Alice" -> Memory stores it
Interaction 2 -> Load memory -> "Your name is Alice"
```
Memory persists across completely separate interactions.

## Key Insights

### Memory is Explicit Storage

Memory is **explicit storage**, not consciousness. It's data you can inspect, modify, and delete. There's no hidden reasoning - just stored facts.

### Simple is Powerful

This memory system is simple: store strings, retrieve all of them. Yet it's incredibly useful. More sophisticated retrieval can come later, but this foundation works.

### The Agent Controls Storage

The agent decides what to save via the `save_to_memory` field. You could automate this, but explicit control keeps things predictable.

### Context Loading

Memories are loaded into the prompt context. The model doesn't have direct access to memory - it only sees what you include in the prompt.

## Common Issues

**"The agent doesn't save information"**
- Check that the response includes `save_to_memory`
- Verify the memory.add() is being called
- Make sure the prompt clearly explains when to save

**"The agent forgets things"**
- Verify memory is being loaded into the prompt
- Check that memory persists across calls
- Ensure the memory context string is being included

**"Memory gets too large"**
- This simple system stores all memories forever
- Consider adding memory limits or deletion
- More sophisticated systems can prioritize or summarize memories

## Exercises

1. Save multiple facts and see how they accumulate
2. Try asking about something not in memory
3. Manually inspect `agent.memory.get_all()` to see stored data
4. Modify the memory format and see how it affects behavior

## What's Next?

In [Lesson 08](08_planning.md), we'll add **planning** - the ability to break down complex goals into a sequence of steps.

---

**Key Takeaway:** Memory = data storage, not thoughts. It's explicit, inspectable, and gives agents continuity across interactions.