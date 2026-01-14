# AI Agents from Scratch

A gentle, local-first introduction to AI agents.

This repository teaches how AI agents actually work by building **one agent** step by step from a single local LLM call.

**No frameworks. No cloud APIs. No hidden reasoning. No magic.**


## Related Projects

### [AI Product from Scratch](https://github.com/pguso/ai-product-from-scratch)

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white)](https://nodejs.org/)

Learn AI product development fundamentals with local LLMs. Covers prompt engineering, structured output, multi-step reasoning, API design, and frontend integration through 10 comprehensive lessons with visual diagrams.

### [AI Agents from Scratch in JavaScript](https://github.com/pguso/ai-agents-from-scratch) 

![Python](https://img.shields.io/badge/JavaScript-3776AB?logo=javascript&logoColor=yellow)

![Agent Architecture](diagrams/agent-architecture.png)

## Philosophy

Agents are not personalities. They are loops, state, and constraints.

If something feels like magic, open the file — there is no hidden logic in this repo.

## What You Will Learn

This repository builds one continuously evolving agent across 12 lessons:

| Lesson | Capability Added | Link |
|--------|------------------|------|
| 01 | Text in / text out | [lessons/01_basic_llm_chat.md](lessons/01_basic_llm_chat.md) |
| 02 | Roles and behavior (system prompts) | [lessons/02_system_prompt.md](lessons/02_system_prompt.md) |
| 03 | Structured output (JSON contracts) | [lessons/03_structured_output.md](lessons/03_structured_output.md) |
| 04 | Decisions (routing logic) | [lessons/04_decision_making.md](lessons/04_decision_making.md) |
| 05 | Tools (external capabilities) | [lessons/05_tools.md](lessons/05_tools.md) |
| 06 | Agent loop (observe → decide → act) | [lessons/06_agent_loop.md](lessons/06_agent_loop.md) |
| 07 | Memory (short and long-term) | [lessons/07_memory.md](lessons/07_memory.md) |
| 08 | Planning (as data, not thoughts) | [lessons/08_planning.md](lessons/08_planning.md) |
| 09 | Atomic actions (safe execution) | [lessons/09_atomic_actions.md](lessons/09_atomic_actions.md) |
| 10 | AoT - Atom of Thought (dependency graphs) | [lessons/10_atom_of_thought.md](lessons/10_atom_of_thought.md) |
| 11 | Evals (regression testing) | [lessons/11_evals.md](lessons/11_evals.md) |
| 12 | Telemetry (runtime observability) | [lessons/12_telemetry.md](lessons/12_telemetry.md) |

## Who This Is For

**This repo is for:**
- Developers who can code but feel lost with agents
- People tired of "just use LangChain"
- Learners who want local models
- Engineers who want mechanical understanding
- Educators looking for a clean mental model

**This repo is NOT for:**
- People looking for the fastest demo
- People who want a SaaS starter kit
- People who believe agents "think"
- People who want hidden chain-of-thought

## Quick Start

**For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md)**

In short:
1. Install dependencies: `pip install -r requirements.txt`
2. Download a GGUF model to the `models/` folder
3. Run: `python complete_example.py`

**Note:** The `complete_example.py` file contains executable code examples demonstrating all 12 lessons. You can use it as a reference to see how all the concepts fit together.

## Repository Structure

```
ai-agents-from-scratch/
├─ README.md              # You are here
├─ philosophy.md          # Why this repo exists
├─ QUICKSTART.md          # Detailed setup guide
├─ complete_example.py    # Demonstrations of all 12 lessons
├─ requirements.txt       # Python dependencies
│
├─ models/                # Place GGUF models here
├─ shared/                # Reusable utilities (LLM, prompts, utils)
├─ agent/                 # The evolving agent implementation
│  ├─ agent.py             # Main agent class 
│  ├─ memory.py            # Memory system
│  ├─ planner.py           # Planning and atomic actions
│  ├─ state.py             # Agent state management
│  ├─ tools.py             # Tool definitions
│  ├─ evals.py             # Evaluation framework (Lesson 11)
│  └─ telemetry.py         # Telemetry system (Lesson 12)
├─ evals/                 # Golden datasets for testing
│  └─ golden_datasets.py   # Known-good test cases
└─ lessons/               # Step-by-step explanations (01-12)
```

### Key Files Explained

**`agent/agent.py`** - The heart of the repository
- Contains the `Agent` class that evolves across all 12 lessons
- Each lesson adds new methods and capabilities to this same class
- This is what you study and modify as you learn

**`complete_example.py`** - Learning reference
- Contains 12 separate functions, one for each lesson
- Each function demonstrates that lesson's concepts in isolation
- Use this to see how individual lessons work before combining them
- Run: `python complete_example.py`

**`agent/evals.py`** - Regression testing (Lesson 11)
- Test your agent against known-good cases
- Catch prompt regressions before deployment

**`agent/telemetry.py`** - Runtime observability (Lesson 12)
- Structured logging for debugging
- Track latency, success rates, and traces

**Relationship**: 
- `agent/agent.py` = the code you're learning (the implementation)
- `complete_example.py` = isolated examples of each lesson (for learning and experimentation)

## What This Repo Is Not

- This is **not a framework**
- This is **not a chatbot demo**
- This does **not claim models think**
- This does **not expose chain-of-thought**
- This does **not require OpenAI or cloud APIs**

## Core Principles

1. **One agent, many stages** - The same `agent.py` file grows across lessons
2. **Explicit over implicit** - No hidden logic, no magic abstractions
3. **Structure over prompting** - Reliability comes from constraints, not clever wording
4. **Local-first** - No API keys, no rate limits, no cloud dependency
5. **Educational, not production** - This teaches fundamentals, not best practices

## Learning Path

Each lesson builds on the previous one. **Do not skip ahead.**

The curriculum is designed to build understanding gradually:
- Lessons 1-3: Foundation (LLM basics)
- Lessons 4-6: Agency (decisions, tools, loops)
- Lessons 7-10: Intelligence (memory, planning, execution)
- Lessons 11-12: Observability (evals, telemetry)

## Contributing

This is an educational repository. Contributions should:
- Maintain the gentle, progressive learning style
- Keep code readable over clever
- Add explanations, not just features
- Preserve the "no framework" philosophy

## License

MIT License - see LICENSE file

## Acknowledgments

This repository synthesizes best practices from modern agent development while deliberately avoiding complexity that obscures understanding.

---

**If you find this useful, please star the repository and share it with others learning about AI agents.**
