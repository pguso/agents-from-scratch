# Contributing to AI Agents from Scratch

Thank you for your interest in contributing! This repository has a specific educational philosophy, so please read this guide carefully before contributing.

## Philosophy First

This repository prioritizes:
1. **Clarity over cleverness**
2. **Progressive complexity**
3. **Mechanical understanding**
4. **No magic, no hype**

Every contribution should make the learning experience **better**, not just add features.

## What We Welcome

### ✅ Good Contributions

- **Bug fixes** in existing code
- **Clarifications** in lesson explanations
- **Better examples** that illustrate concepts
- **Additional exercises** at the end of lessons
- **Documentation improvements**
- **Typo fixes and grammar improvements**
- **Translation** of lessons to other languages

### ⚠️ Needs Discussion First

These might be good ideas, but need careful thought:
- **New lessons** - must fit the progression
- **Alternative approaches** - must preserve simplicity
- **Framework integrations** - goes against the philosophy
- **Advanced features** - might break the learning flow

### ❌ We Will Not Accept

- Additions that require external APIs
- Framework dependencies (LangChain, CrewAI, etc.)
- "Smart" abstractions that hide mechanisms
- Chain-of-thought or hidden reasoning
- Anthropomorphic language ("the agent thinks...")
- Hype-driven features without pedagogical value

## Contribution Guidelines

### 1. Code Style

**Python Code:**
- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Prefer readability over brevity
- Comment "why," not "what"

**Example:**
```python
def safe_json_parse(text: str) -> dict | None:
    """
    Safely parse JSON text, returning None on failure.
    
    This handles the common case where LLMs add extra text
    around JSON, making direct parsing fail.
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
```

### 2. Lesson Writing Style

**Principles:**
- Start with the question being answered
- Introduce one concept at a time
- Use concrete examples
- Avoid jargon without explanation
- End with key takeaways

**Structure:**
```markdown
# Lesson XX  -  Title

## What Question Are We Answering?

## What You Will Build

## New Concepts Introduced

## What We Are NOT Doing (Yet)

## The Code

## How to Run

## Key Insights

## Common Issues

## Exercises

## What's Next?

---

**Key Takeaway:**
```

### 3. Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Fix JSON parsing in lesson 03 example"
- "Clarify memory explanation in lesson 07"
- "Add exercise for testing different temperatures"

Bad:
- "Update"
- "Fix bug"
- "Changes"
```

## How to Contribute

### 1. Small Changes (Typos, Small Fixes)

For small changes:
1. Fork the repository
2. Make your changes
3. Submit a pull request with a clear description

### 2. Larger Changes (New Examples, Lessons)

For larger contributions:
1. **Open an issue first** to discuss the idea
2. Wait for maintainer feedback
3. If approved, fork and implement
4. Submit a pull request

### 3. Testing Your Changes

Before submitting:
- Test all code examples work
- Verify markdown renders correctly
- Check that changes don't break the lesson progression
- Run through the lessons as a learner would

## Code Review Process

We will review for:
1. **Pedagogical value** - Does this help learning?
2. **Simplicity** - Is it as simple as possible?
3. **Consistency** - Does it fit the existing style?
4. **Correctness** - Does the code work?

## Questions?

- **For bugs:** Open an issue with steps to reproduce
- **For features:** Open an issue to discuss first
- **For questions:** Use GitHub Discussions

## Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the repository

Thank you for helping make AI agent education better!