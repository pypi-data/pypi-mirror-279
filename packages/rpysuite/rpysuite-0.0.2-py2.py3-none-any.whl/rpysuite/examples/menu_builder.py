from rpysuite.examples.data import menu


class Menu:
    def __init__(self, menu, current=None, compose_mode='flat', key_mode='nested', view_map=None, icon_map=None):
        self.compose_mode = compose_mode
        self.key_mode = key_mode
        self.view_map = view_map
        self.icon_map = icon_map

        self.options = self.keys(menu)
        self.open_map = {e: True for e in self.options}
        self.display_map = {e: True for e in self.options}

        self.level_map = {}
        self.leaf_map = {}
        self.menu = self.build(menu)
        self.current_leaf = current if current else self.menu[0].get('key')
        self.current = current if current else self.menu[0].get('key')
        self.history = [self.current]
        self.statistics = {e: 1 if e == self.current else 0 for e in self.options}

    def select(self, option):
        if option in self.options:
            self.current = option
            self.history.append(option)
            self.statistics[option] += 1
            if self.leaf_map[option]:
                self.current_leaf = option
            for k,v in self.open_map.items():
                if option.startswith(k) and not v:   # tree
                    self.open_map[k] = True
                if k.startswith(option) and v:
                    self.open_map[k] = False

                if k.startswith(option) and len(option)<len(k):
                    open_state = self.open_map[option]
                    if not open_state:
                        self.display_map[k] = False
                    else:
                        self.display_map[k] = True #默认全展开
                        self.open_map[k] = True #默认全展开

    def keys(self, menu, pkey=None):
        results = []
        for e in menu:
            key = f"{pkey}_{e.get('key')}" if pkey and self.key_mode == 'nested' else e.get('key')
            results.append(key)
            subs = e.get('subs')
            if subs:
                results.extend(self.keys(subs,pkey=key))
        return results

    def build(self, menu, pkey=None, ppath=None, level=0):
        results = []
        for m in menu:
            key, path, name, subs = m.get('key'), m.get('path'), m.get('name'), m.get('subs')

            if pkey and level > 0 and self.key_mode == 'nested':
                key = f'{pkey}_{key}'
                path = f'{ppath}{path}'

            self.level_map[key] = level
            self.leaf_map[key] = not subs or len(subs) == 0
            item = {"key": key, "path": path, "level": level, "pkey": pkey, "name": name,
                    "view": self.view_map and self.view_map.get(key),
                    "leaf": not subs or len(subs) == 0,
                    "icon": self.icon_map and self.icon_map.get(key),
                    # "open": self.open_map and self.open_map.get(key)
                    }

            if subs and len(subs) > 0:
                sub_items = self.build(subs, pkey=key, ppath=path, level=level + 1)
                if self.compose_mode == 'nested':
                    item['subs'] = [e for e in sub_items]
                    results.append(item)
                else:
                    results.append(item)
                    results.extend(sub_items)
            else:
                if self.compose_mode == 'nested':
                    item["subs"] = []
                results.append(item)
        return results


if __name__ == '__main__':

    m = Menu(menu, view_map=view)
    print(m.menu)
    print(m.options)
    print(m.current)
    print(m.history)
    print(m.statistics)
    print(m.open_map, '<<<<1')
    m.select('LAYOUT_ASPECTRATIO_MAP')
    print(m.current)
    print(m.history)
    print(m.statistics)
    print(m.open_map, '<<<<2')
    m.select('LAYOUT')
    print(m.current)
    print(m.history)
    print(m.statistics)
    print(m.open_map, '<<<<3')
    m.select('LAYOUT_ASPECTRATIO_MAP')
    print(m.current)
    print(m.history)
    print(m.statistics)
    print(m.open_map, '<<<<4')
    m.select('LAYOUT_ASPECTRATIO')
    print(m.current)
    print(m.history)
    print(m.statistics)
    print(m.open_map, '<<<<5')
    m.select('LAYOUT_ASPECTRATIO')
    print(m.current)
    print(m.history)
    print(m.statistics)
    print(m.open_map, '<<<<6')



