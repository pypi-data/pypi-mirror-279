from __future__ import annotations

from typing import Callable, Literal

from textual import work
from textual.app import ComposeResult, on
from textual.binding import Binding
from textual.containers import Horizontal
from textual.events import DescendantFocus
from textual.reactive import var
from textual.widgets import Footer, Header, Label
from textual.widgets import ListItem as ListItem_

from systema.models.connector import ConnectorCreate, ConnectorRead
from systema.models.node import NodeRead, NodeUpdate
from systema.models.project import ProjectRead
from systema.proxies.connector import ConnectorProxy
from systema.proxies.node import NodeProxy
from systema.tui.geometry import (
    ConnectorWrapper,
    NodeWidget,
    Point,
    Primitive,
)
from systema.tui.graph_viewer import (
    GraphViewer,
)
from systema.tui.screens.base import ProjectScreen
from systema.tui.widgets import ListView

Direction = Literal["up", "down", "left", "right"]


MAX_NODE_WIDTH = 50


class ListItem(ListItem_):
    def __init__(
        self,
        node: NodeRead,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            Label(node.name), name=name, id=id, classes=classes, disabled=disabled
        )
        self.node = node


def get_canvas_size(nodes: list[NodeRead]):
    min_x = min(n.x for n in nodes if n.x)
    min_y = min(n.y for n in nodes if n.y)
    max_x = max(n.x for n in nodes if n.x)
    max_y = max(n.y for n in nodes if n.y)
    size = (max_x - min_x + MAX_NODE_WIDTH, max_y - min_y + MAX_NODE_WIDTH)
    return size


class MindMapScreen(ProjectScreen):
    BINDINGS = [
        Binding("q,escape", "dismiss", "Quit", show=False),
        Binding("down,j", "focus_down", "Focus down", show=False),
        Binding("up,k", "focus_up", "Focus up", show=False),
        Binding("left,h", "focus_left", "Focus left", show=False),
        Binding("right,l", "focus_right", "Focus right", show=False),
        Binding("shift+down,J", "move_down", "Move down", show=False),
        Binding("shift+up,K", "move_up", "Move up", show=False),
        Binding("shift+left,H", "move_left", "Move left", show=False),
        Binding("shift+right,L", "move_right", "Move right", show=False),
        Binding("t", "toggle_collapsible", "Show/Hide side panel", show=True),
        Binding("m", "select_mode", "Select mode", show=True),
        Binding("r", "remove_from_mind_map", "Remove from mind map", show=True),
        Binding("c", "connect", "Connect current node", show=True),
        Binding("tab", "focus_next", show=False),
        Binding("shift+tab", "focus_next", show=False),
    ]
    CSS_PATH = "styles/mind-map.css"

    proxy: NodeProxy
    connector_proxy: ConnectorProxy
    container: GraphViewer = GraphViewer()
    current_node: NodeRead | NodeWidget | None = None
    nodes_without_position: ListView = ListView(classes="sidepane nodes")

    connect_mode: var[bool] = var(False)
    connect_mode_node_a: NodeWidget | None = None
    connect_mode_node_b: NodeWidget | None = None
    connectors_cache: list[ConnectorRead]

    def watch_connect_mode(self, value: bool):
        self.container.set_class(value, "connect-mode")

    def watch_project(self, project: ProjectRead | None):
        if project is None:
            return
        self.connector_proxy = ConnectorProxy(project.id)
        super().watch_project(project)

    async def clear(self):
        self.connectors_cache = []
        await self.container.remove_children()
        await self.nodes_without_position.clear()
        self.nodes_without_position.focus()

    async def populate(self):
        for node in self.proxy.all():
            if node.has_position:
                node_widget = NodeWidget(node)
                await self.container.mount(node_widget)
            else:
                self.nodes_without_position.append(ListItem(node))
            self.nodes_without_position.refresh()
        self.call_after_refresh(self.render_connectors)

    async def render_connectors(self):
        async with self.batch():
            self.connectors_cache = list(self.connector_proxy.all())
            await self.render_connectors_from_cache()

    async def render_connectors_from_cache(self):
        for conn in self.connectors_cache:
            a = self.container.get_child_by_id(f"node-{conn.a}", NodeWidget)
            b = self.container.get_child_by_id(f"node-{conn.b}", NodeWidget)
            c = ConnectorWrapper(a, b, f"node-conn-{conn.a} node-conn-{conn.b}")
            await self.container.mount(*c.widgets)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield self.nodes_without_position
            yield self.container
        yield Footer()

    @on(ListView.Highlighted)
    async def handle_listview_highlighted(self, message: ListView.Highlighted):
        if isinstance(message.item, ListItem):
            self.current_node = message.item.node

    @on(DescendantFocus)
    async def handle_descendant_focus(self, message: DescendantFocus):
        widget = message.widget
        if isinstance(widget, NodeWidget):
            if self.connect_mode:
                self.connect_mode_node_b = widget
                await self.container.remove_children(".temp")
                if self.connect_mode_node_a:
                    conn = ConnectorWrapper(
                        self.connect_mode_node_a,
                        widget,
                        f"node-conn-{self.connect_mode_node_a.node.id} node-conn-{widget.id} temp",
                    )
                    await self.container.mount_all(conn.widgets)
            else:
                self.current_node = widget
        elif isinstance(widget, ListView) and widget.has_class("nodes"):
            if isinstance(widget.highlighted_child, ListItem):
                self.current_node = widget.highlighted_child.node
        else:
            self.selected_event = None

    def _focus(self, direction: Direction):
        if self.nodes_without_position.has_focus and direction in ("left", "right"):
            self.focus_next(NodeWidget)
        self._focus_node(direction)

    def _focus_node(self, direction: Direction):
        curr = self.current_node
        if curr is None:
            return

        if not isinstance(curr, NodeWidget):
            return

        nodes = self._filter_nodes_by_direction(curr.center, direction)

        try:
            node = min(nodes, key=lambda n: n.center.get_distance_to(curr.center))
        except (KeyError, ValueError):
            return

        node.focus()

    def _filter_nodes_by_direction(self, origin: Point, direction: Direction):
        filters: dict[Direction, Callable[[Point], bool]] = {
            "right": lambda p: p.x > 0 and p.x * 2 >= abs(p.y),
            "left": lambda p: p.x < 0 and -p.x * 2 >= abs(p.y),
            "up": lambda p: p.y < 0 and -p.y >= abs(p.x * 2),
            "down": lambda p: p.y > 0 and p.y >= abs(p.x * 2),
        }
        for node in self.query(NodeWidget):
            relative_position = node.center - origin
            filter_ = filters[direction]
            if filter_(relative_position):
                yield node

    async def _move(self, direction: Direction):
        if self.current_node is None:
            return

        node = self.current_node
        if isinstance(node, NodeWidget):
            x, y = node.position
            if direction == "up":
                y -= 1
            elif direction == "down":
                y += 1
            elif direction == "left":
                x -= 2
            elif direction == "right":
                x += 2

            self.proxy.update(node.node.id, NodeUpdate(x=x, y=y))
            node.position = x, y
            async with self.batch():
                await self.container.remove_children(Primitive)
                await self.render_connectors_from_cache()

        elif isinstance(node, NodeRead):
            self.proxy.update(node.id, NodeUpdate(x=0, y=0))
            await self.safe_refresh()

    def action_toggle_collapsible(self):
        self.nodes_without_position.toggle_class("collapsed")

    def action_focus_down(self):
        self._focus("down")

    def action_focus_up(self):
        self._focus("up")

    def action_focus_left(self):
        self._focus("left")

    def action_focus_right(self):
        self._focus("right")

    async def action_move_down(self):
        await self._move("down")

    async def action_move_up(self):
        await self._move("up")

    async def action_move_left(self):
        await self._move("left")

    async def action_move_right(self):
        await self._move("right")

    async def action_remove_from_mind_map(self):
        if self.current_node and isinstance(self.current_node, NodeWidget):
            self.proxy.update(self.current_node.node.id, NodeUpdate(x=None, y=None))
        await self.safe_refresh()

    @work
    async def action_connect(self):
        if not isinstance(self.current_node, NodeWidget):
            return

        if not self.connect_mode:
            self.connect_mode_node_a = self.current_node
        else:
            if (
                self.connect_mode_node_a
                and self.connect_mode_node_b
                and self.connect_mode_node_a != self.connect_mode_node_b
            ):
                created_conn = self.connector_proxy.create(
                    ConnectorCreate(
                        a=self.connect_mode_node_a.node.id,
                        b=self.connect_mode_node_b.node.id,
                    ),
                )
                self.query(Primitive).filter(".temp").remove_class("temp")
                self.connectors_cache.append(created_conn)
            self.connect_mode_node_a = None

        self.connect_mode = not self.connect_mode

    @on(ListView.Selected)
    def print_event_info(self, message: ListView.Selected):
        if isinstance(message.item, ListItem):
            e = message.item.node
            self.notify(e.model_dump_json())

    async def action_focus_next(self):
        if self.connect_mode:
            self.focus_next(NodeWidget)
        else:
            self.focus_next()

    def dismiss(self, result=None):
        if self.connect_mode:
            self.connect_mode = False
            self.query(Primitive).filter(".temp").remove()
        else:
            return super().dismiss(result)
