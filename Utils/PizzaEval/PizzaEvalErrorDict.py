recursion_counter = 0

error_dict = {
    # general errors
    0: "nothing was passed.",
    1: "odd number of single quotes. make sure to close all quotes!",
    2: "condition had `\'` as its first character, which is not allowed. did you quote the entire string instead of the expression value?",
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

    # misc
    401: "ne sie scheiß hurensohn"
}


