from sqlmodel import Session, select

from systema.models.connector import (
    Connector,
    ConnectorCreate,
    ConnectorRead,
    ConnectorUpdate,
)
from systema.proxies.base import Proxy


class ConnectorProxy(Proxy[ConnectorRead]):
    def __init__(self, mind_map_id: str):
        self.mind_map_id = mind_map_id

    @property
    def base_url(self) -> str:
        return super().base_url + f"projects/{self.mind_map_id}/connectors/"

    def _get(self, session: Session, mind_map_id: str, id: str):
        statement = select(Connector).where(
            Connector.id == id, Connector.mind_map_id == mind_map_id
        )
        if result := session.exec(statement).first():
            return result
        raise Connector.NotFound()

    def _get_mind_map(self, session: Session, mind_map_id: str):
        from systema.models.mind_map import MindMap

        if mind_map := session.get(MindMap, mind_map_id):
            return mind_map
        raise MindMap.NotFound

    def get(self, id: str):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                return ConnectorRead.from_conn(self._get(session, self.mind_map_id, id))

        response = self.client.get(f"{self.base_url}{id}")
        response.raise_for_status()
        return ConnectorRead(**response.json())

    def all(self, node_id: str | None = None):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                mind_map = self._get_mind_map(session, self.mind_map_id)
                statement = select(Connector).where(
                    Connector.mind_map_id == mind_map.id,
                )
                if node_id:
                    statement = statement.where(
                        Connector.a == node_id or Connector.b == node_id
                    )
                return (
                    ConnectorRead.from_conn(row)
                    for row in session.exec(statement).all()
                )

        response = self.client.get(self.base_url)
        response.raise_for_status()
        return (ConnectorRead(**p) for p in response.json())

    def create(self, data: ConnectorCreate):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                project = self._get_mind_map(session, self.mind_map_id)
                conn = Connector(mind_map_id=project.id, a=data.a, b=data.b)
                session.add(conn)
                session.commit()
                session.refresh(conn)
                return ConnectorRead.from_conn(conn)

        response = self.client.post(self.base_url, json=data.model_dump(mode="json"))
        response.raise_for_status()
        return ConnectorRead(**response.json())

    def update(self, id: str, data: ConnectorUpdate):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                conn = self._get(session, self.mind_map_id, id)

                conn.sqlmodel_update(data.model_dump(exclude_unset=True))

                session.add(conn)
                session.commit()
                session.refresh(conn)

                return ConnectorRead.from_conn(conn)

        response = self.client.patch(
            f"{self.base_url}{id}/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return ConnectorRead(**response.json())

    def delete(self, id: str):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                conn = self._get(session, self.mind_map_id, id)

                session.delete(conn)

                session.commit()
        else:
            response = self.client.delete(f"{self.base_url}{id}/")
            response.raise_for_status()
