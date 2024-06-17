from pathlib import Path

from fastapi import FastAPI
from reactpy import  html, component
from reactpy.backend._common import CommonOptions
from reactpy.backend.fastapi import configure

from rpysuite.examples.layout import Layout
from rpysuite.examples.menu_builder import Menu
from rpysuite.components.router import simple, route


tailwind_scriptfile = open(Path(__file__).parent / '../tailwind.js').read()
TAILWIND_SCRIPT = html.script(tailwind_scriptfile)
config_content = """
tailwind.config = {
    theme: {
        extend: {
            colors: {
                clifford: '#da373d',
            },
            transitionProperty: {
                'width': 'width'
            },
        }
    }
}
"""
TAILWIND_CONFIG = html.script(config_content)

def missing(option):
    return html.div(f"Page Not Found!!! {option}")

class AppShell:
    def __init__(self, menu, title=None, views=None, icons=None, app=None):
        self.app = FastAPI() if app is None else app
        self.menu = Menu(menu, view_map=views, icon_map=icons)
        self.layout = Layout(title=title, menu=self.menu)
        self.title = title
        # self.menu.select('LAYOUT_ASPECTRATIO_MAP_MAP2')

        @component
        def render():
            return html._(
                TAILWIND_SCRIPT,
                TAILWIND_CONFIG,
                simple.router(
                    *self.build_routes(self.menu.menu)
                )
            )

        options = CommonOptions(head=[html.title(self.title)])
        options.cors = False
        configure(self.app, render, options=options)

    def build_routes(self, menu):
        results = []
        for rt in menu:
            # key = rt.get('key')
            path = rt.get('path')
            results.append(
                route(path, self.layout.view())
            )
            subs = rt.get('subs')
            if subs:
                a = self.build_routes(subs)
                if len(subs) > 0:
                    results.extend(a)
        return results





