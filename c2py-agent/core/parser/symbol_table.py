from typing import Dict, List, Optional, Set, Union
from pycparser import c_ast
import logging

class Symbol:
    """Represents a symbol in the C code (variable, function, type, etc.)"""
    
    def __init__(self, name: str, kind: str, type_info: str, scope: str):
        self.name = name
        self.kind = kind  # 'variable', 'function', 'type', 'struct'
        self.type_info = type_info
        self.scope = scope  # 'global', 'function', 'block'
        self.references: Set[str] = set()  # Files where this symbol is referenced
        
    def add_reference(self, file_path: str):
        """Add a file where this symbol is referenced."""
        self.references.add(file_path)

class SymbolTable:
    """Maintains a table of symbols found in the C code."""
    
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.logger = logging.getLogger(__name__)
        
    def add_symbol(self, symbol: Symbol) -> None:
        """
        Add a symbol to the table.
        
        Args:
            symbol: Symbol object to add
        """
        if symbol.name in self.symbols:
            self.logger.warning(f"Symbol {symbol.name} already exists in table")
            return
        self.symbols[symbol.name] = symbol
        
    def get_symbol(self, name: str) -> Optional[Symbol]:
        """
        Retrieve a symbol by name.
        
        Args:
            name: Name of the symbol to retrieve
            
        Returns:
            Symbol object if found, None otherwise
        """
        return self.symbols.get(name)
        
    def add_function(self, func_def: c_ast.FuncDef) -> None:
        """
        Add a function definition to the symbol table.
        
        Args:
            func_def: Function definition AST node
        """
        name = func_def.decl.name
        return_type = self._get_type_string(func_def.decl.type)
        symbol = Symbol(name, 'function', return_type, 'global')
        self.add_symbol(symbol)
        
    def add_variable(self, decl: c_ast.Decl, scope: str = 'global') -> None:
        """
        Add a variable declaration to the symbol table.
        
        Args:
            decl: Variable declaration AST node
            scope: Scope of the variable ('global', 'function', 'block')
        """
        name = decl.name
        type_info = self._get_type_string(decl.type)
        symbol = Symbol(name, 'variable', type_info, scope)
        self.add_symbol(symbol)
        
    def add_struct(self, struct: c_ast.Struct) -> None:
        """
        Add a struct definition to the symbol table.
        
        Args:
            struct: Struct definition AST node
        """
        if not struct.name:
            return
            
        name = struct.name
        fields = [f.name for f in struct.decls] if struct.decls else []
        type_info = f"struct with fields: {', '.join(fields)}"
        symbol = Symbol(name, 'struct', type_info, 'global')
        self.add_symbol(symbol)
        
    def _get_type_string(self, type_node: c_ast.Node) -> str:
        """
        Convert a type AST node to a string representation.
        
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
            
    def get_all_symbols(self) -> List[Symbol]:
        """
        Get all symbols in the table.
        
        Returns:
            List of all Symbol objects
        """
        return list(self.symbols.values())
        
    def get_symbols_by_kind(self, kind: str) -> List[Symbol]:
        """
        Get all symbols of a specific kind.
        
        Args:
            kind: Kind of symbols to retrieve ('variable', 'function', 'type', 'struct')
            
        Returns:
            List of Symbol objects of the specified kind
        """
        return [s for s in self.symbols.values() if s.kind == kind]
        
    def get_symbols_by_scope(self, scope: str) -> List[Symbol]:
        """
        Get all symbols in a specific scope.
        
        Args:
            scope: Scope to filter by ('global', 'function', 'block')
            
        Returns:
            List of Symbol objects in the specified scope
        """
        return [s for s in self.symbols.values() if s.scope == scope] 