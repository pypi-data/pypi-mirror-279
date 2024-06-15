from fastapi import APIRouter, Depends, HTTPException, status

from systema.models.node import Node, NodeCreate, NodeRead, NodeUpdate
from systema.proxies.node import NodeProxy
from systema.server.auth.utils import get_current_active_user

router = APIRouter(
    prefix="/projects/{project_id}/nodes",
    tags=["nodes"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/", response_model=NodeRead, status_code=status.HTTP_201_CREATED)
async def create_node(node: NodeCreate, project_id: str):
    return NodeProxy(project_id).create(node)


@router.get("/", response_model=list[NodeRead])
async def list_nodes(project_id: str):
    return NodeProxy(project_id).all()


@router.get("/{id}", response_model=NodeRead)
async def get_node(project_id: str, id: str):
    try:
        return NodeProxy(project_id).get(id)
    except Node.NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Node not found")


@router.patch("/{id}", response_model=NodeRead)
async def update_node(project_id: str, id: str, data: NodeUpdate):
    try:
        return NodeProxy(project_id).update(id, data)
    except Node.NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Node not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_node(project_id: str, id: str):
    try:
        return NodeProxy(project_id).delete(id)
    except Node.NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Node not found")
