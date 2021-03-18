from dataclasses import dataclass
from typing import Optional


@dataclass
class Image:
    """A docker container image hosted on dockerhub."""
    tag: str
    source: str = 'docker'

    @property
    def uri(self):
        """Returns a Uniform Resource Identifier (URI) of this image, following the conventions of singularity."""
        return f'{self.source}://{self.tag}'


@dataclass
class Volume:
    """A volume in the host filesystem (source) that will be mounted in the container at destination."""
    source: str
    destination: Optional[str] = None

    @property
    def mount(self):
        """Returns the string that can be used with Singularity to mount the volume in a container during the
        execution.
        """
        if self.destination is not None:
            return f'{self.source}:{self.destination}'

        return self.source


@dataclass
class Container:
    """A singularity container."""
    image: Image
    path: str = 'container_sandbox'

