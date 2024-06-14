#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import annotations
from typing import TYPE_CHECKING, Any

import os

import ibm_watsonx_ai._wrappers.requests as requests
from ibm_watsonx_ai.wml_client_error import WMLClientError
from ibm_watsonx_ai.wml_resource import WMLResource

if TYPE_CHECKING:
    from ibm_watsonx_ai import APIClient
    import pandas as pd

_DEFAULT_LIST_LENGTH = 50


class Import(WMLResource):
    def __init__(self, client: APIClient):
        WMLResource.__init__(self, __name__, client)

        self._client = client

    def start(
        self,
        file_path: str,
        space_id: str | None = None,
        project_id: str | None = None,
    ) -> dict:
        """Start the import. Either `space_id` or `project_id` has to be provided.

        :param file_path: file path to zip file with exported assets
        :type file_path: str
        :param space_id: space identifier
        :type space_id: str, optional
        :param project_id: project identifier
        :type project_id: str, optional

        :return: response json
        :rtype: dict

        **Example**

        .. code-block:: python

            details = client.import_assets.start(space_id="98a53931-a8c0-4c2f-8319-c793155e4598",
                                                 file_path="/home/user/data_to_be_imported.zip")
        """
        if space_id is None and project_id is None:
            raise WMLClientError("Either 'space_id' or 'project_id' has to be provided")

        if space_id is not None and project_id is not None:
            raise WMLClientError(
                "Either 'space_id' or 'project_id' can be provided, not both"
            )

        if not os.path.isfile(file_path):
            raise WMLClientError(
                "File with name: '{}' does not exist".format(file_path)
            )

        with open(file_path, "rb") as file:
            data = file.read()

        href = self._client.service_instance._href_definitions.imports_href()

        params = {}

        if space_id is not None:
            params.update({"space_id": space_id})
        elif project_id is not None:
            params.update({"project_id": project_id})

        creation_response = requests.post(
            href,
            params=params,
            headers=self._client._get_headers(content_type="application/zip"),
            data=data,
        )

        details = self._handle_response(
            expected_status_code=202,
            operationName="import start",
            response=creation_response,
        )

        import_id = details["metadata"]["id"]

        print(
            "import job with id {} has started. Monitor status using client.import_assets.get_details api. "
            "Check 'help(client.import_assets.get_details)' for details on the api usage".format(
                import_id
            )
        )

        return details

    def _validate_input(self, meta_props: dict) -> None:
        if "name" not in meta_props:
            raise WMLClientError(
                "Its mandatory to provide 'NAME' in meta_props. Example: "
                "client.import_assets.ConfigurationMetaNames.NAME: 'name'"
            )

        if "all_assets" not in meta_props and "asset_ids" not in meta_props:
            raise WMLClientError(
                "Its mandatory to provide either 'ALL_ASSETS' or 'ASSET_IDS' in meta_props. Example: "
                "client.import_assets.ConfigurationMetaNames.ALL_ASSETS: True"
            )

    def cancel(
        self, import_id: str, space_id: str | None = None, project_id: str | None = None
    ) -> None:
        """Cancel an import job. Either `space_id` or `project_id` has to be provided.

        .. note::

            To delete an import_id job, use delete() api

        :param import_id: import job identifier
        :type import_id: str
        :param space_id: space identifier
        :type space_id: str, optional
        :param project_id: project identifier
        :type project_id: str, optional


        **Example**

        .. code-block:: python

            client.import_assets.cancel(import_id='6213cf1-252f-424b-b52d-5cdd9814956c',
                                        space_id='3421cf1-252f-424b-b52d-5cdd981495fe')

        """
        Import._validate_type(import_id, "import_id", str, True)

        if space_id is None and project_id is None:
            raise WMLClientError("Its mandatory to provide space_id or project_id")

        if space_id is not None and project_id is not None:
            raise WMLClientError(
                "Either 'space_id' or 'project_id' can be provided, not both"
            )

        href = self._client.service_instance._href_definitions.import_href(import_id)

        params = {}

        if space_id is not None:
            params.update({"space_id": space_id})
        elif project_id is not None:
            params.update({"project_id": project_id})

        cancel_response = requests.delete(
            href, params=params, headers=self._client._get_headers()
        )

        details = self._handle_response(
            expected_status_code=204,
            operationName="cancel import",
            response=cancel_response,
        )

        if "SUCCESS" == details:
            print("Import job cancelled")

    def delete(
        self, import_id: str, space_id: str | None = None, project_id: str | None = None
    ) -> None:
        """Deletes the given `import_id` job. `space_id` or `project_id` has to be provided.

        :param import_id: import job identifier
        :type import_id: str
        :param space_id: space identifier
        :type space_id: str, optional
        :param project_id: project identifier
        :type project_id: str, optional

        **Example**

        .. code-block:: python

            client.import_assets.delete(import_id='6213cf1-252f-424b-b52d-5cdd9814956c',
                                        space_id= '98a53931-a8c0-4c2f-8319-c793155e4598')
        """
        if space_id is None and project_id is None:
            raise WMLClientError("Its mandatory to provide space_id or project_id")

        if space_id is not None and project_id is not None:
            raise WMLClientError(
                "Either 'space_id' or 'project_id' can be provided, not both"
            )

        Import._validate_type(import_id, "import_id", str, True)

        href = self._client.service_instance._href_definitions.import_href(import_id)

        params: dict[str, bool | str] = {"hard_delete": True}

        if space_id is not None:
            params.update({"space_id": space_id})
        elif project_id is not None:
            params.update({"project_id": project_id})

        delete_response = requests.delete(
            href, params=params, headers=self._client._get_headers()
        )

        details = self._handle_response(
            expected_status_code=204,
            operationName="delete import job",
            response=delete_response,
        )

        if "SUCCESS" == details:
            print("Import job deleted")

    def get_details(
        self,
        import_id: str | None = None,
        space_id: str | None = None,
        project_id: str | None = None,
        limit: int | None = None,
        asynchronous: bool = False,
        get_all: bool = False,
    ) -> dict:
        """Get metadata of the given import job. if no `import_id` is specified, all imports metadata is returned.

        :param import_id: import job identifier
        :type import_id: str, optional
        :param space_id: space identifier
        :type space_id: str, optional
        :param project_id: project identifier
        :type project_id: str, optional
        :param limit: limit number of fetched records
        :type limit: int, optional
        :param asynchronous: if `True`, it will work as a generator
        :type asynchronous: bool, optional
        :param get_all: if `True`, it will get all entries in 'limited' chunks
        :type get_all: bool, optional

        :return: import(s) metadata
        :rtype: dict (if import_id is not None) or {"resources": [dict]} (if import_id is None)

        **Example**

        .. code-block:: python

            details = client.import_assets.get_details(import_id)
            details = client.import_assets.get_details()
            details = client.import_assets.get_details(limit=100)
            details = client.import_assets.get_details(limit=100, get_all=True)
            details = []
            for entry in client.import_assets.get_details(limit=100, asynchronous=True, get_all=True):
                details.extend(entry)
        """
        if space_id is None and project_id is None:
            raise WMLClientError("Its mandatory to provide space_id or project_id")

        if space_id is not None and project_id is not None:
            raise WMLClientError(
                "Either 'space_id' or 'project_id' can be provided, not both"
            )

        Import._validate_type(import_id, "import_id", str, False)
        Import._validate_type(limit, "limit", int, False)

        href = self._client.service_instance._href_definitions.imports_href()

        params = {}

        if space_id is not None:
            params.update({"space_id": space_id})
        elif project_id is not None:
            params.update({"project_id": project_id})

        if import_id is None:
            return self._get_artifact_details(
                href,
                import_id,
                limit,
                "import job",
                query_params=params,
                _async=asynchronous,
                _all=get_all,
            )

        else:
            return self._get_artifact_details(
                href, import_id, limit, "import job", query_params=params
            )

    def list(
        self,
        space_id: str | None = None,
        project_id: str | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame:
        """Returns import jobs in a table format. If limit is set to None there will be only first 50 records shown.

        :param space_id: space identifier
        :type space_id: str, optional
        :param project_id: project identifier
        :type project_id: str, optional
        :param limit: limit number of fetched records
        :type limit: int, optional

        :return: pandas.DataFrame with listed assets
        :rtype: pandas.DataFrame

        **Example**

        .. code-block:: python

            client.import_assets.list()
        """
        if space_id is None and project_id is None:
            raise WMLClientError("Its mandatory to provide space_id or project_id")

        if space_id is not None and project_id is not None:
            raise WMLClientError(
                "Either 'space_id' or 'project_id' can be provided, not both"
            )

        if space_id is not None:
            resources = self.get_details(space_id=space_id)["resources"]
        else:
            resources = self.get_details(project_id=project_id)["resources"]

        values = [
            (
                m["metadata"]["id"],
                m["metadata"]["created_at"],
                m["entity"]["status"]["state"],
            )
            for m in resources
        ]

        table = self._list(
            values, ["ID", "CREATED", "STATUS"], limit, _DEFAULT_LIST_LENGTH
        )

        return table

    @staticmethod
    def get_id(import_details: dict) -> str:
        """Get ID of import job from import details.

        :param import_details: metadata of the import job
        :type import_details: dict

        :return: ID of the import job
        :rtype: str

        **Example**

        .. code-block:: python

            id = client.import_assets.get_id(import_details)
        """
        Import._validate_type(import_details, "import_details", object, True)

        return WMLResource._get_required_element_from_dict(
            import_details, "import_details", ["metadata", "id"]
        )
