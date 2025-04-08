import re
from typing import Dict, List, Optional, Set
import logging
from pathlib import Path

class CPreprocessor:
    """Handles C preprocessor directives and macro expansion."""
    
    def __init__(self):
        self.macros: Dict[str, str] = {}
        self.include_paths: List[str] = []
        self.processed_includes: Set[str] = set()
        self.logger = logging.getLogger(__name__)
        
    def add_include_path(self, path: str) -> None:
        """
        Add a directory to the include path search list.
        
        Args:
            path: Directory path to add
        """
        if path not in self.include_paths:
            self.include_paths.append(path)
            
    def define_macro(self, name: str, value: str) -> None:
        """
        Define a preprocessor macro.
        
        Args:
            name: Macro name
            value: Macro value
        """
        self.macros[name] = value
        
    def process_file(self, file_path: str) -> str:
        """
        Process a C source file, expanding macros and includes.
        
        Args:
            file_path: Path to the C source file
            
        Returns:
            Processed source code as string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            return self.process_source(source, file_path)
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            return source
            
    def process_source(self, source: str, current_file: str) -> str:
        """
        Process C source code, expanding macros and includes.
        
        Args:
            source: C source code as string
            current_file: Path to the current file being processed
            
        Returns:
            Processed source code as string
        """
        # Process includes
        source = self._process_includes(source, current_file)
        
        # Process macros
        source = self._expand_macros(source)
        
        # Process conditional compilation
        source = self._process_conditionals(source)
        
        return source
        
    def _process_includes(self, source: str, current_file: str) -> str:
        """
        Process #include directives.
        
        Args:
            source: C source code as string
            current_file: Path to the current file being processed
            
        Returns:
            Processed source code with includes expanded
        """
        include_pattern = r'#include\s*[<"]([^>"]+)[>"]'
        
        def replace_include(match):
            include_path = match.group(1)
            if include_path in self.processed_includes:
                return ""
                
            self.processed_includes.add(include_path)
            
            # Search for the include file
            for include_dir in self.include_paths:
                full_path = Path(include_dir) / include_path
                if full_path.exists():
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            included_content = f.read()
                        return self.process_source(included_content, str(full_path))
                    except Exception as e:
                        self.logger.warning(f"Error processing include {include_path}: {str(e)}")
                        
            self.logger.warning(f"Could not find include file: {include_path}")
            return match.group(0)
            
        return re.sub(include_pattern, replace_include, source)
        
    def _expand_macros(self, source: str) -> str:
        """
        Expand preprocessor macros.
        
        Args:
            source: C source code as string
            
        Returns:
            Source code with macros expanded
        """
        for macro_name, macro_value in self.macros.items():
            pattern = r'\b' + re.escape(macro_name) + r'\b'
            source = re.sub(pattern, macro_value, source)
        return source
        
    def _process_conditionals(self, source: str) -> str:
        """
        Process conditional compilation directives (#if, #ifdef, etc.).
        
        Args:
            source: C source code as string
            
        Returns:
            Processed source code with conditionals evaluated
        """
        # This is a simplified implementation. A full implementation would need to
        # properly evaluate conditions and handle nested conditionals.
        lines = source.split('\n')
        processed_lines = []
        skip_until_endif = False
        
        for line in lines:
            if skip_until_endif:
                if line.strip().startswith('#endif'):
                    skip_until_endif = False
                continue
                
            if line.strip().startswith(('#if', '#ifdef', '#ifndef')):
                # For now, we'll just skip conditional blocks
                skip_until_endif = True
                continue
                
            processed_lines.append(line)
            
        return '\n'.join(processed_lines)
        
    def reset(self) -> None:
        """Reset the preprocessor state."""
        self.macros.clear()
        self.include_paths.clear()
        self.processed_includes.clear() 