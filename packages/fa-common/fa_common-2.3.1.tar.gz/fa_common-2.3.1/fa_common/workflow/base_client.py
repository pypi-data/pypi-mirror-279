"""
Description: This class is used as base client for workflows.

Author: Ben Motevalli (benyamin.motevalli@csiro.au)
Created: 2023-11-07
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from fa_common.models import File

from .base_models import (
    ArgoWorkflowId,
    ArgoWorkflowRun,
    ScidraModule,
    WorkflowProject,
    WorkflowRun,
)


class WorkflowBaseClient(ABC):
    """
    Abstract workflow class.
    """

    @abstractmethod
    async def run_job(
        self,
        project: WorkflowProject,
        description: str,
        module: ScidraModule,
        job_data: Union[dict, List[dict]],
        runner: str = "csiro-swarm",
        files: Union[List[File], List[List[File]]] = [],
        sync: bool = False,
        upload: bool = True,
        upload_runner: str | None = None,
        namespace: str = "cmr-xt-argo",
    ) -> Union[WorkflowRun, ArgoWorkflowRun]:
        """
        The `run_job` function is an asynchronous function that runs a job in a
        workflow project using a specified module and job data, with options for runner,
        files, synchronization, and upload.


        :param files: The `files` parameter is a list of files that you want to include
        in the job. It can be either a list of `File` objects or a list of lists of `File`
        objects. If a single set of input file exists for the jobs, then use a list. If
        you wish to loop over a set of input files, then use of list of lists, where each
        inner list represent one set of input files.
        """

    @abstractmethod
    async def get_workflow(
        self,
        bucket_id: str,
        workflow_id: Union[int, str, ArgoWorkflowId],
        output: bool = False,
        file_refs: bool = True,
        user_id: Optional[str] = None,
        namespace: Optional[str] = None,
    ) -> WorkflowRun:
        """
        This Python function defines an abstract method `get_workflow` that retrieves
        information about a workflow run.
        """

    @abstractmethod
    async def delete_workflow(
        self,
        bucket_id: str,
        workflow_id: Union[int, str, ArgoWorkflowId],
        user_id: Optional[str],
        namespace: Optional[str],
        force_data_delete: Optional[bool] = False,
    ):
        """
        :param force_data_delete: if True, if workflow does not exist in the records,
        it would yet continue with deletion of artifacts and output data.
        """

    @abstractmethod
    async def _delete_workflow_artifacts(self, workflow_id: Union[int, str, ArgoWorkflowId]):
        """
        This method deletes artifacts of a workflow
        """

    @abstractmethod
    async def retry_workflow(self, workflow_id: Union[int, ArgoWorkflowId], user_id: Optional[str] = None):
        """
        Retry the workflow.
        """

    @abstractmethod
    async def get_workflow_log(
        self,
        workflow_id: Union[int, ArgoWorkflowId],
        bucket_id: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        """
        This abstract method defines an asynchronous function to retrieve
        the workflow log based on the workflow ID, with optional parameters
        for bucket ID and namespace.
        """

    @abstractmethod
    async def get_job_log(
        self,
        job_id: Union[int, str],
        workflow_id: Union[int, ArgoWorkflowId, None] = None,
        user_id: Optional[str] = None,
    ):
        """
        This method gets the logs of a job.
        """
