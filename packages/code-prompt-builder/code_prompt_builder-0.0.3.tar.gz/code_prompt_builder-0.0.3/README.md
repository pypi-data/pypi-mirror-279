# code-prompt-builder

A lightweight Python library to construct plain-text code prompts from your code bases, designed for use with Large Language Models (LLMs) in code analysis and assistance tasks.

## Description

`code-prompt-builder` simplifies the process of feeding code to your LLM. It reads files from your project, optionally filtering by file types and directories, and structures them into a single string suitable for LLM input. 

This makes it easy to ask LLMs to analyze your code, identify potential issues, or even generate code suggestions.

## Installation

```bash
pip install code-prompt-builder
```

## Usage
Here's a simple example of using code-prompt-builder:

```python
from code_prompt_builder.utils import build_code_prompt

# Specify directories containing your code
repo_dir_paths = ["path/to/your/code/directory"] 

# Create the code prompt
code_prompt = build_code_prompt(repo_dir_paths=repo_dir_paths)

# Now you can use 'code_prompt' as input to your LLM
print(code_prompt)
```

## Function Parameters

- `repo_tree_paths`: A list of root directory paths to walk through and collect files.
- `repo_dir_paths`: A list of directories to read files from directly (no recursive walk).
- `repo_file_paths`: A list of specific files to include.
- `include_file_regex`: (Optional) A regular expression to include only matching files.
- `exclude_file_regex`: (Optional) A regular expression to exclude matching files.