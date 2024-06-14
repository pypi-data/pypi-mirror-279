#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watsonx_ai.libs.repo.mlrepositoryartifact.hybrid_artifact_loader import HybridArtifactLoader


class HybridPipelineModelLoader(HybridArtifactLoader):
    """
        Returns pipeline model instance associated with this model artifact.

        :return: model
        :rtype: hybrid.model
        """
    def model_instance(self, artifact='full'):
        """
           :param artifact: query param string referring to "pipeline_model" or "full"
           Currently accepts:
           :return: returns a hybrid model content tar.gz file or pipeline_model.json
         """
        return self.load(artifact)
