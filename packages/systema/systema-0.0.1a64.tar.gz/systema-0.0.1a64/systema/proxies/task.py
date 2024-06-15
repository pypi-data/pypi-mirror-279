from abc import abstractmethod
from typing import Any, TypeVar

from sqlmodel import Session, col, select

from systema.models.project import Project
from systema.models.task import SubTaskMixin, Task, TaskCreate, TaskRead, TaskUpdate
from systema.proxies.base import Proxy

ModelRead = TypeVar("ModelRead", bound=TaskRead)
Model = TypeVar("Model", bound=Task)


class SubTaskProxy(Proxy[ModelRead]):
    def __init__(self, project_id: str) -> None:
        self.project_id = project_id
        self.task_proxy = TaskProxy(project_id)

    @property
    @abstractmethod
    def model(self) -> type[SubTaskMixin]:
        pass

    @property
    @abstractmethod
    def model_read(self) -> type[ModelRead]:
        pass

    def get_project(self, session: Session):
        if project := session.get(Project, self.project_id):
            return project
        raise Project.NotFound()

    def get_task(
        self, session: Session, project: Project, id: str
    ) -> tuple[SubTaskMixin, Task]:
        with Session(self.engine) as session:
            statement = (
                select(self.model, Task)
                .join(Task)
                .where(
                    self.model.id == Task.id,
                    self.model.id == id,
                    Task.project_id == project.id,
                )
            )
            return session.exec(statement).one()

    def get(self, id: str):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                return self.model_read.model_validate(session.get(self.model, id))

        response = self.client.get(f"{self.base_url}{id}/")
        response.raise_for_status()
        return self.model_read(**response.json())

    def all(self):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                project = self.get_project(session)
                statement = (
                    select(self.model, Task)
                    .join(Task)
                    .join(Project)
                    .where(
                        self.model.id == Task.id,
                        Task.project_id == Project.id,
                        Project.id == project.id,
                    )
                )
                # TODO: figure out better way to sort
                if hasattr(self.model, "order"):
                    statement = statement.order_by(col(self.model.order).asc())

                statement = statement.order_by(col(Task.status).asc())
                return (
                    self.model_read.model_validate(sub_task, update=task.model_dump())
                    for sub_task, task in session.exec(statement).all()
                )

        response = self.client.get(self.base_url)
        response.raise_for_status()
        return (self.model_read(**p) for p in response.json())

    def create(self, data: TaskCreate):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                project = self.get_project(session)
                task = self.task_proxy.create(data)
                subtask, task = self.get_task(session, project, task.id)
                return self.model_read.from_task(subtask, task)

        response = self.client.post(self.base_url, json=data.model_dump(mode="json"))
        response.raise_for_status()
        return self.model_read(**response.json())

    def update(self, id: str, data: TaskUpdate):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                project = self.get_project(session)
                obj, task = self.get_task(session, project, id)

                original_obj = obj.model_copy()

                task.sqlmodel_update(data.model_dump(exclude_unset=True))
                obj.sqlmodel_update(data.model_dump(exclude_unset=True))

                session.add_all((obj, task))
                session.commit()

                session.refresh(obj)
                session.refresh(task)

                self.post_update(session, project, original_obj, obj)

                session.refresh(obj)
                session.refresh(task)

                return self.model_read.from_task(obj, task)

        response = self.client.patch(
            f"{self.base_url}{id}/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return self.model_read(**response.json())

    def delete(self, id: str):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                project = self.get_project(session)
                obj, task = self.get_task(session, project, id)

                original_obj = obj.model_copy()

                if self.pre_delete(session, project, original_obj):
                    session.delete(obj)
                    session.delete(task)

                    session.commit()
        else:
            response = self.client.delete(f"{self.base_url}{id}/")
            response.raise_for_status()

    def post_update(
        self,
        session: Session,
        project: Project,
        original_obj: Any,
        current_obj: Any,
    ) -> SubTaskMixin:
        lambda: session
        lambda: project
        lambda: original_obj
        return current_obj

    def pre_delete(
        self,
        session: Session,
        project: Project,
        original_obj: Any,
    ) -> bool:
        lambda: session
        lambda: project
        lambda: original_obj
        return True


class TaskProxy(Proxy[TaskRead]):
    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    def get_project(self, session: Session):
        if project := session.get(Project, self.project_id):
            return project
        raise Project.NotFound()

    def _get(self, session: Session, id: str):
        if task := session.get(Task, id):
            return task
        raise Task.NotFound

    def get(self, id: str):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                return TaskRead.model_validate(self._get(session, id))

        response = self.client.get(f"{self.base_url}{id}/")
        response.raise_for_status()
        return TaskRead(**response.json())

    def all(self):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                project = self.get_project(session)
                statement = (
                    select(Task)
                    .join(Project)
                    .where(
                        Task.project_id == Project.id,
                        Project.id == project.id,
                    )
                    .order_by(
                        col(Task.status).asc(),
                    )
                )
                return (
                    TaskRead.model_validate(*r) for r in session.exec(statement).all()
                )

        response = self.client.get(self.base_url)
        response.raise_for_status()
        return (TaskRead(**p) for p in response.json())

    def create(self, data: TaskCreate):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                project = self.get_project(session)
                task = Task(name=data.name, project_id=project.id)
                session.add(task)
                session.commit()

                _ = self.create_subclass_instances(session, task, data)

                session.refresh(task)
                return TaskRead.model_validate(task)

        response = self.client.post(self.base_url, json=data.model_dump(mode="json"))
        response.raise_for_status()
        return TaskRead(**response.json())

    def create_subclass_instances(self, session: Session, task: Task, data: TaskCreate):
        from systema.models.card import Card
        from systema.models.event import Event
        from systema.models.item import Item
        from systema.models.node import Node
        from systema.proxies.card import CardProxy
        from systema.proxies.item import ItemProxy

        session.refresh(task)
        item = Item.model_validate(task, update=data.model_dump())
        session.add(item)

        ItemProxy(self.project_id)._reorder(
            session, task.project_id, item.order, exclude=item.id, shift=True
        )

        card = Card.model_validate(task, update=data.model_dump())
        session.add(card)

        CardProxy(self.project_id)._reorder(
            session,
            task.project_id,
            card.bin_id,
            card.order,
            exclude=card.id,
            shift=True,
        )

        event = Event.model_validate(task, update=data.model_dump())
        session.add(event)

        node = Node.model_validate(task, update=data.model_dump())
        session.add(node)

        session.commit()
        session.refresh(item)
        return item

    def update(self, id: str, data: TaskUpdate):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                self.get_project(session)
                task = self._get(session, id)

                task.sqlmodel_update(data.model_dump(exclude_unset=True))

                session.add(task)
                session.commit()

                session.refresh(task)

                return TaskRead.model_validate(task)

        response = self.client.patch(
            f"{self.base_url}{id}/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return TaskRead(**response.json())

    def delete(self, id: str):
        if self.is_set_as_server():
            with Session(self.engine) as session:
                self.get_project(session)
                task = self._get(session, id)
                session.delete(task)
                session.commit()
                return

        response = self.client.delete(f"{self.base_url}{id}/")
        response.raise_for_status()
