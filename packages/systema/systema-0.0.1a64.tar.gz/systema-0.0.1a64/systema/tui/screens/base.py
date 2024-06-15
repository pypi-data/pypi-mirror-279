from abc import ABC, abstractmethod
from typing import TypeVar

from textual import on
from textual.app import ScreenStackError, events
from textual.reactive import var
from textual.screen import Screen

from systema.models.project import ProjectRead
from systema.proxies.base import Proxy


class BaseProjectScreen(ABC):
    @abstractmethod
    def get_proxy_type(self) -> type[Proxy[ProjectRead]]:
        pass


_Proxy = TypeVar("_Proxy", bound=Proxy)


class ProjectScreen(Screen[None]):
    project: var[ProjectRead | None] = var(None)

    def __init__(
        self,
        proxy_type: type[_Proxy],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.proxy_type = proxy_type
        self.loading = True

    def watch_project(self, project: ProjectRead | None):
        if project:
            self.sub_title = project.name
            self.proxy = self.proxy_type(project.id)

    @abstractmethod
    async def populate(self):
        raise NotImplementedError(
            f"Class {self.__class__.__name__} must implement method populate"
        )

    @abstractmethod
    async def clear(self):
        raise NotImplementedError(
            f"Class {self.__class__.__name__} must implement method clear"
        )

    @on(events.ScreenResume)
    async def handle_screen_resume(self, _: events.ScreenResume):
        self.loading = False

    async def safe_refresh(self):
        if hasattr(self, "proxy"):
            await self.clear()
            await self.populate()

    def dismiss(self, result=None):
        try:
            self.loading = True
            return super().dismiss(result)
        except ScreenStackError:
            self.app.switch_mode("main")
