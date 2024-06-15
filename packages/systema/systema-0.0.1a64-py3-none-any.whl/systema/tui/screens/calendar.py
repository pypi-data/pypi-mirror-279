from datetime import date, datetime, timedelta
from typing import Literal

from textual import on, work
from textual.app import ComposeResult, events
from textual.binding import Binding
from textual.containers import Grid, Horizontal, Vertical
from textual.reactive import var
from textual.widgets import Button, Footer, Header, Label, ListItem

from systema.models.event import EventCreate, EventRead, EventUpdate
from systema.proxies.event import EventProxy
from systema.tui.screens.base import ProjectScreen
from systema.tui.screens.confirmation import Confirmation
from systema.tui.screens.event_modal import EventModal
from systema.tui.widgets import EventCalendarDay, EventListItem, ListView
from systema.utils import (
    get_final_date_of_monthly_calendar,
    get_initial_date_of_monthly_calendar,
)


class CalendarScreen(ProjectScreen):
    BINDINGS = [
        Binding("q,escape", "dismiss", "Quit"),
        Binding("n", "next_month", "Next month", show=True),
        Binding("p", "previous_month", "Previous month", show=True),
        Binding("r", "remove_from_calendar", "Remove from calendar", show=True),
        Binding("a", "add_event", "Add", show=True),
        Binding("e", "edit_event", "Edit", show=True),
        Binding("d", "delete_event", "Delete", show=True),
        Binding("shift+right,L", "move_right", "Move right", show=True),
        Binding("shift+left,H", "move_left", "Move left", show=True),
        Binding("shift+up,K", "move_up", "Move up", show=True),
        Binding("shift+down,J", "move_down", "Move down", show=True),
        Binding("left,h", "focus_left", "Focus left", show=False),
        Binding("right,l", "focus_right", "Focus right", show=False),
        Binding("t", "toggle_collapsible", "Show/Hide side panel", show=True),
        Binding("m", "select_mode", "Select mode", show=True),
    ]
    CSS_PATH = "styles/calendar.css"

    proxy: EventProxy
    datetime_label: Label = Label()
    days: list[EventCalendarDay] = [EventCalendarDay() for _ in range(7 * 6)]
    grid: Grid

    month_year: var[tuple[int, int]] = var(
        (datetime.today().month, datetime.today().year)
    )
    selected_event: EventRead | None = None
    events_without_date = ListView(classes="sidepane events")

    def compose(self) -> ComposeResult:
        today = datetime.today()
        self.grid = Grid(*self.days)
        self.month_year = (today.month, today.year)

        yield Header()
        with Horizontal():
            yield self.events_without_date
            with Vertical(classes="calendar-container"):
                with Horizontal(classes="topbar"):
                    yield Button("Previous", classes="previous")
                    yield self.datetime_label
                    yield Button("Next", classes="next")

                yield self.grid
        yield Footer()

    @property
    def reference_date(self):
        month, year = self.month_year
        return date(year, month, 1)

    @property
    def initial_date(self):
        month, year = self.month_year
        initial_date = get_initial_date_of_monthly_calendar(year, month)
        return initial_date

    async def watch_month_year(self, month_year: tuple[int, int]):
        month, year = month_year

        self.datetime_label.update(date(year, month, 1).strftime("%b %Y"))

        initial_date = get_initial_date_of_monthly_calendar(year, month)
        final_date = get_final_date_of_monthly_calendar(year, month)

        qty_days = (final_date - initial_date).days
        weeks = qty_days // 7
        if qty_days % 7:
            weeks += 1

        self.grid.styles.grid_size_rows = weeks

        for day, offset in zip(self.days, range((final_date - initial_date).days + 1)):
            date_ = initial_date + timedelta(days=offset)
            day.dt = date_
            day.set_class(date_.month == month, "current-month")
            day.set_class(date_ == datetime.today().date(), "today")

        await self.clear()
        await self.populate()

    async def highlight_event(self, event: EventRead | None):
        if event is None:
            return

        for list_view in self.query(ListView).filter(".events"):
            for idx, list_item in enumerate(list_view.query(ListItem)):
                if (
                    isinstance(list_item, EventListItem)
                    and list_item.event.id == event.id
                ):
                    list_view.focus()
                    list_view.index = idx

    async def populate(self):
        for event in self.proxy.all():
            if event.reference_timestamp is None:
                self.events_without_date.append(EventListItem(event=event))
            else:
                delta = (event.reference_timestamp.date() - self.initial_date).days
                if delta >= 0:
                    try:
                        widget = self.days[delta]
                        await widget.add(event)
                    except IndexError:
                        pass

    async def clear(self):
        await self.events_without_date.clear()
        for days in self.days:
            await days.clear()

    def action_toggle_collapsible(self):
        self.events_without_date.toggle_class("collapsed")

    @work
    async def action_add_event(self):
        data_for_creation = await self.app.push_screen_wait(EventModal())
        if not isinstance(data_for_creation, EventCreate):
            return
        created_item = self.proxy.create(data_for_creation)
        self.notify(f"Event created {created_item.name}")
        await self.clear()
        await self.populate()

    @work
    async def action_edit_event(self):
        event = self.selected_event
        if event is None:
            return

        data_for_update = await self.app.push_screen_wait(EventModal(event))
        if not isinstance(data_for_update, EventUpdate):
            return
        updated_event = self.proxy.update(event.id, data_for_update)
        self.notify(f"Event updated {updated_event.name}")
        await self.clear()
        await self.populate()
        self.selected_event = updated_event

    @work
    async def action_delete_event(self):
        event = self.selected_event
        if event is None:
            return
        if await self.app.push_screen_wait(Confirmation("Delete event?", {"d"})):
            self.proxy.delete(event.id)
            self.notify("Event deleted")
            await self.clear()
            await self.populate()

    @on(ListView.Highlighted)
    async def handle_listview_highlighted(self, message: ListView.Highlighted):
        if isinstance(message.item, EventListItem):
            self.selected_event = message.item.event

    @on(events.DescendantFocus)
    def handle_descendant_focus(self, message: events.DescendantFocus):
        widget = message.widget
        if isinstance(widget, ListView) and widget.has_class("events"):
            if isinstance(widget.highlighted_child, EventListItem):
                self.selected_event = widget.highlighted_child.event
        else:
            self.selected_event = None

    @on(Button.Pressed, ".previous")
    async def go_to_previous_month(self):
        await self.action_previous_month()

    async def action_previous_month(self):
        month, year = self.month_year
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        self.month_year = (month, year)

    async def action_focus_left(self):
        self.focus_previous(ListView)

    async def action_focus_right(self):
        self.focus_next(ListView)

    @on(Button.Pressed, ".next")
    async def go_to_next_month(self):
        await self.action_next_month()

    async def action_next_month(self):
        month, year = self.month_year
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        self.month_year = (month, year)

    async def action_move_right(self):
        await self._move("r")

    async def action_move_left(self):
        await self._move("l")

    async def action_move_up(self):
        await self._move("u")

    async def action_move_down(self):
        await self._move("d")

    async def _move(self, direction: Literal["u", "d", "l", "r"]):
        event = self.selected_event
        if event is None:
            return

        if event.reference_timestamp is None:
            if direction == "r":
                month, year = self.month_year
                reference_datetime = datetime(year, month, 1)
            else:
                return
        else:
            if direction == "r":
                reference_datetime = event.reference_timestamp + timedelta(days=1)
            elif direction == "l":
                reference_datetime = event.reference_timestamp - timedelta(days=1)
            elif direction == "d":
                reference_datetime = event.reference_timestamp + timedelta(days=7)
            elif direction == "u":
                reference_datetime = event.reference_timestamp - timedelta(days=7)
            else:
                return

        async with self.batch():
            updated_event = self.proxy.update(
                event.id, EventUpdate(reference_timestamp=reference_datetime)
            )
            await self.clear()
            await self.populate()
            self.selected_event = updated_event
            await self.highlight_event(updated_event)

    async def action_remove_from_calendar(self):
        event = self.selected_event
        if event is None:
            return

        if event.reference_timestamp:
            async with self.batch():
                self.proxy.update(event.id, EventUpdate(reference_timestamp=None))
                await self.clear()
                await self.populate()
                # TODO: select event of same day

    @on(ListView.Selected)
    def print_event_info(self, message: ListView.Selected):
        if isinstance(message.item, EventListItem):
            e = message.item.event
            self.notify(e.model_dump_json())
