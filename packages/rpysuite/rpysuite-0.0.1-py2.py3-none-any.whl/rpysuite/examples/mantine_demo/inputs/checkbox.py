from reactpy import component, html, use_state, use_ref

from rpysuite.components.mantine import MTProvider, MTTabs, MTTabsList, MTTabsTab, MTTabsPanel, \
    MTPaper, MTGrid, MTGridCol, \
    MTCheckbox,MTTitle, MTStack, MTSegmentedControl, \
    MTInputX, \
    MTCenter, MTColorDefault


def basic_panel():

    checked, set_checked = use_state(True)
    position, set_position = use_state("right")
    label, set_label = use_state("label")
    desc, set_desc = use_state("desc")
    error, set_error = use_state(None)
    color, set_color = use_state("blue")


    def handle_change(v):
        set_checked(v)
    def handle_position(v):
        set_position(v)
    return MTPaper(
        {"shadow": 'lg', "className": "m-10 p-10"},
        MTGrid(
            {"className": "px-10 pb-10"},
            [
                MTGridCol(
                    {"span": 7, "offset": 1, "className": "bg-lime-50 "},
                    MTCenter(
                        { "className": "mt-1/2 h-400 relative ",
                          "style": { "width": "auto", "height": '100%' }
                          },
                        MTCheckbox({
                            "checked": checked,
                            "onChange": handle_change,
                            "label": label,
                            "description": desc,
                            "error": error,
                            "labelPosition": position,
                            "color": color
                        })
                    )
                ),
                MTGridCol(
                    {"span": 3 },
                    MTStack(
                        MTSegmentedControl({
                            "data": ["left", "right"],
                            "value": position,
                            "onChange": handle_position
                        }),
                        MTInputX(
                            {
                                "label": "Label",
                                "value": label,
                                "sync": set_label,
                            }
                        ),
                        MTInputX(
                            {
                                "label": "Description",
                                "value": desc,
                                "sync": set_desc,
                            }
                        ),
                        MTInputX(
                            {
                                "label": "Error",
                                "value": error,
                                "sync": set_error,
                            }
                        ),
                        MTColorDefault({
                            "value": color,
                            "onChange": set_color
                        })

                    )
                ),
            ]
        ),
    )
def build_tab_layout():
    return MTTabs(
        {"defaultValue": "basic", "className": "mx-10"},
        [
            MTTabsList([
                MTTabsTab({"value": "basic"}, "basic"),
            ]),
            MTTabsPanel({"value": "basic"}, basic_panel()),
        ]
    )

@component
def plot_checkbox(option):
    return MTProvider(
        build_tab_layout()
    )

def wrap():
    label, set_label = use_state("check me!")


    return html.div(
        [

            MTProvider(
                MTInputX({"sync": set_label, "value": label}),
            ),
            html.div(label)

        ]
    )

