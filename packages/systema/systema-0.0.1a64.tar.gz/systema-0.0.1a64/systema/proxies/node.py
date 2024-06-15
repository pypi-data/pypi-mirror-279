from systema.models.node import Node, NodeRead
from systema.proxies.task import SubTaskProxy


class NodeProxy(SubTaskProxy[NodeRead]):
    @property
    def base_url(self) -> str:
        return super().base_url + f"projects/{self.project_id}/nodes/"

    @property
    def model(self):
        return Node

    @property
    def model_read(self):
        return NodeRead
