# C to Python Conversion Agent

A powerful tool for converting C code to Python, leveraging LLM capabilities for intelligent code translation.

## Features

- **Intelligent Code Translation**: Converts C code to Python while preserving functionality and following Python best practices
- **Interactive Mode**: Step-by-step conversion with user control
- **Comprehensive Analysis**: Analyzes code structure, dependencies, and potential issues
- **Customizable Rules**: Configurable translation rules for different C constructs
- **Modern Python Output**: Generates Python code with type hints, docstrings, and PEP 8 compliance
- **Dependency Management**: Handles C dependencies and converts them to Python equivalents
- **Error Handling**: Robust error handling and logging

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/c2py-agent.git
cd c2py-agent
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Basic Usage

Convert a single C file to Python:
```bash
python -m c2py-agent input.c output.py
```

Convert a directory of C files:
```bash
python -m c2py-agent input_dir/ output_dir/
```

### Interactive Mode

Run in interactive mode for step-by-step conversion:
```bash
python -m c2py-agent input.c output.py --interactive
```

### Configuration

The tool can be configured using a YAML file. Default configuration is in `config/default_config.yml`:

```yaml
parser:
  ignore_headers: ["vendor/*", "test/*"]
  preprocess_macros: true
  max_file_size: 10485760  # 10MB

llm:
  model: "gpt-4"
  temperature: 0.2
  max_tokens: 4096
  retry_attempts: 3
  timeout: 30

generator:
  use_type_hints: true
  style: "pep8"
  doc_style: "google"
  max_line_length: 88
  generate_tests: true

verification:
  max_iterations: 5
  run_tests: true
  strict_imports: true
  static_analysis: true

logging:
  level: "INFO"
  file: "c2py.log"
  max_size: 10485760  # 10MB
  backup_count: 5
```

Use a custom configuration file:
```bash
python -m c2py-agent input.c output.py --config my_config.yml
```

## Project Structure

```
c2py-agent/
├── config/
│   └── default_config.yml
├── core/
│   ├── parser/
│   │   ├── ast_generator.py
│   │   ├── c_preprocessor.py
│   │   ├── dependency_mapper.py
│   │   └── symbol_table.py
│   └── llm/
│       ├── api_client.py
│       ├── code_analyzer.py
│       ├── prompt_templates.py
│       └── translation_rules.py
├── cli/
│   ├── main.py
│   └── interactive.py
├── tests/
├── requirements.txt
└── README.md
```

## Development

### Setting Up Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

### Running Tests

```bash
pytest tests/
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- pylint for code analysis

Format code:
```bash
black .
isort .
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [pycparser](https://github.com/eliben/pycparser) for C parsing capabilities
- OpenAI for LLM capabilities
- All contributors and maintainers 