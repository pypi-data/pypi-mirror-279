import os

def read_function_from_file(file_path, function_name):
    """
        Extract Function (function_name) from file_path
    """
    start_copying = False
    function_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith(f"def {function_name}("):
                start_copying = True
            if start_copying:
                function_lines.append(line)
            if start_copying and line.strip().startswith("def "):
                break  # Assumes no nested functions and that functions are sequentially defined
    return function_lines[:-1]  # Exclude the starting line of the next function


def extract_function(file_path, function_name):
    """
    Extracts a function from a file using simple string matching and indentation levels.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    function_lines = []
    copy = False
    indent_level = None
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(f"def {function_name}("):
            copy = True
            indent_level = len(line) - len(stripped_line)
        elif copy and (len(line) - len(stripped_line)) <= indent_level and stripped_line:
            if stripped_line.startswith("def "):
                break  # Stop if another function definition is encountered at the same or higher indent level
            copy = False  # Stop if any non-blank line is encountered at the same or higher indent level

        if copy:
            function_lines.append(line)

    return function_lines


def update_or_append_function(target_file, function_lines, function_name):
    if not os.path.exists(target_file):
        with open(target_file, 'w') as file:
            pass  # Create the file by opening it in write mode and then closing it.

    with open(target_file, 'r') as file:
        original_lines = file.readlines()

    updated_lines = []
    function_exists = False
    in_function = False
    function_start_index = None

    # Process original lines to determine if the function exists and its location
    for i, line in enumerate(original_lines):
        if line.strip().startswith(f"def {function_name}("):
            function_exists = True
            function_start_index = i
            in_function = True
        elif in_function and line.startswith('def '):
            in_function = False  # Assuming no nested functions for simplicity
        if not in_function:
            updated_lines.append(line)

    # Handling newlines before function
    if function_exists and function_start_index is not None:
        # Remove original function and ensure two newlines before the updated function
        del updated_lines[function_start_index - len(function_lines) - 1:function_start_index]
        if function_start_index - 2 > 0 and not original_lines[function_start_index - 2].strip():
            updated_lines.insert(function_start_index - len(function_lines) - 1, '\n')
        else:
            updated_lines.insert(function_start_index - len(function_lines) - 1, '\n\n')
    else:
        # If appending, ensure two newlines before the function if it's not the very first element
        if updated_lines and updated_lines[-1].strip():
            updated_lines.append('\n\n')
        elif updated_lines and not updated_lines[-1].strip() and (len(updated_lines) < 2 or updated_lines[-2].strip()):
            updated_lines.append('\n')

    # Add or update the function with correct spacing
    updated_lines.extend(function_lines)

    # Ensure exactly two newlines at the end of the function
    if not function_lines[-1].endswith('\n\n'):
        updated_lines.append('\n')

    with open(target_file, 'w') as file:
        file.writelines(updated_lines)
