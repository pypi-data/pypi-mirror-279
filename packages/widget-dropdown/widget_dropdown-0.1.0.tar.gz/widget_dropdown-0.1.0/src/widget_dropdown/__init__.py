import importlib.metadata
import pathlib

import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("widget_dropdown")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class DropdownWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"

    placeholder_text = traitlets.Unicode("Select an option").tag(sync=True)
    selected_value = traitlets.Unicode("").tag(sync=True)
    options = traitlets.List([]).tag(sync=True)

    def __init__(self, options=None, **kwargs):
        """Method to create the widget.

        The traitlets defined above can be set as a kwargs.
        """
        super().__init__(**kwargs)
        if options:
            self.options = options
        else:
            self.options = [{"value": "", "text": "No options", "disabled": True}]
