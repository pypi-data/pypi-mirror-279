#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

__all__ = [
    "WrongDeploymnetType",
    "ModelTypeNotSupported",
    "NotAutoAIExperiment",
    "EnvironmentNotSupported",
    "BatchJobFailed",
    "MissingScoringResults",
    "ModelStoringFailed",
    "DeploymentNotSupported",
    "MissingSpace",
    "PromotionFailed",
    "ModelPromotionFailed",
    "ServingNameNotAvailable",
]


from ibm_watsonx_ai.wml_client_error import WMLClientError


class WrongDeploymnetType(WMLClientError, ValueError):
    def __init__(self, value_name: str, reason: str | None = None):
        WMLClientError.__init__(
            self, f"This deployment is not of type: {value_name} ", reason
        )


class ModelTypeNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name: str, reason: str | None = None):
        WMLClientError.__init__(
            self, f"This model type is not supported yet: {value_name} ", reason
        )


class NotAutoAIExperiment(WMLClientError, ValueError):
    def __init__(self, value_name: str, reason: str | None = None):
        WMLClientError.__init__(
            self,
            f"This experiment_run_id is not from an AutoAI experiment: {value_name} ",
            reason,
        )


class EnvironmentNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name: str, reason: str | None = None):
        WMLClientError.__init__(
            self, f"This environment is not supported: {value_name}", reason
        )


class BatchJobFailed(WMLClientError, ValueError):
    def __init__(self, value_name: str | None = None, reason: str | None = None):
        WMLClientError.__init__(self, f"Batch job failed for job: {value_name}", reason)


class MissingScoringResults(WMLClientError, ValueError):
    def __init__(self, value_name: str | None = None, reason: str | None = None):
        WMLClientError.__init__(
            self, f"Scoring of deployment job: {value_name} not completed.", reason
        )


class ModelStoringFailed(WMLClientError, ValueError):
    def __init__(self, value_name: str | None = None, reason: str | None = None):
        WMLClientError.__init__(self, f"Model: {value_name} store failed.", reason)


class DeploymentNotSupported(WMLClientError, ValueError):
    def __init__(self, value_name: str | None = None, reason: str | None = None):
        WMLClientError.__init__(
            self, f"Deployment of type: {value_name} is not supported.", reason
        )


class MissingSpace(WMLClientError, ValueError):
    def __init__(self, value_name: str | None = None, reason: str | None = None):
        WMLClientError.__init__(
            self, f"Deployment needs to have space specified", reason
        )


class PromotionFailed(WMLClientError, ValueError):
    def __init__(
        self,
        project_id: str,
        space_id: str,
        promotion_response: dict | None = None,
        reason: str | None = None,
    ):
        WMLClientError.__init__(
            self,
            f"Asset promotion from project {project_id} to space {space_id} failed."
            f" Full response {promotion_response}",
            reason,
        )
        self.project_id = project_id
        self.space_id = space_id
        self.promotion_response = promotion_response
        self.reason = reason


class ModelPromotionFailed(PromotionFailed):
    def __init__(
        self,
        project_id: str,
        space_id: str,
        promotion_response: dict | None = None,
        reason: str | None = None,
    ):
        PromotionFailed.__init__(self, project_id, space_id, promotion_response, reason)


class ServingNameNotAvailable(WMLClientError, ValueError):
    def __init__(self, message: str):
        WMLClientError.__init__(self, message)
