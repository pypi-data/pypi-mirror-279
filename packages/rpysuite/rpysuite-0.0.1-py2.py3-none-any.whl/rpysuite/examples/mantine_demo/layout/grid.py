from reactpy import component, html

from rpysuite.components.mantine import MTGrid, MTGridCol, MTProvider, MTPaper, \
    MTTitle, MTSelect, MTTabs, MTTabsList, MTTabsTab, MTTabsPanel
from rpysuite.components.monaco import MonacoEditor


def basic_panel():
    return MTPaper(
        {"shadow": 'lg', "className": "m-10 p-10"},
        MTGrid(
            {"className": "px-10 pb-10"},
            [
                MTGridCol(
                    {"span": 4},
                    html.div({"class": "bg-green-100 border  p-5"}, 1)
                ),
                MTGridCol(
                    {"span": 4},
                    html.div({"class": "bg-green-100 border p-5"}, 2)
                ),
                MTGridCol(
                    {"span": 4},
                    html.div({"class": "bg-green-100 border p-5"}, 3)
                ),
            ]
        ),

        MonacoEditor({
            "defaultValue": """
MTGrid(
    [
        MTGridCol(
            {"span": 4},
            html.div(1)
        ),
        MTGridCol(
            {"span": 4},
            html.div(2)
        ),
        MTGridCol(
            {"span": 4},
            html.div(3)
        )
    ]
)
                """,
            "height": "400px",
            "language": "python",
            "options": {"readOnly": True}
        }),

        MTTitle({"order": 3, "className": "pt-5"}, "Columns & Span"),
        html.div(
            {"className": "p-5"},
            "span prop controls the ratio of column width to the total width of the row. By default, grid uses 12 columns layout, so span prop can be any number from 1 to 12."
        )
    )

def gutter_panel():
    return MTPaper(
        {"shadow": 'xs', "className": "m-10 p-10"},
        MTGrid(
            {"gutter": { "base": 5, "xs": 'md', "md": "xl", "xl": 50 },

             "className": "px-10 pb-10",
             },
            [
                MTGridCol(
                    {"span": 4},
                    html.div({"class": "bg-green-100 border p-5"}, 1)
                ),
                MTGridCol(
                    {"span": 4},
                    html.div({"class": "bg-green-100 border p-5"}, 2)
                ),
                MTGridCol(
                    {"span": 4},
                    html.div({"class": "bg-green-100 border p-5"}, 3)
                ),
            ]
        ),

        MonacoEditor({
            "defaultValue": """
MTGrid(
    {"gutter": { "base": 5, "xs": 'md', "md": "xl", "xl": 50 }},
    [
        MTGridCol(
            {"span": 4},
            html.div(1)
        ),
        MTGridCol(
            {"span": 4},
            html.div(2)
        ),
        MTGridCol(
            {"span": 4},
            html.div(3)
        )
    ]
)
                    """,
            "height": "35vh",
            "language": "python",
            "options": {"readOnly": True}
        }),
        MTTitle({"order": 3, "className": "pt-5"}, "Gutter"),
        html.div(
            {"class": "p-5"},
            "Set gutter prop to control spacing between columns."
        )
    )


def build_tab_layout():
    return MTTabs(
        {"defaultValue": "basic", "className": "mx-10"},
        [
            MTTabsList([
                MTTabsTab({"value": "basic"}, "basic"),
                MTTabsTab({"value": "gutter"}, "gutter"),
            ]),
            MTTabsPanel({"value": "basic"}, basic_panel()),
            MTTabsPanel({"value": "gutter"}, gutter_panel())
        ]
    )


@component
def plot_grid(option):
    return MTProvider(
        build_tab_layout()
    )
