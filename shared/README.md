# Shared Code

This folder contains small, boring helpers used by the agent.

## Files

- **llm.py** - Minimal wrapper around llama-cpp-python
- **utils.py** - JSON parsing and text formatting helpers
- **prompts.py** - Prompt templates that evolve across lessons

## Philosophy

Nothing clever lives here.

If something feels complex, it doesn't belong in this folder.

These utilities exist to:
1. Reduce repetition
2. Keep lesson code focused
3. Maintain consistency

They are intentionally simple and well-documented.