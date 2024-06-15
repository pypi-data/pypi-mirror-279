from __future__ import annotations

import enum
from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal

from textual.geometry import Offset
from textual.reactive import reactive
from textual.widget import Widget

from systema.models.node import NodeRead

Point = Offset


class NodeWidget(Widget):
    DEFAULT_CSS = """
    NodeWidget {
        height: auto;
        width: auto;
        padding: 0;
        border: round $primary;
        layer: nodes;

        &:focus {
            border: round $secondary;
        }
    }
    """
    position: reactive[tuple[int, int]] = reactive((0, 0))

    def __init__(
        self,
        node: NodeRead,
        name: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            name=name, id=f"node-{node.id}", classes=classes, disabled=disabled
        )
        self.node = node
        self.can_focus = True
        if node.x is None or node.y is None:
            raise ValueError
        self.position = node.x, node.y

    def render(self):
        if self.position:
            self.styles.offset = self.position
        return self.node.name

    @property
    def center(self):
        pos = Point(*self.position)
        pos += (self.outer_size.width // 2, self.outer_size.height // 2)
        return pos


class Primitive(Widget):
    DEFAULT_CSS = """
    Primitive {
        background: transparent;
        color: $secondary;
        border: none;
        layer: primitives;
    }
    """

    position: Point = Point()

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.styles.offset = self.position.x, self.position.y


class _Line(Primitive):
    DEFAULT_CSS = """
    _Line {
        height: 1;
        width: 1;
    }
    """

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        position: Point = Point(0, 0),
        length: int = 1,
        sign: bool = True,
    ) -> None:
        self.position = position
        self.length = length
        self.sign = sign
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)


class _Char(Primitive):
    DEFAULT_CSS = """
    _Char {
        height: 1;
        width: 1;
    }
    """

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        position: Point = Point(0, 0),
        char: str = ".",
    ) -> None:
        self.position = position
        self.char = char
        if classes:
            classes += " segment"
        else:
            classes = "segment"
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def render(self):
        return self.char


class VerticalLine(_Line):
    def render(self):
        x, y = self.position.x, self.position.y
        if not self.sign:
            y -= self.length - 1
        self.styles.offset = x, y
        self.styles.width = 1
        self.styles.height = self.length
        return "│" * self.length


class HorizontalLine(_Line):
    def render(self):
        x, y = self.position.x, self.position.y
        if not self.sign:
            x -= self.length - 1
        self.styles.offset = x, y
        self.styles.height = 1
        self.styles.width = self.length
        return "─" * self.length


def comparison_map(a: int, b: int):
    if a > b:
        return 1
    if a < b:
        return -1
    return 0


class Direction(enum.Enum):
    V = enum.auto()
    H = enum.auto()

    def shift(self):
        if self == Direction.H:
            return Direction.V
        return Direction.H


class TerminalType(enum.Enum):
    START = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


class Orientation(enum.Enum):
    NE = enum.auto()
    NW = enum.auto()
    SE = enum.auto()
    SW = enum.auto()

    def flip(self, direction: Direction):
        map = {
            Direction.V: {
                Orientation.NE: Orientation.SE,
                Orientation.NW: Orientation.SW,
                Orientation.SE: Orientation.NE,
                Orientation.SW: Orientation.NW,
            },
            Direction.H: {
                Orientation.NE: Orientation.NW,
                Orientation.NW: Orientation.NE,
                Orientation.SE: Orientation.SW,
                Orientation.SW: Orientation.SE,
            },
        }
        return map[direction][self]


@dataclass
class Segment:
    @abstractmethod
    def _get_widget(self) -> Widget:
        pass

    def get_widget(self, classes=""):
        widget = self._get_widget()
        widget.add_class(*classes.split(" "))
        return widget


@dataclass
class Terminal(Segment):
    char_map = {
        TerminalType.START: "⭘",
        TerminalType.UP: "▲",
        TerminalType.DOWN: "▼",
        TerminalType.LEFT: "◀",
        TerminalType.RIGHT: "▶",
    }

    point: Point
    terminal_type: TerminalType

    def _get_widget(self):
        return _Char(position=self.point, char=self.char_map[self.terminal_type])


@dataclass
class Line(Segment):
    widget_map = {
        Direction.V: VerticalLine,
        Direction.H: HorizontalLine,
    }

    point: Point
    direction: Direction
    length: int
    sign: bool

    def _get_widget(self):
        return self.widget_map[self.direction](
            position=self.point, length=self.length, sign=self.sign
        )


@dataclass
class Elbow(Segment):
    char_map = {
        Orientation.NE: "╮",
        Orientation.NW: "╭",
        Orientation.SE: "╯",
        Orientation.SW: "╰",
    }
    point: Point
    orientation: Orientation

    def _get_widget(self):
        return _Char(position=self.point, char=self.char_map[self.orientation])


class ConnectorWrapper:
    direction: Direction
    rightwards: Literal[-1, 0, 1]
    downwards: Literal[-1, 0, 1]
    start: Point
    end: Point
    segments: list[Segment]

    def __init__(self, a: NodeWidget, b: NodeWidget, classes: str = "") -> None:
        self.a = a
        self.b = b
        self.classes = classes

        self._set_directions()
        self._set_terminations()
        self._build()

    def _set_directions(self):
        start_center = self.a.center
        end_center = self.b.center
        self.direction = (
            Direction.H
            if abs(end_center.x - start_center.x) >= abs(end_center.y - start_center.y)
            else Direction.V
        )
        self.rightwards = comparison_map(end_center.x, start_center.x)
        self.downwards = comparison_map(end_center.y, start_center.y)

    def _set_terminations(self):
        self.start = Point(*self.a.position)
        self.end = Point(*self.b.position)
        if self.direction == Direction.V:
            height_a = self.a.outer_size.height
            height_b = self.b.outer_size.height
            half_width_a = self.a.outer_size.width // 2
            half_width_b = self.b.outer_size.width // 2
            if self.downwards == 1:
                self.start += (half_width_a, height_a - 1)
                self.end += (half_width_b, 0)
            elif self.downwards == -1:
                self.start += (half_width_a, 0)
                self.end += (half_width_b, height_b - 1)
        elif self.direction == Direction.H:
            w_a = self.a.outer_size.width
            w_b = self.b.outer_size.width
            if self.rightwards == 1:
                self.start += (w_a - 1, self.a.outer_size.height // 2)
                self.end += (0, self.b.outer_size.height // 2)
            elif self.rightwards == -1:
                self.start += (0, self.a.outer_size.height // 2)
                self.end += (w_b - 1, self.b.outer_size.height // 2)

    def _build(self):
        self.segments = []
        is_null = self.start.get_distance_to(self.end) == 0
        if is_null:
            return

        cursor = self.start
        cursor = self._add_start_terminal(cursor)

        is_straight = not self.downwards or not self.rightwards
        if is_straight:
            cursor = self._add_straight_body(cursor)
        else:
            cursor = self._add_first_body_half(cursor)

            cursor = self._add_first_elbow(cursor)
            cursor = self._add_step(cursor)
            cursor = self._add_second_elbow(cursor)

            cursor = self._add_second_body_half(cursor)

        cursor = self._add_end_terminal(cursor)

    def _add_segment(self, segment: Segment):
        self.segments.append(segment)

    def _add_start_terminal(self, cursor: Point):
        self._add_segment(Terminal(cursor, TerminalType.START))
        if self.direction == Direction.H:
            cursor += Point(self.rightwards, 0)
        else:
            cursor += Point(0, self.downwards)
        return cursor

    def _add_straight_body(self, cursor: Point):
        end = self.end
        length = int(cursor.get_distance_to(end))
        if self.direction == Direction.H:
            sign = self.rightwards == 1
        else:
            sign = self.downwards == 1
        if length >= 1:
            self._add_segment(Line(cursor, self.direction, length, sign))
        if self.direction == Direction.H:
            cursor += Point(self.rightwards * length, 0)
        else:
            cursor += Point(0, self.downwards * length)
        return cursor

    def _add_first_body_half(self, cursor: Point):
        end = self.end
        if self.direction == Direction.H:
            length = abs((end.x - cursor.x) // 2)
            sign = self.rightwards == 1
        else:
            length = abs((end.y - cursor.y) // 2)
            sign = self.downwards == 1
        self._add_segment(Line(cursor, self.direction, length, sign))
        if self.direction == Direction.H:
            cursor += Point(self.rightwards * length, 0)
        else:
            cursor += Point(0, self.downwards * length)
        return cursor

    def _add_first_elbow(self, cursor: Point):
        orientation = Orientation.NE
        if self.rightwards == -1:
            orientation = orientation.flip(Direction.H)
        if self.downwards == -1:
            orientation = orientation.flip(Direction.V)
        if self.direction == Direction.V:
            orientation = orientation.flip(Direction.H).flip(Direction.V)
        self._add_segment(Elbow(cursor, orientation))
        if self.direction.shift() == Direction.H:
            cursor += Point(self.rightwards, 0)
        else:
            cursor += Point(0, self.downwards)
        return cursor

    def _add_step(self, cursor: Point):
        end = self.end
        if self.direction.shift() == Direction.H:
            length = abs(end.x - cursor.x)
            sign = self.rightwards == 1
        else:
            length = abs(end.y - cursor.y)
            sign = self.downwards == 1
        self._add_segment(Line(cursor, self.direction.shift(), length, sign))

        if self.direction.shift() == Direction.H:
            cursor += Point(self.rightwards * length, 0)
        else:
            cursor += Point(0, self.downwards * length)
        return cursor

    def _add_second_elbow(self, cursor: Point):
        orientation = Orientation.SW
        if self.rightwards == -1:
            orientation = orientation.flip(Direction.H)
        if self.downwards == -1:
            orientation = orientation.flip(Direction.V)
        if self.direction == Direction.V:
            orientation = orientation.flip(Direction.H).flip(Direction.V)
        self._add_segment(Elbow(cursor, orientation))
        if self.direction == Direction.H:
            cursor += Point(self.rightwards, 0)
        else:
            cursor += Point(0, self.downwards)
        return cursor

    def _add_second_body_half(self, cursor: Point):
        end = self.end
        if self.direction == Direction.H:
            length = abs(end.x - cursor.x)
            sign = self.rightwards == 1
        else:
            length = abs(end.y - cursor.y)
            sign = self.downwards == 1
        self._add_segment(Line(cursor, self.direction, length, sign))
        if self.direction == Direction.H:
            cursor += Point(self.rightwards * length, 0)
        else:
            cursor += Point(0, self.downwards * length)
        return cursor

    def _add_end_terminal(self, cursor: Point):
        if self.direction == Direction.H:
            sign = self.rightwards == 1
            terminal_type = TerminalType.RIGHT if sign else TerminalType.LEFT
        else:
            sign = self.downwards == 1
            terminal_type = TerminalType.DOWN if sign else TerminalType.UP
        self._add_segment(Terminal(cursor, terminal_type))
        if self.direction == Direction.H:
            cursor += Point(self.rightwards, 0)
        else:
            cursor += Point(0, self.downwards)
        return cursor

    @property
    def widgets(self):
        for segment in self.segments:
            widget = segment.get_widget(classes=self.classes)
            yield widget
