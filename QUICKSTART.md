# Quick Start Guide

Get up and running with AI Agents from Scratch in 10 minutes.

## Prerequisites

- Python 3.10 or higher
- 8GB+ RAM (for running local models)
- ~5-10GB free disk space (for model files)

## Step 1: Install Dependencies

```bash
pip install llama-cpp-python
```

**Optional but recommended:**
```bash
# Create a virtual environment first
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install llama-cpp-python
```

## Step 2: Download a Model

You need a GGUF model file. Here's the easiest way:

1. Go to https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF
2. Download `Meta-Llama-3-8B-Instruct-Q4_K_M.gguf` (~5GB)
3. Place it in the `models/` directory
4. Rename it to `llama-3-8b-instruct.gguf` (optional, for simplicity)

**Alternative models:**
- Mistral 7B: https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.2-GGUF
- Gemma 7B: https://huggingface.co/bartowski/gemma-7b-it-GGUF

## Step 3: Verify Setup

```bash
python setup_check.py
```

This checks:
- Python version
- Dependencies
- Models directory
- Repository structure

## Step 4: Run Examples

```bash
python complete_example.py
```

This will run examples from all 10 lessons. You can also open `complete_example.py` and modify the model path or comment out lessons you want to skip.

## Step 6: Start Learning

Now read the lessons in order:

1. `lessons/01_basic_llm_chat.md` - Understanding the basics
2. `lessons/02_system_prompt.md` - Adding behavior
3. `lessons/03_structured_output.md` - Making it reliable
4. ... and so on through lesson 10

Each lesson builds on the previous one.

## Troubleshooting

### "Module 'llama_cpp' not found"

```bash
pip install llama-cpp-python
```

### "Model file not found"

Check that:
1. The model file is in `models/` directory
2. The path in `complete_example.py` matches the actual filename
3. The file has a `.gguf` extension

### "Out of memory" error

Try a smaller model or smaller quantization:
- Q4_K_M: ~5GB RAM
- Q5_K_M: ~6GB RAM  
- Q8_0: ~8GB RAM

### Slow responses

This is normal for CPU inference. Each response takes 10-30 seconds depending on:
- Your CPU speed
- Model size
- Response length

## Next Steps

- **Read philosophy.md** to understand the approach
- **Work through lessons** one at a time
- **Modify the agent** to experiment
- **Check examples/** for complete code examples

## Getting Help

- Check existing [GitHub Issues](https://github.com/your-repo/issues)
- Read the lesson markdown files carefully
- Ask questions in [GitHub Discussions](https://github.com/your-repo/discussions)

## Tips for Success

1. **Don't skip lessons** - they build on each other
2. **Run the code** - reading isn't enough
3. **Experiment** - modify examples and see what happens
4. **Be patient** - local inference is slow but worth it
5. **Read comments** - the code explains the "why"

Happy learning! 🚀