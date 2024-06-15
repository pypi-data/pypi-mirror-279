from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select

from systema.models.event import EventCreate, EventRead, EventUpdate, TimeUnit


class EventModal(ModalScreen[EventCreate | EventUpdate]):
    CSS_PATH = "styles/event-modal.css"
    BINDINGS = [
        ("enter", "submit", "Submit"),
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(
        self,
        event: EventRead | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        self.event = event
        self.form_data = {}
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        is_for_creation = self.event is None
        with Vertical():
            yield Label("Event")
            yield Input(
                placeholder="Name",
                name="name",
                value=self.event.name if self.event else "",
            )
            yield Input(
                placeholder="Reference date",
                name="reference_timestamp",
                value=(
                    self.event.reference_timestamp.isoformat()
                    if self.event and self.event.reference_timestamp
                    else ""
                ),
            )
            yield Input(
                placeholder="Duration",
                name="duration",
                value=(
                    str(self.event.duration)
                    if self.event and self.event.duration
                    else ""
                ),
            )
            yield Select(
                [(i.name.lower(), i.value) for i in TimeUnit],
                name="duration_unit",
                value=self.event.duration_unit if self.event else TimeUnit.MINUTES,
            )
            with Horizontal():
                yield Button("Cancel", "default", id="cancel")
                yield Button(
                    "Create" if is_for_creation else "Update", "primary", id="submit"
                )

    def action_submit(self):
        if self.event:
            changed_data = EventUpdate(**self.form_data)
            original_data = EventUpdate.model_validate(self.event)
            if changed_data == original_data:
                self.notify("Nothing to update")
                self.dismiss()
                return
            return_value = changed_data
        else:
            return_value = EventCreate(**self.form_data)
        self.dismiss(return_value)
        self.clear()

    def action_cancel(self):
        self.dismiss()
        self.clear()

    def clear(self):
        for i in self.query(Input):
            i.clear()
        for i in self.query(Select):
            i.clear()
        self.query(Input).first().focus()

    @on(Input.Changed)
    def handle_input_changed(self, message: Input.Changed):
        self.form_data[message.input.name] = message.value

    @on(Select.Changed)
    def handle_select_changed(self, message: Select.Changed):
        self.form_data[message.select.name] = message.value

    @on(Input.Submitted)
    def handle_input_submitted(self, _: Input.Submitted):
        self.action_submit()

    @on(Button.Pressed)
    def handle_button_pressed(self, message: Button.Pressed):
        actions = {"submit": self.action_submit, "cancel": self.action_cancel}
        if id := message.button.id:
            actions[id]()
