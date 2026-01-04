"""
LocalLLM - A simple wrapper around llama-cpp-python.

This class provides a minimal interface to interact with local language models.
It intentionally has no magic:
- No retries (added in lesson 03)
- No tool calling (added in lesson 05)
- No memory (added in lesson 07)

Just text in, text out.
"""

from shared.llama_logging import disable_llama_logging
from llama_cpp import Llama

disable_llama_logging()

class LocalLLM:
    """
    A minimal wrapper for local LLM inference using llama.cpp.
    
    This class is intentionally simple and grows throughout the lessons.
    """
    
    def __init__(
        self,
        model_path: str,
        temperature: float = 0.2,
        max_tokens: int = 512,
        n_ctx: int = 2048
    ):
        """
        Initialize the local LLM.
        
        Args:
            model_path: Path to the GGUF model file
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum tokens to generate per response
            n_ctx: Context window size
        """
        self.llm = Llama(
            model_path=model_path,
            temperature=temperature,
            n_ctx=n_ctx,
            verbose=False,
        )
        self.max_tokens = max_tokens
    
    def generate(self, prompt: str, temperature: float = None, stop: list[str] = None) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: The input text prompt
            temperature: Optional temperature override
            stop: Optional list of stop sequences
            
        Returns:
            Generated text as a string
        """
        kwargs = {
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "stop": stop if stop is not None else ["</s>", "\n\n", "User:", "Assistant:"],
        }
        
        if temperature is not None:
            kwargs["temperature"] = temperature
        
        response = self.llm(**kwargs)
        return response["choices"][0]["text"].strip()