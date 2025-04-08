from typing import Dict, List, Set, Optional
from pathlib import Path
import logging
from collections import defaultdict

class DependencyMapper:
    """Maps dependencies between files in a C project."""
    
    def __init__(self):
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.file_symbols: Dict[str, Set[str]] = defaultdict(set)
        self.symbol_files: Dict[str, Set[str]] = defaultdict(set)
        self.logger = logging.getLogger(__name__)
        
    def add_file_dependency(self, source_file: str, target_file: str) -> None:
        """
        Add a dependency between two files.
        
        Args:
            source_file: Path to the source file
            target_file: Path to the target file
        """
        source_file = str(Path(source_file).resolve())
        target_file = str(Path(target_file).resolve())
        
        if source_file != target_file:
            self.dependencies[source_file].add(target_file)
            self.reverse_dependencies[target_file].add(source_file)
            
    def add_symbol_definition(self, file_path: str, symbol_name: str) -> None:
        """
        Record that a symbol is defined in a file.
        
        Args:
            file_path: Path to the file containing the symbol definition
            symbol_name: Name of the defined symbol
        """
        file_path = str(Path(file_path).resolve())
        self.file_symbols[file_path].add(symbol_name)
        self.symbol_files[symbol_name].add(file_path)
        
    def add_symbol_reference(self, file_path: str, symbol_name: str) -> None:
        """
        Record that a symbol is referenced in a file.
        
        Args:
            file_path: Path to the file containing the symbol reference
            symbol_name: Name of the referenced symbol
        """
        file_path = str(Path(file_path).resolve())
        
        # Find files that define this symbol
        defining_files = self.symbol_files.get(symbol_name, set())
        
        # Add dependencies for each defining file
        for def_file in defining_files:
            self.add_file_dependency(file_path, def_file)
            
    def get_file_dependencies(self, file_path: str) -> Set[str]:
        """
        Get all files that a given file depends on.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Set of file paths that the given file depends on
        """
        file_path = str(Path(file_path).resolve())
        return self.dependencies.get(file_path, set())
        
    def get_file_dependents(self, file_path: str) -> Set[str]:
        """
        Get all files that depend on a given file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Set of file paths that depend on the given file
        """
        file_path = str(Path(file_path).resolve())
        return self.reverse_dependencies.get(file_path, set())
        
    def get_file_symbols(self, file_path: str) -> Set[str]:
        """
        Get all symbols defined in a given file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Set of symbol names defined in the file
        """
        file_path = str(Path(file_path).resolve())
        return self.file_symbols.get(file_path, set())
        
    def get_symbol_files(self, symbol_name: str) -> Set[str]:
        """
        Get all files that define a given symbol.
        
        Args:
            symbol_name: Name of the symbol
            
        Returns:
            Set of file paths that define the symbol
        """
        return self.symbol_files.get(symbol_name, set())
        
    def get_dependency_order(self) -> List[str]:
        """
        Get files in dependency order (least dependent first).
        
        Returns:
            List of file paths in dependency order
        """
        visited = set()
        temp_mark = set()
        order = []
        
        def visit(file_path: str) -> None:
            if file_path in temp_mark:
                self.logger.warning(f"Circular dependency detected involving {file_path}")
                return
            if file_path in visited:
                return
                
            temp_mark.add(file_path)
            
            for dep in self.dependencies.get(file_path, set()):
                visit(dep)
                
            temp_mark.remove(file_path)
            visited.add(file_path)
            order.append(file_path)
            
        for file_path in self.dependencies:
            if file_path not in visited:
                visit(file_path)
                
        return order
        
    def get_strongly_connected_components(self) -> List[Set[str]]:
        """
        Find strongly connected components in the dependency graph.
        
        Returns:
            List of sets of file paths, where each set represents a strongly connected component
        """
        visited = set()
        components = []
        
        def dfs(file_path: str, component: Set[str]) -> None:
            visited.add(file_path)
            component.add(file_path)
            
            for dep in self.dependencies.get(file_path, set()):
                if dep not in visited:
                    dfs(dep, component)
                    
        for file_path in self.dependencies:
            if file_path not in visited:
                component = set()
                dfs(file_path, component)
                components.append(component)
                
        return components 