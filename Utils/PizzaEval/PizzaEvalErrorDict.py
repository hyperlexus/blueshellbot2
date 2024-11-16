error_dict = {
    # general errors
    -1: "complex condition was successfully evaluated, but is somehow still not valid",
    0: "nothing was passed",
    1: "condition had \' as its first character, which is not allowed. did you quote the entire string instead of the expression value?",
    2: "no complex operator was passed, but the input is also not a simple expression. there is nothing to parse.",
    3: "no valid simple type check contained in complex expression",
    4: "due to how the compiler is coded, the characters '|', '&' and '^' are not allowed inside single quoted strings (\')",
    5: "you cannot pass 'True' or 'False' as a standalone function, as it would always be true or false.",

    # simple expression handler errors
    101: "simple expression doesn't contain necessary simple type check",
    102: "simple expression has an incorrect amount of single quotes",
    103: "simple expression has no single quotes around the expression value, but more than 1 space",
    104: "simple expression contains a simple keyword, but 'expression_type' did not receive it correctly",
    105: "simple expression has text after or before single quotes. single quotes have to encompass the entire expression value",

    # evaluate_two_sides errors
    201: "couldn't evaluate two sides, as one side was not correctly evaluated to True/False",
    202: "wrong operand was passed to evaluate_two_sides function",
    203: "less than 2 sides were passed to two_side function",

    # parentheses-related errors
    301: "input contained no or only one of two parentheses types `'(', ')'`",
    302: "amount of opening and closing parentheses do not match",
    303: "input contains empty pairs of parentheses `()`, which is not allowed",

    # not expression errors
    401: "not expression has more than 1 space",
}


