import httpx

from systema.models.notification import Notification
from systema.notification.base import NotificationBackend


class Ntfy(NotificationBackend):
    def __init__(self):
        self.base_url = "https://ntfy.sh/"

    def _send(self, notification: Notification):
        headers = {"Title": notification.title}
        response = httpx.post(
            f"{self.base_url}systema-{notification.user_id}",
            content=notification.message,
            headers=headers,
        )
        if not response.is_success:
            raise self.Failed
