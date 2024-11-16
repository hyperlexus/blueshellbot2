from Utils.PizzaEval.PizzaEvalUtils import identify_error, is_complex_expression, is_valid_simple_expression, \
    PizzaError, bool_operators_in_quotes, is_valid_complex_expression, valid_parentheses_amount


def split_by_brackets_1_layer():
    pass

def evaluate_simple_expression(simple_expression: str | bool, message_content: str):
    """handles ONLY bottom-level expressions, such as "start a" or "is 'c d'" """
    if isinstance(simple_expression, bool):
        return simple_expression

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
            next_layer_array[0] = evaluate_two_sides(next_layer_array[0], next_layer_array[1], message_content, operator)
            next_layer_array.pop(1)
        return next_layer_array[0]

def evaluate_not_expression(not_expression: str, bool_to_flip: bool):
    if not_expression.count(' ') != 1:
        raise PizzaError({'c': 401, 'e': not_expression})

def get_lowest_depth_expression(complex_condition: str) -> str | bool:
    expr_in_parenth_start = ""
    for char in complex_condition:
        if char == '(':
            expr_in_parenth_start = ""
        elif char == ')':
            return expr_in_parenth_start
        else:
            expr_in_parenth_start += char

def recursively_evaluate_parentheses(complex_condition: str, message_content: str) -> any:
    pass


def pizza_eval_read(complex_condition: str | bool, message_content: str) -> bool:
    if isinstance(complex_condition, bool):  # for recursion
        return complex_condition

    if not is_valid_complex_expression(complex_condition):
        print('man this fucking fella failed again', complex_condition, message_content)

    if all(i not in complex_condition for i in [' | ', ' ^ ', ' & ', '(', ')']):
        if is_valid_simple_expression(complex_condition):
            return evaluate_simple_expression(complex_condition, message_content)

    if '(' in complex_condition or ')' in complex_condition:
        if valid_parentheses_amount(complex_condition):
            return pizza_eval_read(get_lowest_depth_expression(complex_condition), message_content)

    for i in [' | ', ' ^ ', ' & ']:
        if i in complex_condition:
            return recursively_evaluate_two_sides_for_operator(complex_condition, message_content, i)

try:
    print(pizza_eval_read("in a & (in b | (in c))", "ac"))
except PizzaError as e:
    details = e.args[0]
    print(identify_error(details['c'], details['e']))

# try:
#     print(pizza_eval_read("(is a)", "a"))
# except PizzaError as e:
#     details = e.args[0]
#     print(identify_error(details['c'], details['e']))

# game plan: pass everything to eval_parenth if containing parentheses. function will then call itself if it has more parentheses, and will then work bottom to top to evaluate parentheses from inside out by calling pizza_eval_read
