"""
The Agent - This file grows across all 10 lessons.

This is the heart of the repository. Each lesson adds exactly one capability
to this agent, building understanding progressively.

Lesson progression:
01: Basic LLM chat
02: System prompts (roles)
03: Structured outputs (JSON)
04: Decision-making
05: Tool calling
06: Agent loop
07: Memory
08: Planning
09: Atomic actions
10: AoT (Atom of Thought)
"""

from typing import Any

from shared.llm import LocalLLM
from shared.utils import safe_json_parse, extract_json_from_text
from agent.state import AgentState
from agent.memory import Memory
from agent.tools import get_tool_schema, execute_tool
from agent.planner import create_plan, create_atomic_action, create_aot_graph, execute_graph


class Agent:
    """
    An AI agent that grows in capability across lessons.
    
    This is the same agent throughout the repository - it just gains
    new methods and capabilities as lessons progress.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the agent.
        
        Args:
            model_path: Path to the GGUF model file
        """
        # Lesson 01: Basic LLM interaction
        self.llm = LocalLLM(model_path)
        
        # Lesson 02: System prompt for consistent behavior
        self.system_prompt = (
            "You are a calm, precise, and helpful AI assistant. "
            "You explain concepts simply and avoid unnecessary jargon. "
            "You are honest about what you know and don't know."
        )
        
        # Lesson 06: Agent state
        self.state = AgentState()
        
        # Lesson 07: Memory system
        self.memory = Memory()
    
    # ============================================================
    # LESSON 01: Basic LLM Chat
    # ============================================================
    
    def simple_generate(self, user_input: str) -> str:
        """
        Simplest possible interaction - just pass text to the LLM.
        
        Lesson 01 version.
        
        Args:
            user_input: The user's question or request
            
        Returns:
            The model's response
        """
        return self.llm.generate(user_input)
    
    # ============================================================
    # LESSON 02: System Prompts (Roles)
    # ============================================================
    
    def generate_with_role(self, user_input: str) -> str:
        """
        Generate with a system prompt to shape behavior.
        
        Lesson 02 version.
        
        Args:
            user_input: The user's question or request
            
        Returns:
            The model's response with role-based behavior
        """
        # Use a format that doesn't confuse the model
        prompt = f"""{self.system_prompt}

User: {user_input}
Assistant:"""
        
        response = self.llm.generate(prompt)
        # Clean up any potential tag artifacts
        response = response.replace('<SYSTEM>', '').replace('</SYSTEM>', '')
        response = response.replace('<USER>', '').replace('</USER>', '')
        return response.strip()
    
    # ============================================================
    # LESSON 03: Structured Outputs
    # ============================================================
    
    def generate_structured(self, user_input: str, schema: str) -> dict | None:
        """
        Generate structured JSON output with validation and retries.
        
        Lesson 03 version.
        
        Args:
            user_input: The user's question or request
            schema: JSON schema description
            
        Returns:
            Parsed JSON dictionary or None if all retries failed
        """
        prompt = f"""{self.system_prompt}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no extra text before or after the JSON
3. Start your response with {{ and end with }}

Schema you must follow:
{schema}

User request: {user_input}

Response (JSON only):"""
        
        # Try up to 3 times
        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)
            
            if parsed is not None:
                return parsed
        
        return None
    
    # ============================================================
    # LESSON 04: Decision Making
    # ============================================================
    
    def decide(self, user_input: str, choices: list[str]) -> str | None:
        """
        Make the model choose from a finite set of options.
        
        Lesson 04 version.
        
        Args:
            user_input: The input to make a decision about
            choices: List of possible actions/decisions
            
        Returns:
            The chosen action or None if decision failed
        """
        options = "\n".join(f"- {choice}" for choice in choices)
        
        prompt = f"""{self.system_prompt}

You must choose ONE of the following options. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Available choices:
{options}

Required JSON format:
{{"decision": "one_of_the_choices_above"}}

User request: {user_input}

Response (JSON only):"""
        
        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)
            
            if parsed and "decision" in parsed:
                decision = parsed["decision"]
                if decision in choices:
                    return decision
        
        return None
    
    # ============================================================
    # LESSON 05: Tools
    # ============================================================
    
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
    
    # ============================================================
    # LESSON 06: Agent Loop
    # ============================================================
    
    def agent_step(self, user_input: str) -> dict | None:
        """
        Execute one step of the agent loop: observe → decide → act.
        
        Lesson 06 version.
        
        Args:
            user_input: User's input or system observation
            
        Returns:
            Action decision or None if step failed
        """
        state_dict = self.state.to_dict()
        
        prompt = f"""{self.system_prompt}

You are an agent. You must decide the next action and respond with ONLY valid JSON.

Current state: steps={state_dict.get('steps', 0)}, done={state_dict.get('done', False)}

Available actions: analyze, research, summarize, answer, done

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"action": "action_name", "reason": "explanation"}}

User input: {user_input}

Response (JSON only):"""
        
        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)
            
            if parsed and "action" in parsed:
                if "reason" not in parsed:
                    parsed["reason"] = f"Taking action: {parsed['action']}"
                self.state.increment_step()
                return parsed
        
        return None
    
    def run_loop(self, user_input: str, max_steps: int = 5):
        """
        Run the agent loop for multiple steps.
        
        Args:
            user_input: Initial user input
            max_steps: Maximum number of steps to execute
            
        Returns:
            List of action results
        """
        self.state.reset()
        results = []
        
        while not self.state.done and self.state.steps < max_steps:
            action = self.agent_step(user_input)
            
            if action:
                results.append(action)
                
                # Simple termination condition
                if action.get("action") == "done":
                    self.state.mark_done()
            else:
                break
        
        return results
    
    # ============================================================
    # LESSON 07: Memory
    # ============================================================
    
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
- User says "My name is Alice" → {{"reply": "Nice to meet you, Alice!", "save_to_memory": "User's name is Alice"}}
- User asks "What's my name?" and you remember "User's name is Alice" → {{"reply": "Your name is Alice", "save_to_memory": null}}

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
    
    # ============================================================
    # LESSON 08: Planning
    # ============================================================
    
    def create_plan(self, goal: str) -> dict | None:
        """
        Generate a plan to achieve a goal.
        
        Lesson 08 version.
        
        Args:
            goal: The goal to achieve
            
        Returns:
            Plan with steps
        """
        plan = create_plan(self.llm, goal)
        
        if plan:
            self.state.current_plan = plan
        
        return plan
    
    def execute_plan(self, plan: dict) -> list:
        """
        Execute a plan step by step.
        
        Args:
            plan: Plan dictionary with "steps" list
            
        Returns:
            List of execution results
        """
        if not plan or "steps" not in plan:
            return []
        
        results = []
        
        for step in plan["steps"]:
            # Simple execution - in reality you'd call tools, etc.
            result = {
                "step": step,
                "executed": True
            }
            results.append(result)
            self.state.increment_step()
        
        return results
    
    # ============================================================
    # LESSON 09: Atomic Actions
    # ============================================================
    
    def create_atomic_action(self, step: str) -> dict | None:
        """
        Convert a plan step into an atomic action.
        
        Lesson 09 version.
        
        Atomic actions are the smallest possible actions that can be:
        - Validated independently
        - Tested in isolation
        - Executed safely
        - Rolled back if needed
        
        Args:
            step: A step from a plan (e.g., "Write an explanation of AI agents")
            
        Returns:
            Atomic action dictionary with "action" and "inputs", or None if generation failed
        """
        return create_atomic_action(self.llm, step)
    
    # ============================================================
    # LESSON 10: Atom of Thought (AoT)
    # ============================================================
    
    def create_aot_plan(self, goal: str) -> dict | None:
        """
        Generate an AoT execution graph.
        
        Lesson 10 version.
        
        Args:
            goal: The goal to achieve
            
        Returns:
            AoT graph with atomic nodes and dependencies
        """
        return create_aot_graph(self.llm, goal)
    
    def execute_aot_plan(self, graph: dict) -> list:
        """
        Execute an AoT graph respecting dependencies.
        
        Args:
            graph: AoT graph
            
        Returns:
            List of execution results
        """
        def execute_action(action: str):
            # Placeholder for actual action execution
            return f"Executed: {action}"
        
        return execute_graph(graph, execute_action)
    
    # ============================================================
    # MAIN RUN METHOD (evolves across lessons)
    # ============================================================
    
    def run(self, user_input: str) -> str:
        """
        Main entry point for the agent.
        
        This method evolves across lessons to use different capabilities.
        Currently, at: Lesson 07 (with memory)
        
        Args:
            user_input: The user's question or request
            
        Returns:
            The agent's response
        """
        result = self.run_with_memory(user_input)
        
        if result and "reply" in result:
            return result["reply"]
        
        # Fallback to simple generation
        return self.generate_with_role(user_input)
