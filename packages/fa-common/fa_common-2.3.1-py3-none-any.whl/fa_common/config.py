import logging
from enum import Enum
from typing import List, Optional, Set

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from .enums import StorageType, WorkflowEnums

# from app.shared.utils import auth

# @REVIEW: I've moved StorageType to enums.py. I suggest we move all enums to a separate file, to avoid unexpected circular dependency.
# class StorageType(str, Enum):
#     MINIO = "MINIO"
#     GCP_STORAGE = "GCP_STORAGE"
#     FIREBASE_STORAGE = "FIREBASE_STORAGE"
#     NONE = "NONE"


class DatabaseType(str, Enum):
    MONGODB = "MONGODB"
    GCP_FIRESTORE = "GCP_FIRESTORE"
    SQLITEDB = "SQLITEDB"
    NONE = "NONE"


class AuthType(str, Enum):
    OAUTH2 = "OAUTH2"
    STANDALONE = "STANDALONE"


class FACommonSettings(BaseSettings):
    VERSION: str = "2.3.1"
    API_VERSION: int = 1
    API_PRE_PATH: str = f"/api/v{API_VERSION}"

    SECURE: bool = False  # Use secure.py (set to true for prod)
    ROLLBAR_KEY: Optional[str] = None
    ROLLBAR_LOG_LEVEL: int = logging.ERROR
    FA_DEBUG: bool = False
    UNIT_TESTING: bool = False
    ENVIRONMENT: str = "local"

    # SECRET_KEY: SecretBytes = os.urandom(32)  # type:ignore
    BUILD_DATE: Optional[str] = None
    PROJECT_NAME: str = "FastAPI Backend"
    BACKEND_CORS_ORIGINS: Set[str] = set()
    # @SUGGESTION: Refactoring the name of creds required for Storages to start with
    # STORAGE prefix rather than the name of the storage so that we will have a unified
    # naming. Makes it easier to refer to this variable in other locations without needing to check
    # the storage type.
    MINIO_SECRET_KEY: Optional[SecretStr] = None
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_ACCESS_TOKEN: Optional[str] = None  # Used for Local Testing
    MINIO_ENDPOINT: Optional[str] = None
    MINIO_SSL: bool = False

    # WORKFLOW SETTINGS
    ENABLE_WORKFLOW: bool = False
    WORKFLOW_TYPE: Optional[WorkflowEnums.Type] = WorkflowEnums.Type.ARGO

    GITLAB_PRIVATE_TOKEN: Optional[str] = None
    GITLAB_GROUP_ID: Optional[int] = None
    GITLAB_URL: Optional[str] = "https://gitlab.com/"

    ARGO_TOKEN: Optional[str] = None
    ARGO_URL: Optional[str] = "https://argo.csiro.easi-eo.solutions"
    ARGO_NAMESPACE: Optional[str] = "cmr-xt-argo"
    # ARGO_FILE_ACCESS_METHOD: Optional[WorkflowEnums.FileAccess.METHOD] = WorkflowEnums.FileAccess.METHOD.DIRECT
    # ARGO_FILE_ACCESS_TYPE: Optional[WorkflowEnums.FileAccess.ACCESS_TYPE] = WorkflowEnums.FileAccess.ACCESS_TYPE.SERVICE_ACCOUNT
    # ARGO_FILE_STORAGE: Optional[WorkflowEnums.FileAccess.STORAGE] = WorkflowEnums.FileAccess.STORAGE.GCS
    STORAGE_SECRET_NAME: Optional[
        str
    ] = None  # FIXME: Check with Sam. This might overlap with MINIO secrets. @REVIEW. Refer to consistent naming suggestion.
    STORAGE_SECRET_KEY: Optional[
        str
    ] = None  # FIXME: Check with Sam. This might overlap with MINIO secrets. @REVIEW. Refer to consistent naming suggestion.
    # ARGO_UPLOAD_STRATEGY: Optional[WorkflowEnums.Upload.STRATEGY] = WorkflowEnums.Upload.STRATEGY.EVERY
    # ARGO_RUN_STRATEGY: Optional[WorkflowEnums.Run.STRATEGY] = WorkflowEnums.Run.STRATEGY.GLOBAL
    # ARGO_SAVE_RUN_LOGS: Optional[bool] = True
    # ARGO_LOGGING_STRATEGY: Optional[WorkflowEnums.Logging.STRATEGY] = WorkflowEnums.Logging.STRATEGY.FROM_ARTIFACT

    WORKFLOW_UPLOAD_PATH: str = "job_data"

    BUCKET_NAME: str = ""
    BUCKET_PREFIX: str = ""
    BUCKET_USER_FOLDER: str = "user-storage/"

    ################### AUTH #############################
    AUTH0_DOMAIN: str = ""
    API_AUDIENCE: str = ""
    """For AAD this is the Application ID"""
    USE_EXTERNAL_PROFILE: bool = True

    OAUTH2_JWKS_URI: str = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    OAUTH2_ISSUER: str = f"https://{AUTH0_DOMAIN}/"
    OAUTH2_AUTH_URL: str = f"https://{AUTH0_DOMAIN}/authorize?audience={API_AUDIENCE}"
    JWT_ALGORITHMS: List[str] = ["RS256"]
    ROLES_NAMESPACE: str = "http://namespace/roles"
    ENABLE_SCOPES: bool = True

    AUTH_TYPE: AuthType = AuthType.OAUTH2
    API_KEY_NAME: str = "api_key"
    MASTER_API_KEY: Optional[str] = None
    ######################################################

    # logging configuration
    LOGGING_LEVEL: int = logging.DEBUG if FA_DEBUG else logging.INFO

    DATABASE_TYPE: DatabaseType = DatabaseType.NONE  # FIRESTORE or MONGODB
    STORAGE_TYPE: StorageType = StorageType.NONE
    USE_FIREBASE: bool = False

    MONGODB_DSN: Optional[str] = None
    MONGODB_DBNAME: Optional[str] = None
    LOCALFS_STORAGE_PATH: Optional[str] = None
    USE_BEANIE: bool = False
    MONGO_AUTO_CONNECT: bool = True
    SQLITEDB_PATH: Optional[str] = None
    mongodb_min_pool_size: int = 0
    mongodb_max_pool_size: int = 100
    TZ: str = "UTC"
    APP_PATH: str = "fa_common"
    FASTAPI_APP: str = ""

    debug_timing: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings: Optional[FACommonSettings] = None


def get_settings(env_path=None) -> FACommonSettings:
    # Load env variables from .env file

    global settings
    if settings is None or env_path is not None:
        settings = FACommonSettings(_env_file=env_path)  # type: ignore

    return settings
