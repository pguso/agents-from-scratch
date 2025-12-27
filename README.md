# AI Agents From Scratch

A step-by-step guide to building AI agents from first principles. No magic, no hype, no heavy frameworks - just the core concepts you need to understand how agents really work.

---

## Learning Path

### 1. Talking to a Model (Nothing Else)
**Directory:** `01_basic_llm_chat/`

**Question you'll answer:**  
"How do I talk to a model at all?"

**What you'll learn**
- Load a local LLM
- Send text in
- Get text out

**Concepts**
- Prompt
- Context
- Tokens

**What to expect:** You'll start with the absolute basics. No agents, no tools, no magic - just you and a language model.

---

### 2. Giving the Model a Role
**Directory:** `02_system_prompt_and_roles/`

**Question you'll answer:**  
"Why does the same model behave differently?"

**What you'll learn**
- System prompts
- Stable behavior via instructions
- Simple output constraints (tone, format)

**Concepts**
- Instruction hierarchy
- Behavior shaping

**What to expect:** You'll discover how powerful system prompts are, even without adding any complexity.

---

### 3. Making Output Reliable
**Directory:** `03_structured_output_basics/`

**Question you'll answer:**  
"How do I stop parsing free-text?"

**What you'll learn**
- JSON outputs
- Validation
- Retrying bad responses

**Concepts**
- Output contracts
- Trust boundaries

**What to expect:** This is your first "engineering" moment—gently introduced so you see why it matters.

---

### 4. Letting the Model Choose an Action
**Directory:** `04_decision_making_with_llms/`

**Question you'll answer:**  
"Can the model decide what to do, not just answer?"

**What you'll learn**
- Classification & routing
- Intent detection
- "Should I respond or do something?"

**Concepts**
- Decision prompts
- Choice spaces
- Routing logic

**What to expect:** This is where you'll experience the first glimpse of real agency, but it's still simple and understandable.

---

### 5. Introducing Tools 
**Directory:** `05_simple_tools/`

**Question you'll answer:**  
"Can the model ask me to do something?"

**What you'll learn**
- Tool definitions
- When a tool should be used
- Structured tool calls (JSON)

**Concepts**
- Tool interfaces
- Model-chosen actions

**What to expect:** The model can now request actions, but you're still in control. No autonomy yet—you execute the tools.

---

### 6. The Agent Loop 
**Directory:** `06_basic_agent_loop/`

**Question you'll answer:**  
"How does this become an agent instead of a chatbot?"

**What you'll learn**
- Observe → Decide → Act loop
- One step at a time
- Explicit state

**Concepts**
- Agent loop
- State transitions
- Termination conditions

**What to expect:** You'll build a clean, explicit agent loop that's easier to understand than traditional ReAct patterns.

---

### 7. Memory (Short and Long)
**Directory:** `07_agent_memory/`

**Question you'll answer:**  
"How does the agent remember things?"

**What you'll learn**
- Short-term memory
- Simple long-term storage
- Memory retrieval

**Concepts**
- Context vs memory
- Persistence

**What to expect:** Memory keeps things small and understandable - you won't get lost in complexity.

---

### 8. Planning as Data (Not Thoughts)
**Directory:** `08_simple_planning/`

**Question you'll answer:**  
"How can an agent solve multi-step tasks?"

**What you'll learn**
- Generate a plan first
- Plans as lists or JSON
- Validating plans before execution

**Concepts**
- Planning vs execution
- Step ordering

**What to expect:** This is your gentle introduction to planning - before you dive into Atomic Planning, you'll understand the fundamentals.

---

### 9. Atomic Steps & Safe Execution
**Directory:** `09_atomic_actions/`

**Question you'll answer:**  
"How do I make plans safe and predictable?"

**What you'll learn**
- Atomic steps
- Typed actions
- Failure handling

**Concepts**
- Atomicity
- Determinism

**What to expect:** Safety and predictability emerge naturally here, leading you smoothly toward Atomic Planning without hype.

---

### 10. Atomic Planning (AoT) - Now It Makes Sense
**Directory:** `10_atom_of_thought/`

**Question you'll answer:**  
"How do I scale planning without losing control?"

**What you'll learn**
- Atomic Planning (AoT)
- Dependency graphs
- Validated execution

**Concepts**
- Atomic planning
- Dependency resolution

**What to expect:** By now, Atomic Planning will feel inevitable, not advanced. You'll understand exactly why it exists and how to use it.

---

## Philosophy

### Our Mental Model

"An AI agent is:
- an LLM
- that can make decisions
- using structured outputs
- inside a loop
- with memory
- and a planner when needed"

**No hype. No frameworks. No magic.**

### Why This Path?

Most tutorials either:
- Throw you into a complex framework immediately
- Skip fundamental concepts in favor of "cool demos"
- Assume you already understand agent architecture

This path is different. It builds understanding from the ground up, one concept at a time, showing you **why** each piece exists before adding the next one.

### Who This Is For

- Developers who want to understand agents, not just use them
- Anyone tired of "magic" abstractions that hide how things work
- People who learn best by building progressively
- Engineers who want to make informed decisions about agent architecture

### What You Won't Find Here

- Heavy frameworks that hide the fundamentals
- Buzzword-driven explanations
- Shortcuts that create confusion later
- Hype about AGI or "autonomous agents"

---

## Getting Started

Each directory contains:
- **Concept explanation**: What you're learning and why
- **Working code**: Complete, runnable examples
- **Commentary**: Inline explanations of decisions
- **Next steps**: How this connects to what's coming

**Recommended approach:**
1. Read through in order, each builds on the previous
2. Run the code and experiment
3. Don't skip ahead, the progression matters
4. Take your time with concepts before moving on

---

## Requirements

- Python 3.9+
- A local LLM (instructions in `01_basic_llm_chat/`)
- Curiosity and patience

---

## Contributing

This is a learning resource focused on clarity over completeness. If you find:
- Confusing explanations
- Missing conceptual links
- Code that doesn't run
- Ways to make the path gentler

Please open an issue or PR. We value simplicity and understanding above all.

---

## License

MIT - Learn freely, build responsibly.

---

## Acknowledgments

Built on the principle that **understanding beats abstraction**, and that the best way to learn AI agents is to build them from scratch, one honest step at a time.
