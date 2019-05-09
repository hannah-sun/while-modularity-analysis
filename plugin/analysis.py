import copy
from . import ast_utils
import whiletranspiler.transpiler.ast as ast_module

def create_rw_sets(ast, variable_mapping):
    """
    Adds attributes `read_edges` and `write_edges` to all nodes in AST.
    """

    ast.read_edges = set()
    ast.write_edges = set()

    if isinstance(ast, ast_module.AST.SEQUENCE):
        reads, writes = set(), set()
        if ast.statements is not None:
            for statement in ast.statements:
                _reads, _writes = create_rw_sets(
                        statement, variable_mapping)

                reads |= _reads
                writes |= _writes

        return reads, writes

    elif isinstance(ast, ast_module.AST.ASSIGN):
        writes = set([ast.lhs])

        reads, _ = create_rw_sets(ast.rhs, variable_mapping)

        dependencies = set()

        for reads_from in reads:
            prev_nodes, depends_on = (
                    variable_mapping.get(reads_from, (set(), set())))

            ast.read_edges |= prev_nodes
            dependencies |= depends_on

        dependencies |= reads

        if ast.lhs in dependencies:
            write_nodes, _ = variable_mapping.get(ast.lhs, (set(), None))
            ast.write_edges |= write_nodes

            # TODO: maybe-write for conditional control flow
            variable_mapping[ast.lhs] = (set([ast]), dependencies)
        else:
            variable_mapping[ast.lhs] = (set([ast]), dependencies)

        return reads, writes

    elif isinstance(ast, ast_module.AST.IF):
        condition_reads, _ = create_rw_sets(ast.condition, variable_mapping)

        var_map_true = dict(variable_mapping)
        reads_true, writes_true = create_rw_sets(ast.if_true, var_map_true)

        if ast.if_false is not None:
            var_map_false = dict(variable_mapping)
            reads_false, writes_false = (
                    create_rw_sets(ast.if_false, var_map_false))
        else:
            var_map_false = variable_mapping
            reads_false, writes_false = set(), set()

        reads = condition_reads | reads_true | reads_false
        writes = writes_true | writes_false

        for variable in writes:
            prev_nodes, _ = variable_mapping.get(variable, (set(), None))

            _, dep_true = var_map_true.get(variable, (None, set()))
            _, dep_false = var_map_false.get(variable, (None, set()))
            if variable in (dep_true | dep_false):
                ast.write_edges |= prev_nodes

        for variable in reads:
            prev_nodes, _ = variable_mapping.get(variable, (set(), None))
            ast.read_edges |= prev_nodes

        # set of variables we might've writen to
        maybe_variables = set()

        for variable in writes_true:
            if variable in writes_false:
                # variables that we definitely wrote to, regardless of which
                # conditional branch we took
                _, dep_true = var_map_true.get(variable, (None, set()))
                _, dep_false = var_map_false.get(variable, (None, set()))
                dep = dep_true | dep_false
                variable_mapping[variable] = (set([ast]), dep)
            else:
                maybe_variables.add((True, variable))

        for variable in writes_false:
            if variable not in writes_true:
                maybe_variables.add((False, variable))

        for case, variable in maybe_variables:
            var_map = var_map_true if case == True else var_map_false
            prev_nodes, dep = (
                    variable_mapping.get(variable, (set(), set())))
            variable_mapping[variable] = (prev_nodes | set([ast]),
                    dep | var_map.get(variable, (None, set()))[1])

        return reads, writes

    elif isinstance(ast, ast_module.AST.WHILE):
        condition_reads, _ = create_rw_sets(ast.condition, variable_mapping)

        var_map_body = dict(variable_mapping)
        body_reads, body_writes = create_rw_sets(ast.body, var_map_body)

        reads = condition_reads | body_reads
        writes = body_writes

        for variable in reads:
            prev_nodes, _ = variable_mapping.get(variable, (set(), None))
            ast.read_edges |= prev_nodes

        for variable in writes:
            prev_nodes, _ = variable_mapping.get(variable, (set(), None))

            _, dep_body = var_map_body.get(variable, (None, set()))
            if variable in dep_body:
                ast.write_edges |= prev_nodes

        for variable in writes:
            prev_nodes, dep = (
                    variable_mapping.get(variable, (set(), set())))
            variable_mapping[variable] = (prev_nodes | set([ast]),
                    dep | var_map_body.get(variable, (None, set()))[1])

        return reads, writes

    elif isinstance(ast, ast_module.AST.PRINT):
        reads, _ = create_rw_sets(ast.expression, variable_mapping)

        for variable in reads:
            prev_nodes, _ = variable_mapping.get(variable, (set(), None))
            ast.read_edges |= prev_nodes

        return reads, set()

    elif isinstance(ast, ast_module.AST.COMMENT):
        return set(), set()

    elif isinstance(ast, ast_module.AST.NOT):
        condition_reads, _ = create_rw_sets(ast.condition, variable_mapping)

        return condition_reads, set()

    elif isinstance(ast, ast_module.BinOp):
        arg1_reads, _ = create_rw_sets(ast.arg1, variable_mapping)
        arg2_reads, _ = create_rw_sets(ast.arg2, variable_mapping)

        return arg1_reads | arg2_reads, set()

    elif isinstance(ast, ast_module.AST.Symbols.VARIABLE):
        return set([ast]), set()

    elif isinstance(ast, ast_module.ASTSymbol):
        return set(), set()

    else:
        print("ERROR >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        raise ValueError

def serialize_ast_graph(ast):
    """
    Returns a serialized JSON representation of the graph of read and write
    edges for the top level of the AST.
    """

    nodes = []
    node_mapping = {} # map node to index in nodes list

    if not isinstance(ast, ast_module.AST.SEQUENCE):
        return nodes

    for node in ast.statements:
        if isinstance(node, ast_module.AST.COMMENT):
            continue

        node_mapping[node] = len(nodes)

        nodes.append({
            "label": ast_utils.str_label(node),
            "read_edges": [node_mapping[x] for x in node.read_edges],
            "write_edges": [node_mapping[x] for x in node.write_edges],
        })

    return nodes

def analyze_ast(emit, ast):

    if ast is None:
        emit("plugin_analysisgraph", { "error": True }),
        return

    # create a deep copy so we can play around with it
    ast = copy.deepcopy(ast)

    create_rw_sets(ast, {})

    emit("plugin_analysisgraph", {
        "error": False,
        "graph": serialize_ast_graph(ast)
    }),

