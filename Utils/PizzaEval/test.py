# all hail test.py
import re

def evaluate_expression_no_eval(expression):
    def simple_eval(expr):
        """Evaluates a simple arithmetic expression without parentheses."""
        tokens = re.split(r'(\D)', expr.replace(' ', ''))  # Split by operators
        tokens = [t for t in tokens if t]  # Remove empty tokens
        # Perform multiplication and division first
        while '*' in tokens or '/' in tokens:
            for i, token in enumerate(tokens):
                if token in '*/':
                    left = float(tokens[i - 1])
                    right = float(tokens[i + 1])
                    result = left * right if token == '*' else left / right
                    tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
                    break
        # Perform addition and subtraction
        while '+' in tokens or '-' in tokens:
            for i, token in enumerate(tokens):
                if token in '+-':
                    left = float(tokens[i - 1])
                    right = float(tokens[i + 1])
                    result = left + right if token == '+' else left - right
                    tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
                    break
        return tokens[0]

    # Regex pattern to find innermost parentheses
    pattern = r'\(([^()]+)\)'  # Matches content inside the deepest level of parentheses

    while '(' in expression:  # Continue while there are parentheses
        # Find and evaluate the innermost parenthetical expression
        match = re.search(pattern, expression)
        if match:
            inner_expr = match.group(1)  # Extract the innermost expression
            result = simple_eval(inner_expr)  # Evaluate the expression
            # Replace the evaluated expression back into the original string
            expression = expression[:match.start()] + result + expression[match.end():]
        else:
            break  # No more parentheses found

    # Final evaluation for the remaining expression without parentheses
    return float(simple_eval(expression))

# Example Usage
expression = "2 * (3 + (4 * (5 - 2)))"
result = evaluate_expression_no_eval(expression)
print(f"Result: {result}")
