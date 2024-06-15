from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal

from textual.color import Color

from systema.tui.whiteboard.widgets import Box

if TYPE_CHECKING:
    from systema.tui.whiteboard.screens import Whiteboard

Direction = Literal["up", "down", "left", "right"]


class Command(ABC):
    @abstractmethod
    async def execute(self):
        pass

    @abstractmethod
    async def undo(self):
        pass


class CommandStack:
    def __init__(self) -> None:
        self._stack: list[Command] = []
        self._pointer: int = -1

    async def new(self, cmd: Command):
        await cmd.execute()
        self._stack = self._stack[: self._pointer + 1]
        self._pointer += 1
        self._stack.append(cmd)

    async def undo(self):
        if self._pointer <= -1:
            raise IndexError

        cmd = self._stack[self._pointer]
        self._pointer -= 1
        await cmd.undo()

    async def redo(self):
        if self._pointer >= len(self._stack) - 1:
            raise IndexError

        self._pointer += 1
        cmd = self._stack[self._pointer]
        await cmd.execute()


class ScreenCommandStack(CommandStack):
    async def undo(self):
        try:
            return await super().undo()
        except IndexError:
            self.screen.notify("Nothing to undo.")

    async def redo(self):
        try:
            return await super().redo()
        except IndexError:
            self.screen.notify("Nothing to redo.")

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen: Whiteboard):
        self._screen = screen


class AddBox(Command):
    def __init__(self, screen: Whiteboard, box: Box) -> None:
        self.prev_focus = screen._curr_el
        self.screen = screen
        self.box = box
        x, y = (0, 0)
        while self.screen.has_widget_at(x, y):
            y += 5

        self.box.position = (x, y)
        self.box.styles.background = Color(0, 0, 0, 0)
        self.box.styles.border = ("solid", "transparent")

    async def execute(self):
        self.box = self.box.clone()
        self.screen.container.mount(self.box)
        self.screen._curr_el = self.box

    async def undo(self):
        self.box.blur()
        await self.box.remove()
        if isinstance(self.prev_focus, Box):
            self.prev_focus.focus()


class DeleteBox(Command):
    def __init__(self, screen: Whiteboard, box: Box) -> None:
        self.screen = screen
        self.box = box

    async def execute(self):
        self.box.blur()
        await self.box.remove()
        if self.screen._curr_el is self.box:
            self.screen._curr_el = None

    async def undo(self):
        self.box = self.box.clone()
        self.screen.container.mount(self.box)
        self.box.focus()


class MoveBox(Command):
    def __init__(self, screen: Whiteboard, box: Box, direction: Direction) -> None:
        self.screen = screen
        self.box = box
        self.direction = direction

    def _flip(self):
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        self.direction = opposites[self.direction]

    async def execute(self):
        x, y = self.box.position

        if self.direction == "down":
            y += 1
        elif self.direction == "up":
            y -= 1
        elif self.direction == "right":
            x += 2
        elif self.direction == "left":
            x -= 2

        self.box.position = (x, y)

    async def undo(self):
        self._flip()
        await self.execute()
        self._flip()
