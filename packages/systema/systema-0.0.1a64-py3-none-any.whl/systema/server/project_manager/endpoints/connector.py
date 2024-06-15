from fastapi import APIRouter, Depends, HTTPException, status

from systema.models.connector import (
    Connector,
    ConnectorCreate,
    ConnectorRead,
    ConnectorUpdate,
)
from systema.proxies.connector import ConnectorProxy
from systema.server.auth.utils import get_current_active_user

router = APIRouter(
    prefix="/projects/{project_id}/connectors",
    tags=["connectors"],
    dependencies=[Depends(get_current_active_user)],
)


@router.post("/", response_model=ConnectorRead, status_code=status.HTTP_201_CREATED)
async def create_connector(conn: ConnectorCreate, project_id: str):
    return ConnectorProxy(project_id).create(conn)


@router.get("/", response_model=list[ConnectorRead])
async def list_connectors(project_id: str):
    return ConnectorProxy(project_id).all()


@router.get("/{id}", response_model=ConnectorRead)
async def get_connector(project_id: str, id: str):
    try:
        return ConnectorProxy(project_id).get(id)
    except Connector.NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Connector not found")


@router.patch("/{id}", response_model=ConnectorRead)
async def update_connector(project_id: str, id: str, data: ConnectorUpdate):
    try:
        return ConnectorProxy(project_id).update(id, data)
    except Connector.NotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Connector not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connector(project_id: str, id: str):
    try:
        return ConnectorProxy(project_id).delete(id)
    except Connector.NotFound:
        raise HTTPException(status.HTTP_404NOT_FOUND, "Connector not found")
