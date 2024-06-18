import os
import re
import nbformat
import logging

# Set up basic default logger with formatting
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_text_from_ipynb(notebook_file):
    nb = nbformat.read(notebook_file, as_version=4)
    extracted_text = ""
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            extracted_text += "```python\n" + cell['source'] + "\n```\n\n"
        elif cell['cell_type'] == 'markdown':
            extracted_text += "```ipynb\n" + cell['source'] + "\n```\n\n"
    return extracted_text


def include_exclude_check(file_name, include_file_regex=None, exclude_file_regex=None):
    """Returns True if the file should be included and False if it should be excluded."""
    includes = include_file_regex is None or re.search(include_file_regex, file_name) is not None
    excludes = exclude_file_regex is None or re.search(exclude_file_regex, file_name) is None
    return includes and excludes


def walk_and_match_files(start_path, include_file_regex=None, exclude_file_regex=None):
    """Walk through directories starting from start_path and collect files that match include_file_regex and don't match exclude_file_regex."""
    matched_files = []
    for root, _, files in os.walk(start_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if include_exclude_check(file_path, include_file_regex, exclude_file_regex):
                matched_files.append(file_path)
    return matched_files


def list_and_match_files(dir_path, include_file_regex=None, exclude_file_regex=None):
    """List files in dir_path and collect files that match include_file_regex and don't match exclude_file_regex."""
    matched_files = []
    for file_name in os.listdir(dir_path):
        if include_exclude_check(file_name, include_file_regex, exclude_file_regex):
            matched_files.append(os.path.join(dir_path, file_name))
    return matched_files


def read_files(file_paths):
    """Read the contents of the files."""
    file_contents = {}
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.endswith('.ipynb'):
                    file_contents[file_path] = extract_text_from_ipynb(file_path)
                else:
                    file_contents[file_path] = f.read()
        except UnicodeDecodeError:
            logging.error(f"Failed to decode file: {file_path}")
    return file_contents


def format_for_analysis(file_contents):
    """Format the contents for model prompting."""
    formatted_string = ""
    for file_path, content in file_contents.items():
        formatted_string += f"<file path={file_path}>\n{content}\n</file>\n\n"
    return formatted_string


def build_code_prompt(repo_tree_paths=None, repo_dir_paths=None, repo_file_paths=None, include_file_regex=None, exclude_file_regex=None):
    """Build a large string containing all the text in the repo files."""
    all_file_paths = []
    if repo_tree_paths is not None:
        for start_path in repo_tree_paths:
            all_file_paths.extend(walk_and_match_files(start_path, include_file_regex, exclude_file_regex))

    if repo_dir_paths is not None:
        for dir_path in repo_dir_paths:
            all_file_paths.extend(list_and_match_files(dir_path, include_file_regex, exclude_file_regex))

    if repo_file_paths is not None:
        all_file_paths.extend(repo_file_paths)
    all_file_contents = read_files(all_file_paths)
    formatted_code = format_for_analysis(all_file_contents)
    return formatted_code
