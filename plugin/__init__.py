"""
Setup to tell WHILE transpiler what functionality to add to web interface
"""

from . import main

class PLUGIN_SETTINGS:
    class web_interface:
        # static files to load into <head> tag
        css = [
            "static/css/general.css",
        ]

        js = [
            "static/js/general.js",
        ]

        # javascript function to call with data so that plugin can use
        # socket handler
        js_main = "while_plugin"

        # html to load in tab windows
        windows = [
            ("Graph", "templates/graph.html"),
            ("Snippets", "templates/snippets.html"),
        ]

        # python function to call so plugin can add Flask views or socket
        # actions
        main = main.plugin_generator

