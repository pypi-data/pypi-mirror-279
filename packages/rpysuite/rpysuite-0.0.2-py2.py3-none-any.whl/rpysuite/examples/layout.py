
from reactpy import component, html, use_location, use_state, use_ref, event

from rpysuite.components.mantine import MTProvider, MTGroup, MTText
from rpysuite.components.icons import Icon
from rpysuite.components.router import link



@component
def missing(option):
    return html.div(
        {"class": "pl-1/2 h-400 relative ",
         "style": {"width": "100%", "height": '100%'}
         },
         f"Page {option} is still under construction!")


class Layout:
    def __init__(self, title=None, menu=None):
        self.title = title
        self.menu = menu
        self.aside_width = 60
        self.aside_opened = True

    def handle_fold(self, e):
        self.aside_opened = not self.aside_opened

    @component
    def view(self):
        aside_opened, set_aside_opened = use_state(True)
        return (
            html.div(
                self.build_control(aside_opened, set_aside_opened),
                self.build_header(),
                html.div(
                    {"class": "flex "},
                    [
                        self.build_aside(aside_opened),
                        self.build_content(aside_opened)
                    ]

                )
            )
        )
    def build_header(self):
        return html.nav(
            {"class": "fixed border-b border-gray-200 bg-gray-50  pl-8 left-0 right-0 top-0 z-40"},
            MTProvider(
                MTGroup(
                    MTText({ "size": "xl"},  self.title)
                )
            )
        )

    def build_control(self, aside_opened, set_aside_opened):
        return Icon({
                "class": "fixed bg-gray-100 fixed  left-1  top-6 z-50 rounded-lg",
                "name": f'{aside_opened and "ChevronLeft" or "ChevronRight"}',
                "onClick": lambda e: set_aside_opened(not aside_opened),
                "size": 18,
                "color": "green"
          })


    def build_aside(self, aside_opened):
        navs = []
        for route in self.menu.menu:
            navs.append(self.navitem(route))
        return html.aside(
                    {
                        "class": f"overflow-x-hidden pt-10 pl-2 top-0 left-0 bg-gray-50 h-screen overflow-auto transition-all "
                    },

                    [
                        html.div(
                            {"class": f"h-full px-3 py-0  overflow-auto "
                                      f"w-{self.aside_width} "
                                      f"{aside_opened and '1' or 'hidden'}"
                             },
                            html.ul(
                                {"class": "space-y-2 font-medium"},
                                [nav for nav in navs]
                            ),

                        ),


                    ]
                )






    @component
    def build_content(self, asided_opened):
        view_map = self.menu.view_map
        current = self.menu.current
        current_leaf = self.menu.current_leaf
        view = view_map.get(current_leaf, missing)
        if isinstance(view, dict):
            view_func = view.get('fun')
            view_option = view.get('opt', current_leaf)
            view_comp = view_func(view_option)
        else:
            view_comp = view(current_leaf)

        return html.main(
            {"class": f"relative flex-items top-20  left-{self.aside_width+10}  w-full h-full"},
            view_comp
        )


    def navitem(self, option, opened=None, active=None):
        menu = self.menu
        open_map = menu.open_map
        level_map = menu.level_map
        display_map = menu.display_map
        key = option.get('key')
        name = option.get('name')
        subs = option.get('subs')
        level = option.get('level')
        path = option.get('path')
        leaf = option.get('leaf')
        icon = option.get('icon', {
            "name": "Bulldozer",
            "color": "orange",
        })
        if isinstance(icon, dict):
            icon_name = icon.get('name', 'Bulldozer')
            icon_color = icon.get('color', 'orange')
            icon_size = icon.get('size', 16)
        elif isinstance(icon, str):
            icon_name = icon
            icon_color = 'gray'
            icon_size = 16
        else:
            icon_name = 'Bulldozer'
            icon_color = 'orange'
            icon_size = 16



        def handle_click(e):

            menu.select(key)

        path_map = {e.get('key'): e.get('path') for e in menu.menu}
        to_path = path if leaf else path_map.get(menu.current)

        return html.div(
            {"class": "flex gap-1 py-1 align-items-center hover:bg-green-100 align-items-center "
                      f"ml-{(level) * (4)} "
                      f'{menu.current == key and "text-[color:green]"  or "text-[color:#606060]"} '
                      f'{menu.current == key and "font-bold"  or ""} '
                      f'{not display_map.get(key) and level>0  and "hidden"}',
             "style": {"align-items": "center"},
             },

            [
                Icon({"name": f"{(leaf and (menu.current_leaf == key and 'SquareRoundedFilled' or 'SquareRounded') or (open_map.get(key) and 'ChevronDown') or 'ChevronRight')}",
                      "size": 20}
                     ),
                link(name , to=to_path,
                     className="pl-1",
                     onClick= handle_click,
                     ),
                Icon({
                    "name": f"{icon_name}", "color": icon_color, "size": icon_size}
                )
            ]
        )

