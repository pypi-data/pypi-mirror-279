from abc import ABC, abstractmethod

from sqlmodel import Session, create_engine

from systema.models.notification import Notification, NotificationStatus


class NotificationBackend(ABC):
    class Failed(Exception):
        """When backend fails to send notification"""

    @abstractmethod
    def _send(self, notification: Notification):
        pass

    def send(self, notification: Notification):
        from systema.management import Settings

        engine = create_engine(Settings().db_address)
        with Session(engine) as session:
            self._create_in_db(session, notification)
            try:
                self._send(notification)
            except self.Failed:
                notification.status = NotificationStatus.ERROR

            self._update_in_db(session, notification)

    def _create_in_db(self, session: Session, notification: Notification):
        session.add(notification)
        session.commit()
        session.refresh(notification)

    def _update_in_db(self, session: Session, notification: Notification):
        session.add(notification)
        session.commit()
        session.refresh(notification)
