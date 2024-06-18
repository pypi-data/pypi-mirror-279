from rpysuite.examples.echarts_demo.basic_demo import plot_echarts_line
from rpysuite.examples.home import plot_home
from rpysuite.examples.mantine_demo.inputs.checkbox import plot_checkbox
from rpysuite.examples.mantine_demo.layout.grid import plot_grid




menu = [
    {"key": "HOME", "name": "Home",  "path": "/" },
    {
        "key": "MANTINE", "name": "Mantine", "path": "/mantine",
        "subs": [
            {
                "key": "LAYOUT", "name": "Layout", "path": "/layout",
                "subs": [
                    {
                        "key": "GRID", "name": "Grid", "option": {"mode": "basic"},
                        "path": "/grid",
                    },
                    {
                        "key": "STACK", "name": "Stack", "option": {"mode": "basic"},
                        "path": "/stack",
                    },
                    {
                        "key": "FLEX", "name": "Flex", "option": {"mode": "basic"},
                        "path": "/flex",
                    },
                    {
                        "key": "CONTAINER", "name": "Container", "option": {"mode": "basic"},
                        "path": "/container",
                    },
                    {
                        "key": "CENTER", "name": "Center", "option": {"mode": "basic"},
                        "path": "/center",
                    },
                    {
                        "key": "BOX", "name": "Box", "option": {"mode": "basic"},
                        "path": "/box",
                    },
                ]
            },

            {
                "key": "INPUTS", "name": "Inputs", "path": "/inputs", "icon": "LayoutBoard",
                "subs": [
                    {
                        "key": "CHECKBOX", "name": "Checkbox", "option": {"mode": "basic"},
                        "path": "/checkbox",
                    },
                    {
                        "key": "SELECT", "name": "Select", "option": {"mode": "basic"},
                        "path": "/select",
                    },
                    {
                        "key": "TEXTINPUT", "name": "TextInput", "option": {"mode": "basic"},
                        "path": "/textinput",
                    },
                    {
                        "key": "BUTTON", "name": "Button", "option": {"mode": "basic"},
                        "path": "/button",
                    },
                ]
            },
            {"key": "ORNAMENTS", "name": "Ornaments", "path": "/ornaments", "icon": "SmartHome",
             "subs": [

                 {"key": "TOOLTIP", "name": "Tooltip", "path": "/tooltip", "icon": "SmartHome",
                  "subs": []
                  }
             ]
             },
        ]
    },
    {"key": "ECHARTS", "name": "ECharts", "path": "/echarts",

     "subs": [
         {
             "key": "BASIC", "name": "Basic", "path": "/basic",
          },


     ]
     }
]



views = {
    "HOME": {"fun": plot_home, "opt": None},
    "MANTINE_LAYOUT_GRID": {"fun": plot_grid, "opt": None},
    "MANTINE_INPUTS_CHECKBOX": {"fun": plot_checkbox, "opt": None},
    "ECHARTS_BASIC": {"fun": plot_echarts_line, "opt": None},
}

icons = {
    "MANTINE_LAYOUT": "LayoutBoard",
    "MANTINE_INPUTS": "KeyboardShow",
    "ECHARTS": "ChartHistogram",
    "MANTINE_LAYOUT_GRID": {"name": "LayoutBoard", "color": "green", "size": 16},
    "MANTINE_INPUTS_CHECKBOX": {"name": "Checkbox", "color": "green", "size": 16},
    "ECHARTS_BASIC": {"name": "ChartHistogram", "color": "green", "size": 16},
}
