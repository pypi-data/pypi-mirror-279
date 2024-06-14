#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
from __future__ import annotations
from typing import TYPE_CHECKING

import re

if TYPE_CHECKING:
    from ibm_watsonx_ai import APIClient

TRAINING_MODEL_HREF_PATTERN = "{}/v4/trainings/{}"
TRAINING_MODELS_HREF_PATTERN = "{}/v4/trainings"
REPO_MODELS_FRAMEWORKS_HREF_PATTERN = "{}/v3/models/frameworks"

INSTANCE_ENDPOINT_HREF_PATTERN = "{}/v3/wml_instance"
INSTANCE_BY_ID_ENDPOINT_HREF_PATTERN = "{}/v3/wml_instances/{}"
TOKEN_ENDPOINT_HREF_PATTERN = "{}/v3/identity/token"
CPD_TOKEN_ENDPOINT_HREF_PATTERN = "{}/icp4d-api/v1/authorize"
CPD_BEDROCK_TOKEN_ENDPOINT_HREF_PATTERN = "{}/idprovider/v1/auth/identitytoken"
CPD_VALIDATION_TOKEN_ENDPOINT_HREF_PATTERN = "{}/v1/preauth/validateAuth"
EXPERIMENTS_HREF_PATTERN = "{}/v4/experiments"
EXPERIMENT_HREF_PATTERN = "{}/v4/experiments/{}"
EXPERIMENT_RUNS_HREF_PATTERN = "{}/v3/experiments/{}/runs"
EXPERIMENT_RUN_HREF_PATTERN = "{}/v3/experiments/{}/runs/{}"

PUBLISHED_MODEL_HREF_PATTERN = "{}/v4/models/{}"
PUBLISHED_MODELS_HREF_PATTERN = "{}/v4/models"
LEARNING_CONFIGURATION_HREF_PATTERN = (
    "{}/v3/wml_instances/{}/published_models/{}/learning_configuration"
)
LEARNING_ITERATION_HREF_PATTERN = (
    "{}/v3/wml_instances/{}/published_models/{}/learning_iterations/{}"
)
LEARNING_ITERATIONS_HREF_PATTERN = (
    "{}/v3/wml_instances/{}/published_models/{}/learning_iterations"
)
EVALUATION_METRICS_HREF_PATTERN = (
    "{}/v3/wml_instances/{}/published_models/{}/evaluation_metrics"
)
FEEDBACK_HREF_PATTERN = "{}/v3/wml_instances/{}/published_models/{}/feedback"

DEPLOYMENTS_HREF_PATTERN = "{}/v4/deployments"
DEPLOYMENT_HREF_PATTERN = "{}/v4/deployments/{}"
DEPLOYMENT_JOB_HREF_PATTERN = "{}/v4/deployment_jobs"
DEPLOYMENT_JOBS_HREF_PATTERN = "{}/v4/deployment_jobs/{}"
DEPLOYMENT_ENVS_HREF_PATTERN = "{}/v4/deployments/environments"
DEPLOYMENT_ENV_HREF_PATTERN = "{}/v4/deployments/environments/{}"

MODEL_LAST_VERSION_HREF_PATTERN = "{}/v4/models/{}"
DEFINITION_HREF_PATTERN = "{}/v3/ml_assets/training_definitions/{}"
DEFINITIONS_HREF_PATTERN = "{}/v3/ml_assets/training_definitions"

FUNCTION_HREF_PATTERN = "{}/v4/functions/{}"
FUNCTION_LATEST_CONTENT_HREF_PATTERN = "{}/v4/functions/{}/content"
FUNCTIONS_HREF_PATTERN = "{}/v4/functions"

IAM_TOKEN_API = "{}&grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey"
IAM_TOKEN_URL = "{}/oidc/token"
PROD_SVT_URL = [
    "https://us-south.ml.cloud.ibm.com",
    "https://eu-gb.ml.cloud.ibm.com",
    "https://eu-de.ml.cloud.ibm.com",
    "https://jp-tok.ml.cloud.ibm.com",
    "https://ibm-watson-ml.mybluemix.net",
    "https://ibm-watson-ml.eu-gb.bluemix.net",
    "https://private.us-south.ml.cloud.ibm.com",
    "https://private.eu-gb.ml.cloud.ibm.com",
    "https://private.eu-de.ml.cloud.ibm.com",
    "https://private.jp-tok.ml.cloud.ibm.com",
    "https://yp-qa.ml.cloud.ibm.com",
    "https://private.yp-qa.ml.cloud.ibm.com",
    "https://yp-cr.ml.cloud.ibm.com",
    "https://private.yp-cr.ml.cloud.ibm.com",
]

PIPELINES_HREF_PATTERN = "{}/v4/pipelines"
PIPELINE_HREF_PATTERN = "{}/v4/pipelines/{}"


SPACES_HREF_PATTERN = "{}/v4/spaces"
SPACE_HREF_PATTERN = "{}/v4/spaces/{}"
MEMBER_HREF_PATTERN = "{}/v4/spaces/{}/members/{}"
MEMBERS_HREF_PATTERN = "{}/v4/spaces/{}/members"

SPACES_PLATFORM_HREF_PATTERN = "{}/v2/spaces"
SPACE_PLATFORM_HREF_PATTERN = "{}/v2/spaces/{}"
SPACES_MEMBERS_HREF_PATTERN = "{}/v2/spaces/{}/members"
SPACES_MEMBER_HREF_PATTERN = "{}/v2/spaces/{}/members/{}"

V4_INSTANCE_ID_HREF_PATTERN = "{}/ml/v4/instances/{}"

API_VERSION = "/v4"
SPACES = "/spaces"
PIPELINES = "/pipelines"
EXPERIMENTS = "/experiments"
LIBRARIES = "/libraries"
RUNTIMES = "/runtimes"
SOFTWARE_SPEC = "/software_specifications"
DEPLOYMENTS = "/deployments"
ASSET = "{}/v2/assets/{}"
ASSETS = "{}/v2/assets"
ASSET_TYPE = "{}/v2/asset_types"
ASSET_FILES = "{}/v2/asset_files/"
ATTACHMENT = "{}/v2/assets/{}/attachments/{}"
ATTACHMENT_COMPLETE = "{}/v2/assets/{}/attachments/{}/complete"
ATTACHMENTS = "{}/v2/assets/{}/attachments"
SEARCH_ASSETS = "{}/v2/asset_types/{}/search"
SEARCH_MODEL_DEFINITIONS = "{}/v2/asset_types/wml_model_definition/search"
SEARCH_DATA_ASSETS = "{}/v2/asset_types/data_asset/search"
SEARCH_SHINY = "{}/v2/asset_types/shiny_asset/search"
SEARCH_SCRIPT = "{}/v2/asset_types/script/search"
GIT_BASED_PROJECT_ASSET = "{}/userfs/v2/assets/{}"
GIT_BASED_PROJECT_ASSETS = "{}/userfs/v2/assets"
GIT_BASED_PROJECT_ASSET_TYPE = "{}/userfs/v2/asset_types"
GIT_BASED_PROJECT_ASSET_FILES = "{}/v2/asset_files/"
GIT_BASED_PROJECT_ATTACHMENT = "{}/userfs/v2/assets/{}/attachments/{}"
GIT_BASED_PROJECT_ATTACHMENT_COMPLETE = "{}/userfs/v2/assets/{}/attachments/{}/complete"
GIT_BASED_PROJECT_ATTACHMENTS = "{}/userfs/v2/assets/{}/attachments"
GIT_BASED_PROJECT_SEARCH_ASSETS = "{}/userfs/v2/asset_types/{}/search"
GIT_BASED_PROJECT_SEARCH_MODEL_DEFINITIONS = (
    "{}/userfs/v2/asset_types/wml_model_definition/search"
)
GIT_BASED_PROJECT_SEARCH_DATA_ASSETS = "{}/userfs/v2/asset_types/data_asset/search"
GIT_BASED_PROJECT_SEARCH_SHINY = "{}/userfs/v2/asset_types/shiny_asset/search"
GIT_BASED_PROJECT_SEARCH_SCRIPT = "{}/userfs/v2/asset_types/script/search"
DATA_SOURCE_TYPE = "{}/v2/datasource_types"
DATA_SOURCE_TYPE_BY_ID = "{}/v2/datasource_types/{}"
CONNECTION_ASSET = "{}/v2/connections"
CONNECTION_ASSET_SEARCH = "{}/v2/connections"
CONNECTION_BY_ID = "{}/v2/connections/{}"
CONNECTIONS_FILES = "{}/v2/connections/files"
CONNECTIONS_FILE = "{}/v2/connections/files/{}"
SOFTWARE_SPECIFICATION = "{}/v2/software_specifications/{}"
SOFTWARE_SPECIFICATIONS = "{}/v2/software_specifications"
HARDWARE_SPECIFICATION = "{}/v2/hardware_specifications/{}"
HARDWARE_SPECIFICATIONS = "{}/v2/hardware_specifications"
PACKAGE_EXTENSION = "{}/v2/package_extensions/{}"
PACKAGE_EXTENSIONS = "{}/v2/package_extensions"
PARAMETER_SET = "{}/v2/parameter_sets/{}"
PARAMETER_SETS = "{}/v2/parameter_sets"
PROJECT = "{}/v2/projects/{}"
LIST_SOFTWARE_SPECIFICATIONS = "{}/ml/v4/list/software_specifications"

V4GA_CLOUD_MIGRATION = "{}/ml/v4/repository"
V4GA_CLOUD_MIGRATION_ID = "{}/ml/v4/repository/{}"

REMOTE_TRAINING_SYSTEM = "{}/v4/remote_training_systems"
REMOTE_TRAINING_SYSTEM_ID = "{}/v4/remote_training_systems/{}"

FM_GENERATION = "{}/ml/v1/text/generation"
FM_GENERATION_BETA = "{}/ml/v1-beta/generation/{}"  # Remove on CPD 5.0 release
FM_GENERATION_STREAM = "{}/ml/v1/text/generation_stream"
FM_GET_SPECS = "{}/ml/v1/foundation_model_specs"
FM_GET_SPECS_BETA = "{}/ml/v1-beta/foundation_model_specs?version=2022-08-01"  # Remove on CPD 5.0 release
FM_GET_CUSTOM_FOUNDATION_MODELS = "{}/ml/v4/custom_foundation_models"
FM_GET_TASKS = "{}/ml/v1/foundation_model_tasks?limit={}"
FM_TOKENIZE = "{}/ml/v1/text/tokenization"
FM_TOKENIZE_BETA = "{}/ml/v1-beta/text/tokenization"  # Remove on CPD 5.0 release
FM_EMBEDDINGS = "{}/ml/v1/text/embeddings"

FM_DEPLOYMENT_GENERATION = "{}/ml/v1/deployments/{}/text/generation"
FM_DEPLOYMENT_GENERATION_STREAM = "{}/ml/v1/deployments/{}/text/generation_stream"
FM_DEPLOYMENT_GENERATION_BETA = (
    "{}/ml/v1-beta/deployments/{}/generation/{}"  # Remove on CPD 5.0 release
)

PROMPTS = "{}/wx/v1-beta/prompts"
PROMPTS_GET_ALL = "{}/v2/asset_types/wx_prompt/search"

EXPORTS = "{}/v2/asset_exports"
EXPORT_ID = "{}/v2/asset_exports/{}"
EXPORT_ID_CONTENT = "{}/v2/asset_exports/{}/content"

IMPORTS = "{}/v2/asset_imports"
IMPORT_ID = "{}/v2/asset_imports/{}"

VOLUMES = "{}/zen-data/v3/service_instances"
VOLUME_ID = "{}/zen-data/v3/service_instances/{}"
VOLUME_SERVICE = "{}/zen-data/v1/volumes/volume_services/{}"
VOLUME_SERVICE_FILE_UPLOAD = "{}/zen-volumes/{}/v1/volumes/files/"
VOLUME_MONITOR = "{}/zen-volumes/{}/v1/monitor"

PROMOTE_ASSET = "{}/projects/api/rest/catalogs/assets/{}/promote"

DATAPLATFORM_URLS_MAP = {
    "https://wml-fvt.ml.test.cloud.ibm.com": "https://dataplatform.dev.cloud.ibm.com",
    "https://yp-qa.ml.cloud.ibm.com": "https://dataplatform.test.cloud.ibm.com",
    "https://private.yp-qa.ml.cloud.ibm.com": "https://dataplatform.test.cloud.ibm.com",
    "https://yp-cr.ml.cloud.ibm.com": "https://dataplatform.test.cloud.ibm.com",
    "https://private.yp-cr.ml.cloud.ibm.com": "https://dataplatform.test.cloud.ibm.com",
    "https://jp-tok.ml.cloud.ibm.com": "https://jp-tok.dataplatform.cloud.ibm.com",
    "https://eu-gb.ml.cloud.ibm.com": "https://eu-gb.dataplatform.cloud.ibm.com",
    "https://eu-de.ml.cloud.ibm.com": "https://eu-de.dataplatform.cloud.ibm.com",
    "https://us-south.ml.cloud.ibm.com": "https://dataplatform.cloud.ibm.com",
}

WKC_MODEL_REGISTER = "{}/v1/aigov/model_inventory/models/{}/model_entry"
WKC_MODEL_LIST_FROM_CATALOG = "{}/v1/aigov/model_inventory/{}/model_entries"
WKC_MODEL_LIST_ALL = "{}/v1/aigov/model_inventory/model_entries"
TASK_CREDENTIALS = "{}/v1/task_credentials/{}"
TASK_CREDENTIALS_ALL = "{}/v1/task_credentials"


def is_url(s: str) -> bool:
    res = re.match("https?:\/\/.+", s)
    return res is not None


def is_id(s: str) -> bool:
    res = re.match("[a-z0-9\-]{36}", s)
    return res is not None


class HrefDefinitions:
    def __init__(
        self,
        client: APIClient,
        cloud_platform_spaces: bool = False,
        platform_url: str | None = None,
        cp4d_platform_spaces: bool = False,
    ):
        self._credentials = client.credentials
        self._client = client
        self.cloud_platform_spaces = cloud_platform_spaces
        self.cp4d_platform_spaces = cp4d_platform_spaces
        self.platform_url = platform_url
        self.prepend = "/ml"

    def _is_git_based_project(self) -> bool:
        return self._client.project_type == "local_git_storage"

    def _get_platform_url_if_exists(self) -> str:
        return self.platform_url if self.platform_url else self._credentials.url

    def get_training_href(self, model_id: str) -> str:
        return TRAINING_MODEL_HREF_PATTERN.format(
            self._credentials.url + self.prepend, model_id
        )

    def get_trainings_href(self) -> str:
        return TRAINING_MODELS_HREF_PATTERN.format(self._credentials.url + self.prepend)

    def get_repo_models_frameworks_href(self) -> str:
        return REPO_MODELS_FRAMEWORKS_HREF_PATTERN.format(
            self._credentials.url + self.prepend
        )

    def get_instance_endpoint_href(self) -> str:
        return INSTANCE_ENDPOINT_HREF_PATTERN.format(self._credentials.url)

    def get_instance_by_id_endpoint_href(self) -> str:
        return INSTANCE_BY_ID_ENDPOINT_HREF_PATTERN.format(
            self._credentials.url, self._credentials.instance_id
        )

    def get_token_endpoint_href(self) -> str:
        return TOKEN_ENDPOINT_HREF_PATTERN.format(self._credentials.url)

    def get_cpd_token_endpoint_href(self) -> str:
        return CPD_TOKEN_ENDPOINT_HREF_PATTERN.format(
            self._credentials.url.replace(":31002", ":31843")
        )

    def get_cpd_bedrock_token_endpoint_href(self) -> str:
        return CPD_BEDROCK_TOKEN_ENDPOINT_HREF_PATTERN.format(
            self._credentials.bedrock_url
        )

    def get_cpd_validation_token_endpoint_href(self) -> str:
        return CPD_VALIDATION_TOKEN_ENDPOINT_HREF_PATTERN.format(self._credentials.url)

    def get_published_model_href(self, model_id: str) -> str:
        return PUBLISHED_MODEL_HREF_PATTERN.format(
            self._credentials.url + self.prepend, model_id
        )

    def get_published_models_href(self) -> str:
        return PUBLISHED_MODELS_HREF_PATTERN.format(
            self._credentials.url + self.prepend
        )

    def get_learning_configuration_href(self, model_id: str) -> str:
        return LEARNING_CONFIGURATION_HREF_PATTERN.format(
            self._credentials.url, self._credentials.instance_id, model_id
        )

    def get_learning_iterations_href(self, model_id: str) -> str:
        return LEARNING_ITERATIONS_HREF_PATTERN.format(
            self._credentials.url, self._credentials.instance_id, model_id
        )

    def get_learning_iteration_href(self, model_id: str, iteration_id: str) -> str:
        return LEARNING_ITERATION_HREF_PATTERN.format(
            self._credentials.url,
            self._credentials.instance_id,
            model_id,
            iteration_id,
        )

    def get_evaluation_metrics_href(self, model_id: str) -> str:
        return EVALUATION_METRICS_HREF_PATTERN.format(
            self._credentials.url, self._credentials.instance_id, model_id
        )

    def get_feedback_href(self, model_id: str) -> str:
        return FEEDBACK_HREF_PATTERN.format(
            self._credentials.url, self._credentials.instance_id, model_id
        )

    def get_model_last_version_href(self, artifact_id: str) -> str:
        return MODEL_LAST_VERSION_HREF_PATTERN.format(
            self._credentials.url + self.prepend, artifact_id
        )

    def get_deployments_href(self) -> str:
        return DEPLOYMENTS_HREF_PATTERN.format(self._credentials.url + self.prepend)

    def get_experiments_href(self) -> str:
        return EXPERIMENTS_HREF_PATTERN.format(self._credentials.url + self.prepend)

    def get_experiment_href(self, experiment_id: str) -> str:
        return EXPERIMENT_HREF_PATTERN.format(
            self._credentials.url + self.prepend, experiment_id
        )

    def get_experiment_runs_href(self, experiment_id: str) -> str:
        return EXPERIMENT_RUNS_HREF_PATTERN.format(self._credentials.url, experiment_id)

    def get_experiment_run_href(
        self, experiment_id: str, experiment_run_id: str
    ) -> str:
        return EXPERIMENT_RUN_HREF_PATTERN.format(
            self._credentials.url, experiment_id, experiment_run_id
        )

    def get_deployment_href(self, deployment_id: str) -> str:
        return DEPLOYMENT_HREF_PATTERN.format(
            self._credentials.url + self.prepend, deployment_id
        )

    def get_definition_href(self, definition_id: str) -> str:
        return DEFINITION_HREF_PATTERN.format(self._credentials.url, definition_id)

    def get_definitions_href(self) -> str:
        return DEFINITIONS_HREF_PATTERN.format(self._credentials.url)

    def get_function_href(self, ai_function_id: str) -> str:
        return FUNCTION_HREF_PATTERN.format(
            self._credentials.url + self.prepend, ai_function_id
        )

    def get_function_latest_revision_content_href(self, ai_function_id: str) -> str:
        return FUNCTION_LATEST_CONTENT_HREF_PATTERN.format(
            self._credentials.url, ai_function_id
        )

    def get_functions_href(self) -> str:
        return FUNCTIONS_HREF_PATTERN.format(self._credentials.url + self.prepend)

    def get_pipeline_href(self, pipeline_id: str) -> str:
        return PIPELINE_HREF_PATTERN.format(
            self._credentials.url + self.prepend, pipeline_id
        )

    def get_pipelines_href(self) -> str:
        return PIPELINES_HREF_PATTERN.format(self._credentials.url + self.prepend)

    def get_space_href(self, spaces_id: str) -> str:
        return SPACE_HREF_PATTERN.format(self._credentials.url, spaces_id)

    def get_spaces_href(self) -> str:
        return SPACES_HREF_PATTERN.format(self._credentials.url)

    def get_platform_space_href(self, spaces_id: str) -> str:
        return SPACE_PLATFORM_HREF_PATTERN.format(
            self._get_platform_url_if_exists(), spaces_id
        )

    def get_platform_spaces_href(self) -> str:
        return SPACES_PLATFORM_HREF_PATTERN.format(self._get_platform_url_if_exists())

    def get_platform_spaces_member_href(self, spaces_id: str, member_id: str) -> str:
        return SPACES_MEMBER_HREF_PATTERN.format(
            self._get_platform_url_if_exists(), spaces_id, member_id
        )

    def get_platform_spaces_members_href(self, spaces_id: str) -> str:
        return SPACES_MEMBERS_HREF_PATTERN.format(
            self._get_platform_url_if_exists(), spaces_id
        )

    def get_v4_instance_id_href(self, instance_id: str) -> str:
        return V4_INSTANCE_ID_HREF_PATTERN.format(self._credentials.url, instance_id)

    def get_async_deployment_job_href(self) -> str:
        return DEPLOYMENT_JOB_HREF_PATTERN.format(self._credentials.url + self.prepend)

    def get_async_deployment_jobs_href(self, job_id: str) -> str:
        return DEPLOYMENT_JOBS_HREF_PATTERN.format(
            self._credentials.url + self.prepend, job_id
        )

    def get_iam_token_api(self) -> str:
        return IAM_TOKEN_API.format(self._credentials.api_key)

    def get_iam_token_url(self) -> str:
        if self._credentials.url in PROD_SVT_URL:
            return IAM_TOKEN_URL.format("https://iam.cloud.ibm.com")
        else:
            return IAM_TOKEN_URL.format("https://iam.test.cloud.ibm.com")

    def get_member_href(self, spaces_id: str, member_id: str) -> str:
        return MEMBER_HREF_PATTERN.format(self._credentials.url, spaces_id, member_id)

    def get_members_href(self, spaces_id: str) -> str:
        return MEMBERS_HREF_PATTERN.format(self._credentials.url, spaces_id)

    def get_data_asset_href(self, asset_id: str) -> str:
        return (
            ASSET if not self._is_git_based_project() else GIT_BASED_PROJECT_ASSET
        ).format(self._get_platform_url_if_exists(), asset_id)

    def get_data_assets_href(self) -> str:
        return (
            ASSETS if not self._is_git_based_project() else GIT_BASED_PROJECT_ASSETS
        ).format(self._get_platform_url_if_exists())

    def get_assets_href(self) -> str:
        return (
            ASSETS if not self._is_git_based_project() else GIT_BASED_PROJECT_ASSETS
        ).format(self._get_platform_url_if_exists())

    def get_asset_href(self, asset_id: str) -> str:
        return (
            ASSET if not self._is_git_based_project() else GIT_BASED_PROJECT_ASSET
        ).format(self._get_platform_url_if_exists(), asset_id)

    def get_base_asset_href(self, asset_id: str) -> str:
        return (
            ASSET if not self._is_git_based_project() else GIT_BASED_PROJECT_ASSET
        ).format("", asset_id)

    def get_base_assets_href(self) -> str:
        return (
            ASSETS if not self._is_git_based_project() else GIT_BASED_PROJECT_ASSETS
        ).format("")

    def get_base_asset_with_type_href(self, asset_type: str, asset_id: str) -> str:
        return (
            (
                ASSET if not self._is_git_based_project() else GIT_BASED_PROJECT_ASSET
            ).format("", asset_type)
            + "/"
            + asset_id
        )

    def get_attachment_href(self, asset_id: str, attachment_id: str) -> str:
        return (
            ATTACHMENT
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_ATTACHMENT
        ).format(self._get_platform_url_if_exists(), asset_id, attachment_id)

    def get_attachments_href(self, asset_id: str) -> str:
        return (
            ATTACHMENTS
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_ATTACHMENTS
        ).format(self._get_platform_url_if_exists(), asset_id)

    def get_attachment_complete_href(self, asset_id: str, attachment_id: str) -> str:
        return (
            ATTACHMENT_COMPLETE
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_ATTACHMENT_COMPLETE
        ).format(self._get_platform_url_if_exists(), asset_id, attachment_id)

    def get_search_asset_href(self) -> str:
        return (
            SEARCH_DATA_ASSETS
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_SEARCH_DATA_ASSETS
        ).format(self._get_platform_url_if_exists())

    def get_search_shiny_href(self) -> str:
        return (
            SEARCH_SHINY
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_SEARCH_SHINY
        ).format(self._get_platform_url_if_exists())

    def get_search_script_href(self) -> str:
        return (
            SEARCH_SCRIPT
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_SEARCH_SCRIPT
        ).format(self._get_platform_url_if_exists())

    def get_model_definition_assets_href(self) -> str:
        return (
            ASSETS if not self._is_git_based_project() else GIT_BASED_PROJECT_ASSETS
        ).format(self._get_platform_url_if_exists())

    def get_model_definition_search_asset_href(self) -> str:
        return (
            SEARCH_MODEL_DEFINITIONS
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_SEARCH_MODEL_DEFINITIONS
        ).format(self._get_platform_url_if_exists())

    # note: leave `wsd` in name since APIClient is still wrapped
    def get_wsd_model_attachment_href(self) -> str:
        return (
            ASSET_FILES
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_ASSET_FILES
        ).format(self._credentials.url)

    def get_asset_search_href(self, asset_type: str) -> str:
        return (
            SEARCH_ASSETS
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_SEARCH_ASSETS
        ).format(self._get_platform_url_if_exists(), asset_type)

    def get_wsd_asset_type_href(self) -> str:
        return (
            ASSET_TYPE
            if not self._is_git_based_project()
            else GIT_BASED_PROJECT_ASSET_TYPE
        ).format(self._credentials.url)

    def get_connections_href(self) -> str:
        return CONNECTION_ASSET.format(self._get_platform_url_if_exists())

    def get_connection_by_id_href(self, connection_id: str) -> str:
        return CONNECTION_BY_ID.format(
            self._get_platform_url_if_exists(), connection_id
        )

    def get_connections_files_href(self) -> str:
        return CONNECTIONS_FILES.format(self._get_platform_url_if_exists())

    def get_connections_file_href(self, file_name: str) -> str:
        return CONNECTIONS_FILE.format(self._get_platform_url_if_exists(), file_name)

    def get_connection_data_types_href(self) -> str:
        return DATA_SOURCE_TYPE.format(self._get_platform_url_if_exists())

    def get_connection_data_type_by_id_href(self, datasource_type_id: str) -> str:
        return DATA_SOURCE_TYPE_BY_ID.format(
            self._get_platform_url_if_exists(), datasource_type_id
        )

    def get_sw_spec_href(self, sw_spec_id: str) -> str:
        return SOFTWARE_SPECIFICATION.format(
            self._get_platform_url_if_exists(), sw_spec_id
        )

    def get_sw_specs_href(self) -> str:
        return SOFTWARE_SPECIFICATIONS.format(self._get_platform_url_if_exists())

    def get_hw_spec_href(self, hw_spec_id: str) -> str:
        return HARDWARE_SPECIFICATION.format(
            self._get_platform_url_if_exists(), hw_spec_id
        )

    def get_hw_specs_href(self) -> str:
        return HARDWARE_SPECIFICATIONS.format(self._get_platform_url_if_exists())

    def get_pkg_extn_href(self, pkg_extn_id: str) -> str:
        return PACKAGE_EXTENSION.format(self._get_platform_url_if_exists(), pkg_extn_id)

    def get_pkg_extns_href(self) -> str:
        return PACKAGE_EXTENSIONS.format(self._get_platform_url_if_exists())

    def get_project_href(self, project_id: str) -> str:
        return PROJECT.format(self._get_platform_url_if_exists(), project_id)

    def get_software_specifications_list_href(self) -> str:
        return LIST_SOFTWARE_SPECIFICATIONS.format(self._credentials.url)

    def v4ga_cloud_migration_href(self) -> str:
        return V4GA_CLOUD_MIGRATION.format(self._credentials.url)

    def v4ga_cloud_migration_id_href(self, migration_id: str) -> str:
        return V4GA_CLOUD_MIGRATION_ID.format(self._credentials.url, migration_id)

    def exports_href(self) -> str:
        return EXPORTS.format(self._get_platform_url_if_exists())

    def export_href(self, export_id: str) -> str:
        return EXPORT_ID.format(self._get_platform_url_if_exists(), export_id)

    def export_content_href(self, export_id: str) -> str:
        return EXPORT_ID_CONTENT.format(self._get_platform_url_if_exists(), export_id)

    def imports_href(self) -> str:
        return IMPORTS.format(self._get_platform_url_if_exists())

    def import_href(self, export_id: str) -> str:
        return IMPORT_ID.format(self._get_platform_url_if_exists(), export_id)

    def remote_training_systems_href(self) -> str:
        return REMOTE_TRAINING_SYSTEM.format(self._credentials.url + self.prepend)

    def remote_training_system_href(self, remote_training_systems_id: str) -> str:
        return REMOTE_TRAINING_SYSTEM_ID.format(
            self._credentials.url + self.prepend, remote_training_systems_id
        )

    def volumes_href(self) -> str:
        return VOLUMES.format(self._credentials.url)

    def volume_href(self, volume_id: str) -> str:
        return VOLUME_ID.format(self._credentials.url, volume_id)

    def volume_service_href(self, volume_name: str) -> str:
        return VOLUME_SERVICE.format(self._credentials.url, volume_name)

    def volume_upload_href(self, volume_name: str) -> str:
        return VOLUME_SERVICE_FILE_UPLOAD.format(self._credentials.url, volume_name)

    def volume_monitor_href(self, volume_name: str) -> str:
        return VOLUME_MONITOR.format(self._credentials.url, volume_name)

    def promote_asset_href(self, asset_id: str) -> str:
        if self.cloud_platform_spaces:
            data_platform_url = DATAPLATFORM_URLS_MAP[self._credentials.url]
            return PROMOTE_ASSET.format(data_platform_url, asset_id)
        else:
            promote_href = PROMOTE_ASSET.format(self._credentials.url, asset_id)
            try:
                # note: For CPD older than 4.0 we need to roll back to older endpoint.
                if float(self._credentials.version) < 4.0:
                    promote_href = promote_href.replace("/projects", "")
                # --- end note
            finally:
                return promote_href

    def get_wkc_model_register_href(self, model_id: str) -> str:
        return WKC_MODEL_REGISTER.format(self._get_platform_url_if_exists(), model_id)

    def get_wkc_model_list_from_catalog_href(self, catalog_id: str) -> str:
        return WKC_MODEL_LIST_FROM_CATALOG.format(
            self._get_platform_url_if_exists(), catalog_id
        )

    def get_wkc_model_list_all_href(self) -> str:
        return WKC_MODEL_LIST_ALL.format(self._get_platform_url_if_exists())

    def get_wkc_model_delete_href(self, asset_id: str) -> str:
        return WKC_MODEL_REGISTER.format(self._get_platform_url_if_exists(), asset_id)

    def get_task_credentials_href(self, task_credentials_id: str) -> str:
        return TASK_CREDENTIALS.format(
            self._get_platform_url_if_exists(), task_credentials_id
        )

    def get_task_credentials_all_href(self) -> str:
        return TASK_CREDENTIALS_ALL.format(self._get_platform_url_if_exists())

    def get_fm_specifications_href(self) -> str:
        if self._client._use_fm_ga_api:
            return FM_GET_SPECS.format(self._credentials.url)
        else:
            return FM_GET_SPECS_BETA.format(
                self._credentials.url
            )  # Remove on CPD 5.0 release

    def get_fm_custom_foundation_models_href(self) -> str:
        return FM_GET_CUSTOM_FOUNDATION_MODELS.format(self._credentials.url)

    def get_fm_tasks_href(self, limit: str) -> str:
        return FM_GET_TASKS.format(self._credentials.url, limit)

    def get_fm_generation_href(self, item: str | None = None) -> str:
        if self._client._use_fm_ga_api:
            return FM_GENERATION.format(self._credentials.url)
        else:
            return FM_GENERATION_BETA.format(
                self._credentials.url, item
            )  # Remove on CPD 5.0 release

    def get_fm_generation_stream_href(self) -> str:
        return FM_GENERATION_STREAM.format(self._credentials.url)

    def get_fm_tokenize_href(self) -> str:
        if self._client._use_fm_ga_api:
            return FM_TOKENIZE.format(self._credentials.url)
        else:
            return FM_TOKENIZE_BETA.format(
                self._credentials.url
            )  # Remove on CPD 5.0 release

    def get_fm_deployment_generation_href(
        self, deployment_id: str, item: str | None = None
    ) -> str:
        if self._client._use_fm_ga_api:
            return FM_DEPLOYMENT_GENERATION.format(self._credentials.url, deployment_id)
        else:
            return FM_DEPLOYMENT_GENERATION_BETA.format(
                self._credentials.url, deployment_id, item
            )  # Remove on CPD 5.0 release

    def get_fm_deployment_generation_stream_href(self, deployment_id: str) -> str:
        return FM_DEPLOYMENT_GENERATION_STREAM.format(
            self._credentials.url, deployment_id
        )

    def get_prompts_href(self) -> str:
        return PROMPTS.format(self._get_platform_url_if_exists())

    def get_prompts_all_href(self) -> str:
        return PROMPTS_GET_ALL.format(self._get_platform_url_if_exists())

    def get_parameter_set_href(self, parameter_sets_id: str) -> str:
        return PARAMETER_SET.format(
            self._get_platform_url_if_exists(), parameter_sets_id
        )

    def get_parameter_sets_href(self) -> str:
        return PARAMETER_SETS.format(self._get_platform_url_if_exists())

    def get_fm_embeddings_href(self):
        return FM_EMBEDDINGS.format(self._credentials.url)
