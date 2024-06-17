from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from launchflow.gcp.resource import GCPResource
from launchflow.models.enums import EnvironmentType, ResourceProduct
from launchflow.node import Inputs, Outputs


@dataclass
class ArtifactRegistryOutputs(Outputs):
    pass


@dataclass
class ArtifactRegistryInputs(Inputs):
    format: str
    location: Optional[str] = None


class RegistryFormat(Enum):
    DOCKER = "DOCKER"
    MAVEN = "MAVEN"
    NPM = "NPM"
    PYTHON = "PYTHON"
    APT = "APT"
    YUM = "YUM"
    KUBEFLOW = "KUBEFLOW"
    GENERIC = "GENERIC"


class ArtifactRegistryRepository(GCPResource[ArtifactRegistryOutputs]):
    def __init__(
        self,
        name: str,
        format: Union[str, RegistryFormat],
        location: Optional[str] = None,
    ) -> None:
        super().__init__(
            name=name,
            product=ResourceProduct.GCP_ARTIFACT_REGISTRY_REPOSITORY,
        )
        if isinstance(format, str):
            format = RegistryFormat(format.upper())
        self.format = format
        self.location = location

    def outputs(self) -> ArtifactRegistryOutputs:
        return ArtifactRegistryOutputs()

    async def outputs_async(self) -> ArtifactRegistryOutputs:
        return ArtifactRegistryOutputs()

    def inputs(self, environment_type: EnvironmentType) -> ArtifactRegistryInputs:
        return ArtifactRegistryInputs(format=self.format.value, location=self.location)
