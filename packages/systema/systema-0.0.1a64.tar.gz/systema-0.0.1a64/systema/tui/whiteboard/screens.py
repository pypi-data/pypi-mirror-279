from typing import Callable, Literal

from textual import on, work
from textual.app import ComposeResult, events
from textual.binding import Binding
from textual.geometry import Offset
from textual.screen import ModalScreen, Screen
from textual.widgets import Footer, Header, Input

from systema.tui.graph_viewer import GraphViewer
from systema.tui.screens.confirmation import Confirmation
from systema.tui.whiteboard.commands import (
    AddBox,
    CommandStack,
    DeleteBox,
    MoveBox,
    ScreenCommandStack,
)
from systema.tui.whiteboard.widgets import Box

Direction = Literal["up", "down", "left", "right"]


class BoxForm(ModalScreen[str]):
    DEFAULT_CSS = """
    BoxForm {
        align: center middle;

        & > Input {
            width: 30;
        }
    }
    """

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Type a text")

    @on(Input.Submitted)
    def handle_input_submitted(self, message: Input.Submitted):
        if text := message.input.value:
            self.dismiss(text)

    async def handle_key(self, event: events.Key) -> bool:
        if event.key == "escape":
            self.dismiss()

        return await super().handle_key(event)


class Whiteboard(Screen):
    _curr_el: Box | None = None
    BINDINGS = [
        Binding("q,escape", "dismiss", "Quit", show=True),
        Binding("a", "add", "Add box", show=True),
        Binding("d", "delete", "Delete box", show=True),
        Binding("space", "cmd", "Commands", show=True),
        Binding("tab", "focus_next", "Focus next", show=True),
        Binding("h", "focus_left", "Focus left", show=False),
        Binding("l", "focus_right", "Focus right", show=False),
        Binding("j", "focus_down", "Focus down", show=False),
        Binding("k", "focus_up", "Focus up", show=False),
        Binding("H", "move_left", "Move left", show=False),
        Binding("L", "move_right", "Move right", show=False),
        Binding("J", "move_down", "Move down", show=False),
        Binding("K", "move_up", "Move up", show=False),
        Binding("u", "undo", "Undo", show=False),
        Binding("r", "redo", "Redo", show=False),
    ]
    DEFAULT_CSS = """
    Whiteboard {
        & > GraphViewer {
            width: 100%;
            height: 100%;
            border: round $primary;
        }
    }
    """

    container: GraphViewer = GraphViewer()
    commands: CommandStack = CommandStack()

    def compose(self) -> ComposeResult:
        self._curr_el = None
        self.commands = ScreenCommandStack()
        self.commands.screen = self
        self.container.can_focus_children = True
        yield Header()
        yield self.container
        yield Footer()

    @on(events.DescendantFocus)
    def handle_descendant_focus(self, message: events.DescendantFocus):
        widget = message.widget
        if isinstance(widget, Box):
            self.notify(widget.text)
            self._curr_el = widget
            widget.styles.border = ("solid", "red")

    @on(events.DescendantBlur)
    def handle_descendant_blur(self, message: events.DescendantBlur):
        widget = message.widget
        if isinstance(widget, Box):
            self._curr_el = None
            widget.styles.border = ("solid", "transparent")

    @on(Box.Mount)
    def handle_box_mount(self, message: Box.Mount):
        widget = message.widget
        if isinstance(widget, Box):
            widget.focus()

    async def move(self, direction: Direction):
        if self._curr_el is None:
            self.notify("no curr")
            return

        if isinstance(self._curr_el, Box):
            cmd = MoveBox(self, self._curr_el, direction)
            await self.commands.new(cmd)

    def _focus(self, direction: Direction):
        if self._curr_el is None:
            self.query(Box).first().focus()
            return

        if not isinstance(self._curr_el, Box):
            return

        nodes = self._filter_nodes_by_direction(self._curr_el.center, direction)

        try:
            node = min(nodes, key=lambda n: n.get_distance_to(self._curr_el))
        except (KeyError, ValueError):
            return

        node.focus()

    def _filter_nodes_by_direction(self, origin: Offset, direction: Direction):
        filters: dict[Direction, Callable[[Offset], bool]] = {
            "right": lambda p: p.x > 0 and p.x * 2 >= abs(p.y),
            "left": lambda p: p.x < 0 and -p.x * 2 >= abs(p.y),
            "up": lambda p: p.y < 0 and -p.y >= abs(p.x * 2),
            "down": lambda p: p.y > 0 and p.y >= abs(p.x * 2),
        }
        for node in self.query(Box):
            relative_position = node.center - origin
            filter_ = filters[direction]
            if filter_(relative_position):
                yield node

    async def action_move_up(self):
        await self.move("up")

    async def action_move_down(self):
        await self.move("down")

    async def action_move_right(self):
        await self.move("right")

    async def action_move_left(self):
        await self.move("left")

    def action_focus_up(self):
        self._focus("up")

    def action_focus_down(self):
        self._focus("down")

    def action_focus_right(self):
        self._focus("right")

    def action_focus_left(self):
        self._focus("left")

    async def action_undo(self):
        await self.commands.undo()

    async def action_redo(self):
        await self.commands.redo()

    @work
    async def action_add(self):
        if text := await self.app.push_screen_wait(BoxForm()):
            box = Box(text)
            cmd = AddBox(self, box)
            await self.commands.new(cmd)

    @work
    async def action_delete(self):
        global _curr_el
        if self._curr_el and await self.app.push_screen_wait(
            Confirmation("Delete box?")
        ):
            cmd = DeleteBox(self, self._curr_el)
            await self.commands.new(cmd)

    def has_widget_at(self, x: int, y: int):
        return any(box.overlaps(x, y) for box in self.query(Box))
