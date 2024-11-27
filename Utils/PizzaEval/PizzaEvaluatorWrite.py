import random
from datetime import datetime

from Utils.PizzaEval.PizzaEvalUtils import is_valid_replace_statement, PizzaError, identify_error


def pizza_eval_write(author_name: str, original_message: str, write_result: str) -> str:
    def process_block(block: str) -> str:
        if block == "author":
            return str(author_name)
        elif block == "time":
            return datetime.now().strftime('%H:%M:%S')
        elif block == "message":
            return original_message
        elif block.startswith("random\\"):
            options = block[7:].split('\\')
            weighted_options = {}
            for option in options:
                try:
                    event, weight = option.rsplit('-', 1)
                    try:
                        weight = int(weight)
                    except ValueError:
                        raise PizzaError({'c': 1103, 'e': block})
                    weighted_options[event] = weight
                except ValueError:
                    raise PizzaError({'c': 1102, 'e': block})
            return random.choices(list(weighted_options.keys()), list(weighted_options.values()), k=1)[0]
        else:
            return f"[{block}]"  # dont change irrelevant blocks

    def process_replace_block(string: str) -> str:
        result = ""
        in_quotes = False
        inside_block_statement = False
        temp_block_statement = ""

        for i in string:
            if i == "'":
                in_quotes = not in_quotes
                result += i
            elif not in_quotes:
                if i not in ("[", "]") and not inside_block_statement:
                    result += i
                if i == "[":
                    inside_block_statement = True
                if inside_block_statement and i not in ("[", "]"):
                    temp_block_statement += i
                if i == "]" and inside_block_statement:
                    inside_block_statement = False
                    result += process_block(temp_block_statement)
                    temp_block_statement = ""
            elif in_quotes:
                result += i

        return result

    def parse_replace(write_result: str):
        if not is_valid_replace_statement(write_result):
            raise PizzaError({'c': 1200, 'e': write_result})

        content = write_result[1:-1]
        segments = []
        current_segment = ""
        in_quotes = False
        i = 0
        while i < len(content):
            char = content[i]
            if char == "\\" and not in_quotes:
                segments.append(current_segment)
                current_segment = ""
            elif char == "'":
                in_quotes = not in_quotes
                current_segment += char
            else:
                current_segment += char
            i += 1

        segments.append(current_segment)

        if len(segments) != 3:
            raise PizzaError({'c': 1207, 'e': write_result})

        return segments[1], segments[2]

    # [replace\stringa\stringb]
    if write_result.startswith("[replace\\") and write_result.endswith("]"):
        try:
            stringa, stringb = parse_replace(write_result)
            processed_stringb = process_replace_block(stringb)
            return original_message.replace(stringa, processed_stringb) if stringa in original_message else original_message
        except:
            raise PizzaError({'c': 1208, 'e': write_result})

    result = ""
    in_quotes = False
    start_idx = 0

    while start_idx < len(write_result):
        start = write_result.find('[', start_idx)
        if start == -1:
            result += write_result[start_idx:]
            break

        quote_pos = write_result.rfind("'", 0, start)
        if quote_pos != -1 and write_result[quote_pos:].count("'") % 2 != 0:
            in_quotes = True

        if in_quotes:
            end_quote = write_result.find("'", start)
            if end_quote == -1:
                raise PizzaError({'c': 1001, 'e': write_result})
            result += write_result[start_idx:end_quote + 1]
            start_idx = end_quote + 1
            in_quotes = False
            continue

        end = write_result.find(']', start)
        if end == -1:
            raise PizzaError({'c': 1002, 'e': write_result})

        result += write_result[start_idx:start]
        block_content = write_result[start + 1:end]
        result += process_block(block_content)
        start_idx = end + 1

    return result

# try:
#     print(pizza_eval_write(422800248935546880, "siis", "[random\eiersalat-1\eierkuchen-5]"))
# except PizzaError as e:
#     details = e.args[0]
#     print(identify_error(details['c'], details['e']))
