import re

from Utils.PizzaEval import PizzaEvalErrorDict
from Utils.PizzaEval.PizzaEvalErrorDict import error_dict

class PizzaError(Exception):
    pass

def identify_error(error_code: int, expression: str) -> str:
    return f"Error code {str(error_code)}: {error_dict[error_code]} \nprocessing this expression: `{expression}`"

def bool_operators_in_quotes(expression: str) -> bool:
    return any(char in match for match in re.findall(r"'[^']*'", expression) for char in '|&^()')

def is_always_true_or_false(complex_condition: str) -> bool:
    if complex_condition.strip() in ("True", "False"):
        raise PizzaError({'c': 5, 'e': complex_condition})

    if complex_condition.strip() in ("not True", "not False") and PizzaEvalErrorDict.recursion_counter == 1:
        raise PizzaError({'c': 6, 'e': complex_condition})

    if 'True' in complex_condition or 'False' in complex_condition:
        raise PizzaError({'c': 7, 'e': complex_condition})

    return False

def is_valid_complex_expression(complex_condition: str) -> bool:
    if complex_condition in ("True", "False"):
        return True

    if complex_condition == "":
        raise PizzaError({'c': 0, 'e': complex_condition})

    if complex_condition[0] == "'":
        raise PizzaError({'c': 1, 'e': complex_condition})

    if all(i not in complex_condition for i in [' | ', ' ^ ', ' & ', '(', ')', 'not ']):
        if not is_valid_simple_expression(complex_condition):
            raise PizzaError({'c': 2, 'e': complex_condition})

    if all(i not in complex_condition for i in ['in ', 'is ', 'start ', 'end ', 'not ']):
        raise PizzaError({'c': 3, 'e': complex_condition})

    if bool_operators_in_quotes(complex_condition):
        raise PizzaError({'c': 4, 'e': complex_condition})

    if 'not(' in complex_condition:
        raise PizzaError({'c': 405, 'e': complex_condition})

    if 'not' in complex_condition and not any(i in complex_condition for i in ['not (', 'not T', 'not F']):
        raise PizzaError({'c': 406, 'e': complex_condition})

    return True

def has_simple_keywords(read_string: str) -> int | bool:
    """Checks if string is allowed input for pizza type 'complex'"""
    return not all(i not in read_string for i in ['is ', 'in ', 'start ', 'end '])

def is_only_simple_keyword(read_string: str) -> bool:
    return any(i == read_string for i in ['is', 'in', 'start', 'end'])

def is_complex_expression(expression: str):
    return not all(i not in expression for i in [' | ', ' ^ ', ' & ', ' (', ') ', ' not '])

def is_valid_simple_expression(expression: str) -> bool:
    if expression in ("True", "False"):
        return True
    if is_only_simple_keyword(expression):
        raise PizzaError({'c': 106, 'e': expression})
    if not has_simple_keywords(expression):
        raise PizzaError({'c': 101, 'e': expression})
    if '\'' in expression:
        if expression.count('\'') % 2:
            raise PizzaError({'c': 102, 'e': expression})
        else:
            expr_array = expression.split("\'")
            if len(expr_array) > 3 or expr_array[2] != '':
                raise PizzaError({'c': 105, 'e': expression})
            expr_array = expr_array[:-1]
            expression_type, expression_value = expr_array[0].strip(), expr_array[1].strip()
    else:
        if expression.count(' ') != 1:
            raise PizzaError({'c': 103, 'e': expression})
        expression_type, text = expression.split(" ")
    if expression_type not in ['in', 'is', 'start', 'end']:
        raise PizzaError({'c': 104, 'e': expression})
    return True

def is_valid_not_expression(expression: str) -> bool:  # expression should be "not True" or "not False" only
    if is_complex_expression(expression) and 'not' in expression:
        return False
    if "True" not in expression and "False" not in expression:
        raise PizzaError({'c': 402, 'e': expression})
    if "not" not in expression:
        raise PizzaError({'c': 404, 'e': expression})
    if expression.count(" ") != 1:
        raise PizzaError({'c': 401, 'e': expression})
    if expression not in ("not True", "not False"):
        print(expression)
        raise PizzaError({'c': 403, 'e': expression})
    return True

def valid_parentheses_amount(expression: str) -> bool:
    if '(' not in expression or ')' not in expression:
        raise PizzaError({'c': 301, 'e': expression})
    if expression.count('(') != expression.count(')'):
        raise PizzaError({'c': 302, 'e': expression})
    if '(True)' in expression or '(False)' in expression:
        raise PizzaError({'c': 304, 'e': expression})
    return True


