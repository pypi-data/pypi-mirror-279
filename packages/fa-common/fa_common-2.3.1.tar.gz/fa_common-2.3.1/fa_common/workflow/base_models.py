"""
Description: models for Workflows.

Author: Ben Motevalli (benyamin.motevalli@csiro.au)
Created: 2023-11-07
"""

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import pytz
from dateutil import parser
from pydantic import ConfigDict, field_validator

from fa_common import CamelModel
from fa_common.enums import WorkflowEnums
from fa_common.models import File

from .base_enums import ArgoWorkflowStoreType, ModuleType

######  ### ####### #          #    ######     #       #######  #####     #     #####  #     #
#     #  #     #    #         # #   #     #    #       #       #     #   # #   #     #  #   #
#        #     #    #        #   #  #     #    #       #       #        #   #  #         # #
#  ####  #     #    #       #     # ######     #       #####   #  #### #     # #          #
#     #  #     #    #       ####### #     #    #       #       #     # ####### #          #
#     #  #     #    #       #     # #     #    #       #       #     # #     # #     #    #
######  ###    #    ####### #     # ######     ####### #######  #####  #     #  #####     #


class JobRun(CamelModel):
    """JobRun"""

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
        """get_compare_time"""
        if self.started_at is None:
            if self.status not in ["failed", "canceled", "skipped"]:
                return datetime.min.replace(tzinfo=timezone.utc)
            else:
                return datetime.now(tz=timezone.utc)
        else:
            return parser.isoparse(self.started_at)


class WorkflowRun(CamelModel):
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


class FileFieldDescription(CamelModel):
    """
    FileFieldDescription
    """

    name: str
    description: str
    valid_extensions: List[str]
    max_size: Optional[int] = None
    mandatory: bool = False


class ScidraModule(CamelModel):
    """
    ScidraModule
    """

    version: str = "1.0.0"
    name: str
    description: str = ""
    module_type: ModuleType = ModuleType.ASYNC
    docker_image: str
    docker_image_pull_secrets: Optional[List[str]] = []
    input_schema: str = ""
    output_schema: str = ""
    input_files: List[FileFieldDescription] = []
    cpu_limit: Union[str, int, float] = "4000m"
    cpu_request: Union[str, int, float] = "1000m"
    memory_limit_gb: Union[str, int] = 8
    memory_request_gb: Union[str, int] = 2


class WorkflowProject(CamelModel):
    """
    WorkflowProject
    """

    name: str
    user_id: str
    bucket_id: str
    gitlab_project_id: Optional[int] = None
    created: Optional[str] = None
    timezone: str = "UTC"

    @field_validator("timezone")
    @classmethod
    def must_be_valid_timezone(cls, v):
        """ """
        if v not in pytz.all_timezones:
            raise ValueError(f"{v} is not a valid timezone")
        return v


######
#     # ######  ####     ##### ###### #    # #####  #        ##   ##### # #    #  ####
#     # #      #    #      #   #      ##  ## #    # #       #  #    #   # ##   # #    #
######  #####  #    #      #   #####  # ## # #    # #      #    #   #   # # #  # #
#   #   #      #  # #      #   #      #    # #####  #      ######   #   # #  # # #  ###
#    #  #      #   #       #   #      #    # #      #      #    #   #   # #   ## #    #
#     # ######  ### #      #   ###### #    # #      ###### #    #   #   # #    #  ####


class GetWorkflowRes(CamelModel):
    """
    GetWorkflowRes
    """

    workflow: Any = None
    is_found: bool = False
    source_type: Optional[ArgoWorkflowStoreType] = None


class InputJobTemplate(CamelModel):
    """
    InputJobTemplate
    """

    files: Optional[List[File]] = []
    parameters: str = '"{"message": "no inputs!"}"'


class JobSecrets(CamelModel):
    """
    :param: name: name of secret
    :param: mount_path: where to mount the secret.
    """

    name: Optional[str] = None
    mount_path: Optional[str] = None


class WorkflowCallBack(CamelModel):
    """
    This class defines callback attributes. Callback executes
    in the Archive Node as this node runs onExit event hook.
    Callback can be used to notify client that a workflow is completed
    and it can be used to handle post-workflow logics.

    Note that callback should be implemented in the backend
    api. The callback api then is called in the workflow.

    :param: url: callback url (implemented in the backend api)
    :param: metadata: A json string used to input metadata that you want to
    receive back on the callback, e.g. project_name.
    :param: env_secrets: can be used to pass required secrets for the
    callback, e.g. API key.
    :param: env_vars: can be used to pass required secrets for the
    callback, e.g. API key. With env_vars, the secrets can directly
    be passed from the backend api.
    """

    url: str  # URL for callback
    metadata: Optional[str] = ""
    env_secrets: List[str] = []
    env_vars: Dict = {}


class CustomUpload(CamelModel):
    tar_path: str = ""
    file_names: Optional[str] = []  # If empty, copy all


class JobUploads(CamelModel):
    """
    :param: `default_path`: this is the default path constructed from
    WORKFLOW_UPLOAD_PATH. All logs and workflow steps are stored here.
    Also, this is the default path where outputs of a job are stored.

    :param: `custom_path`: if defined, the main outputs of the job
    is stored in this location, instead of the default location.

    :param: `copy_paths`: this is used, if a copy of the main outputs
    are required in other locations as well.

    :param: `selected_outputs`: if empty, copies all outputs. Note
    the paths in selected_outputs are subpaths of the outputs folder
    within the container (defined by output_path in JobTemplate). These
    paths can point to either file or folder.
    """

    default_path: str = ""
    custom_path: Optional[str] = None
    copy_paths: Optional[List[str]] = []
    selected_outputs: Optional[List[str]] = []

    @property
    def is_custom_upload(self):
        return self.custom_path is not None and self.custom_path != ""

    @property
    def has_all_outputs(self):
        return len(self.selected_outputs) == 0


class JobTemplate(CamelModel):
    """
    JobTemplate is definition of individual job (and not necessarily a task).
    A job usually is composed of a download node (if input files are required),
    at least one main node to run the job, and a upload node to upload results.

    :param: custom_id: `custom_id` for reference purposes, e.g. inside the workflow or
    to correlate inputs/outputs

    :param: custom_name: `custom_name` for reference purposes, e.g. inside the workflow
    or to correlate inputs/outputs

    :param: module_name: `module_name`: the name of the analysis module. At present,
    it is used as metadata

    :param: inputs: type of InputJobTemplate. This is where you define input params/files.

    :param: dependency:List of `custom_id` which current job depends on. It is useful
    for multi-run scenarios.

    :param: upload_path_base: the full address path to upload output files to cloud storage.
    This is the default path that all logs and files related to the workflow would be stored.
    This is a required field, even if there is no upload outputs. This path is required to
    store workflow logs.

    :param: upload_copy_paths: these are additional paths where you wish to make a copy of the
    main results. This is useful for scenarios where referring to the default path does not
    best suits your scenario.

    :param: `upload_custom_path`: if defined, the main outputs of the folder are copied into
    this path instead of `upload_path_base`.

    :param: image: container image address

    :param: image_pull_policy: if not present | always | never

    :param: commands_main: the main command that executes in main node.

    :param: commands_pre: list of commands to be run prior to the main block (not implemented)

    :param: commands_post: list of commands to be run after the main block (not implemented)

    :param: resource_cpu: sets limit/required

    :param: resource_memory: sets limit/required

    :param: env_secrets: list of kubernetes secrets required for the main node. Loads the
    secrets to env vars.

    :param: mount_secrets: list of kubernetes secrets required for the main node. Mounts
    secrets in the defined path.

    :param: env_configs: list of kubernetes configmaps required for the main node.

    :param: env_vars: A dictionary of env vars that are directly loaded to the main node.

    :param: input_path: where to refer for the inputs within the main container.

    :param: output_path: where to locate the outputs
    """

    custom_id: Union[int, str] = None
    custom_name: Optional[str] = None
    module_name: Optional[str] = None
    inputs: InputJobTemplate = None
    dependency: Optional[List[str]] = []
    uploads: JobUploads = None
    # upload_base_path: str = None
    # upload_copy_paths: Optional[List[str]] = []
    # upload_custom_path: Optional[CustomUpload] = None
    image: str = None
    image_pull_policy: WorkflowEnums.Run.ImagePullPolicy = WorkflowEnums.Run.ImagePullPolicy.IF_NOT_PRESENT
    commands_main: str = None
    commands_pre: Optional[str] = "echo empty pre-command"
    commands_post: Optional[str] = "echo empty post-command"
    resource_cpu: Union[float, str] = 0.2
    resource_memory: str = "128Mi"
    env_secrets: List[str] = []
    mount_secrets: List[JobSecrets] = []
    env_configs: List[str] = []
    env_vars: Dict = {}
    input_path: str = "/app/input"
    output_path: str = "/app/module/output"


######                                                                            #
#     # ######  ####      ######  ####  #####       # #   #####   ####   ####
#     # #      #    #     #      #    # #    #     #   #  #    # #    # #    #
######  #####  #    #     #####  #    # #    #    #     # #    # #      #    #
#   #   #      #  # #     #      #    # #####     ####### #####  #  ### #    #
#    #  #      #   #      #      #    # #   #     #     # #   #  #    # #    #
#     # ######  ### #     #       ####  #    #    #     # #    #  ####   ####


class NodeResourceDuration(CamelModel):
    """
    NodeResourceDuration
    """

    cpu: Optional[int] = None
    memory: Optional[int] = None


class Parameters(CamelModel):
    """
    Parameters
    """

    name: Optional[str] = None
    value: Optional[Union[str, int]] = None


class ArgoArtifactRepoS3(CamelModel):
    """
    ArgoArtifactRepoS3
    """

    key: str


class ArgoArtifacts(CamelModel):
    """
    ArgoArtifacts
    """

    name: Optional[str] = None
    path: Optional[str] = None
    s3: Optional[ArgoArtifactRepoS3] = None


class ArgoNodeInOut(CamelModel):
    """
    ArgoNodeInOut
    """

    parameters: Optional[List[Parameters]] = None
    artifacts: Optional[List[ArgoArtifacts]] = None


class ArgoWorkflowId(CamelModel):
    """
    ArgoWorkflowId
    """

    uid: Optional[str] = None
    name: Optional[str] = None


class ArgoNode(CamelModel):
    """
    ArgoNode represents each node in the workflow.
    """

    id: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    type: Optional[str] = None
    template_name: Optional[str] = None
    template_scope: Optional[str] = None
    phase: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    progress: Optional[str] = None
    resources_duration: Optional[NodeResourceDuration] = None
    children: Optional[List[str]] = None
    outbound_nodes: Optional[List[str]] = None
    inputs: Optional[ArgoNodeInOut] = None
    outputs: Optional[ArgoNodeInOut] = None

    # Extra Amendments
    pod_name: Optional[str] = None
    task_name: Optional[str] = None  # This is the task name initially defined in the manifest
    output_json: Optional[Union[List, dict]] = None
    files: Optional[List[File]] = None
    log: Optional[bytes] = None
    model_config = ConfigDict(use_enum_values=True)

    def set_pod_task_names(self):
        """
        Argo Node represents each node in the workflow. Most of these nodes
        are tasks. A task is run in a kube pod, however the pod_name is not
        directly returned when getting workflow from Argo's api. This method
        will set the pod_name of each task from available fields in the
        get workflow response.
        """
        if self.id is not None and self.name is not None:
            # Set pod-name
            match = re.match(r"^(.*?)-(\d+)$", self.id if self.id is not None else "")
            if match:
                prefix, id_number = match.groups()
                self.pod_name = f"{prefix}-{self.template_name}-{id_number}"

            # Set task-name
            parts = self.name.split(".")
            self.task_name = parts[-1] if len(parts) > 1 else ""
        # @FIXME else case

    def get_compare_time(self) -> datetime:
        """
        get_compare_time
        """
        if self.started_at is None:
            if self.status not in ["Failed"]:
                return datetime.min.replace(tzinfo=timezone.utc)
            else:
                return datetime.now(tz=timezone.utc)
        else:
            return parser.isoparse(self.started_at)


class ArgoWorkflowMetadata(CamelModel):
    """
    ArgoWorkflowMetadata
    """

    name: Optional[str] = None
    generate_name: Optional[str] = None
    namespace: Optional[str] = None
    uid: Optional[str] = None
    creation_timestamp: Optional[str] = None


class ArgoWorkflowStatus(CamelModel):
    """
    ArgoWorkflowStatus
    """

    phase: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    progress: Optional[str] = None
    nodes: Optional[List[ArgoNode]] = []


T = TypeVar("T", bound="ArgoWorkflowRun")


class ArgoWorkflowRun(CamelModel):
    """
    ArgoWorkflowRun
    """

    metadata: Optional[ArgoWorkflowMetadata] = None
    status: Optional[ArgoWorkflowStatus] = None
    spec: Optional[dict] = {}
    jobs: Optional[List[JobRun]] = []

    @classmethod
    def populate_from_res(cls: Type[T], res, fields) -> T:
        """
        This method populates ArgoWorkflowRun attributes
        from the response received from getting the
        workflow
        """
        try:
            res_dict = res if isinstance(res, dict) else res.to_dict()

            init_args: Dict[str, Any] = {}
            if "metadata" in fields:
                init_args["metadata"] = ArgoWorkflowMetadata(**res_dict.get("metadata", {}))
            if "status" in fields:
                status = res_dict.get("status", {})
                if ("nodes" in status) and (isinstance(status["nodes"], dict)):
                    nodes = []
                    for _, v in status["nodes"].items():
                        nodes.append(v)
                    status["nodes"] = nodes
                init_args["status"] = ArgoWorkflowStatus(**status)
            if "spec" in fields:
                init_args["spec"] = res_dict.get("spec", {})

            return cls(**init_args)
        except Exception as e:
            raise ValueError("Could not parse response") from e
