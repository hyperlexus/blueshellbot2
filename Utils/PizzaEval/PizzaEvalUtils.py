import re
from Utils.PizzaEval.PizzaEvalErrorDict import error_dict


class OwnError(Exception):
    pass

def identify_error(error_code: int, expression: str) -> str:
    return f"Error code {str(error_code)}: {error_dict[error_code]}. \nprocessing this expression: `{expression}`"

def is_valid_complex_expression(complex_condition: str) -> bool:
    if complex_condition == "":
        raise OwnError({'c': 0, 'e': complex_condition})

    if complex_condition[0] == "'":
        raise OwnError({'c': 4, 'e': complex_condition})

    if all(i not in complex_condition for i in [' | ', ' ^ ', ' & ', '(', ')']):
        if not is_valid_simple_expression(complex_condition):
            raise OwnError({'c': 1, 'e': complex_condition})

    if all(i not in complex_condition for i in ['in ', 'is ', 'start ', 'end ']):
        raise OwnError({'c': 2, 'e': complex_condition})

    if bool_operators_in_quotes(complex_condition):
        raise OwnError({'c': 3, 'e': complex_condition})
    return True

def has_simple_keywords(read_string: str) -> int | bool:
    """Checks if string is allowed input for pizza type 'complex'"""
    return not all(i not in read_string for i in ['is ', 'in ', 'start ', 'end '])

def is_complex_expression(expression: str):
    return not all(i not in expression for i in [' | ', ' ^ ', ' & ', ' (', ') ', ' not '])

def is_valid_simple_expression(expression: str) -> bool:
    if not has_simple_keywords(expression):
        raise OwnError({'c': 101, 'e': expression})
    if '\'' in expression:
        if expression.count('\'') % 2:
            raise OwnError({'c': 102, 'e': expression})
        else:
            expr_array = expression.split("\'")
            if len(expr_array) > 3 or expr_array[2] != '':
                raise OwnError({'c': 105, 'e': expression})
            expr_array = expr_array[:-1]
            expression_type, expression_value = expr_array[0].strip(), expr_array[1].strip()
    else:
        if expression.count(' ') != 1:
            raise OwnError({'c': 103, 'e': expression})
        expression_type, text = expression.split(" ")
    if expression_type not in ['in', 'is', 'start', 'end']:
        raise OwnError({'c': 104, 'e': expression})
    return True

def is_valid_not_expression(expression: str) -> bool:
    pass

def valid_parentheses_amount(expression: str) -> bool:
    if '(' not in expression or ')' not in expression:
        raise OwnError({'c': 301, 'e': expression})

def bool_operators_in_quotes(expression: str) -> bool:
    return any(char in match for match in re.findall(r"'[^']*'", expression) for char in '|&^')

try:
    pass
except OwnError as e:
    details = e.args[0]
    print(identify_error(details['c'], details['e']))

# print(bool_operators_in_quotes("is a | is 'b  is c' | is 'd is e'"))