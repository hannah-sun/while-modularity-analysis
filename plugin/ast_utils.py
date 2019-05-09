import re
import whiletranspiler.transpiler as transpiler

multiple_spaces_pattern = re.compile("[ ]+")

def str_label(ast):
    """
    Returns a human readable string representing the AST.
    """

    if ast is None:
        return ""

    string = transpiler.transpile_c.transpile_ast_to_string(ast)
    return (multiple_spaces_pattern
            .sub(" ", string.replace("\n", " "))
            .strip(" \n"))
