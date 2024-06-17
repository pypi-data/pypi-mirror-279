import json
from typing import List, Union

from fa_common import File, get_settings
from fa_common.storage import get_storage_client

from .base_models import JobRun


class GitlabService:
    @staticmethod
    async def get_job_output(bucket_id: str, workflow_id: int, job_id: int) -> Union[dict, List, None]:
        # client = get_workflow_client()
        storage = get_storage_client()
        file = await storage.get_file(
            bucket_id,
            f"{get_settings().WORKFLOW_UPLOAD_PATH}/{workflow_id}/{job_id}/outputs.json",
        )
        if file is None:
            return None
        return json.load(file)

    @staticmethod
    async def get_job_file_refs(bucket_id: str, workflow_id: int, job_id: int) -> List[File]:
        storage = get_storage_client()
        return await storage.list_files(
            bucket_id,
            f"{get_settings().WORKFLOW_UPLOAD_PATH}/{workflow_id}/{job_id}/",
        )

    # @staticmethod
    # async def get_job_file_refs(bucket_id: str, workflow_id: int, job_id: int) -> List[File]:
    #     storage = get_storage_client()
    #     return await storage.list_files(
    #         bucket_id,
    #         f"{get_settings().WORKFLOW_UPLOAD_PATH}/{workflow_id}/{job_id}/",
    #     )

    @staticmethod
    async def add_data_to_job(job: JobRun, bucket_id: str, output: bool = True, file_refs: bool = True) -> JobRun:
        if job.status == "success":
            if file_refs:
                job.files = await GitlabService.get_job_file_refs(bucket_id, job.workflow_id, job.id)
            if output and job.output is None:
                job.output = await GitlabService.get_job_output(bucket_id, job.workflow_id, job.id)
        return job
