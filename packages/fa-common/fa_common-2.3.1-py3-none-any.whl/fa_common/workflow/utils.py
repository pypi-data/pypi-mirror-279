import oyaml as yaml
from fastapi import FastAPI

from fa_common import get_current_app, get_settings, logger
from fa_common.enums import WorkflowEnums


def setup_workflow(app: FastAPI) -> None:
    settings = get_settings()
    if settings.WORKFLOW_TYPE == WorkflowEnums.Type.GITLAB:
        setup_gitlab(app)
        return

    if settings.WORKFLOW_TYPE == WorkflowEnums.Type.ARGO:
        setup_argo(app)
        return

    if settings.WORKFLOW_TYPE == WorkflowEnums.Type.NONE:
        logger.info("Workflow is set to NONE and cannot be used!")
        return

    raise ValueError("WORKFLOW_TYPE Setting is not a valid workflow option.")


def setup_argo(app: FastAPI) -> None:
    """
    Helper function to setup argo workflows
    """
    settings = get_settings()
    if settings.ARGO_TOKEN is not None and settings.ARGO_URL is not None:
        import argo_workflows

        config = argo_workflows.Configuration()
        config.host = settings.ARGO_URL

        argo = argo_workflows.ApiClient(config)
        access_token = f"Bearer {settings.ARGO_TOKEN}"

        argo.set_default_header("Authorization", access_token)

        app.argo_workflow_client = argo

        logger.info("Argo client has been setup")

    else:
        raise ValueError("Insufficient configuration to create argo client need (ARGO_URL and ARGO_TOKEN).")


def setup_gitlab(app: FastAPI) -> None:
    """
    Helper function to setup gitlab workflows
    """
    settings = get_settings()
    if settings.GITLAB_PRIVATE_TOKEN is not None and settings.GITLAB_URL is not None and settings.GITLAB_GROUP_ID is not None:
        import gitlab

        gl = gitlab.Gitlab(settings.GITLAB_URL, private_token=settings.GITLAB_PRIVATE_TOKEN)
        app.gitlab = gl  # type:ignore
        logger.info("Gitlab client has been setup")

    else:
        raise ValueError(
            "Insufficient configuration to create gitlab client need (GITLAB_URL, GITLAB_PRIVATE_TOKEN and " + "GITLAB_GROUP_ID)."
        )


def get_workflow_client():
    settings = get_settings()

    if settings.WORKFLOW_TYPE == WorkflowEnums.Type.ARGO:
        return get_argo_client()

    if settings.WORKFLOW_TYPE == WorkflowEnums.Type.GITLAB:
        return get_gitlab_client()

    raise ValueError("There is no workflow set. Nothing to return.")


def get_argo_client():
    """
    Gets instance of ArgoClient for you to make argo workflow calls.
    :return: ArgoClient
    """
    try:
        app = get_current_app()
        if app.argo_workflow_client is not None:
            from .argo_client import ArgoClient

            logger.info("Trying to create an ArgoClient instance.")
            return ArgoClient()
    except Exception as err:
        raise ValueError("Problem returning Argo client, may not be initialised.") from err
    raise ValueError("Argo client has not been initialised.")


def get_gitlab_client():
    """
    Gets instance of GitlabClient for you to make gitlab calls.
    :return: GitlabClient
    """
    try:
        app = get_current_app()
        if app.gitlab is not None:
            from .gitlab_client import GitlabClient

            return GitlabClient()
    except Exception as err:
        raise ValueError("Problem returning gitlab client, may not be initialised.") from err
    raise ValueError("Gitlab client has not been initialised.")


class GitlabCIYAMLDumper(yaml.Dumper):
    """Correctly dumps yaml for gitlab ci formatting

    Arguments:
        yaml {[type]} -- [description]
    """

    def increase_indent(self, flow=False, indentless=False):
        return super(GitlabCIYAMLDumper, self).increase_indent(flow, False)
