#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import annotations
from typing import TYPE_CHECKING, Generator, cast, overload, Literal

from ibm_watsonx_ai.wml_client_error import (
    WMLClientError,
    MissingValue,
    PromptVariablesError,
    UnsupportedOperation,
)
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from ibm_watsonx_ai.messages.messages import Messages
from ibm_watsonx_ai.foundation_models.utils.utils import _check_model_state

from .base_model_inference import BaseModelInference

if TYPE_CHECKING:
    from ibm_watsonx_ai import APIClient

__all__ = ["DeploymentModelInference"]


class DeploymentModelInference(BaseModelInference):
    """Base abstract class for the model interface."""

    def __init__(
        self, *, deployment_id: str, api_client: APIClient, params: dict | None = None
    ) -> None:
        self.deployment_id = deployment_id

        self.params = params
        DeploymentModelInference._validate_type(params, "params", dict, False)

        self._client = api_client
        self._deployment_details = self._client.deployments.get_details(
            deployment_id=self.deployment_id, _silent=True
        )
        _check_model_state(
            self._client,
            self._deployment_details.get("entity", {}).get("base_model_id"),
        )

        if not self._client.CLOUD_PLATFORM_SPACES and self._client.CPD_version < 4.8:
            raise WMLClientError(error_msg="Operation is unsupported for this release.")

        BaseModelInference.__init__(self, __name__, self._client)

    def get_details(self) -> dict:
        """Get deployment's details

        :return: details of model or deployment
        :rtype: dict
        """
        return self._client.deployments.get_details(
            deployment_id=self.deployment_id, _silent=True
        )

    @overload
    def generate(
        self,
        prompt: str | list | None = ...,
        params: dict | None = ...,
        guardrails: bool = ...,
        guardrails_hap_params: dict | None = ...,
        guardrails_pii_params: dict | None = ...,
        concurrency_limit: int = ...,
        async_mode: Literal[False] = ...,
        validate_prompt_variables: bool = ...,
    ) -> dict | list[dict]: ...

    @overload
    def generate(
        self,
        prompt: str | list | None,
        params: dict | None,
        guardrails: bool,
        guardrails_hap_params: dict | None,
        guardrails_pii_params: dict | None,
        concurrency_limit: int,
        async_mode: Literal[True],
        validate_prompt_variables: bool,
    ) -> Generator: ...

    @overload
    def generate(
        self,
        prompt: str | list | None = ...,
        params: dict | None = ...,
        guardrails: bool = ...,
        guardrails_hap_params: dict | None = ...,
        guardrails_pii_params: dict | None = ...,
        concurrency_limit: int = ...,
        async_mode: bool = ...,
        validate_prompt_variables: bool = ...,
    ) -> dict | list[dict] | Generator: ...

    def generate(
        self,
        prompt: str | list | None = None,
        params: dict | None = None,
        guardrails: bool = False,
        guardrails_hap_params: dict | None = None,
        guardrails_pii_params: dict | None = None,
        concurrency_limit: int = 10,
        async_mode: bool = False,
        validate_prompt_variables: bool = True,
    ) -> dict | list[dict] | Generator:
        """
        Given a text prompt as input, and parameters the selected inference
        will generate a completion text as generated_text response.
        """
        prompt_required = self._deployment_type_validation(
            params, validate_prompt_variables
        )
        self._validate_type(
            prompt, "prompt", [str, list], prompt_required, raise_error_for_list=True
        )
        self._validate_type(guardrails_hap_params, "guardrails_hap_params", dict, False)
        self._validate_type(guardrails_pii_params, "guardrails_pii_params", dict, False)
        generate_text_url = self._client.service_instance._href_definitions.get_fm_deployment_generation_href(
            deployment_id=self.deployment_id, item="text"
        )

        if async_mode:
            return self._generate_with_url_async(
                prompt=prompt,
                params=params or self.params,
                generate_url=generate_text_url,
                guardrails=guardrails,
                guardrails_hap_params=guardrails_hap_params,
                guardrails_pii_params=guardrails_pii_params,
                concurrency_limit=concurrency_limit,
            )
        else:
            return self._generate_with_url(
                prompt=prompt,
                params=params,
                generate_url=generate_text_url,
                guardrails=guardrails,
                guardrails_hap_params=guardrails_hap_params,
                guardrails_pii_params=guardrails_pii_params,
                concurrency_limit=concurrency_limit,
            )

    def generate_text_stream(
        self,
        prompt: str | None = None,
        params: dict | None = None,
        raw_response: bool = False,
        guardrails: bool = False,
        guardrails_hap_params: dict | None = None,
        guardrails_pii_params: dict | None = None,
        validate_prompt_variables: bool = True,
    ) -> Generator:
        """
        Given a text prompt as input, and parameters the selected inference
        will generate a completion text as generator.
        """
        prompt_required = self._deployment_type_validation(
            params, validate_prompt_variables
        )
        self._validate_type(prompt, "prompt", str, prompt_required)
        self._validate_type(guardrails_hap_params, "guardrails_hap_params", dict, False)
        self._validate_type(guardrails_pii_params, "guardrails_pii_params", dict, False)
        if self._client._use_fm_ga_api:
            generate_text_stream_url = self._client.service_instance._href_definitions.get_fm_deployment_generation_stream_href(
                deployment_id=self.deployment_id
            )
        else:  # Remove on CPD 5.0 release
            generate_text_stream_url = self._client.service_instance._href_definitions.get_fm_deployment_generation_href(
                deployment_id=self.deployment_id, item="text_stream"
            )

        return self._generate_stream_with_url(
            prompt=prompt,
            params=params,
            raw_response=raw_response,
            generate_stream_url=generate_text_stream_url,
            guardrails=guardrails,
            guardrails_hap_params=guardrails_hap_params,
            guardrails_pii_params=guardrails_pii_params,
        )

    def tokenize(self, prompt: str, return_tokens: bool = False) -> dict:
        """
        Given a text prompt as input, and return_tokens parameter will return tokenized input text.
        """
        raise UnsupportedOperation(
            Messages.get_message(message_id="fm_tokenize_no_supported_deployment")
        )

    def get_identifying_params(self) -> dict:
        """Represent Model Inference's setup in dictionary"""
        return {
            "deployment_id": self.deployment_id,
            "params": self.params,
            "project_id": self._client.default_project_id,
            "space_id": self._client.default_space_id,
        }

    def _prepare_inference_payload(
        self,
        prompt: str | None,
        params: dict | None = None,
        guardrails: bool = False,
        guardrails_hap_params: dict | None = None,
        guardrails_pii_params: dict | None = None,
    ) -> dict:
        payload: dict = {
            "input": prompt,
        }

        if guardrails:
            if guardrails_hap_params is None:
                guardrails_hap_params = dict(
                    input=True, output=True
                )  # HAP enabled if guardrails = True

            for guardrail_type, guardrails_params in zip(
                ("hap", "pii"), (guardrails_hap_params, guardrails_pii_params)
            ):
                if guardrails_params is not None:
                    if "moderations" not in payload:
                        payload["moderations"] = {}
                    payload["moderations"].update(
                        {
                            guardrail_type: self._update_moderations_params(
                                guardrails_params
                            )
                        }
                    )

        if params:
            payload["parameters"] = params
        elif self.params:
            payload["parameters"] = self.params

        if (
            "parameters" in payload
            and GenTextParamsMetaNames.DECODING_METHOD in payload["parameters"]
        ):
            if isinstance(
                payload["parameters"][GenTextParamsMetaNames.DECODING_METHOD],
                DecodingMethods,
            ):
                payload["parameters"][GenTextParamsMetaNames.DECODING_METHOD] = payload[
                    "parameters"
                ][GenTextParamsMetaNames.DECODING_METHOD].value

        if "parameters" in payload and "return_options" in payload["parameters"]:
            if not (
                payload["parameters"]["return_options"].get("input_text", False)
                or payload["parameters"]["return_options"].get("input_tokens", False)
            ):
                raise WMLClientError(
                    Messages.get_message(
                        message_id="fm_required_parameters_not_provided"
                    )
                )

        return payload

    def _prepare_beta_inference_payload(
        self,  # Remove on CPD 5.0 release
        prompt: str | None,
        params: dict | None = None,
        guardrails: bool = False,
        guardrails_hap_params: dict | None = None,
        guardrails_pii_params: dict | None = None,
    ) -> dict:
        payload: dict = {
            "input": prompt,
        }

        if guardrails:
            default_moderations_params = {"input": True, "output": True}
            payload.update(
                {
                    "moderations": {
                        "hap": (
                            default_moderations_params | (guardrails_hap_params or {})
                        )
                    }
                }
            )

            if guardrails_pii_params is not None:
                payload["moderations"].update({"pii": guardrails_pii_params})

        if params:
            payload["parameters"] = params
        elif self.params:
            payload["parameters"] = self.params

        if (
            "parameters" in payload
            and GenTextParamsMetaNames.DECODING_METHOD in payload["parameters"]
        ):
            if isinstance(
                payload["parameters"][GenTextParamsMetaNames.DECODING_METHOD],
                DecodingMethods,
            ):
                payload["parameters"][GenTextParamsMetaNames.DECODING_METHOD] = payload[
                    "parameters"
                ][GenTextParamsMetaNames.DECODING_METHOD].value

        if "parameters" in payload and "return_options" in payload["parameters"]:
            if not (
                payload["parameters"]["return_options"].get("input_text", False)
                or payload["parameters"]["return_options"].get("input_tokens", False)
            ):
                raise WMLClientError(
                    Messages.get_message(
                        message_id="fm_required_parameters_not_provided"
                    )
                )

        return payload

    def _deployment_type_validation(
        self, params: dict | None, validate_prompt_variables: bool
    ) -> bool:
        prompt_required = True
        prompt_id = (
            self._deployment_details.get("entity", {})
            .get("prompt_template", {})
            .get("id")
        )
        if prompt_id is not None:
            prompt_required = False
            if validate_prompt_variables:
                from ibm_watsonx_ai.foundation_models.prompts import (
                    PromptTemplateManager,
                )

                prompt_template = PromptTemplateManager(
                    api_client=self._client
                ).load_prompt(prompt_id)
                prompt_template.input_variables = cast(
                    dict, prompt_template.input_variables
                )
                # params may be not specified but instead self.params is specified
                parameters = params if params is not None else self.params
                template_inputs: dict | None = (
                    parameters.get("prompt_variables")
                    if parameters is not None
                    else None
                )
                if (
                    template_inputs is None
                    and prompt_template.input_variables is not None
                ):
                    raise MissingValue(
                        "prompt_variables",
                        reason=(
                            "Prompt template contains input variables but "
                            "`prompt_variables` parameter not provided in `params`."
                        ),
                    )
                if (
                    input_variables := set(prompt_template.input_variables.keys())
                ) - set(template_inputs.keys()):
                    raise PromptVariablesError(
                        str(input_variables - set(template_inputs.keys()))
                    )
        return prompt_required
