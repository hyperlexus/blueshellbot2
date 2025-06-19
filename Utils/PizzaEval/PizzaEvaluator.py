from Utils.PizzaEval import PizzaEvalErrorDict
from Utils.PizzaEval.PizzaEvalUtils import is_valid_condition, PizzaError, logical_xor


def condition_to_blocks(condition):
    sub_blocks = []
    parenthesesLvl = 0  # paranthese.
    isInsideQuotes = False
    lastBlockStartIdx = 0
    for searchedOperator in ["|", "^", "&"]:
        for i in range(len(condition)):
            if condition[i] == "'":
                isInsideQuotes = not isInsideQuotes
            elif not isInsideQuotes:
                if condition[i] == "(":
                    parenthesesLvl += 1
                elif condition[i] == ")":
                    parenthesesLvl -= 1
                elif condition[i] == searchedOperator and parenthesesLvl == 0:
                    blankBefore = i > 0 and condition[i-1] == " "
                    blankAfter = i < len(condition) - 1 and condition[i+1] == " "
                    if i - lastBlockStartIdx > 0:
                        sub_blocks.append(condition[lastBlockStartIdx:i - (1 if blankBefore else 0)])
                    sub_blocks.append(condition[i])
                    sub_blocks.append(condition[i + (2 if blankAfter else 1):])
                    return sub_blocks
    if len(sub_blocks) == 0:
        if condition.startswith("(") and condition.endswith(")"):
            return condition_to_blocks(condition[1:-1])
        sub_blocks.append(condition)
    return sub_blocks


def remove_quotes(string):
    string.strip()
    if string.startswith("'") and string.endswith("'"):
        return string[1:-1]
    elif " " in string:
        raise PizzaError({'c': 5, 'e': string})
    return string


def eval_single_expression(expression, message):
    isNot = False
    if expression.startswith("not "):
        isNot = True
        expression = expression[4:]
    if expression.startswith("is"):
        cond = expression.partition("is ")[2]
        operationResult = remove_quotes(cond) == message
    elif expression.startswith("in"):
        cond = expression.partition("in ")[2]
        operationResult = remove_quotes(cond) in message
    elif expression.startswith("start "):
        cond = expression.partition("start ")[2]
        operationResult = message.startswith(remove_quotes(cond))
    elif expression.startswith("end "):
        cond = expression.partition("end ")[2]
        operationResult = message.endswith(remove_quotes(cond))
    else:
        raise PizzaError({'c': 104, 'e': expression})
    return operationResult if not isNot else not operationResult


def pizza_eval_read(condition, message):
    message = message.lower()
    condition = condition.lower()
    if PizzaEvalErrorDict.recursion_counter == 0 and not is_valid_condition(condition):
        raise PizzaError({'c': -1, 'e': condition})

    blocks = condition_to_blocks(condition)
    if not len(blocks) % 2:
        raise PizzaError({'c': 201, 'e': condition})
    else:
        if len(blocks) == 1:
            return eval_single_expression(blocks[0], message)
        if "|" in blocks:
            return pizza_eval_read(blocks[0], message) or pizza_eval_read(blocks[2], message)
        elif "&" in blocks:
            return pizza_eval_read(blocks[0], message) and pizza_eval_read(blocks[2], message)
        elif "^" in blocks:
            return logical_xor(pizza_eval_read(blocks[0], message), pizza_eval_read(blocks[2], message))
        else:
            raise PizzaError({'c': 202, 'e': condition})
