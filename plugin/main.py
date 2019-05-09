from . import analysis

def plugin_generator(flask_app, socket_action, socket_triggers):
    socket_triggers.ast.append(analysis.analyze_ast)

