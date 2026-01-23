from Utils.PizzaEval.PizzaEvalErrorDict import error_dict


# error handling
class PizzaError(Exception):
    pass


def identify_error(error_code: int, expression: str) -> str:
    return f"Error code {str(error_code)}: {error_dict[error_code]} \nprocessing this expression: `{expression}`"


def logical_xor(a, b):
    return (a or b) and not (a and b)


# condition validator 3000
def remove_text_inside_gaensefuesschen(expression):  # for contains_a_check
    out = ""
    inside_gaensefuesschen = False
    for char in expression:
        if char == "'":
            out += char
            inside_gaensefuesschen = not inside_gaensefuesschen
            continue
        if not inside_gaensefuesschen:
            out += char
    return out


def is_parenthese_lvl_fine(condition):
    insideGaensefuesschen = False
    parantheseLvl = 0
    for char in condition:
        if char == "'":
            insideGaensefuesschen = not insideGaensefuesschen
        if insideGaensefuesschen:
            continue
        if char == "(":
            parantheseLvl += 1
        elif char == ")":
            parantheseLvl -= 1
    return parantheseLvl


def two_gaensefuesschen_in_a_row(condition):
    last_char_gaensefuesschen = False
    for char in condition:
        if char == "'":
            if not last_char_gaensefuesschen:
                last_char_gaensefuesschen = True
            else:
                return True
        else:
            last_char_gaensefuesschen = False
    return False


def bracket_open_close_in_a_row(condition):
    insideGaensefuesschen = False
    last_paranthese_open = False
    for char in condition:
        if char == "'":
            insideGaensefuesschen = not insideGaensefuesschen
        if insideGaensefuesschen:
            continue
        if char == "(":
            last_paranthese_open = True
        if char == ")" and last_paranthese_open:
            return True
        if not char == "(":
            last_paranthese_open = False


def is_valid_singel_expression(singel_expression):
    if all(check not in remove_text_inside_gaensefuesschen(singel_expression) for check in ['is ', 'in ', 'start ', 'end ']):
        raise PizzaError({'c': 101, 'e': singel_expression})
    if singel_expression.count("'") % 2:
        raise PizzaError({'c': 102, 'e': singel_expression})
    if any(check == singel_expression for check in ['is', 'in', 'start', 'end', 'is ', 'in ', 'start ', 'end ']):
        raise PizzaError({'c': 103, 'e': singel_expression})


def is_valid_condition(condition):
    if not condition:
        raise PizzaError({'c': 0, 'e': condition})
    if condition.count("'") % 2:
        raise PizzaError({'c': 1, 'e': condition})
    if condition[0] == "'":
        raise PizzaError({'c': 2, 'e': condition})
    if all(check not in condition for check in ['is ', 'in ', 'start ', 'end ']):
        raise PizzaError({'c': 3, 'e': condition})
    if is_parenthese_lvl_fine(condition) > 0:
        raise PizzaError({'c': 301, 'e': condition})
    if is_parenthese_lvl_fine(condition) < 0:
        raise PizzaError({'c': 302, 'e': condition})
    if bracket_open_close_in_a_row(condition):
        raise PizzaError({'c': 303, 'e': condition})
    if two_gaensefuesschen_in_a_row(condition):
        raise PizzaError({'c': 6, 'e': condition})
    return True

def is_valid_replace_statement(replace_statement: str):
    if not replace_statement.startswith("[replace\\") or not replace_statement.endswith("]"):
        raise PizzaError({'c': 1201, 'e': replace_statement})

    if replace_statement.count("'") % 2:
        raise PizzaError({'c': 1204, 'e': replace_statement})

    inquotes = False
    openbracketcount, closebracketcount = 0, 0
    bracket_level = 0
    backslashcount = 0
    checked_valid_stringb_block = False  # (for performance)
    for i in replace_statement:
        if i == "'":
            inquotes = not inquotes
        elif not inquotes:
            if i == "\\" and bracket_level == 1:
                backslashcount += 1
            if i == "[":
                openbracketcount += 1
                bracket_level += 1
            elif i == "]":
                closebracketcount += 1
                bracket_level -= 1
            if backslashcount == 2 and not checked_valid_stringb_block:  # valid block but not random
                stringb_to_check = replace_statement.split("\\")[2]
                if stringb_to_check.startswith("[") and not stringb_to_check.startswith("[random"):
                    raise PizzaError({'c': 1208, 'e': replace_statement})
                checked_valid_stringb_block = True

    if backslashcount != 2:
        raise PizzaError({'c': 1205, 'e': replace_statement})

    if openbracketcount != closebracketcount or bracket_level != 0:
        raise PizzaError({'c': 1202, 'e': replace_statement})

    return True

# try:
#     print(is_valid_replace_statement("[replace\\siis\\[message], richtiger [author], der um [time] fucking '[' sagt]"))
# except PizzaError as e:
#     details = e.args[0]
#     print(identify_error(details['c'], details['e']))
