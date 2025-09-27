"""Utility functions for loading and managing prompts"""

import yaml
import os
from typing import Dict, Any


class PromptManager:
    """Manages loading and formatting of prompts from YAML configuration"""
    
    def __init__(self, config_path: str = "config/prompts.yaml"):
        self.config_path = config_path
        self._prompts = None
        self.load_prompts()
    
    def load_prompts(self) -> Dict[str, Any]:
        """Load prompts from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self._prompts = yaml.safe_load(file)
            return self._prompts
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompts configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
    
    def get_prompt(self, *keys: str, **kwargs) -> str:
        """
        Get a prompt template and format it with provided kwargs
        
        Args:
            *keys: Nested keys to access the prompt (e.g., 'summarization', 'planner', 'template')
            **kwargs: Variables to format the prompt template with
            
        Returns:
            Formatted prompt string
            
        Example:
            prompt = manager.get_prompt('summarization', 'planner', 'template', 
                                     parsed_docs="Your document text here")
        """
        if not self._prompts:
            self.load_prompts()
        
        # Navigate through nested keys
        current = self._prompts
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                raise KeyError(f"Prompt key path not found: {' -> '.join(keys)}")
        
        if not isinstance(current, str):
            raise ValueError(f"Expected string template at {' -> '.join(keys)}, got {type(current)}")
        
        # Format the template with provided kwargs
        try:
            return current.format(**kwargs)
        except KeyError as e:
            raise KeyError(f"Missing required variable {e} for prompt template")
    
    def get_system_message(self, key: str) -> str:
        """Get a system message by key"""
        return self.get_prompt('system', key)
    
    def list_available_prompts(self) -> Dict[str, Any]:
        """Return the full prompt structure for inspection"""
        if not self._prompts:
            self.load_prompts()
        return self._prompts or {}


# Global instance for easy importing
prompt_manager = PromptManager()