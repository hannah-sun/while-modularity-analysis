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

class JoinableSet:
    """
    Wrapper for set. 2 JoinableSets instances can be joined so they point to
    the same union of their underlying sets.
    """

    class _Set:
        _set_cnt = 0
        def __init__(self, *args, **kwargs):
            JoinableSet._Set._set_cnt += 1
            self._set = set(*args, **kwargs)
            self._id = JoinableSet._Set._set_cnt

    def __init__(self, *args, **kwargs):
        self.data = self._Set(*args, **kwargs)

    def add(self, value):
        self.data._set.add(value)

    def join(self, other):
        assert isinstance(other, self.__class__)

        self.data._set = self.data._set | other.data._set
        other.data = self.data

    def __hash__(self):
        return self.data._id

    def __eq__(self, other):
        if isinstance(self, JoinableSet):
            return hash(self) == hash(other)
        else:
            return super().__eq__(other)

    def __iter__(self):
        return iter(self.data._set)
