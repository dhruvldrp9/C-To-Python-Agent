import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from ..core.parser import ASTGenerator, CPreprocessor, SymbolTable, DependencyMapper
from ..core.llm import LLMClient, PromptTemplates, CodeAnalyzer, TranslationRules
from .interactive import interactive_mode

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level
        log_file: Optional log file path
    """
    level = getattr(logging, log_level.upper())
    handlers = [logging.StreamHandler()]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
        
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Convert C code to Python",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input",
        help="Input C source file or directory"
    )
    
    parser.add_argument(
        "output",
        help="Output Python file or directory"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file",
        default="config/default_config.yml"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level"
    )
    
    parser.add_argument(
        "--log-file",
        help="Log file path"
    )
    
    return parser.parse_args()

def main() -> int:
    """
    Main entry point for the CLI.
    
    Returns:
        Exit code
    """
    args = parse_args()
    setup_logging(args.log_level, args.log_file)
    logger = logging.getLogger(__name__)
    
    try:
        # Convert paths to absolute paths
        input_path = Path(args.input).resolve()
        output_path = Path(args.output).resolve()
        
        # Check if input exists
        if not input_path.exists():
            logger.error(f"Input path does not exist: {input_path}")
            return 1
            
        # Create output directory if it doesn't exist
        if output_path.is_dir():
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
        # Run in interactive mode if requested
        if args.interactive:
            return interactive_mode(input_path, output_path, args.config)
            
        # Initialize components
        preprocessor = CPreprocessor()
        ast_generator = ASTGenerator()
        symbol_table = SymbolTable()
        dependency_mapper = DependencyMapper()
        
        llm_client = LLMClient()
        prompt_templates = PromptTemplates()
        code_analyzer = CodeAnalyzer(llm_client)
        translation_rules = TranslationRules()
        
        # Process input
        if input_path.is_file():
            # Single file conversion
            logger.info(f"Converting file: {input_path}")
            # TODO: Implement file conversion
            pass
        else:
            # Directory conversion
            logger.info(f"Converting directory: {input_path}")
            # TODO: Implement directory conversion
            pass
            
        return 0
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 