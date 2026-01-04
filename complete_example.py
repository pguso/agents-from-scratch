#!/usr/bin/env python3
"""
Complete Agent Example

This script demonstrates the agent using features from all 10 lessons.
It's meant as a reference for how the pieces fit together.
"""

from agent.agent import Agent


def lesson_01_basic_chat():
    """Lesson 01: Basic LLM interaction"""
    print("\n" + "="*50)
    print("LESSON 01: Basic LLM Chat")
    print("="*50)
    
    agent = Agent("models/llama-3-8b-instruct.gguf")
    response = agent.simple_generate("What is an AI agent?")
    print(f"Response: {response}")


def lesson_02_with_role():
    """Lesson 02: System prompts"""
    print("\n" + "="*50)
    print("LESSON 02: With System Prompt")
    print("="*50)
    
    agent = Agent("models/llama-3-8b-instruct.gguf")
    response = agent.generate_with_role("What is an AI agent?")
    print(f"Response: {response}")


def lesson_03_structured():
    """Lesson 03: Structured outputs"""
    print("\n" + "="*50)
    print("LESSON 03: Structured Output")
    print("="*50)

    agent = Agent("models/llama-3-8b-instruct.gguf")

    schema = """{
  "topic": string,
  "difficulty": "beginner" | "intermediate" | "advanced"
}"""

    result = agent.generate_structured(
        "Explain quantum computing",
        schema
    )
    print(f"Structured result: {result}")


def lesson_04_decisions():
    """Lesson 04: Decision making"""
    print("\n" + "="*50)
    print("LESSON 04: Decision Making")
    print("="*50)

    agent = Agent("models/llama-3-8b-instruct.gguf")

    decision = agent.decide(
        "Can you summarize this article for me?",
        choices=["answer_question", "summarize_text", "translate"]
    )
    print(f"Decision: {decision}")


def lesson_05_tools():
    """Lesson 05: Tool calling"""
    print("\n" + "="*50)
    print("LESSON 05: Tool Calling")
    print("="*50)

    agent = Agent("models/llama-3-8b-instruct.gguf")

    tool_call = agent.request_tool("What is 42 * 7?")
    print(f"Tool request: {tool_call}")

    if tool_call:
        result = agent.execute_tool_call(tool_call)
        print(f"Tool result: {result}")


def lesson_06_agent_loop():
    """Lesson 06: Agent loop"""
    print("\n" + "="*50)
    print("LESSON 06: Agent Loop")
    print("="*50)

    agent = Agent("models/llama-3-8b-instruct.gguf")

    results = agent.run_loop("Help me understand loops", max_steps=3)
    print(f"Loop results: {results}")


def lesson_07_memory():
    """Lesson 07: Memory"""
    print("\n" + "="*50)
    print("LESSON 07: Memory")
    print("="*50)

    agent = Agent("models/llama-3-8b-instruct.gguf")

    # First interaction - store name
    response1 = agent.run_with_memory("My name is Alice")
    if response1 and "reply" in response1:
        print(f"Response 1: {response1['reply']}")
        if response1.get("save_to_memory"):
            print(f"  → Saved to memory: {response1['save_to_memory']}")
    else:
        print(f"Response 1: {response1}")

    # Second interaction - recall name
    response2 = agent.run_with_memory("What's my name?")
    if response2 and "reply" in response2:
        print(f"Response 2: {response2['reply']}")
        if response2.get("save_to_memory"):
            print(f"  → Saved to memory: {response2['save_to_memory']}")
    else:
        print(f"Response 2: {response2}")

    print(f"\nMemory contents: {agent.memory.get_all()}")


def lesson_08_planning():
    """Lesson 08: Planning"""
    print("\n" + "="*50)
    print("LESSON 08: Planning")
    print("="*50)

    agent = Agent("models/llama-3-8b-instruct.gguf")

    plan = agent.create_plan("Write a blog post about AI agents")
    print(f"Plan: {plan}")

    if plan:
        results = agent.execute_plan(plan)
        print(f"Execution results: {results}")


def lesson_09_atomic_actions():
    """Lesson 09: Atomic actions"""
    print("\n" + "="*50)
    print("LESSON 09: Atomic Actions")
    print("="*50)

    agent = Agent("models/llama-3-8b-instruct.gguf")

    # Convert a plan step into an atomic action
    step = "Write an explanation of AI agents"
    atomic_action = agent.create_atomic_action(step)
    print(f"Step: {step}")
    print(f"Atomic action: {atomic_action}")

    # Example with a step from a plan
    plan = agent.create_plan("Create a tutorial about Python")
    if plan and "steps" in plan and plan["steps"]:
        first_step = plan["steps"][0]
        atomic_action_from_plan = agent.create_atomic_action(first_step)
        print(f"\nPlan step: {first_step}")
        print(f"Atomic action from plan step: {atomic_action_from_plan}")


def lesson_10_aot():
    """Lesson 10: Atom of Thought"""
    print("\n" + "="*50)
    print("LESSON 10: Atom of Thought")
    print("="*50)

    agent = Agent("models/llama-3-8b-instruct.gguf")
    
    graph = agent.create_aot_plan("Research and write article")
    print(f"AoT graph: {graph}")
    
    if graph:
        results = agent.execute_aot_plan(graph)
        print(f"Execution results: {results}")


def main():
    """Run all lesson examples"""
    print("\n" + "#"*50)
    print("# AI Agent Examples - All Lessons")
    print("#"*50)
    
    try:
        # Comment out lessons you want to skip
        lesson_01_basic_chat()
        lesson_02_with_role()
        lesson_03_structured()
        lesson_04_decisions()
        lesson_05_tools()
        lesson_06_agent_loop()
        lesson_07_memory()
        lesson_08_planning()
        lesson_09_atomic_actions()
        lesson_10_aot()
        
        print("\n" + "="*50)
        print("All examples completed!")
        print("="*50)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Downloaded a GGUF model")
        print("2. Placed it in the models/ directory")
        print("3. Updated the model path in this script")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
