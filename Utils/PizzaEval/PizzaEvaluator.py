from Utils.PizzaEval.PizzaEvalUtils import identify_error, is_valid_simple_expression, PizzaError, \
    is_valid_complex_expression, valid_parentheses_amount, is_valid_not_expression, is_always_true_or_false
from Utils.PizzaEval import PizzaEvalErrorDict

def split_by_brackets_1_layer():
    pass

def evaluate_simple_expression(simple_expression: str | bool, message_content: str):
    """handles ONLY bottom-level expressions, such as "start a" or "is 'c d'" """
    if isinstance(simple_expression, bool):
        return simple_expression

    if simple_expression.strip() in ("True", "False"):
        return eval(simple_expression.strip())

    if '\'' in simple_expression:
        expr_array = simple_expression.split("\'")
        expr_array = expr_array[:-1]
        expression_type, expression_value = expr_array[0].strip(), expr_array[1].strip()
    else:
        expression_type, expression_value = simple_expression.split(" ")

    if expression_type == 'in':
        return expression_value in message_content
    elif expression_type == 'is':
        return expression_value == message_content
    elif expression_type == 'start':
        return message_content.startswith(expression_value)
    elif expression_type == 'end':
        return message_content.endswith(expression_value)
    else:
        return False

def evaluate_two_sides(left_expression: str | bool, right_expression: str | bool, message_content: str, operator: str) -> bool:
    left_side = pizza_eval_read(left_expression, message_content)
    right_side = pizza_eval_read(right_expression, message_content)
    if not isinstance(left_side, bool) or not isinstance(right_side, bool):
        raise PizzaError({'c': 201, 'e': left_expression + operator + right_expression + " (inside evaluate_two_sides)"})
    match operator:
        case ' | ':
            return left_side or right_side
        case ' & ':
            return left_side and right_side
        case ' ^ ':
            return left_side ^ right_side
        case _:
            raise PizzaError({'c': 202, 'e': left_expression + right_expression})

def recursively_evaluate_two_sides_for_operator(complex_condition: str, message_content: str, operator: str) -> bool:
    next_layer_array = complex_condition.split(operator)
    amount_operations = len(next_layer_array)
    if amount_operations == 2:
        return evaluate_two_sides(next_layer_array[0], next_layer_array[1], message_content, operator)
    elif amount_operations < 2:
        raise PizzaError({'c': 203, 'e': complex_condition})
    else:
        for i in range(len(next_layer_array) - 1):
            if 'not' in next_layer_array[i]:
                next_layer_array[i] = evaluate_not_expression(next_layer_array[i])
        for i in range(len(next_layer_array) - 1):
            next_layer_array[0] = evaluate_two_sides(next_layer_array[0], next_layer_array[1], message_content, operator)
            next_layer_array.pop(1)
        return next_layer_array[0]

def evaluate_not_expression(not_string: str):  # not_string is literally just "not True" or "not False"
    return not eval(not_string[4:])

def get_lowest_depth_expression(complex_condition: str) -> str | bool:
    stack = []

    for index, char in enumerate(complex_condition):
        if char == '(':
            stack.append(index)
        elif char == ')':
            if stack:
                start_index = stack.pop()  # Get the matching '('
                return complex_condition[start_index + 1:index]  # Return contents inside parentheses
    raise PizzaError({'c': 303, 'e': complex_condition})


def pizza_eval_read(complex_condition: str | bool, message_content: str) -> bool:
    PizzaEvalErrorDict.recursion_counter += 1

    if isinstance(complex_condition, bool):  # for recursion
        return complex_condition

    if PizzaEvalErrorDict.recursion_counter == 1 and is_always_true_or_false(complex_condition):
        PizzaError({'c': 8, 'e': complex_condition})

    if not is_valid_complex_expression(complex_condition):
        raise PizzaError({'c': -1, 'e': complex_condition})

    if all(i not in complex_condition for i in [' | ', ' ^ ', ' & ', '(', ')', 'not']):
        if is_valid_simple_expression(complex_condition):
            return evaluate_simple_expression(complex_condition, message_content)

    if '(' in complex_condition or ')' in complex_condition:
        if valid_parentheses_amount(complex_condition):
            while '(' in complex_condition and ')' in complex_condition:
                lowest_depth_expression = get_lowest_depth_expression(complex_condition)
                inner_result = pizza_eval_read(lowest_depth_expression, message_content)
                complex_condition = complex_condition.replace(f"({lowest_depth_expression})", str(inner_result))

    if 'not True' in complex_condition or 'not False' in complex_condition:
        if is_valid_not_expression(complex_condition):
            return evaluate_not_expression(complex_condition)

    for i in [' | ', ' ^ ', ' & ']:
        if i in complex_condition:
            return recursively_evaluate_two_sides_for_operator(complex_condition, message_content, i)

    raise PizzaError({'c': -2, 'e': complex_condition + str(PizzaEvalErrorDict.recursion_counter)})

try:
    print(pizza_eval_read("is 🙂", "a"))
except PizzaError as e:
    details = e.args[0]
    print(identify_error(details['c'], details['e']))
