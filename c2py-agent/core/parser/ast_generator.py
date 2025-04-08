from pycparser import c_parser, c_ast
from typing import Dict, List, Optional, Union
import logging

class ASTGenerator:
    """Generates Abstract Syntax Trees from C source code."""
    
    def __init__(self):
        self.parser = c_parser.CParser()
        self.logger = logging.getLogger(__name__)
        
    def parse_file(self, file_path: str) -> Optional[c_ast.FileAST]:
        """
        Parse a C source file and return its AST.
        
        Args:
            file_path: Path to the C source file
            
        Returns:
            FileAST object if parsing successful, None otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            return self.parse_source(source)
        except Exception as e:
            self.logger.error(f"Error parsing file {file_path}: {str(e)}")
            return None
            
    def parse_source(self, source: str) -> Optional[c_ast.FileAST]:
        """
        Parse C source code string and return its AST.
        
        Args:
            source: C source code as string
            
        Returns:
            FileAST object if parsing successful, None otherwise
        """
        try:
            return self.parser.parse(source)
        except Exception as e:
            self.logger.error(f"Error parsing source: {str(e)}")
            return None
            
    def get_functions(self, ast: c_ast.FileAST) -> List[c_ast.FuncDef]:
        """
        Extract all function definitions from the AST.
        
        Args:
            ast: FileAST object
            
        Returns:
            List of function definition nodes
        """
        functions = []
        for node in ast:
            if isinstance(node, c_ast.FuncDef):
                functions.append(node)
        return functions
        
    def get_structs(self, ast: c_ast.FileAST) -> List[c_ast.Struct]:
        """
        Extract all struct definitions from the AST.
        
        Args:
            ast: FileAST object
            
        Returns:
            List of struct definition nodes
        """
        structs = []
        for node in ast:
            if isinstance(node, c_ast.Decl) and isinstance(node.type, c_ast.Struct):
                structs.append(node.type)
        return structs
        
    def get_typedefs(self, ast: c_ast.FileAST) -> List[c_ast.Typedef]:
        """
        Extract all typedef definitions from the AST.
        
        Args:
            ast: FileAST object
            
        Returns:
            List of typedef nodes
        """
        typedefs = []
        for node in ast:
            if isinstance(node, c_ast.Typedef):
                typedefs.append(node)
        return typedefs
        
    def get_includes(self, ast: c_ast.FileAST) -> List[str]:
        """
        Extract all include directives from the AST.
        
        Args:
            ast: FileAST object
            
        Returns:
            List of include paths
        """
        includes = []
        for node in ast:
            if isinstance(node, c_ast.Include):
                includes.append(node.filename)
        return includes 