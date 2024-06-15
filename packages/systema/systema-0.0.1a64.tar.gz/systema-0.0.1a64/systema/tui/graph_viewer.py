from textual.widget import Widget

from .layouts import FreeLayout


class GraphViewer(Widget):
    DEFAULT_CSS = """
    GraphViewer {
        layers: nodes primitives;
    }
    """
    SCOPED_CSS = False

    def __init__(
        self,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            *children, name=name, id=id, classes=classes, disabled=disabled
        )
        self._default_layout = FreeLayout()
