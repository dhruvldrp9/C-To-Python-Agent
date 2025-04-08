from typing import Dict, List, Optional, Union
import json
import logging

class TranslationRules:
    """Manages rules for translating C code to Python."""
    
    def __init__(self):
        self.rules = {
            "types": {
                "int": "int",
                "char": "str",
                "float": "float",
                "double": "float",
                "void": "None",
                "bool": "bool",
                "long": "int",
                "short": "int",
                "unsigned int": "int",
                "unsigned char": "str",
                "unsigned long": "int",
                "unsigned short": "int",
                "size_t": "int",
                "FILE*": "TextIO",
                "FILE": "TextIO",
                "time_t": "float",
                "struct tm": "datetime.datetime",
                "pthread_t": "threading.Thread",
                "pthread_mutex_t": "threading.Lock",
                "pthread_cond_t": "threading.Condition",
                "pthread_attr_t": "threading.Thread",
                "pthread_mutexattr_t": "threading.Lock",
                "pthread_condattr_t": "threading.Condition"
            },
            
            "functions": {
                "malloc": "None",  # Will be handled specially
                "free": "None",    # Will be handled specially
                "printf": "print",
                "scanf": "input",
                "fprintf": "print",
                "fscanf": "input",
                "sprintf": "str.format",
                "sscanf": "str.split",
                "strcpy": "str.copy",
                "strcat": "str.__add__",
                "strcmp": "str.__eq__",
                "strlen": "len",
                "memset": "list.__init__",
                "memcpy": "list.__copy__",
                "memcmp": "list.__eq__",
                "atoi": "int",
                "atof": "float",
                "atol": "int",
                "rand": "random.randint",
                "srand": "random.seed",
                "time": "time.time",
                "sleep": "time.sleep",
                "exit": "sys.exit",
                "abort": "sys.exit",
                "assert": "assert",
                "isalpha": "str.isalpha",
                "isdigit": "str.isdigit",
                "isalnum": "str.isalnum",
                "islower": "str.islower",
                "isupper": "str.isupper",
                "tolower": "str.lower",
                "toupper": "str.upper"
            },
            
            "macros": {
                "NULL": "None",
                "TRUE": "True",
                "FALSE": "False",
                "EOF": "-1",
                "BUFSIZ": "8192",
                "EXIT_SUCCESS": "0",
                "EXIT_FAILURE": "1"
            },
            
            "patterns": {
                "pointer_declaration": {
                    "c": r"(\w+)\s*\*\s*(\w+)\s*=\s*(.*);",
                    "python": "{type} {name} = {value}"
                },
                "array_declaration": {
                    "c": r"(\w+)\s+(\w+)\s*\[(\d+)\]\s*=\s*{(.*)};",
                    "python": "{name} = [{values}]"
                },
                "struct_declaration": {
                    "c": r"struct\s+(\w+)\s*{([^}]*)};",
                    "python": "class {name}:\n    def __init__(self{params}):\n        {assignments}"
                },
                "function_definition": {
                    "c": r"(\w+)\s+(\w+)\s*\((.*)\)\s*{([^}]*)}",
                    "python": "def {name}({params}) -> {return_type}:\n    {body}"
                }
            }
        }
        self.logger = logging.getLogger(__name__)
        
    def get_type_mapping(self, c_type: str) -> str:
        """
        Get Python type for a C type.
        
        Args:
            c_type: C type name
            
        Returns:
            Corresponding Python type name
        """
        return self.rules["types"].get(c_type, "Any")
        
    def get_function_mapping(self, c_func: str) -> str:
        """
        Get Python function for a C function.
        
        Args:
            c_func: C function name
            
        Returns:
            Corresponding Python function name
        """
        return self.rules["functions"].get(c_func, c_func)
        
    def get_macro_mapping(self, macro: str) -> str:
        """
        Get Python value for a C macro.
        
        Args:
            macro: C macro name
            
        Returns:
            Corresponding Python value
        """
        return self.rules["macros"].get(macro, macro)
        
    def get_pattern_mapping(self, pattern_type: str) -> Dict[str, str]:
        """
        Get pattern mapping for a specific type.
        
        Args:
            pattern_type: Type of pattern to get
            
        Returns:
            Dictionary with C and Python patterns
        """
        return self.rules["patterns"].get(pattern_type, {})
        
    def add_type_mapping(self, c_type: str, python_type: str) -> None:
        """
        Add a new type mapping.
        
        Args:
            c_type: C type name
            python_type: Python type name
        """
        self.rules["types"][c_type] = python_type
        
    def add_function_mapping(self, c_func: str, python_func: str) -> None:
        """
        Add a new function mapping.
        
        Args:
            c_func: C function name
            python_func: Python function name
        """
        self.rules["functions"][c_func] = python_func
        
    def add_macro_mapping(self, macro: str, value: str) -> None:
        """
        Add a new macro mapping.
        
        Args:
            macro: C macro name
            value: Python value
        """
        self.rules["macros"][macro] = value
        
    def add_pattern_mapping(self, pattern_type: str, c_pattern: str, python_pattern: str) -> None:
        """
        Add a new pattern mapping.
        
        Args:
            pattern_type: Type of pattern
            c_pattern: C pattern
            python_pattern: Python pattern
        """
        self.rules["patterns"][pattern_type] = {
            "c": c_pattern,
            "python": python_pattern
        }
        
    def save_rules(self, file_path: str) -> None:
        """
        Save rules to a file.
        
        Args:
            file_path: Path to save rules to
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(self.rules, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving rules: {str(e)}")
            
    def load_rules(self, file_path: str) -> None:
        """
        Load rules from a file.
        
        Args:
            file_path: Path to load rules from
        """
        try:
            with open(file_path, 'r') as f:
                self.rules = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading rules: {str(e)}")
            
    def get_all_mappings(self) -> Dict[str, Dict[str, str]]:
        """
        Get all mappings.
        
        Returns:
            Dictionary containing all mappings
        """
        return self.rules 