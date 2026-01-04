"""
Utility functions for the agent.

These are boring, predictable helpers that do exactly what they say.
Nothing clever lives here.
"""

import json


def safe_json_parse(text: str) -> dict | None:
    """
    Safely parse JSON text, returning None on failure.
    
    Args:
        text: String that might be valid JSON
        
    Returns:
        Parsed JSON as a dictionary, or None if parsing fails
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None


def extract_json_from_text(text: str) -> dict | None:
    """
    Try to extract JSON from text that might have extra content.
    
    This handles cases where the model adds explanations before/after JSON.
    
    Args:
        text: Text that might contain JSON
        
    Returns:
        Parsed JSON if found, None otherwise
    """
    if not text:
        return None
    
    # Clean up the text - remove common markdown code blocks
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()
    
    # Remove common prefixes that models sometimes add
    prefixes = ["JSON:", "Response:", "Answer:", "Here's the JSON:", "The JSON is:"]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    
    # Try direct parsing first
    result = safe_json_parse(text)
    if result is not None:
        return result
    
    # Try to find JSON between curly braces (most common case)
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        json_text = text[start:end+1]
        result = safe_json_parse(json_text)
        if result is not None:
            return result
        
        # Try to fix common issues: unclosed strings, missing quotes
        # This is a simple heuristic - if we're close, try to fix it
        if json_text.count('"') % 2 != 0:
            # Odd number of quotes - try to close the last string
            last_quote = json_text.rfind('"')
            if last_quote > 0:
                # Check if it's an opening quote
                before = json_text[:last_quote]
                if before.count('"') % 2 == 0:
                    # This might be an unclosed string, try adding a closing quote
                    try_fix = json_text[:last_quote+1] + '"' + json_text[last_quote+1:] + '}'
                    result = safe_json_parse(try_fix)
                    if result is not None:
                        return result
    
    # Try to find JSON between square brackets (for arrays)
    start = text.find('[')
    end = text.rfind(']')
    
    if start != -1 and end != -1 and end > start:
        json_text = text[start:end+1]
        result = safe_json_parse(json_text)
        if result is not None:
            return result
    
    # Last resort: try to extract key-value pairs from text
    # This is very heuristic and may not work well
    if '{' in text or '[' in text:
        # Try to find any JSON-like structure
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('{') or line.startswith('['):
                result = safe_json_parse(line)
                if result is not None:
                    return result
    
    return None


def format_messages(messages: list[dict]) -> str:
    """
    Format a list of messages into a readable string.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        
    Returns:
        Formatted string representation
    """
    formatted = []
    for msg in messages:
        role = msg.get('role', 'unknown').upper()
        content = msg.get('content', '')
        formatted.append(f"[{role}]\n{content}\n")
    
    return "\n".join(formatted)