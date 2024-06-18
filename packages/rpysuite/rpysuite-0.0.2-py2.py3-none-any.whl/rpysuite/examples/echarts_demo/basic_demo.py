import json

from reactpy import component,  use_state

from rpysuite.components.echarts import ECharts
from rpysuite.components.mantine import MTProvider, MTGrid, MTPaper, \
    MTGridCol, MTCenter, MTStack, MTSegmentedControl, MTColorDefault, MTTabs, MTTabsList, MTTabsTab, MTTabsPanel

option1 = {
    "xAxis": {
        "type": 'category',
        "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    "yAxis": {
        "type": 'value'
    },
    "series": [
        {
            "data": [150, 230, 224, 218, 135, 147, 260],
            "type": 'line',
            "smooth": False,
        }
    ]
}
option2 = {
    "xAxis": {
        "type": 'category',
        "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    "yAxis": {
        "type": 'value'
    },
    "series": [
        {
            "data": [150, 230, 224, 218, 135, 147, 260],
            "type": 'line',
            "smooth": True,
        }
    ]
}

def mixed_plot():
    opt, set_opt = use_state("basic")
    color, set_color = use_state("blue")
    tp, set_tp = use_state("line")
    option = {
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "top": '5%',
            "left": 'center'
        },
        "xAxis": {
            "type": 'category',
            "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [
            {
                "label": {
                    "show": False,
                    "position": 'center'
                },

                "labelLine": {
                    "show": False,
                },
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": '#fff',
                    "borderWidth": 2
                },
                "radius": ['40%', '70%'],
                "data": [
                    {"value": 150, "name": 'Mon'},
                    {"value": 230,  "name": 'Tue'},
                    {"value": 224,  "name": 'Wed'},
                    {"value": 218,  "name": 'Thu'},
                    {"value": 135,  "name": 'Fri'},
                    {"value": 147, "name": 'Sat'},
                    {"value": 260, "name": 'Sun'},
                ],
                "emphasis": {
                    "label": {
                        "show": True,
                        "fontSize": 40,
                        "fontWeight": 'bold'
                    }
                },
                "type": tp,
                "smooth": opt == 'smooth',
                "color": color,

            }
        ]
    }

    return MTProvider(
        MTPaper(
            {"shadow": 'lg', "className": "m-10"},
            MTGrid(
                {"className": "px-5"},
                [
                    MTGridCol(
                        {"span": 7, "offset": 1, "className": "bg-gray-50 "},
                        MTCenter(
                            {"className": "mt-1/2 h-800 relative ",
                             "style": {"width": "100%", "height": '100%'}
                             },
                            ECharts(
                                {
                                    "option": option,
                                    "height": 800,
                                    "width": 800
                                }
                            )
                        )
                    ),
                    MTGridCol(
                        {"span": 3},
                        MTStack(
                            MTSegmentedControl({
                                "data": ["scatter", "line", "bar", "pie"],
                                "default": "line",
                                "value": tp,
                                "onChange": set_tp
                            }),
                            MTSegmentedControl({
                                "data": ["basic", "smooth"],
                                "default": "basic",
                                "value": opt,
                                "onChange": set_opt
                            }),
                            MTColorDefault({
                                "value": color,
                                "onChange": set_color
                            }),
                        )
                    ),
                ]
            ),
        )
    )
def build_tab_layout():
    default, set_default = use_state("linebasic")
    return MTTabs(
        {"defaultValue": default, "className": "mx-10", "onChange": set_default},
        [
            MTTabsList([
                MTTabsTab({"value": "linebasic"}, "line-basic"),
                MTTabsTab({"value": "linesmooth"}, "line-smooth"),
                MTTabsTab({"value": "mixed"}, "mixed"),
            ]),
            MTTabsPanel({"value": "linebasic"},

                        MTPaper(
                            {"shadow": 'lg', "className": "m-10"},
                            ECharts(
                                {
                                    "option": option1,
                                    "height": 800,
                                }
                            ))
                        ),
            MTTabsPanel({"value": "linesmooth"},
                        MTPaper(
                            {"shadow": 'lg', "className": "m-10"},
                            ECharts(
                                {
                                    "option": option2,
                                    "height": 800,
                                }
                            ))
                        ),

            MTTabsPanel({"value": "mixed"}, mixed_plot())
        ]
    )


@component
def plot_echarts_line(cmd=None):
    return MTProvider(
        build_tab_layout()
    )

    #
