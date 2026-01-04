"""
Agent memory system.

Memory is explicit storage, not consciousness.
It's data that persists across agent steps and can be queried.
"""


class Memory:
    """
    Simple memory storage for the agent.
    
    This is intentionally basic and grows in lessons:
    - Lesson 07: Basic list-based memory
    - Future: Add semantic search, persistence, etc.
    """
    
    def __init__(self):
        """Initialize empty memory."""
        self.items = []
    
    def add(self, item: str):
        """
        Add an item to memory.
        
        Args:
            item: String to remember
        """
        if item and item not in self.items:
            self.items.append(item)
    
    def get_all(self) -> list[str]:
        """
        Retrieve all memory items.
        
        Returns:
            List of all stored items
        """
        return self.items.copy()
    
    def get_recent(self, n: int = 5) -> list[str]:
        """
        Get the n most recent memory items.
        
        Args:
            n: Number of recent items to retrieve
            
        Returns:
            List of recent items
        """
        return self.items[-n:] if self.items else []
    
    def search(self, query: str) -> list[str]:
        """
        Simple search through memory items.
        
        Args:
            query: String to search for
            
        Returns:
            List of items containing the query
        """
        query_lower = query.lower()
        return [item for item in self.items if query_lower in item.lower()]
    
    def clear(self):
        """Clear all memory."""
        self.items = []
    
    def __len__(self) -> int:
        """Return the number of items in memory."""
        return len(self.items)
    
    def __repr__(self) -> str:
        """String representation of memory."""
        return f"Memory({len(self.items)} items)"