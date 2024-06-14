#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Any, Literal, TypeAlias, cast

from dataclasses import dataclass

from requests import Response

from ibm_watsonx_ai._wrappers import requests
from pandas import DataFrame

from ibm_watsonx_ai.experiments import Experiments
from ibm_watsonx_ai.functions import Functions
from ibm_watsonx_ai.libs.repo.mlrepositoryclient import MLRepositoryClient
from ibm_watsonx_ai.lifecycle import SpecStates
from ibm_watsonx_ai.messages.messages import Messages
from ibm_watsonx_ai.metanames import (
    ExperimentMetaNames,
    FunctionMetaNames,
    PipelineMetanames,
    SpacesMetaNames,
    ModelMetaNames,
    MemberMetaNames,
)
from ibm_watsonx_ai.models import Models
from ibm_watsonx_ai.pipelines import Pipelines
from ibm_watsonx_ai.utils import inherited_docstring, get_url
from ibm_watsonx_ai.utils.utils import _get_id_from_deprecated_uid
from ibm_watsonx_ai.wml_client_error import WMLClientError
from ibm_watsonx_ai.wml_resource import WMLResource

if TYPE_CHECKING:
    from ibm_watsonx_ai import APIClient
    import numpy
    import pandas
    import pyspark

    LabelColumnNamesType: TypeAlias = (
        numpy.ndarray[Any, numpy.dtype[numpy.str_]] | list[str]
    )
    TrainingDataType: TypeAlias = (
        pandas.DataFrame | numpy.ndarray | pyspark.sql.Dataframe | list
    )
    TrainingTargetType: TypeAlias = (
        pandas.DataFrame | pandas.Series | numpy.ndarray | list
    )
    FeatureNamesArrayType: TypeAlias = numpy.ndarray | list

_DEFAULT_LIST_LENGTH = 50


class Repository(WMLResource):
    """Store and manage models, functions, spaces, pipelines and experiments
    using Watson Machine Learning Repository.

    To view ModelMetaNames, use:

    .. code-block:: python

        client.repository.ModelMetaNames.show()

    To view ExperimentMetaNames, use:

    .. code-block:: python

        client.repository.ExperimentMetaNames.show()

    To view FunctionMetaNames, use:

    .. code-block:: python

        client.repository.FunctionMetaNames.show()

    To view PipelineMetaNames, use:

    .. code-block:: python

        client.repository.PipelineMetaNames.show()

    """

    @dataclass
    class ModelAssetTypes:
        """Data class with supported model asset types."""

        DO_DOCPLEX_20_1: str = "do-docplex_20.1"
        DO_OPL_20_1: str = "do-opl_20.1"
        DO_CPLEX_20_1: str = "do-cplex_20.1"
        DO_CPO_20_1: str = "do-cpo_20.1"
        DO_DOCPLEX_22_1: str = "do-docplex_22.1"
        DO_OPL_22_1: str = "do-opl_22.1"
        DO_CPLEX_22_1: str = "do-cplex_22.1"
        DO_CPO_22_1: str = "do-cpo_22.1"
        WML_HYBRID_0_1: str = "wml-hybrid_0.1"
        PMML_4_2_1: str = "pmml_4.2.1"
        PYTORCH_ONNX_1_12: str = "pytorch-onnx_1.12"
        PYTORCH_ONNX_RT22_2: str = "pytorch-onnx_rt22.2"
        PYTORCH_ONNX_2_0: str = "pytorch-onnx_2.0"
        PYTORCH_ONNX_RT23_1: str = "pytorch-onnx_rt23.1"
        SCIKIT_LEARN_1_1: str = "scikit-learn_1.1"
        MLLIB_3_3: str = "mllib_3.3"
        SPSS_MODELER_17_1: str = "spss-modeler_17.1"
        SPSS_MODELER_18_1: str = "spss-modeler_18.1"
        SPSS_MODELER_18_2: str = "spss-modeler_18.2"
        TENSORFLOW_2_9: str = "tensorflow_2.9"
        TENSORFLOW_RT22_2: str = "tensorflow_rt22.2"
        TENSORFLOW_2_12: str = "tensorflow_2.12"
        TENSORFLOW_RT23_1: str = "tensorflow_rt23.1"
        XGBOOST_1_6: str = "xgboost_1.6"
        PROMPT_TUNE_1_0: str = "prompt_tune_1.0"
        CUSTOM_FOUNDATION_MODEL_1_0: str = "custom_foundation_model_1.0"

    cloud_platform_spaces = False
    icp_platform_spaces = False

    def __init__(self, client: APIClient) -> None:
        WMLResource.__init__(self, __name__, client)
        self._ml_repository_client: MLRepositoryClient | None = None

        self.ExperimentMetaNames = ExperimentMetaNames()
        self.FunctionMetaNames = FunctionMetaNames()
        self.PipelineMetaNames = PipelineMetanames()
        self.SpacesMetaNames = SpacesMetaNames()
        self.ModelMetaNames = ModelMetaNames()
        self.MemberMetaNames = MemberMetaNames()

        self._refresh_repo_client()  # regular token is initialized in service_instance

    def _refresh_repo_client(self) -> None:
        # If apiKey is passed in credentials then refresh repoclient with IAM token else MLToken
        self._ml_repository_client = MLRepositoryClient(self._credentials.url)
        if self._client.proceed is True:
            if self._client.service_instance._is_iam() is not None:
                self._ml_repository_client.authorize_with_token(self._client.token)
                self._ml_repository_client._add_header(
                    "X-WML-User-Client", "PythonClient"
                )
                if self._client.default_project_id is not None:
                    self._ml_repository_client._add_header(
                        "X-Watson-Project-ID", self._client.default_project_id
                    )
            else:
                self._ml_repository_client.authorize_with_iamtoken(
                    self._client.token,
                    self._credentials.instance_id,
                    True,
                )

                self._ml_repository_client._add_header(
                    "X-WML-User-Client", "PythonClient"
                )

                if self._client.default_project_id is not None:
                    self._ml_repository_client._add_header(
                        "X-Watson-Project-ID", self._client.default_project_id
                    )
        else:
            if self._client._is_IAM():
                self._ml_repository_client.authorize_with_iamtoken(
                    self._client.token,
                    self._credentials.instance_id,
                    True,
                )

                self._ml_repository_client._add_header(
                    "X-WML-User-Client", "PythonClient"
                )

                if self._client.default_project_id is not None:
                    self._ml_repository_client._add_header(
                        "X-Watson-Project-ID", self._client.default_project_id
                    )
            else:
                if self._client.ICP_PLATFORM_SPACES:
                    self._repotoken = self._client.service_instance._get_token()
                    self._ml_repository_token = self._repotoken.replace("Bearer", "")
                    self._ml_repository_client.authorize_with_token(
                        self._ml_repository_token
                    )
                else:
                    self._ml_repository_client.authorize(
                        self._credentials.username,
                        self._credentials.password,
                    )

                    self._ml_repository_client._add_header(
                        "X-WML-User-Client", "PythonClient"
                    )

                    if self._client.default_project_id is not None:
                        self._ml_repository_client._add_header(
                            "X-Watson-Project-ID", self._client.default_project_id
                        )

    @inherited_docstring(
        Experiments.store, {"experiments.get_href": "repository.get_experiment_href"}
    )
    def store_experiment(self, meta_props: dict) -> dict:
        return self._client.experiments.store(meta_props)

    @inherited_docstring(Pipelines.store)
    def store_pipeline(self, meta_props: dict) -> dict:
        return self._client.pipelines.store(meta_props)

    @inherited_docstring(Models.store, {"store()": "store_model()"})
    def store_model(
        self,
        model: str | object | None = None,
        meta_props: dict | None = None,
        training_data: TrainingDataType | None = None,
        training_target: TrainingTargetType | None = None,
        pipeline: object | None = None,
        feature_names: FeatureNamesArrayType | None = None,
        label_column_names: LabelColumnNamesType | None = None,
        subtrainingId: str | None = None,
        round_number: int | None = None,
        experiment_metadata: dict | None = None,
        training_id: str | None = None,
    ) -> dict:
        return self._client._models.store(
            model=model,
            meta_props=meta_props,
            training_data=training_data,
            training_target=training_target,
            pipeline=pipeline,
            feature_names=feature_names,
            label_column_names=label_column_names,
            subtrainingId=subtrainingId,
            round_number=round_number,
            experiment_metadata=experiment_metadata,
            training_id=training_id,
        )

    def clone(
        self,
        artifact_id: str,
        space_id: str | None = None,
        action: str = "copy",
        rev_id: str | None = None,
    ) -> dict:
        raise WMLClientError(Messages.get_message(message_id="cloning_not_supported"))

    @inherited_docstring(Functions.store)
    def store_function(
        self, function: str | Callable, meta_props: str | dict[str, Any]
    ) -> dict:
        return self._client._functions.store(function, meta_props)

    @inherited_docstring(Models.create_revision)
    def create_model_revision(self, model_id: str | None = None, **kwargs: Any) -> dict:
        model_id = _get_id_from_deprecated_uid(kwargs, model_id, "model")
        return self._client._models.create_revision(model_id=model_id)

    @inherited_docstring(Pipelines.create_revision)
    def create_pipeline_revision(
        self, pipeline_id: str | None = None, **kwargs: Any
    ) -> dict:
        pipeline_id = _get_id_from_deprecated_uid(kwargs, pipeline_id, "pipeline")
        return self._client.pipelines.create_revision(pipeline_id=pipeline_id)

    @inherited_docstring(Functions.create_revision)
    def create_function_revision(
        self, function_id: str | None = None, **kwargs: Any
    ) -> dict:
        return self._client._functions.create_revision(
            function_id=function_id, **kwargs
        )

    @inherited_docstring(Experiments.create_revision)
    def create_experiment_revision(self, experiment_id: str) -> dict:
        return self._client.experiments.create_revision(experiment_id=experiment_id)

    @inherited_docstring(Models.update, {"meta_props": "updated_meta_props"})
    def update_model(
        self,
        model_id: str | None = None,
        updated_meta_props: dict | None = None,
        update_model: Any | None = None,
        **kwargs: Any,
    ) -> dict:
        model_id = _get_id_from_deprecated_uid(kwargs, model_id, "model")
        return self._client._models.update(model_id, updated_meta_props, update_model)

    @inherited_docstring(Experiments.update)
    def update_experiment(
        self,
        experiment_id: str | None = None,
        changes: dict | None = None,
        **kwargs: Any,
    ) -> dict:
        return self._client.experiments.update(experiment_id, changes, **kwargs)

    @inherited_docstring(Functions.update)
    def update_function(
        self,
        function_id: str | None,
        changes: dict | None = None,
        update_function: str | Callable | None = None,
        **kwargs: Any,
    ) -> dict:
        return self._client._functions.update(
            function_id, changes, update_function, **kwargs
        )

    @inherited_docstring(Pipelines.update)
    def update_pipeline(
        self,
        pipeline_id: str | None = None,
        changes: dict | None = None,
        rev_id: str | None = None,
        **kwargs: Any,
    ) -> dict:
        pipeline_id = _get_id_from_deprecated_uid(kwargs, pipeline_id, "pipeline")
        return self._client.pipelines.update(pipeline_id, changes, rev_id, **kwargs)

    @inherited_docstring(Models.load)
    def load(self, artifact_id: str | None = None, **kwargs: Any) -> object:
        artifact_id = _get_id_from_deprecated_uid(kwargs, artifact_id, "artifact")
        return self._client._models.load(artifact_id)

    def download(
        self,
        artifact_id: str | None = None,
        filename: str = "downloaded_artifact.tar.gz",
        rev_id: str | None = None,
        format: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Downloads configuration file for artifact with specified id.

        :param artifact_id: Unique Id of model or function
        :type artifact_id: str
        :param filename: name of the file to which the artifact content has to be downloaded
        :type filename: str, optional
        :param rev_id: revision id
        :type rev_id: str, optional
        :param format: format of the content, applicable for models
        :type format: str, optional

        :return: path to the downloaded artifact content
        :rtype: str

        **Examples**

        .. code-block:: python

            client.repository.download(model_id, 'my_model.tar.gz')
            client.repository.download(model_id, 'my_model.json') # if original model was saved as json, works only for xgboost 1.3
        """
        artifact_id = _get_id_from_deprecated_uid(kwargs, artifact_id, "artifact")
        rev_id = _get_id_from_deprecated_uid(kwargs, rev_id, "rev", can_be_none=True)

        self._validate_type(artifact_id, "artifact_id", str, True)
        self._validate_type(filename, "filename", str, True)

        res = self._check_artifact_type(str(artifact_id))

        if res["model"] is True:
            return self._client._models.download(artifact_id, filename, rev_id, format)
        elif res["function"] is True:
            return self._client._functions.download(artifact_id, filename, rev_id)
        else:
            raise WMLClientError(
                "Unexpected type of artifact to download or Artifact with artifact_id: '{}' does not exist.".format(
                    artifact_id
                )
            )

    def delete(
        self, artifact_id: str | None = None, **kwargs: Any
    ) -> Literal["SUCCESS"]:
        """Delete model, experiment, pipeline or function from repository.

        :param artifact_id: Unique id of stored model, experiment, function or pipeline
        :type artifact_id: str

        :return: status "SUCCESS" if deletion is successful
        :rtype: Literal["SUCCESS"]

        **Example**

        .. code-block:: python

            client.repository.delete(artifact_id)
        """
        artifact_id = _get_id_from_deprecated_uid(kwargs, artifact_id, "artifact")

        Repository._validate_type(artifact_id, "artifact_id", str, True)
        if self._if_deployment_exist_for_asset(artifact_id):
            raise WMLClientError(
                "Cannot delete artifact that has existing deployments. Please delete all associated deployments and try again"
            )
        params = self._client._params()
        params.update({"purge_on_delete": "true"})

        response = requests.delete(
            self._client.service_instance._href_definitions.get_asset_href(artifact_id),
            params=params,
            headers=self._client._get_headers(),
        )

        if response.status_code == 200 or response.status_code == 204:
            if response.status_code == 200:
                response = self._handle_response(200, "delete assets", response)
                return response
            else:
                response = self._handle_response(204, "delete assets", response)
                return response
        else:
            if response.status_code == 404:
                raise WMLClientError(
                    "Artifact with artifact_id: '{}' does not exist.".format(
                        artifact_id
                    )
                )
            else:
                raise WMLClientError(
                    "Deletion error for the given id : ", response.text
                )

    def get_details(
        self,
        artifact_id: str | None = None,
        spec_state: SpecStates | None = None,
        **kwargs: Any,
    ) -> dict:
        """Get metadata of stored artifacts. If `artifact_id` is not specified returns all models, experiments,
        functions and pipelines metadata.

        :param artifact_id: Unique Id of stored model, experiment, function or pipeline
        :type artifact_id: str, optional

        :param spec_state: software specification state, can be used only when `artifact_id` is None
        :type spec_state: SpecStates, optional

        :return: stored artifact(s) metadata
        :rtype: dict (if artifact_id is not None) or {"resources": [dict]} (if artifact_id is None)

        **Examples**

        .. code-block:: python

            details = client.repository.get_details(artifact_id)
            details = client.repository.get_details()

        Example of getting all repository assets with deprecated software specifications:

        .. code-block:: python

            from ibm_watsonx_ai.lifecycle import SpecStates

            details = client.repository.get_details(spec_state=SpecStates.DEPRECATED)
        """
        artifact_id = _get_id_from_deprecated_uid(
            kwargs, artifact_id, "artifact", can_be_none=True
        )
        Repository._validate_type(artifact_id, "artifact_id", str, False)

        if artifact_id is None:
            model_details = self._client._models.get_details(spec_state=spec_state)
            experiment_details = (
                self.get_experiment_details() if not spec_state else {"resources": []}
            )
            pipeline_details = (
                self.get_pipeline_details() if not spec_state else {"resources": []}
            )
            function_details = self._client._functions.get_details(
                spec_state=spec_state
            )

            details = {
                "models": model_details,
                "experiments": experiment_details,
                "pipeline": pipeline_details,
                "functions": function_details,
            }
        else:
            artifact_type = self._check_artifact_type(str(artifact_id))

            if artifact_type["model"] is True:
                details = self.get_model_details(artifact_id)
            elif artifact_type["experiment"] is True:
                details = self.get_experiment_details(artifact_id)
            elif artifact_type["pipeline"] is True:
                details = self.get_pipeline_details(artifact_id)
            elif artifact_type["function"] is True:
                details = self.get_function_details(artifact_id)
            else:
                raise WMLClientError(
                    "Getting artifact details failed. Artifact id: '{}' not found.".format(
                        artifact_id
                    )
                )

        return details

    @inherited_docstring(Models.get_details)
    def get_model_details(
        self,
        model_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
        spec_state: SpecStates | None = None,
        **kwargs: Any,
    ) -> dict:
        model_id = _get_id_from_deprecated_uid(
            kwargs, model_id, "model", can_be_none=True
        )
        return self._client._models.get_details(
            model_id,
            limit,
            asynchronous=asynchronous,
            get_all=get_all,
            spec_state=spec_state,
        )

    @inherited_docstring(Models.get_revision_details)
    def get_model_revision_details(
        self, model_id: str | None = None, rev_id: str | None = None, **kwargs: Any
    ) -> dict:
        model_id = _get_id_from_deprecated_uid(kwargs, model_id, "model")
        rev_id = _get_id_from_deprecated_uid(kwargs, rev_id, "rev")
        return self._client._models.get_revision_details(model_id, rev_id)

    @inherited_docstring(Experiments.get_details)
    def get_experiment_details(
        self,
        experiment_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
        **kwargs: Any,
    ) -> dict:
        return self._client.experiments.get_details(
            experiment_id, limit, asynchronous, get_all, **kwargs
        )

    @inherited_docstring(Experiments.get_revision_details)
    def get_experiment_revision_details(
        self, experiment_id: str, rev_id: str, **kwargs: Any
    ) -> dict:
        return self._client.experiments.get_revision_details(
            experiment_id, rev_id, **kwargs
        )

    @inherited_docstring(Functions.get_details)
    def get_function_details(
        self,
        function_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
        spec_state: SpecStates | None = None,
        **kwargs: Any,
    ) -> dict:
        return self._client._functions.get_details(
            function_id, limit, asynchronous, get_all, spec_state, **kwargs
        )

    @inherited_docstring(Functions.get_revision_details)
    def get_function_revision_details(
        self, function_id: str, rev_id: str, **kwargs: Any
    ) -> dict:
        return self._client._functions.get_revision_details(
            function_id, rev_id, **kwargs
        )

    @inherited_docstring(Pipelines.get_details)
    def get_pipeline_details(
        self,
        pipeline_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
        **kwargs: Any,
    ) -> dict:
        pipeline_id = _get_id_from_deprecated_uid(
            kwargs, pipeline_id, "pipeline", can_be_none=True
        )
        Repository._validate_type(pipeline_id, "pipeline_id", str, False)
        Repository._validate_type(limit, "limit", int, False)
        Repository._validate_type(asynchronous, "asynchronous", bool, False)
        Repository._validate_type(get_all, "get_all", bool, False)
        return self._client.pipelines.get_details(
            pipeline_id, limit, asynchronous, get_all, **kwargs
        )

    @inherited_docstring(Pipelines.get_revision_details)
    def get_pipeline_revision_details(
        self, pipeline_id: str | None = None, rev_id: str | None = None, **kwargs: Any
    ) -> dict:
        pipeline_id = _get_id_from_deprecated_uid(kwargs, pipeline_id, "pipeline")
        return self._client.pipelines.get_revision_details(
            pipeline_id, rev_id, **kwargs
        )

    @staticmethod
    @inherited_docstring(Models.get_href)
    def get_model_href(model_details: dict) -> str:
        return Models.get_href(model_details)

    @staticmethod
    @inherited_docstring(Models.get_id)
    def get_model_id(model_details: dict) -> str:
        return Models.get_id(model_details)

    @staticmethod
    @inherited_docstring(
        Experiments.get_id,
        {"experiments.get_details": "repository.get_experiment_details"},
    )
    def get_experiment_id(experiment_details: dict) -> str:
        return Experiments.get_id(experiment_details)

    @staticmethod
    @inherited_docstring(
        Experiments.get_href,
        {"experiments.get_details": "repository.get_experiment_details"},
    )
    def get_experiment_href(experiment_details: dict) -> str:
        return Experiments.get_href(experiment_details)

    @staticmethod
    @inherited_docstring(Functions.get_id)
    def get_function_id(function_details: dict) -> str:
        return Functions.get_id(function_details)

    @staticmethod
    @inherited_docstring(Functions.get_href)
    def get_function_href(function_details: dict) -> str:
        return Functions.get_href(function_details)

    @staticmethod
    @inherited_docstring(
        Pipelines.get_href, {"pipelines.get_details": "repository.get_pipeline_details"}
    )
    def get_pipeline_href(pipeline_details: dict) -> str:
        return Pipelines.get_href(pipeline_details)

    @staticmethod
    @inherited_docstring(Pipelines.get_id)
    def get_pipeline_id(pipeline_details: dict) -> str:
        return Pipelines.get_id(pipeline_details)

    def list(self, framework_filter: str | None = None) -> DataFrame:
        """Lists/gets stored models, pipelines, runtimes, libraries, functions, spaces and experiments in a table/DataFrame format.
        If limit is set to None there will be only first 50 records shown.

        :param framework_filter: Get only frameworks with desired names
        :type framework_filter: str, optional

        :return: DataFrame with listed names and ids of stored models
        :rtype: pandas.DataFrame

        **Example**

        .. code-block:: python

            client.repository.list()
            client.repository.list(framework_filter='prompt_tune')
        """

        params = self._client._params()
        params.update({"limit": 1000})
        # params = {u'limit': 1000} # TODO - should be unlimited, if results not sorted

        isIcp = self._client.ICP_PLATFORM_SPACES

        endpoints = {
            "model": self._client.service_instance._href_definitions.get_published_models_href(),
            "experiment": self._client.service_instance._href_definitions.get_experiments_href(),
            "pipeline": self._client.service_instance._href_definitions.get_pipelines_href(),
            "function": self._client.service_instance._href_definitions.get_functions_href(),
        }

        artifact_get = {}
        for artifact in endpoints:
            params = self._client._params()
            artifact_get[artifact] = get_url(
                endpoints[artifact], self._client._get_headers(), params, isIcp
            )

        resources: dict[str, list] = {artifact: [] for artifact in endpoints}

        for artifact in endpoints:
            try:
                response = artifact_get[artifact]
                response_text = self._handle_response(
                    200, "getting all {}s".format(artifact), response
                )
                resources[artifact] = response_text["resources"]
            except Exception as e:
                self._logger.error(e)

        sw_spec_info = {
            s["id"]: s
            for s in self._client.software_specifications.get_details(state_info=True)[
                "resources"
            ]
        }

        def get_spec_info(spec_id: str, prop: str) -> str:
            if spec_id and spec_id in sw_spec_info:
                return sw_spec_info[spec_id].get(prop, "")
            else:
                return ""

        values = []
        for t in endpoints.keys():
            values += [
                (
                    m["metadata"]["id"],
                    m["metadata"]["name"],
                    m["metadata"]["created_at"],
                    m["entity"]["type"] if t == "model" else "-",
                    t if t != "function" else m["entity"]["type"] + " function",
                    get_spec_info(
                        m["entity"].get("software_spec", {}).get("id"), "state"
                    ),
                    get_spec_info(
                        m["entity"].get("software_spec", {}).get("id"),
                        "replacement",
                    ),
                )
                for m in resources[t]
            ]

        columns = [
            "ID",
            "NAME",
            "CREATED",
            "FRAMEWORK",
            "TYPE",
            "SPEC_STATE",
            "SPEC_REPLACEMENT",
        ]
        table = DataFrame(data=values, columns=columns)

        table = table.sort_values(by=["CREATED"], ascending=False).reset_index(
            drop=True
        )

        if framework_filter:
            table = table[table["FRAMEWORK"].str.contains(framework_filter)]

        if len(values) > _DEFAULT_LIST_LENGTH:
            print(
                "Note: Only first {} records were displayed. To display more use more specific list functions.".format(
                    _DEFAULT_LIST_LENGTH
                )
            )

        return table[:_DEFAULT_LIST_LENGTH]

    @inherited_docstring(Models.list)
    def list_models(
        self,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
    ) -> DataFrame:
        return self._client._models.list(
            limit=limit, asynchronous=asynchronous, get_all=get_all
        )

    @inherited_docstring(Experiments.list)
    def list_experiments(self, limit: int | None = None) -> DataFrame:
        return self._client.experiments.list(limit=limit)

    @inherited_docstring(Functions.list)
    def list_functions(self, limit: int | None = None) -> DataFrame:
        return self._client._functions.list(limit=limit)

    @inherited_docstring(Pipelines.list)
    def list_pipelines(self, limit: int | None = None) -> DataFrame:
        return self._client.pipelines.list(limit=limit)

    def _check_artifact_type(self, artifact_id: str) -> dict[str, bool]:
        Repository._validate_type(artifact_id, "artifact_id", str, True)

        def _artifact_exists(response: Response | None) -> bool:
            return (
                (response is not None)
                and ("status_code" in dir(response))
                and (response.status_code == 200)
            )

        isIcp = self._client.ICP_PLATFORM_SPACES

        endpoints = {
            "model": self._client.service_instance._href_definitions.get_model_last_version_href(
                artifact_id
            ),
            "pipeline": self._client.service_instance._href_definitions.get_pipeline_href(
                artifact_id
            ),
            "experiment": self._client.service_instance._href_definitions.get_experiment_href(
                artifact_id
            ),
            "function": self._client.service_instance._href_definitions.get_function_href(
                artifact_id
            ),
        }

        artifact_get = {}
        for artifact in endpoints:
            params = self._client._params()
            artifact_get[artifact] = get_url(
                endpoints[artifact], self._client._get_headers(), params, isIcp
            )

        response_get: dict[str, Response | None] = {
            artifact: None for artifact in endpoints
        }

        for artifact in endpoints:
            try:
                response_get[artifact] = artifact_get[artifact]
                artifact_res = cast(Response, response_get[artifact])

                self._logger.debug(
                    "Response({})[{}]: {}".format(
                        endpoints[artifact],
                        artifact_res.status_code,
                        artifact_res.text,
                    )
                )

            except Exception as e:
                self._logger.debug("Error during checking artifact type: " + str(e))

        artifact_type = {
            artifact: _artifact_exists(response_get[artifact])
            for artifact in response_get
        }

        return artifact_type

    def create_revision(self, artifact_id: str | None = None, **kwargs: Any) -> dict:
        """Create revision for passed `artifact_id`.

        :param artifact_id: Unique id of stored model, experiment, function or pipelines
        :type artifact_id: str

        :return: artifact new revision metadata
        :rtype: dict

        **Example**

        .. code-block:: python

            details = client.repository.create_revision(artifact_id)
        """
        artifact_id = _get_id_from_deprecated_uid(kwargs, artifact_id, "artifact")

        Repository._validate_type(artifact_id, "artifact_id", str, True)

        artifact_type = self._check_artifact_type(str(artifact_id))
        if artifact_type["experiment"] is True:
            return self._client.experiments.create_revision(artifact_id)
        if artifact_type["pipeline"] is True:
            return self._client.pipelines.create_revision(artifact_id)
        else:
            raise WMLClientError(
                "Getting artifact details failed. Artifact id: '{}' not found.".format(
                    artifact_id
                )
            )

    def _get_revision_details(
        self, artifact_id: str | None = None, **kwargs: Any
    ) -> dict:
        """Get metadata of stored artifacts revisions.

        :param artifact_id:  unique id of stored model or experiment or function or pipelines
        :type artifact_id: str

        :return: stored artifacts metadata
        :rtype: dict

        **Example**

        .. code-block:: python

            details = client.repository.get_revision_details(artifact_id)

        """
        artifact_id = _get_id_from_deprecated_uid(kwargs, artifact_id, "artifact")

        Repository._validate_type(artifact_id, "artifact_id", str, True)

        artifact_type = self._check_artifact_type(str(artifact_id))

        if artifact_type["experiment"] is True:
            details = self._client.experiments.get_revision_details(artifact_id)
        elif artifact_type["pipeline"] is True:
            details = self._client.pipelines.get_revisions(artifact_id)
        else:
            raise WMLClientError(
                "Getting artifact details failed. Artifact id: '{}' not found.".format(
                    artifact_id
                )
            )
        return details

    @inherited_docstring(Models.list_revisions)
    def list_models_revisions(
        self, model_id: str | None = None, limit: int | None = None, **kwargs: Any
    ) -> DataFrame:
        model_id = _get_id_from_deprecated_uid(kwargs, model_id, "model")
        return self._client._models.list_revisions(model_id, limit=limit, **kwargs)

    @inherited_docstring(Pipelines.list_revisions)
    def list_pipelines_revisions(
        self, pipeline_id: str | None = None, limit: int | None = None, **kwargs: Any
    ) -> DataFrame:
        pipeline_id = _get_id_from_deprecated_uid(kwargs, pipeline_id, "pipeline")
        return self._client.pipelines.list_revisions(pipeline_id, limit=limit)

    @inherited_docstring(Functions.list_revisions)
    def list_functions_revisions(
        self, function_id: str | None = None, limit: int | None = None, **kwargs: Any
    ) -> DataFrame:
        return self._client._functions.list_revisions(
            function_id, limit=limit, **kwargs
        )

    @inherited_docstring(Experiments.list_revisions)
    def list_experiments_revisions(
        self, experiment_id: str | None = None, limit: int | None = None, **kwargs: Any
    ) -> DataFrame:
        return self._client.experiments.list_revisions(
            experiment_id, limit=limit, **kwargs
        )

    @inherited_docstring(Models.promote)
    def promote_model(
        self, model_id: str, source_project_id: str, target_space_id: str
    ) -> str:  # deprecated
        return self._client._models.promote(
            model_id, source_project_id, target_space_id
        )
