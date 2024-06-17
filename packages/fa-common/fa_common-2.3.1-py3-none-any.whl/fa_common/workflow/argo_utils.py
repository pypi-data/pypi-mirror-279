"""
Description: This script is the main script to generate argo workflow templates.

Author: Ben Motevalli (benyamin.motevalli@csiro.au)
Created: 2023-11-07
"""

import json
import os
from typing import List, Optional, Union

import yaml
from jinja2 import BaseLoader, Environment

from fa_common import CamelModel, get_settings
from fa_common.enums import WorkflowEnums
from fa_common.exceptions import UnImplementedError

from .base_enums import CloudBaseImage
from .base_models import JobTemplate, WorkflowCallBack


def str_presenter(dumper, data):
    """
    multiline in yaml.
    """
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)
# to use with safe_dump:
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


dirname = os.path.dirname(__file__)


class CloudStorageConfig(CamelModel):
    """
    Workflow config attributes for Cloud Storag.
    """

    access_method: WorkflowEnums.FileAccess.Method = WorkflowEnums.FileAccess.Method.DIRECT
    access_type: WorkflowEnums.FileAccess.AccessType = WorkflowEnums.FileAccess.AccessType.WITH_ROLE
    access_secret_name: Optional[str] = None
    access_secret_key: Optional[str] = None
    save_logs: bool = True

    def __init__(self, **data):
        super().__init__(**data)  # Call the superclass __init__ to handle Pydantic model initialization
        settings = get_settings()
        # Directly assign the values post-initialization if not provided
        if self.access_secret_name is None:
            self.access_secret_name = settings.STORAGE_SECRET_NAME
        if self.access_secret_key is None:
            self.access_secret_key = settings.STORAGE_SECRET_KEY

    @property
    def has_secret(self) -> bool:
        """
        checks if access type is set with secret or via a trust relationship
        through a service account.
        """
        return self.access_type == WorkflowEnums.FileAccess.AccessType.WITH_SECRET

    @property
    def cloud_base_image(self) -> str:
        """
        what cloud base image to use.
        """
        settings = get_settings()
        if settings.STORAGE_TYPE == WorkflowEnums.FileAccess.STORAGE.FIREBASE_STORAGE:
            return CloudBaseImage.GUTILS.value
        if settings.STORAGE_TYPE == WorkflowEnums.FileAccess.STORAGE.MINIO:
            return CloudBaseImage.AWS.value
        return None

    def set(self, **kwargs):
        """
        sets attributes.
        """
        for key, value in kwargs.items():
            if key == "has_secret":
                raise AttributeError("has_secret is a computed property and cannot be set directly.")
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"{self.__class__.__name__} has no attribute '{key}'")

    def set_default(self):
        """
        resets attributes to default values.
        """
        default_instance = CloudStorageConfig()
        for attr in vars(default_instance):
            setattr(self, attr, getattr(default_instance, attr))
        self.has_secret = self.access_type == WorkflowEnums.FileAccess.AccessType.WITH_SECRET


class UploadConfig(CloudStorageConfig):
    """
    Workflow config attributes for Upload Template
    """

    strategy: WorkflowEnums.Upload.Strategy = WorkflowEnums.Upload.Strategy.EVERY
    loc_name: WorkflowEnums.Upload.LocName = WorkflowEnums.Upload.LocName.POD_NAME


class RunConfig(CamelModel):
    """
    Workflow config attributes for Run Template
    """

    strategy: WorkflowEnums.Run.Strategy = WorkflowEnums.Run.Strategy.GLOBAL
    max_all_jobs_dependency: Optional[int] = 0
    save_logs: bool = True
    logging_strategy: WorkflowEnums.Logging.Strategy = WorkflowEnums.Logging.Strategy.FROM_ARTIFACT

    @property
    def is_unified(self) -> bool:
        """
        checks if access type is set with secret or via a trust relationship
        through a service account.
        """
        return "uni" in self.strategy.value


class BaseConfig(CamelModel):
    """
    Workflow config attributes for Base Template
    """

    continue_on_run_task_failure: bool = True
    is_error_tolerant: bool = False
    image_pull_secrets: List[str] = []
    service_account_name: Optional[str] = "argo-workflow-patch"

    @property
    def has_argo_token(self) -> bool:
        """
        checks if argo token is provided. useful for local dev.
        """
        st = get_settings()
        return not (st.ARGO_TOKEN is None or st.ARGO_TOKEN == "")

    @property
    def is_argo_local(self) -> bool:
        st = get_settings()
        return "localhost" in st.ARGO_URL


class ArgoTemplateConfig(CamelModel):
    """
    Workflow config attributes
    """

    download: CloudStorageConfig = CloudStorageConfig()
    upload: UploadConfig = UploadConfig()
    run: RunConfig = RunConfig()
    base: BaseConfig = BaseConfig()

    @property
    def logs_to_include(self) -> List:
        """
        Which logs to include.
        """
        lst_logs = []
        if self.run.save_logs:
            lst_logs.append(WorkflowEnums.Templates.RUN)
        if self.download.save_logs:
            lst_logs.append(WorkflowEnums.Templates.DOWNLOAD)
        if self.upload.save_logs:
            lst_logs.append(WorkflowEnums.Templates.UPLOAD)

        return lst_logs


class ArgoTemplateGenerator:
    #####  ####### #     # ####### ###  #####
    #     # #     # ##    # #        #  #     #
    #       #     # # #   # #        #  #
    #       #     # #  #  # #####    #  #  ####
    #       #     # #   # # #        #  #     #
    #     # #     # #    ## #        #  #     #
    #####  ####### #     # #       ###  #####

    config: ArgoTemplateConfig = ArgoTemplateConfig()
    jinja_env: Environment = Environment(
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",
        block_end_string="%>",
        loader=BaseLoader(),
    )

    ######  ######  #######    #    ####### #######
    #     # #     # #         # #      #    #
    #       #     # #        #   #     #    #
    #       ######  #####   #     #    #    #####
    #       #   #   #       #######    #    #
    #     # #    #  #       #     #    #    #
    ######  #     # ####### #     #    #    #######

    @classmethod
    def create(
        cls,
        workflow_name: str,
        jobs: List[JobTemplate],
        job_base: JobTemplate,
        workflow_callbacks: List[WorkflowCallBack] = [],
        has_upload: Optional[bool] = True,
    ):
        """
        @AddMe: Handle None checks.
        """
        base_template = cls.gen_base_block(workflow_name)
        run_template = cls.gen_run_template(job_base, has_upload)
        main_template = cls.gen_tasks_main_template(jobs, has_upload)
        arch_template = cls.get_archive_template(job_base, workflow_callbacks)

        base_template["spec"]["templates"] = [main_template]
        if not cls.config.run.is_unified:
            download_template = cls.gen_download_template()
            base_template["spec"]["templates"].append(download_template)

        base_template["spec"]["templates"].append(run_template)
        base_template["spec"]["templates"].append(arch_template)

        if has_upload:
            upload_template = cls.gen_upload_template(jobs)
            base_template["spec"]["templates"].append(upload_template)

        return base_template

    #    ###### ####### ######     ####### ####### #     # ######  #          #    ####### #######
    #    #     # #     #       #    #       ##   ## #     # #         # #      #    #
    #    #     # #     #       #    #       # # # # #     # #        #   #     #    #
    #    #     # ######        #    #####   #  #  # ######  #       #     #    #    #####
    #    #     # #             #    #       #     # #       #       #######    #    #
    #    #     # #             #    #       #     # #       #       #     #    #    #
    #    ####### #             #    ####### #     # #       ####### #     #    #    #######

    @classmethod
    def gen_base_block(cls, workflow_name: str):
        """
        This function creates the base-top block of the manifest.
        Most contents in this block are common.
        """
        # FIXME: Check with Sam. This might overlap with MINIO secrets.
        # @REVIEW

        settings = get_settings()
        params = {
            "NAME": f"{workflow_name}-",
            "SECRET_NAME": settings.STORAGE_SECRET_NAME,
            # "HAS_SECRET": cls.config.has_secret,
            "IS_LOCAL": cls.config.base.is_argo_local,
            "ARCHIVE_TEMP_NAME": WorkflowEnums.Templates.ARCHIVE.value,
            "IMAGE_PULL_SECRETS": cls.config.base.image_pull_secrets,
            "SERVICE_ACCOUNT_NAME": cls.config.base.service_account_name,
        }

        return cls._populate_template_block("template_base.yaml", params)

    @classmethod
    def get_archive_template(cls, job_base: JobTemplate, workflow_callbacks: WorkflowCallBack):
        """
        Handles archive template
        """
        settings = get_settings()
        argo_url = settings.ARGO_URL
        if cls.config.base.is_argo_local:
            argo_url = settings.ARGO_URL.replace("localhost", "host.docker.internal")
        if len(workflow_callbacks) > 0:
            for callback in workflow_callbacks:
                if "localhost" in callback.url:
                    callback.url = callback.url.replace("localhost", "host.docker.internal")

        params = {
            "ARCHIVE_TEMP_NAME": WorkflowEnums.Templates.ARCHIVE.value,
            "IS_ERR_TOLER": cls.config.base.is_error_tolerant,
            "SECRET_NAME": cls.config.upload.access_secret_name,
            "SECRET_KEY": cls.config.upload.access_secret_key,
            "HAS_SECRET": cls.config.upload.has_secret,
            "STORAGE_TYPE": settings.STORAGE_TYPE,
            "STORAGE_ENUM": WorkflowEnums.FileAccess.STORAGE,
            "CLOUD_BASE_IMAGE": cls.config.upload.cloud_base_image,
            "UPLOAD_BASE_PATH": job_base.uploads.default_path,
            "HAS_ARGO_TOKEN": cls.config.base.has_argo_token,
            "ARGO_BASE_URL": argo_url,
            "IS_LOCAL": cls.config.base.is_argo_local,
            "NAMESPACE": settings.ARGO_NAMESPACE,
            "HAS_WORKFLOW_CALLBACKS": len(workflow_callbacks) > 0,
            "WORKFLOW_CALLBACKS": workflow_callbacks,
        }

        return cls._populate_template_block("template_archive_workflow.yaml", params)

    ######  ####### #     # #     # #       #######    #    ######
    #     # #     # #  #  # ##    # #       #     #   # #   #     #
    #     # #     # #  #  # # #   # #       #     #  #   #  #     #
    #     # #     # #  #  # #  #  # #       #     # #     # #     #
    #     # #     # #  #  # #   # # #       #     # ####### #     #
    #     # #     # #  #  # #    ## #       #     # #     # #     #
    ######  #######  ## ##  #     # ####### ####### #     # ######

    @classmethod
    def gen_download_template(cls):
        """
        Generate Download Template
        """
        if cls.config.download.access_method == WorkflowEnums.FileAccess.Method.SIGNED_URL:
            raise UnImplementedError("Signed url for downloading files is not yet implemented.")

        if cls.config.download.access_method is None:
            raise ValueError(
                "Download access method and storage type should be defined."
                + "Make sure config parameters (file_access_method, file_cloud_storage) are set."
            )

        settings = get_settings()

        params = {
            "TEMPLATE_NAME": WorkflowEnums.Templates.DOWNLOAD.value,
            "IS_ERR_TOLER": cls.config.base.is_error_tolerant,
            "SECRET_NAME": cls.config.download.access_secret_name,
            "SECRET_KEY": cls.config.download.access_secret_key,
            "HAS_SECRET": cls.config.download.has_secret,
            "STORAGE_TYPE": settings.STORAGE_TYPE,
            "STORAGE_ENUM": WorkflowEnums.FileAccess.STORAGE,
            "MINIO_ENDPOINT_URL": settings.MINIO_ENDPOINT,
            "DOWNLOAD_LOGGING": cls.config.download.save_logs,
            "CLOUD_BASE_IMAGE": cls.config.download.cloud_base_image,
        }

        return cls._populate_template_block("template_download.yaml", params)

    ######  #     # #     #    #     # ####### ######  #######
    #     # #     # ##    #    ##    # #     # #     # #
    #     # #     # # #   #    # #   # #     # #     # #
    ######  #     # #  #  #    #  #  # #     # #     # #####
    #   #   #     # #   # #    #   # # #     # #     # #
    #    #  #     # #    ##    #    ## #     # #     # #
    #     #  #####  #     #    #     # ####### ######  #######

    @classmethod
    def gen_run_template(
        cls,
        job_base: JobTemplate,
        has_upload: bool = True,
        # image_url: Optional[str] = None,
        # run_command: Optional[str] = None,
        # cpu: Optional[Union[int,str]] = None,
        # memory: Optional[str] = None,
        # max_dependency: Optional[int] = 0
    ):
        """
        Generate Run Template
        """
        if cls.config.run.strategy is None:
            raise ValueError("Running strategy is not set!")

        settings = get_settings()

        params = {
            "SECRET_NAME": cls.config.download.access_secret_name,
            "SECRET_KEY": cls.config.download.access_secret_key,
            "HAS_SECRET": cls.config.download.has_secret,
            "STORAGE_TYPE": settings.STORAGE_TYPE,
            "STORAGE_ENUM": WorkflowEnums.FileAccess.STORAGE,
            "MINIO_ENDPOINT_URL": settings.MINIO_ENDPOINT,
            "CLOUD_BASE_IMAGE": cls.config.download.cloud_base_image,
            "IS_ERR_TOLER": cls.config.base.is_error_tolerant,
            "MAX_NUM": cls.config.run.max_all_jobs_dependency,
            "HAS_UPLOAD": has_upload,
            "JOB": job_base,
            # "IMG_PULL_POLICY": job_base.image_pull_policy.value,
            # "APP_INPUT_PATH": job_base.input_path,
            # "APP_PRE_COMMAND": job_base.commands_pre,
            # "APP_MAIN_COMMAND": job_base.commands_main,
            # "APP_POST_COMMAND": job_base.commands_post,
            # "APP_OUTPUT_PATH": job_base.output_path,
            # "MEMORY": job_base.resource_memory,
            # "ENV_SECRETS": job_base.env_secrets,
            # "MOUNT_SECRETS": job_base.mount_secrets,
            # "ENV_CONFIGS": job_base.env_configs,
            # "ENV_VARS": job_base.env_vars,
            # "CPU": job_base.resource_cpu,
            # "IMAGE_URL": job_base.image,
        }

        if cls.config.run.strategy == WorkflowEnums.Run.Strategy.GLOBAL:
            return cls._populate_template_block("template_run_global.yaml", params)

        if cls.config.run.strategy == WorkflowEnums.Run.Strategy.NODAL:
            return cls._populate_template_block("template_run_nodal.yaml", params)

        if cls.config.run.strategy == WorkflowEnums.Run.Strategy.UNI_GLOBAL:
            return cls._populate_template_block("unified_template_run_global.yaml", params)

        if cls.config.run.strategy == WorkflowEnums.Run.Strategy.UNI_NODAL:
            return cls._populate_template_block("unified_template_run_nodal.yaml", params)

        raise ValueError("Running strategy is unknown in the workflow!")

    #     # ######  #       #######    #    ######     #     # ####### ######  #######
    #     # #     # #       #     #   # #   #     #    ##    # #     # #     # #
    #     # #     # #       #     #  #   #  #     #    # #   # #     # #     # #
    #     # ######  #       #     # #     # #     #    #  #  # #     # #     # #####
    #     # #       #       #     # ####### #     #    #   # # #     # #     # #
    #     # #       #       #     # #     # #     #    #    ## #     # #     # #
    ######  #       ####### ####### #     # ######     #     # ####### ######  #######

    @classmethod
    def gen_upload_template(cls, jobs: List[JobTemplate]):
        """
        Generate Upload Templates
        """
        if cls.config.upload.strategy is None:
            raise ValueError(
                "Upload strategy and storage type should be defined."
                + "Make sure config parameters (upload_strategy, file_cloud_storage) are set."
            )

        settings = get_settings()

        params = {
            "TEMPLATE_NAME": WorkflowEnums.Templates.UPLOAD.value,
            "IS_ERR_TOLER": cls.config.base.is_error_tolerant,
            "SECRET_NAME": cls.config.upload.access_secret_name,
            "SECRET_KEY": cls.config.upload.access_secret_key,
            "MINIO_ENDPOINT_URL": settings.MINIO_ENDPOINT,
            "HAS_SECRET": cls.config.upload.has_secret,
            "STORAGE_TYPE": settings.STORAGE_TYPE,
            "STORAGE_ENUM": WorkflowEnums.FileAccess.STORAGE,
            "UPLOAD_LOGGING": cls.config.upload.save_logs,
            "RUN_LOGGING": cls.config.run.save_logs,
            "CLOUD_BASE_IMAGE": cls.config.upload.cloud_base_image,
        }

        if cls.config.upload.strategy == WorkflowEnums.Upload.Strategy.EVERY:
            return cls._populate_template_block("template_upload_every.yaml", params)

        if cls.config.upload.strategy == WorkflowEnums.Upload.Strategy.ONE_GO:
            params["JOBS"] = jobs
            # job_params = []
            # for _, job in enumerate(jobs):
            #     job_custom_id = job.custom_id
            #     job_name = cls._gen_internal_job_name(job_custom_id)
            #     tar_path = job_name
            #     if cls.config.upload.loc_name == WorkflowEnums.Upload.LocName.POD_NAME:
            #         tar_path = f"{cls.config.upload.loc_name.value}-{job_custom_id}"

            #     job_params.append(
            #         {
            #             "NAME": job_name,
            #             "ID": job_custom_id,
            #             "TAR_PATH": tar_path,
            #             "UPLOAD_BASE_PATH": job.uploads.default_path,
            #         }
            #     )

            # params["JOBS"] = job_params
            return cls._populate_template_block("template_upload_one_go.yaml", params)

    #     #                    #######
    ##   ##   ##   # #    #       #      ##    ####  #    #  ####
    # # # #  #  #  # ##   #       #     #  #  #      #   #  #
    #  #  # #    # # # #  #       #    #    #  ####  ####    ####
    #     # ###### # #  # #       #    ######      # #  #        #
    #     # #    # # #   ##       #    #    # #    # #   #  #    #
    #     # #    # # #    #       #    #    #  ####  #    #  ####

    @classmethod
    def gen_tasks_main_template(cls, jobs: List[JobTemplate], has_upload: Optional[bool] = True):
        """
        Generate Main Tasks
        """
        is_nodal = cls.config.run.strategy == WorkflowEnums.Run.Strategy.NODAL

        tasks_temp = []
        tasks = []
        for i, job in enumerate(jobs):
            job_name = cls._gen_internal_job_name(job.custom_id)
            task = {
                "INDEX": i,
                "DOWNLOAD_TASK_NAME": f"download-files-{job.custom_id}",
                "DOWNLOAD_TEMPLATE_NAME": WorkflowEnums.Templates.DOWNLOAD.value,
                "DOWNLOAD_FILES": json.dumps(json.dumps([file_ref.model_dump() for file_ref in job.inputs.files])),
                "DOWNLOAD_REQUIRED": len(job.inputs.files) > 0,
                "RUN_TASK_NAME": job_name,
                "RUN_TASK_CUSTOM_ID": job.custom_id,
                "RUN_TEMPLATE_NAME": WorkflowEnums.Templates.RUN.value,
                "RUN_INPUT_PARAMS": job.inputs.parameters,
                "RUN_HAS_DEPENDENCY": len(job.dependency) > 0,
                "RUN_CONTINUE_ON": cls.config.base.continue_on_run_task_failure,
                "RUN_LIST_DEPENDENCY": [
                    {
                        "INDEX": ii,
                        "PAR_JOB_NAME": cls._gen_internal_job_name(par_custom_id),
                        "PAR_JOB": cls._get_job(jobs, par_custom_id),
                        "ART_NAME": cls._get_dependency_artifact_name(ii)[1],
                        "LOC_NAME": cls._get_dependency_artifact_name(ii)[0],
                    }
                    for ii, par_custom_id in enumerate(job.dependency)
                ],
                "RUN_NODAL_PARAMS": (
                    [
                        {"NAME": "IMAGE", "VALUE": job.image},
                        {"NAME": "MEMORY", "VALUE": job.resource_memory},
                        {"NAME": "CPU", "VALUE": job.resource_cpu},
                        {"NAME": "COMMAND", "VALUE": job.commands_main},
                        {"NAME": "PRE_COMMAND", "VALUE": job.commands_pre},
                        {"NAME": "POST_COMMAND", "VALUE": job.commands_post},
                    ]
                    if is_nodal
                    else []
                ),
                "UPLOAD_TASK_NAME": f"upload-{job.custom_id}",
                "UPLOAD_TEMPLATE_NAME": WorkflowEnums.Templates.UPLOAD.value,
                "UPLOAD_BASE_PATH": job.uploads.default_path,
                "UPLOAD_COPY_PATHS": json.dumps(job.uploads.copy_paths),
                "UPLOAD_CUSTOM_PATH": job.uploads.custom_path,
                "SELECTED_UPLOAD_OBJECTS": job.uploads.selected_outputs,
            }

            # DOWNLOAD, RUN, UPLOAD -> ONE NODE
            if cls.config.run.is_unified:
                if task["RUN_HAS_DEPENDENCY"]:
                    tasks_temp.append(cls._populate_template_block("unified_task_run_chained.yaml", {"TASK": task}))
                else:
                    tasks_temp.append(cls._populate_template_block("unified_task_run_single.yaml", {"TASK": task}))
                continue

            # DOWNLOAD, RUN, UPLOAD -> SEPARATE NODES
            if task["DOWNLOAD_REQUIRED"]:
                tasks_temp.append(cls._populate_template_block("task_download.yaml", {"TASK": task}))

            if task["RUN_HAS_DEPENDENCY"]:
                tasks_temp.append(cls._populate_template_block("task_run_chained.yaml", {"TASK": task}))
            else:
                tasks_temp.append(cls._populate_template_block("task_run_single.yaml", {"TASK": task}))

            if has_upload and cls.config.upload.strategy == WorkflowEnums.Upload.Strategy.EVERY:
                tasks_temp.append(cls._populate_template_block("task_upload_every.yaml", {"TASK": task}))

            tasks.append(task)

        # UPLOAD STRATEGY -> ONCE ALL JOBS COMPLETED
        # NOT IMPLEMENTED FOR UNIFIED
        if has_upload and cls.config.upload.strategy == WorkflowEnums.Upload.Strategy.ONE_GO:
            if cls.config.run.is_unified:
                raise UnImplementedError("One go upload is not implmented for Unified Nodes.")
            tasks_temp.append(cls._populate_template_block("task_upload_one_go.yaml", {"TASKS": tasks}))

        # return TASKS
        return {"name": "main", "dag": {"tasks": tasks_temp}}

    ######                                       #######
    #     # ###### #      ###### ##### ######       #    ###### #    # #####  #        ##   ##### ######
    #     # #      #      #        #   #            #    #      ##  ## #    # #       #  #    #   #
    #     # #####  #      #####    #   #####        #    #####  # ## # #    # #      #    #   #   #####
    #     # #      #      #        #   #            #    #      #    # #####  #      ######   #   #
    #     # #      #      #        #   #            #    #      #    # #      #      #    #   #   #
    ######  ###### ###### ######   #   ######       #    ###### #    # #      ###### #    #   #   ######

    @classmethod
    def delete_workflow_artifacts(cls, workflow_uname: str):
        """
        Generates template block to delete workflow's artifact.
        """
        manifest = cls._get_template_block(
            "workflow_delete_artifacts.yaml",
            temp_format=WorkflowEnums.TemplateFormats.YAML,
        )
        manifest["spec"]["arguments"]["parameters"][0]["value"] = workflow_uname
        manifest["spec"]["templates"][0]["image"] = CloudBaseImage.AWS
        return manifest

    #     #
    #     # ###### #      #####  ###### #####   ####
    #     # #      #      #    # #      #    # #
    ####### #####  #      #    # #####  #    #  ####
    #     # #      #      #####  #      #####       #
    #     # #      #      #      #      #   #  #    #
    #     # ###### ###### #      ###### #    #  ####

    @classmethod
    def _gen_internal_job_name(cls, custom_id: Union[str, int]):
        return f"task-{custom_id}"

    @classmethod
    def _get_job(cls, jobs: List[JobTemplate], custom_id: Union[str, int]):
        job = list(filter(lambda job: job.custom_id == custom_id, jobs))

        if len(job) == 1:
            return job[0]
        raise ValueError(f"Cannot get a unique job with provided id: {custom_id}")

    @classmethod
    def _get_dependency_artifact_name(cls, index: int):
        loc_name = f"dep-art-loc-{index + 1}"
        art_name = f"dep-art-{index + 1}"
        return loc_name, art_name

    @classmethod
    def manifest_to_yaml(cls, template, filename=None):
        """
        Converts workflow template to yaml.
        """
        if filename is None:
            filename = f"{template['metadata']['generateName']}.yaml"

        with open(filename, "w") as outfile:
            yaml.dump(template, outfile)

    @classmethod
    def yaml_to_manifest(cls, yaml_path):
        """
        Converts a yaml file to workflow template.
        """
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @classmethod
    def _get_template_block(
        cls,
        name: str,
        temp_format: WorkflowEnums.TemplateFormats = WorkflowEnums.TemplateFormats.TEXT,
    ):
        """
        Gets yaml template from `argo-templates` folder and returns it in different formats.
        """
        if temp_format == WorkflowEnums.TemplateFormats.YAML:
            return ArgoTemplateGenerator.yaml_to_manifest(os.path.join(dirname, f"argo-templates/{name}"))

        if temp_format == WorkflowEnums.TemplateFormats.TEXT:
            with open(os.path.join(dirname, f"argo-templates/{name}"), "r", encoding="utf-8") as f:
                return f.read()

        raise ValueError("Unknown template format.")

    @classmethod
    def _populate_template_block(cls, name: str, parameters: dict):
        """
        Pass the name of template and its parameters and get back the populated template.
        """
        template_txt = cls._get_template_block(name, temp_format=WorkflowEnums.TemplateFormats.TEXT)
        template_jin = cls.jinja_env.from_string(template_txt)
        return yaml.safe_load(template_jin.render(parameters))
