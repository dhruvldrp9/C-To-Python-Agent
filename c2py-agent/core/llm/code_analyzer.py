from typing import Dict, List, Optional, Set
import logging
from pycparser import c_ast
from .api_client import LLMClient

class CodeAnalyzer:
    """Analyzes C code structure and intent."""
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize the code analyzer.
        
        Args:
            llm_client: LLM client for code analysis
        """
        self.llm_client = llm_client
        self.logger = logging.getLogger(__name__)
        
    def analyze_function(self, func_def: c_ast.FuncDef) -> Dict:
        """
        Analyze a function definition.
        
        Args:
            func_def: Function definition AST node
            
        Returns:
            Analysis results as dictionary
        """
        try:
            # Extract function information
            name = func_def.decl.name
            return_type = self._get_type_string(func_def.decl.type)
            params = self._get_parameters(func_def.decl.type)
            
            # Get function body
            body = self._get_function_body(func_def)
            
            # Analyze using LLM
            analysis = self.llm_client.analyze_code(
                body,
                "function_analysis"
            )
            
            return {
                "name": name,
                "return_type": return_type,
                "parameters": params,
                "analysis": analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing function: {str(e)}")
            return {}
            
    def analyze_struct(self, struct: c_ast.Struct) -> Dict:
        """
        Analyze a struct definition.
        
        Args:
            struct: Struct definition AST node
            
        Returns:
            Analysis results as dictionary
        """
        try:
            # Extract struct information
            name = struct.name
            fields = self._get_struct_fields(struct)
            
            # Analyze using LLM
            analysis = self.llm_client.analyze_code(
                str(struct),
                "struct_analysis"
            )
            
            return {
                "name": name,
                "fields": fields,
                "analysis": analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing struct: {str(e)}")
            return {}
            
    def analyze_file(self, ast: c_ast.FileAST) -> Dict:
        """
        Analyze an entire file.
        
        Args:
            ast: File AST node
            
        Returns:
            Analysis results as dictionary
        """
        try:
            # Extract file information
            functions = []
            structs = []
            globals = []
            
            for node in ast:
                if isinstance(node, c_ast.FuncDef):
                    functions.append(self.analyze_function(node))
                elif isinstance(node, c_ast.Decl) and isinstance(node.type, c_ast.Struct):
                    structs.append(self.analyze_struct(node.type))
                elif isinstance(node, c_ast.Decl) and node.name:
                    globals.append(self._analyze_global(node))
                    
            # Analyze using LLM
            analysis = self.llm_client.analyze_code(
                str(ast),
                "file_analysis"
            )
            
            return {
                "functions": functions,
                "structs": structs,
                "globals": globals,
                "analysis": analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing file: {str(e)}")
            return {}
            
    def _get_type_string(self, type_node: c_ast.Node) -> str:
        """
        Convert a type AST node to a string.
        
        Args:
            type_node: Type AST node
            
        Returns:
            String representation of the type
        """
        if isinstance(type_node, c_ast.IdentifierType):
            return ' '.join(type_node.names)
        elif isinstance(type_node, c_ast.PtrDecl):
            return f"pointer to {self._get_type_string(type_node.type)}"
        elif isinstance(type_node, c_ast.ArrayDecl):
            return f"array of {self._get_type_string(type_node.type)}"
        elif isinstance(type_node, c_ast.Struct):
            return f"struct {type_node.name}" if type_node.name else "anonymous struct"
        elif isinstance(type_node, c_ast.Union):
            return f"union {type_node.name}" if type_node.name else "anonymous union"
        elif isinstance(type_node, c_ast.Enum):
            return f"enum {type_node.name}" if type_node.name else "anonymous enum"
        else:
            return str(type_node)
            
    def _get_parameters(self, type_node: c_ast.Node) -> List[Dict]:
        """
        Extract function parameters from a type node.
        
        Args:
            type_node: Function type AST node
            
        Returns:
            List of parameter dictionaries
        """
        params = []
        if isinstance(type_node, c_ast.FuncDecl):
            if type_node.args:
                for param in type_node.args.params:
                    if isinstance(param, c_ast.Decl):
                        params.append({
                            "name": param.name,
                            "type": self._get_type_string(param.type)
                        })
        return params
        
    def _get_struct_fields(self, struct: c_ast.Struct) -> List[Dict]:
        """
        Extract fields from a struct definition.
        
        Args:
            struct: Struct definition AST node
            
        Returns:
            List of field dictionaries
        """
        fields = []
        if struct.decls:
            for decl in struct.decls:
                if isinstance(decl, c_ast.Decl):
                    fields.append({
                        "name": decl.name,
                        "type": self._get_type_string(decl.type)
                    })
        return fields
        
    def _get_function_body(self, func_def: c_ast.FuncDef) -> str:
        """
        Get the function body as a string.
        
        Args:
            func_def: Function definition AST node
            
        Returns:
            Function body as string
        """
        return str(func_def.body)
        
    def _analyze_global(self, decl: c_ast.Decl) -> Dict:
        """
        Analyze a global variable declaration.
        
        Args:
            decl: Declaration AST node
            
        Returns:
            Analysis results as dictionary
        """
        return {
            "name": decl.name,
            "type": self._get_type_string(decl.type)
        } 