"""
Agent state management.

State is explicit, inspectable, and modifiable.
It's not hidden in conversation history or mysterious context.
"""


class AgentState:
    """
    Represents the current state of the agent.
    
    This grows throughout the lessons as we add capabilities:
    - Lesson 06: Basic state (steps, done)
    - Lesson 07: Add memory tracking
    - Lesson 08: Add planning state
    - Lesson 09: Add execution state
    - Lesson 10: Add dependency tracking
    """
    
    def __init__(self):
        """Initialize a new agent state."""
        self.steps = 0
        self.done = False
        self.current_plan = None
        self.last_action = None
    
    def increment_step(self):
        """Increment the step counter."""
        self.steps += 1
    
    def mark_done(self):
        """Mark the agent's task as complete."""
        self.done = True
    
    def reset(self):
        """Reset the state for a new task."""
        self.steps = 0
        self.done = False
        self.current_plan = None
        self.last_action = None
    
    def to_dict(self) -> dict:
        """
        Convert state to a dictionary for serialization or prompts.
        
        Returns:
            Dictionary representation of the state
        """
        return {
            "steps": self.steps,
            "done": self.done,
            "current_plan": self.current_plan,
            "last_action": self.last_action,
        }
    
    def __repr__(self) -> str:
        """String representation of the state."""
        return f"AgentState(steps={self.steps}, done={self.done})"
