import re
from difflib import SequenceMatcher

def preprocess_code(code):
    # Remove comments and unnecessary spaces
    code = re.sub(r'#.*', '', code)  # Remove Python style comments
    code = re.sub(r'//.*', '', code)  # Remove C/C++/Java style comments
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)  # Remove block comments
    # Remove extra spaces and newlines
    code = re.sub(r'\s+', ' ', code)
    return code.strip()

def detect_exact_match(original_code, test_code):
    original_cleaned = preprocess_code(original_code)
    test_cleaned = preprocess_code(test_code)
    
    return original_cleaned == test_cleaned

def tokenize_code(code):
    # A simple tokenizer that ignores variable names (identifiers)
    tokens = re.findall(r'[a-zA-Z_]\w*|[+\-*/=<>!&|]+|\d+|\(|\)|\{|\}|\[|\]|,|;', code)
    return tokens

def detect_variable_renaming(original_code, test_code):
    original_tokens = tokenize_code(original_code)
    test_tokens = tokenize_code(test_code)
    
    if len(original_tokens) != len(test_tokens):
        return False
    
    original_var_map = {}
    
    for o_token, t_token in zip(original_tokens, test_tokens):
        if re.match(r'[a-zA-Z_]\w*', o_token) and re.match(r'[a-zA-Z_]\w*', t_token):
            if o_token not in original_var_map:
                original_var_map[o_token] = t_token
            elif original_var_map[o_token] != t_token:
                return False
        elif o_token != t_token:
            return False
    return True

def abstract_structure(code):
    """
    Abstracts code to show structural elements like loops, conditionals, etc.
    - Normalize for-loops to a generic loop pattern.
    - Normalize while-loops that match the same iteration logic as for-loops.
    """
    # Normalize for loops with range
    code = re.sub(r'for\s+\w+\s+in\s+range\(\d+\):', 'LOOP', code)  # Abstract for loops
    
    # Normalize while loops doing similar iteration as for-loops
    # Example: i = 0; while i < 10; i += 1;
    code = re.sub(r'while\s+.*?\s*<\s*\d+:', 'LOOP', code)
    
    # Normalize conditionals
    code = re.sub(r'\bif\b', 'COND', code)
    code = re.sub(r'\belse\b', 'COND', code)
    
    # Remove any trivial differences
    code = re.sub(r'\s+', ' ', code).strip()  # Remove extra whitespace
    
    return code

def detect_structural_similarity(original_code, test_code):
    # Abstract both original and test code
    original_abstracted = abstract_structure(original_code)
    test_abstracted = abstract_structure(test_code)
    
    # Compare abstracted structures using SequenceMatcher
    similarity_ratio = SequenceMatcher(None, original_abstracted, test_abstracted).ratio()
    
    # Consider them structurally similar if similarity ratio is above a certain threshold
    return similarity_ratio > 0.6  # Lower threshold for flexibility

def plagiarism_detection(original_code, test_code):
    # Step 1: Check for exact match first
    exact_match = detect_exact_match(original_code, test_code)
    print(exact_match)
    # Step 2: Check for variable renaming if it's not an exact match
    variable_renaming = detect_variable_renaming(original_code, test_code) if not exact_match else False
    print(variable_renaming)
    # Step 3: Check for structural similarity
    structural_similarity = detect_structural_similarity(original_code, test_code)
    print(structural_similarity)
    # Return the boolean results directly
    return exact_match, variable_renaming, structural_similarity