from collections.abc import Callable
from datetime import datetime

import schedule
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, field_validator

from systema.server.auth.utils import get_current_superuser
from systema.server.scheduler.jobs import add_jobs

router = APIRouter(
    prefix="/scheduler",
    tags=["scheduler"],
    dependencies=[Depends(get_current_superuser)],
)


class Job(BaseModel):
    job_func: str | None
    interval: int
    unit: str | None
    last_run: datetime | None
    next_run: datetime | None

    model_config = {"from_attributes": True}

    @field_validator("job_func", mode="before")
    def parse_job_func(cls, v: Callable):
        return v.__name__


@router.get("/jobs")
async def list_jobs():
    jobs = schedule.get_jobs()
    return (Job.model_validate(j) for j in jobs)


@router.post("/run", status_code=status.HTTP_204_NO_CONTENT)
async def run_now():
    schedule.run_all()


@router.post("/cancel", status_code=status.HTTP_204_NO_CONTENT)
async def cancel():
    schedule.clear()


@router.post("/reset", status_code=status.HTTP_204_NO_CONTENT)
async def reset():
    add_jobs()
