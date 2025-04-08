from typing import Dict, List, Optional
import json

class PromptTemplates:
    """Manages templates for LLM prompts."""
    
    def __init__(self):
        self.templates = {
            "code_translation": {
                "system": """You are an expert code translator specializing in converting C code to Python.
Your task is to translate C code while:
1. Preserving functionality
2. Following Python best practices
3. Using Pythonic idioms
4. Maintaining code readability
5. Adding appropriate type hints
6. Including docstrings
7. Handling C-specific features appropriately""",
                
                "user": """Translate the following C code to Python:

{code}

Additional context:
- File: {file_path}
- Function: {function_name}
- Dependencies: {dependencies}

Requirements:
1. Use Python type hints
2. Add Google-style docstrings
3. Follow PEP 8 style
4. Handle C-specific features appropriately
5. Maintain the same functionality"""
            },
            
            "code_analysis": {
                "system": """You are an expert code analyzer specializing in C code.
Your task is to analyze C code and provide insights about:
1. Code structure
2. Dependencies
3. Potential issues
4. Optimization opportunities
5. Security concerns""",
                
                "user": """Analyze the following C code:

{code}

Focus on:
1. Code structure and organization
2. Dependencies and relationships
3. Potential issues or bugs
4. Performance considerations
5. Security vulnerabilities
6. Best practices violations"""
            },
            
            "test_generation": {
                "system": """You are an expert test engineer specializing in Python.
Your task is to generate comprehensive test cases that:
1. Cover all functionality
2. Include edge cases
3. Test error conditions
4. Follow testing best practices
5. Use appropriate testing frameworks""",
                
                "user": """Generate test cases for the following Python code:

{code}

Requirements:
1. Use pytest framework
2. Include unit tests
3. Test edge cases
4. Test error conditions
5. Include setup and teardown if needed
6. Add appropriate assertions"""
            },
            
            "documentation": {
                "system": """You are an expert technical writer specializing in Python documentation.
Your task is to generate comprehensive documentation that:
1. Explains functionality clearly
2. Includes usage examples
3. Documents parameters and return values
4. Provides implementation details
5. Lists dependencies and requirements""",
                
                "user": """Generate documentation for the following Python code:

{code}

Requirements:
1. Use Google-style docstrings
2. Include usage examples
3. Document all parameters and return values
4. Explain complex logic
5. List dependencies
6. Include type information"""
            }
        }
        
    def get_template(self, template_name: str, **kwargs) -> Dict[str, str]:
        """
        Get a template with variables replaced.
        
        Args:
            template_name: Name of the template to get
            **kwargs: Variables to replace in the template
            
        Returns:
            Dictionary with 'system' and 'user' prompts
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
            
        template = self.templates[template_name]
        return {
            "system": template["system"],
            "user": template["user"].format(**kwargs)
        }
        
    def add_template(self, name: str, system: str, user: str) -> None:
        """
        Add a new template.
        
        Args:
            name: Name of the template
            system: System prompt template
            user: User prompt template
        """
        self.templates[name] = {
            "system": system,
            "user": user
        }
        
    def remove_template(self, name: str) -> None:
        """
        Remove a template.
        
        Args:
            name: Name of the template to remove
        """
        if name in self.templates:
            del self.templates[name]
            
    def list_templates(self) -> List[str]:
        """
        Get a list of available template names.
        
        Returns:
            List of template names
        """
        return list(self.templates.keys())
        
    def save_templates(self, file_path: str) -> None:
        """
        Save templates to a file.
        
        Args:
            file_path: Path to save templates to
        """
        with open(file_path, 'w') as f:
            json.dump(self.templates, f, indent=2)
            
    def load_templates(self, file_path: str) -> None:
        """
        Load templates from a file.
        
        Args:
            file_path: Path to load templates from
        """
        with open(file_path, 'r') as f:
            self.templates = json.load(f) 