from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button

from systema.models.project import ProjectRead
from systema.proxies.node import NodeProxy
from systema.tui.widgets import Select


class NodeSelection(ModalScreen[str]):
    BINDINGS = [
        ("enter", "submit", "Submit"),
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(
        self,
        project: ProjectRead,
        exclude: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.project = project
        self.proxy = NodeProxy(self.project.id)
        self.exclude = exclude

    def compose(self) -> ComposeResult:
        self.load_options()

        self.select = Select(self.options)
        yield self.select
        yield Button("Confirm", id="confirm")
        yield Button("Cancel", id="cancel")

    def load_options(self):
        self.loading = True
        self.options = [
            (n.name, n.id)
            for n in self.proxy.all()
            if n.has_position and n.id != self.exclude
        ]
        self.loading = False

    def action_confirm(self):
        selected = self.select.value
        if isinstance(selected, str):
            self.dismiss(selected)

    def action_cancel(self):
        self.dismiss()

    @on(Button.Pressed)
    def handle_button_pressed(self, message: Button.Pressed):
        actions = {"confirm": self.action_confirm, "cancel": self.action_cancel}
        if id := message.button.id:
            actions[id]()
