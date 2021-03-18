from dataclasses import dataclass


@dataclass
class Package:
    """Package to be built in the container."""
    name: str
    branch: str = 'master'
    defaults: str = 'next-root6'