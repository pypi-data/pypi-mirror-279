from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Union

import pytz
from dateutil import parser
from pydantic import ConfigDict, field_validator

from fa_common import CamelModel, File, deprecated_class

# from fa_common.db import DocumentDBModel


@deprecated_class("The `ModuleType` method is deprecated; use `base_models.ModuleType` instead.")
class ModuleType(str, Enum):
    """@deprecated The `ModuleType` method is deprecated; use `base_models.ModuleType` instead."""

    SYNC = "sync"  # Is run via a service call
    ASYNC = "async"  # Is executed via gitlab ci


@deprecated_class("The `JobAction` method is deprecated; use `base_models.JobAction` instead.")
class JobAction(str, Enum):
    """@deprecated The `JobAction` method is deprecated; use `base_models.JobAction` instead."""

    PLAY = "play"
    RETRY = "retry"
    DELETE = "delete"
    CANCEL = "cancel"


@deprecated_class("The `JobStatus` method is deprecated; use `base_models.JobStatus` instead.")
class JobStatus(str, Enum):
    """@deprecated The `JobStatus` method is deprecated; use `base_models.JobStatus` instead."""

    NOT_SET = ""
    RECEIVED = "RECEIVED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


@deprecated_class("The `FileFieldDescription` method is deprecated; use `base_models.FileFieldDescription` instead.")
class FileFieldDescription(CamelModel):
    """@deprecated The `FileFieldDescription` method is deprecated; use `base_models.FileFieldDescription` instead."""

    name: str
    description: str
    valid_extensions: List[str]
    max_size: Optional[int] = None
    mandatory: bool = False


@deprecated_class("The `ScidraModule` method is deprecated; use `base_models.ScidraModule` instead.")
class ScidraModule(CamelModel):
    """@deprecated The `ScidraModule` method is deprecated; use `base_models.ScidraModule` instead."""

    version: str = "1.0.0"
    name: str
    description: str = ""
    module_type: ModuleType = ModuleType.ASYNC
    docker_image: str
    input_schema: str = ""
    output_schema: str = ""
    input_files: List[FileFieldDescription] = []
    cpu_limit: str = "4000m"
    cpu_request: str = "1000m"
    memory_limit_gb: int = 8
    memory_request_gb: int = 2


@deprecated_class("The `JobRun` method is deprecated; use `base_models.JobRun` instead.")
class JobRun(CamelModel):
    """@deprecated The `JobRun` method is deprecated; use `base_models.JobRun` instead."""

    id: int
    workflow_id: int
    status: str = ""
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: Optional[float] = None
    name: str = ""
    stage: Optional[str] = None
    output: Optional[Union[List, dict]] = None
    files: Optional[List[File]] = None
    log: Optional[bytes] = None
    model_config = ConfigDict(use_enum_values=True)

    def get_compare_time(self) -> datetime:
        if self.started_at is None:
            if self.status not in ["failed", "canceled", "skipped"]:
                return datetime.min.replace(tzinfo=timezone.utc)
            else:
                return datetime.now(tz=timezone.utc)
        else:
            return parser.isoparse(self.started_at)


@deprecated_class("The `WorkflowRun` method is deprecated; use `base_models.WorkflowRun` instead.")
class WorkflowRun(CamelModel):
    """@deprecated The `WorkflowRun` method is deprecated; use `base_models.WorkflowRun` instead."""

    """Equivilant to  gitlab pipeline"""

    id: int
    gitlab_project_id: int
    gitlab_project_branch: str
    commit_id: str
    status: str = ""
    jobs: List[JobRun] = []
    hidden_jobs: Optional[List[JobRun]] = []
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: Optional[int] = None


@deprecated_class("The `WorkflowProject` method is deprecated; use `base_models.WorkflowProject` instead.")
class WorkflowProject(CamelModel):
    """@deprecated The `WorkflowProject` method is deprecated; use `base_models.WorkflowProject` instead."""

    name: str
    user_id: str
    bucket_id: str
    gitlab_project_id: int
    created: Optional[str] = None
    timezone: str = "UTC"

    @field_validator("timezone")
    @classmethod
    def must_be_valid_timezone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError(f"{v} is not a valid timezone")
        return v
