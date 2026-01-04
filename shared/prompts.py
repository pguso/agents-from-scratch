"""
Prompt templates for the agent.

These functions build prompts that evolve across lessons:
- Lesson 01: base_prompt (just text)
- Lesson 02: system_prompt (add role)
- Lesson 03: json_contract (add structure)
- Lesson 04+: specialized prompts for decisions, tools, planning

Prompts are first-class citizens in agent systems.
"""


def base_prompt(user_input: str) -> str:
    """
    The simplest possible prompt - just the user's text.
    
    Used in: Lesson 01
    
    Args:
        user_input: The user's question or request
        
    Returns:
        Unmodified user input
    """
    return user_input


def system_prompt(role: str, user_input: str) -> str:
    """
    Add a system role to shape behavior.
    
    Used in: Lesson 02
    
    Args:
        role: Description of the assistant's role and behavior
        user_input: The user's question or request
        
    Returns:
        Formatted prompt with system and user sections
    """
    return f"""<SYSTEM>
{role}
</SYSTEM>

<USER>
{user_input}
</USER>"""


def json_contract(schema: str, content: str) -> str:
    """
    Enforce structured JSON output.
    
    Used in: Lesson 03
    
    Args:
        schema: JSON schema description
        content: The content to process
        
    Returns:
        Prompt that enforces JSON output
    """
    return f"""Return ONLY valid JSON.
No explanations. No markdown. No extra text.

Schema:
{schema}

Content:
{content}"""


def decision_prompt(choices: list[str], user_input: str) -> str:
    """
    Make the model choose from a finite set of options.
    
    Used in: Lesson 04
    
    Args:
        choices: List of possible actions/decisions
        user_input: The input to make a decision about
        
    Returns:
        Prompt that enforces decision-making
    """
    options = "\n".join(f"- {choice}" for choice in choices)
    
    return f"""You must choose ONE of the following options.
Return ONLY valid JSON.

Available choices:
{options}

Schema:
{{ "decision": string }}

Input:
{user_input}"""


def tool_call_prompt(tools: dict, user_input: str) -> str:
    """
    Request a tool call from the model.
    
    Used in: Lesson 05
    
    Args:
        tools: Dictionary of available tools and their schemas
        user_input: The user's request
        
    Returns:
        Prompt that requests a tool call
    """
    return f"""You may request ONE tool call.

Available tools:
{tools}

Return ONLY valid JSON.

Schema:
{{
  "tool": string,
  "arguments": object
}}

User request:
{user_input}"""


def agent_step_prompt(state: dict, user_input: str) -> str:
    """
    Generate the next agent action based on current state.
    
    Used in: Lesson 06
    
    Args:
        state: Current agent state
        user_input: User's input or system observation
        
    Returns:
        Prompt for agent step execution
    """
    return f"""You are an agent.

Current state:
{state}

Decide the next action.

Return ONLY valid JSON.

Schema:
{{
  "action": string,
  "reason": string
}}

User input:
{user_input}"""


def memory_prompt(state: dict, memory: list, user_input: str) -> str:
    """
    Agent prompt with memory context.
    
    Used in: Lesson 07
    
    Args:
        state: Current agent state
        memory: List of relevant memories
        user_input: User's input
        
    Returns:
        Prompt with memory context
    """
    return f"""You are an agent with memory.

Current state:
{state}

Relevant memory:
{memory}

Decide what to do next.

Return ONLY valid JSON.

Schema:
{{
  "action": string,
  "save_to_memory": string | null
}}

User input:
{user_input}"""


def planning_prompt(goal: str) -> str:
    """
    Generate a plan to achieve a goal.
    
    Used in: Lesson 08
    
    Args:
        goal: The goal to achieve
        
    Returns:
        Prompt for plan generation
    """
    return f"""Create a step-by-step plan to achieve the goal.

Return ONLY valid JSON.

Schema:
{{
  "steps": [string]
}}

Goal:
{goal}"""


def atomic_action_prompt(step: str) -> str:
    """
    Convert a plan step into an atomic action.
    
    Used in: Lesson 09
    
    Args:
        step: A step from a plan
        
    Returns:
        Prompt to generate atomic action
    """
    return f"""Convert this step into an atomic action.

Return ONLY valid JSON.

Schema:
{{
  "action": string,
  "inputs": object
}}

Step:
{step}"""


def aot_prompt(goal: str) -> str:
    """
    Generate an Atom of Thought execution graph.
    
    Used in: Lesson 10
    
    Args:
        goal: The goal to achieve
        
    Returns:
        Prompt for AoT graph generation
    """
    return f"""Create an atomic execution graph for the goal.

Return ONLY valid JSON.

Schema:
{{
  "nodes": [
    {{
      "id": string,
      "action": string,
      "depends_on": [string]
    }}
  ]
}}

Goal:
{goal}"""
