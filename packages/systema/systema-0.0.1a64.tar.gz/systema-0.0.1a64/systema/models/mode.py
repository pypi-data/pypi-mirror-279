import enum


class Mode(str, enum.Enum):
    CHECKLIST = "list"
    KANBAN = "kanban"
    TIMELINE = "timeline"
    CALENDAR = "calendar"
    MIND_MAP = "mind_map"
