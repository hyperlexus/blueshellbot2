import re


def pizza_eval(value: str, condition: str) -> bool:
    def replace_condition(match):
        command, arg = match.groups()
        arg = arg.strip()

        if command == "is":
            return f"(value == '{arg}')"
        elif command == "in":
            return f"('{arg}' in value)"
        elif command == "start":
            return f"(value.startswith('{arg}'))"
        elif command == "end":
            return f"(value.endswith('{arg}'))"
        else:
            return False

    condition = re.sub(r"\b(is|in|start|end) ([^&|()]+)", replace_condition, condition)
    if not condition:
        return False
    condition = condition.replace("&", "and").replace("|", "or")

    # please inshallah DO NOT ACE
    safe_context = {"value": value, "and": lambda x, y: x and y, "or": lambda x, y: x or y}

    try:
        # ahahahahahahahaahahahahahahahahahaahahahahahahah AHAHAHAHAHAHAHAHAHAHAHA
        return eval(condition, safe_context)
    except SyntaxError:
        return False
# print(pizza_eval("banana", "banana"))
