from PizzaEvalUtils import PizzaError


def write_value_to_blocks(write_value):
    special_conditions = []
    is_inside_gaensefuesschen = False
    is_inside_eckige_klammer = False
    for index, i in enumerate(write_value):
        if i == "'":
            is_inside_gaensefuesschen = not is_inside_gaensefuesschen
        elif not is_inside_gaensefuesschen:
            if i == "[":
                if is_inside_eckige_klammer:
                    raise "your great grandma"
                else:
                    is_inside_eckige_klammer = True
            if i == "]":
                if is_inside_eckige_klammer:
                    is_inside_eckige_klammer = False
                else:
                    raise "your great grandpa"

def pizza_eval_write(write_value, message):
    pass