recursion_counter = 0

error_dict = {
    # read eval errors:
    # general errors
    0: "nothing was passed.",
    1: "odd number of single quotes. make sure to close all quotes!",
    2: "condition had `'` as its first character, which is not allowed. did you quote the entire string instead of the expression value?",
    3: "no valid simple type check contained in complex expression.",
    4: "amount of opening and closing parentheses do not match. did you close all opened parentheses?",
    5: "the condition has too many spaces. please set the expression into single quotes `'<expression>'` if your desired expression contains spaces.",
    6: "your condition contains two single quotes `''` in a row. please don't do that 🍕👌",

    # simple expression handler errors
    101: "simple expression doesn't contain necessary simple type check.",
    102: "simple expression has an incorrect amount of single quotes.",
    103: "simple expression contains a type check, but no value. Did you pass both type and value ('is a')?",
    104: "simple expression could not evaluate, as type check is not known.",

    # blocks errors
    201: "blocks were not correctly divided. there are an even number of blocks, which shouldn't happen.",
    202: "blocks were divided, but no valid operator was found.",

    # parentheses-related errors
    301: "input contains more opening parentheses than closing parentheses.",
    302: "input contains more closing parentheses than opening parentheses.",
    303: "input contains at least 1 empty pair of parentheses `()`, which is not allowed.",

    # write eval errors:
    # general errors:
    1000: "invalid write format, uncaught exception.",
    1001: "unmatched single quote in entire result.",
    1002: "entire statement has mismatched [ and ].",

    # random errors:
    1101: "invalid [random\\eventa-n\\eventb-m] format.",
    1102: "invalid eventn-p format.",
    1103: "probability has to be an integer indicating weight.",
    1104: "random statements cannot be chained together as that doesn't make sense mathematically (refer to [this](https://i.imgur.com/LvT3YcW.png)).",

    # replace errors:
    1200: "replace statement not valid for uncaught reason.",
    1201: "replace statement doesn't both start with [replace and end with ].",
    1202: "replace statement has mismatched [ and ].",
    1204: "unmatched single quote in replace statement.",
    1205: "replace statement doesn't contain exactly 2 splitter backslashes outside of blocks.",
    1206: "invalid [replace\\stringa\\stringb] format. length of segments is not two.",
    1207: "replace statements cannot be chained together inside of each other as that doesn't make sense",
    1208: "statement to replace with starts with a [, but isn't a random block, which is not allowed. use single quotes (\') for this if you want to print a [ character."
}


