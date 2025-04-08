import logging
from pathlib import Path
from typing import Optional, List, Dict

from ..core.parser import ASTGenerator, CPreprocessor, SymbolTable, DependencyMapper
from ..core.llm import LLMClient, PromptTemplates, CodeAnalyzer, TranslationRules

def interactive_mode(input_path: Path, output_path: Path, config_path: str) -> int:
    """
    Run the converter in interactive mode.
    
    Args:
        input_path: Path to input C source
        output_path: Path to output Python code
        config_path: Path to configuration file
        
    Returns:
        Exit code
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        preprocessor = CPreprocessor()
        ast_generator = ASTGenerator()
        symbol_table = SymbolTable()
        dependency_mapper = DependencyMapper()
        
        llm_client = LLMClient()
        prompt_templates = PromptTemplates()
        code_analyzer = CodeAnalyzer(llm_client)
        translation_rules = TranslationRules()
        
        # Get list of files to process
        files = get_files_to_process(input_path)
        if not files:
            logger.error("No files found to process")
            return 1
            
        # Process each file
        for file_path in files:
            process_file_interactive(
                file_path,
                output_path,
                preprocessor,
                ast_generator,
                symbol_table,
                dependency_mapper,
                llm_client,
                prompt_templates,
                code_analyzer,
                translation_rules
            )
            
        return 0
        
    except Exception as e:
        logger.error(f"Error in interactive mode: {str(e)}")
        return 1

def get_files_to_process(input_path: Path) -> List[Path]:
    """
    Get list of files to process.
    
    Args:
        input_path: Path to input source
        
    Returns:
        List of file paths to process
    """
    if input_path.is_file():
        return [input_path]
        
    # Get all C source files in directory
    return list(input_path.rglob("*.c"))

def process_file_interactive(
    file_path: Path,
    output_path: Path,
    preprocessor: CPreprocessor,
    ast_generator: ASTGenerator,
    symbol_table: SymbolTable,
    dependency_mapper: DependencyMapper,
    llm_client: LLMClient,
    prompt_templates: PromptTemplates,
    code_analyzer: CodeAnalyzer,
    translation_rules: TranslationRules
) -> None:
    """
    Process a single file in interactive mode.
    
    Args:
        file_path: Path to input file
        output_path: Path to output directory
        preprocessor: C preprocessor instance
        ast_generator: AST generator instance
        symbol_table: Symbol table instance
        dependency_mapper: Dependency mapper instance
        llm_client: LLM client instance
        prompt_templates: Prompt templates instance
        code_analyzer: Code analyzer instance
        translation_rules: Translation rules instance
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Processing file: {file_path}")
    
    try:
        # Preprocess the file
        logger.info("Preprocessing file...")
        processed_source = preprocessor.process_file(str(file_path))
        
        # Generate AST
        logger.info("Generating AST...")
        ast = ast_generator.parse_source(processed_source)
        if not ast:
            logger.error("Failed to generate AST")
            return
            
        # Analyze code
        logger.info("Analyzing code...")
        analysis = code_analyzer.analyze_file(ast)
        
        # Show analysis results
        print("\nCode Analysis Results:")
        print("=====================")
        print(f"Functions: {len(analysis.get('functions', []))}")
        print(f"Structs: {len(analysis.get('structs', []))}")
        print(f"Global variables: {len(analysis.get('globals', []))}")
        
        # Process each function
        for func in analysis.get('functions', []):
            process_function_interactive(
                func,
                output_path,
                llm_client,
                prompt_templates,
                translation_rules
            )
            
        # Process each struct
        for struct in analysis.get('structs', []):
            process_struct_interactive(
                struct,
                output_path,
                llm_client,
                prompt_templates,
                translation_rules
            )
            
        # Generate output file
        output_file = output_path / f"{file_path.stem}.py"
        generate_output_file(
            output_file,
            analysis,
            llm_client,
            prompt_templates,
            translation_rules
        )
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {str(e)}")

def process_function_interactive(
    func: Dict,
    output_path: Path,
    llm_client: LLMClient,
    prompt_templates: PromptTemplates,
    translation_rules: TranslationRules
) -> None:
    """
    Process a function in interactive mode.
    
    Args:
        func: Function analysis results
        output_path: Path to output directory
        llm_client: LLM client instance
        prompt_templates: Prompt templates instance
        translation_rules: Translation rules instance
    """
    print(f"\nProcessing function: {func['name']}")
    print("================================")
    
    # Show function details
    print(f"Return type: {func['return_type']}")
    print("Parameters:")
    for param in func['parameters']:
        print(f"  - {param['name']}: {param['type']}")
        
    # Get user input
    while True:
        choice = input("\nOptions:\n1. Translate function\n2. Skip function\n3. View analysis\n4. Exit\nChoice: ")
        
        if choice == "1":
            # Translate function
            template = prompt_templates.get_template(
                "code_translation",
                code=str(func),
                file_path=str(output_path),
                function_name=func['name'],
                dependencies=", ".join(p['name'] for p in func['parameters'])
            )
            
            translated_code = llm_client.generate_code(
                template['user'],
                template['system']
            )
            
            print("\nTranslated code:")
            print("===============")
            print(translated_code)
            
            save = input("\nSave translation? (y/n): ")
            if save.lower() == 'y':
                # TODO: Save translated code
                pass
                
            break
            
        elif choice == "2":
            print("Skipping function...")
            break
            
        elif choice == "3":
            print("\nAnalysis:")
            print("=========")
            print(func['analysis'])
            
        elif choice == "4":
            print("Exiting...")
            return
            
        else:
            print("Invalid choice. Please try again.")

def process_struct_interactive(
    struct: Dict,
    output_path: Path,
    llm_client: LLMClient,
    prompt_templates: PromptTemplates,
    translation_rules: TranslationRules
) -> None:
    """
    Process a struct in interactive mode.
    
    Args:
        struct: Struct analysis results
        output_path: Path to output directory
        llm_client: LLM client instance
        prompt_templates: Prompt templates instance
        translation_rules: Translation rules instance
    """
    print(f"\nProcessing struct: {struct['name']}")
    print("=============================")
    
    # Show struct details
    print("Fields:")
    for field in struct['fields']:
        print(f"  - {field['name']}: {field['type']}")
        
    # Get user input
    while True:
        choice = input("\nOptions:\n1. Translate struct\n2. Skip struct\n3. View analysis\n4. Exit\nChoice: ")
        
        if choice == "1":
            # Translate struct
            template = prompt_templates.get_template(
                "code_translation",
                code=str(struct),
                file_path=str(output_path),
                function_name=struct['name'],
                dependencies=", ".join(f['name'] for f in struct['fields'])
            )
            
            translated_code = llm_client.generate_code(
                template['user'],
                template['system']
            )
            
            print("\nTranslated code:")
            print("===============")
            print(translated_code)
            
            save = input("\nSave translation? (y/n): ")
            if save.lower() == 'y':
                # TODO: Save translated code
                pass
                
            break
            
        elif choice == "2":
            print("Skipping struct...")
            break
            
        elif choice == "3":
            print("\nAnalysis:")
            print("=========")
            print(struct['analysis'])
            
        elif choice == "4":
            print("Exiting...")
            return
            
        else:
            print("Invalid choice. Please try again.")

def generate_output_file(
    output_file: Path,
    analysis: Dict,
    llm_client: LLMClient,
    prompt_templates: PromptTemplates,
    translation_rules: TranslationRules
) -> None:
    """
    Generate the output Python file.
    
    Args:
        output_file: Path to output file
        analysis: Code analysis results
        llm_client: LLM client instance
        prompt_templates: Prompt templates instance
        translation_rules: Translation rules instance
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Generating output file: {output_file}")
    
    try:
        # Generate file content
        content = []
        
        # Add imports
        content.append("import typing")
        content.append("import datetime")
        content.append("import threading")
        content.append("import time")
        content.append("import random")
        content.append("import sys")
        content.append("")
        
        # Add translated code
        # TODO: Add translated functions and classes
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write('\n'.join(content))
            
        logger.info(f"Successfully generated output file: {output_file}")
        
    except Exception as e:
        logger.error(f"Error generating output file: {str(e)}") 