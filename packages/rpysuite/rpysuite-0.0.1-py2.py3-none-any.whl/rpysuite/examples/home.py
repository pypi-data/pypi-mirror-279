from copy import copy

from reactpy import component, html, use_state

from rpysuite.components.mantine import MTProvider, MTCenter, MTText, MTPaper, MTGrid, MTGridCol, MTTitle, MTInputX, \
    MTCode, MTTabs, MTTabsList, MTTabsTab, MTTabsPanel, MTScrollArea, MTNavLink


def render_real_todo():
    todos, set_todos = use_state([])
    def add_todo(e):
        todos.insert(0, {"done": False, "value": e})
        set_todos(copy(todos))
    def done_todo(i):
        def wrap(e):
            todos[i]["done"] = not todos[i]["done"]
            set_todos(copy(todos))
        return wrap
    def del_todo(i):
        def wrap(e):
            todos and todos.pop(i) and set_todos(copy(todos))
        return wrap

    return html.div(
        [
            MTInputX({
                "sync": add_todo,
                "style": { "width": 400 }
            }),
            html.ul(
                [html.li({
                    "onClick": done_todo(i),
                    "onDoubleClick": del_todo(i),
                    "style": {"text-decoration": v.get('done') and 'line-through'}
                }, v.get('value')) for i,v in enumerate(todos)]
            )
        ]
    )


def build_todo_demo():
    default, set_default = use_state("basic")
    return MTTabs(
        {"defaultValue": default, "onChange": set_default},
        [
            MTTabsList([
                MTTabsTab({"value": "basic"}, "a simple todo list"),
                MTTabsTab({"value": "full"}, "A todo list with add/done/revert/delete support"),
            ]),
            MTTabsPanel({"value": "basic"},
                        MTPaper(
                            {"shadow": 'lg', "class": "m-2"},
                            MTScrollArea(
                                {"h": 200},
                                MTCode({"block": 1}, """todos, set_todos = use_state([])
def add_todo(e):
    todos.insert(0, e)
    set_todos(copy(todos))

return html.div(
    [
        MTInputX({ "sync": add_todo }),
        html.ul([html.li(v) for v in todos])
    ]
)
                        """)),
                        )),
            MTTabsPanel({"value": "full"},
                        MTPaper(
                            {"shadow": 'lg', "class": "m-2"},
                            MTScrollArea(
                                {"h": 200},
                                MTCode({"block": 1}, """
todos, set_todos = use_state([])

def add_todo(e):
    todos.insert(0, {"done": False, "value": e})
    set_todos(copy(todos))
    
def done_todo(i):
    def wrap(e):
        todos[i]["done"] = not todos[i]["done"]
        set_todos(copy(todos))
    return wrap
    
def del_todo(i):
    def wrap(e):
        todos and todos.pop(i) and set_todos(copy(todos))
    return wrap

return html.div(
    [
        MTInputX({ "sync": add_todo }),
        html.ul(
            [html.li({
                "onClick": done_todo(i),
                "onDoubleClick": del_todo(i),
                "style": {"text-decoration": v.get('done') and 'line-through'}
            }, v.get('value')) for i,v in enumerate(todos)]
        )
    ]
)
                                """)
                            ,

                            )

                        )),
        ]
    )


@component
def plot_home(option):
    return MTProvider(
        MTPaper(
            {"shadow": 'lg', "class": "mx-10 "},
            MTGrid(
                {"class": "pb-10", "columns": 48},
                [
                    MTGridCol(
                        {"span": 42, "offset": 2},
                        MTTitle({"order": 2}, "Hello Pythonistas!"),
                        MTText("This is a hobby project for using React & Python to build beautiful web pages!"),
                        MTText("The project is using ReactPy as its backend and integrates with UI library Mantine, graph libraries like echarts, etc."),
                        MTText( "It's aiming at helping Python developers to bring their idea into the visual world easily!"),
                        MTTitle({"order": 4}, "Component"),
                        MTText( "To use a basic component in ReactPy, you need to pass two params:"),
                        MTText( "the first param is about the attributes or props,"),
                        MTText("the second one is about the content or children."),
                        MTTitle({"order": 4}, "A Basic Todo!"),
                        build_todo_demo(),
                        MTText("1.type text in the input. 2. type enter to add to the list. 3. click the item to switch state. 4. double click the item to delete."),
                        render_real_todo()
                    ),
                ]
            )
        )
    )