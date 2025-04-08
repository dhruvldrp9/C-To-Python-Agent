import os
from typing import Dict, List, Optional, Union
import logging
from openai import OpenAI
from dotenv import load_dotenv

class LLMClient:
    """Client for interacting with language models."""
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.2, max_tokens: int = 4096):
        """
        Initialize the LLM client.
        
        Args:
            model: Name of the model to use
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
        """
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logger = logging.getLogger(__name__)
        
    def generate_code(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate code using the language model.
        
        Args:
            prompt: The prompt to send to the model
            system_prompt: Optional system prompt to set context
            
        Returns:
            Generated code as string
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error generating code: {str(e)}")
            return ""
            
    def analyze_code(self, code: str, analysis_type: str) -> Dict:
        """
        Analyze code using the language model.
        
        Args:
            code: Code to analyze
            analysis_type: Type of analysis to perform
            
        Returns:
            Analysis results as dictionary
        """
        prompt = f"Analyze the following code for {analysis_type}:\n\n{code}"
        try:
            response = self.generate_code(prompt)
            # Parse the response into a structured format
            # This is a simplified implementation
            return {"analysis": response}
        except Exception as e:
            self.logger.error(f"Error analyzing code: {str(e)}")
            return {"error": str(e)}
            
    def translate_code(self, code: str, source_lang: str, target_lang: str) -> str:
        """
        Translate code from one language to another.
        
        Args:
            code: Source code to translate
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            Translated code as string
        """
        prompt = f"Translate the following {source_lang} code to {target_lang}:\n\n{code}"
        try:
            return self.generate_code(prompt)
        except Exception as e:
            self.logger.error(f"Error translating code: {str(e)}")
            return ""
            
    def explain_code(self, code: str) -> str:
        """
        Generate an explanation of the code.
        
        Args:
            code: Code to explain
            
        Returns:
            Code explanation as string
        """
        prompt = f"Explain the following code in detail:\n\n{code}"
        try:
            return self.generate_code(prompt)
        except Exception as e:
            self.logger.error(f"Error explaining code: {str(e)}")
            return ""
            
    def suggest_improvements(self, code: str) -> List[str]:
        """
        Suggest improvements for the code.
        
        Args:
            code: Code to analyze
            
        Returns:
            List of improvement suggestions
        """
        prompt = f"Suggest improvements for the following code:\n\n{code}"
        try:
            response = self.generate_code(prompt)
            # Split the response into individual suggestions
            suggestions = [s.strip() for s in response.split('\n') if s.strip()]
            return suggestions
        except Exception as e:
            self.logger.error(f"Error suggesting improvements: {str(e)}")
            return []
            
    def generate_tests(self, code: str) -> str:
        """
        Generate test cases for the code.
        
        Args:
            code: Code to generate tests for
            
        Returns:
            Generated test code as string
        """
        prompt = f"Generate comprehensive test cases for the following code:\n\n{code}"
        try:
            return self.generate_code(prompt)
        except Exception as e:
            self.logger.error(f"Error generating tests: {str(e)}")
            return ""
            
    def fix_bugs(self, code: str, error_message: Optional[str] = None) -> str:
        """
        Fix bugs in the code.
        
        Args:
            code: Code with bugs
            error_message: Optional error message to help with debugging
            
        Returns:
            Fixed code as string
        """
        prompt = f"Fix the bugs in the following code"
        if error_message:
            prompt += f"\nError message: {error_message}"
        prompt += f"\n\n{code}"
        
        try:
            return self.generate_code(prompt)
        except Exception as e:
            self.logger.error(f"Error fixing bugs: {str(e)}")
            return "" 