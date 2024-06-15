import asyncio

from textual import on, work
from textual.app import App, UnknownModeError
from textual.binding import Binding

from systema.management import Settings
from systema.models.project import ProjectRead
from systema.proxies.card import CardProxy
from systema.proxies.event import EventProxy
from systema.proxies.item import ItemProxy
from systema.proxies.node import NodeProxy
from systema.proxies.project import ProjectProxy
from systema.tui.screens.base import ProjectScreen
from systema.tui.screens.calendar import CalendarScreen
from systema.tui.screens.checklist import ChecklistScreen
from systema.tui.screens.config import Config
from systema.tui.screens.dashboard import Dashboard
from systema.tui.screens.kanban import KanbanScreen
from systema.tui.screens.mind_map import MindMapScreen
from systema.tui.screens.mode_modal import Mode, ModeModal
from systema.tui.screens.project_list import ProjectList
from systema.tui.whiteboard.screens import Whiteboard

PROJECT_SCREENS: dict[Mode, ProjectScreen] = {
    Mode.CHECKLIST: ChecklistScreen(ItemProxy),
    Mode.KANBAN: KanbanScreen(CardProxy),
    Mode.CALENDAR: CalendarScreen(EventProxy),
    Mode.MIND_MAP: MindMapScreen(NodeProxy),
}


class SystemaTUIApp(App[None]):
    TITLE = "Systema"
    BINDINGS = [
        Binding("q,escape", "quit", "Quit", show=True),
        Binding("up,k", "focus_previous", "Focus previous", show=False),
        Binding("down,j", "focus_next", "Focus next", show=False),
    ]
    CSS_PATH = "style.css"
    SCREENS = {
        "projects": ProjectList,
        "whiteboard": Whiteboard,
        "mode": ModeModal,
        **PROJECT_SCREENS,
    }
    MODES = {
        "main": Dashboard,
        "config": Config,
        **PROJECT_SCREENS,
    }
    project: ProjectRead | None = None
    COMMANDS = set()

    async def on_mount(self):
        await self.switch_mode("main")

    @on(ProjectList.Selected)
    async def handle_project_selection(self, message: ProjectList.Selected):
        self.project = message.project
        for mode in Mode:
            if screen := PROJECT_SCREENS.get(mode):
                screen.project = self.project

        if self.project:
            await self.switch_to_project_mode(
                self.project.mode or Settings().default_mode
            )

    @work
    async def action_select_mode(self):
        if not self.project:
            return

        mode = await self.push_screen_wait("mode")
        if mode == self.current_mode:
            return

        await self.switch_to_project_mode(mode)

    async def switch_to_project_mode(self, mode: Mode):
        try:
            screen = PROJECT_SCREENS[mode]
            self.call_next(screen.safe_refresh)
            await asyncio.gather(
                self.switch_mode(mode),
                self.save_mode(mode),
            )
        except (UnknownModeError, KeyError):
            self.notify("Mode not implemented yet", severity="error")

    async def save_mode(self, mode: Mode):
        if self.project:
            ProjectProxy().save_mode(self.project.id, mode)


if __name__ == "__main__":
    SystemaTUIApp().run()
