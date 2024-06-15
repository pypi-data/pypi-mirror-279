from __future__ import annotations

from dataclasses import dataclass

from textual.app import RenderResult, events
from textual.geometry import Offset, Region
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget


class Box(Widget):
    @dataclass
    class Mount(Message):
        widget: Box

    DEFAULT_CSS = """
    Box {
        width: auto;
        height: auto;
    }
    """
    position: reactive[tuple[int, int]] = reactive((0, 0))
    can_focus = True

    def __init__(
        self,
        text: str = "",
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            *children, name=name, id=id, classes=classes, disabled=disabled
        )
        self.can_focus = True
        self.text = text

    def _on_mount(self, event: events.Mount) -> None:
        self.post_message(Box.Mount(self))
        return super()._on_mount(event)

    def watch_position(self, pos: tuple[int, int] | None):
        if pos:
            self.styles.offset = pos

    def render(self) -> RenderResult:
        if self.position:
            self.styles.offset = self.position
        return self.text

    @property
    def width(self):
        self.outer_size.width

    def overlaps(self, x: int, y: int):
        r = Region(*self.position, self.outer_size.width, self.outer_size.height)
        return r.contains(x, y)

    @property
    def center(self):
        pos = Offset(*self.position)
        pos += (self.outer_size.width // 2, self.outer_size.height // 2)
        return pos

    def get_distance_to(self, box: Box | None):
        if box is None:
            return 0.0
        return self.center.get_distance_to(box.center)

    def clone(self):
        box = Box(self.text)
        box.position = self.position
        box.styles.background = self.styles.background
        box.styles.border = self.styles.border
        return box
