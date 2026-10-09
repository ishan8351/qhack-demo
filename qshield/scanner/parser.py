import re
from typing import List, Tuple

def strip_comments_python(content: str) -> List[Tuple[int, str]]:
    """
    Strips single line comments (#) and docstrings (''' or \"\"\") from Python code.
    Returns list of (1-indexed line_number, active_code_line).
    """
    lines = content.splitlines()
    active_lines = []
    in_multiline = False
    delimiter = None

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Check multiline docstrings
        if not in_multiline:
            if stripped.startswith('"""'):
                if stripped.count('"""') >= 2 and len(stripped) > 3:
                    # Single line triple-quoted string
                    continue
                in_multiline = True
                delimiter = '"""'
                continue
            elif stripped.startswith("'''"):
                if stripped.count("'''") >= 2 and len(stripped) > 3:
                    continue
                in_multiline = True
                delimiter = "'''"
                continue
            
            # Remove inline comments if not inside string
            code_part = re.sub(r'#.*$', '', line)
            if code_part.strip():
                active_lines.append((i, code_part))
        else:
            if delimiter in line:
                in_multiline = False
                delimiter = None
            continue

    return active_lines

def strip_comments_c_style(content: str) -> List[Tuple[int, str]]:
    """
    Strips // and /* */ comments from Java, Go, and JS.
    Returns list of (1-indexed line_number, active_code_line).
    """
    lines = content.splitlines()
    active_lines = []
    in_block = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        if not in_block:
            if stripped.startswith("/*"):
                if "*/" in stripped:
                    # Inline block comment
                    remainder = stripped.split("*/", 1)[1]
                    if remainder.strip():
                        active_lines.append((i, remainder))
                    continue
                in_block = True
                continue
            elif stripped.startswith("//") or stripped.startswith("*"):
                continue
            
            # Remove inline // comments
            code_part = re.sub(r'//.*$', '', line)
            # Remove inline /* ... */ comments
            code_part = re.sub(r'/\*.*?\*/', '', code_part)
            if code_part.strip():
                active_lines.append((i, code_part))
        else:
            if "*/" in line:
                in_block = False
                remainder = line.split("*/", 1)[1]
                if remainder.strip():
                    active_lines.append((i, remainder))
            continue

    return active_lines

def strip_comments_config(content: str) -> List[Tuple[int, str]]:
    """
    Strips # comments from configuration files (ssh_config, nginx.conf).
    """
    lines = content.splitlines()
    active_lines = []
    for i, line in enumerate(lines, 1):
        code_part = re.sub(r'#.*$', '', line)
        if code_part.strip():
            active_lines.append((i, code_part))
    return active_lines
