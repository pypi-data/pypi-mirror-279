from pathlib import Path

from reactpy.web.module import module_from_file
from reactpy.web.module import export

_js_module = module_from_file(
    "rpysuite",
    file=Path(__file__).parent / "../bundle.js",
    fallback="⏳",
)
def export_component(name):
    return export(_js_module, name)
