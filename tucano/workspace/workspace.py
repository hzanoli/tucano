import logging
import os
import shutil
from typing import Optional, List

import yaml

from ..config import config
from ..container import Volume, Container, Image
from ..singularity import Singularity


class Workspace:
    """Development environment for the ALICE software using singularity.
    It is like alidock, but it runs in your cluster!"""

    workspace_dir_name = 'workspace'

    workdir_volume = Volume(f'{os.getcwd()}/{workspace_dir_name}', f'/{workspace_dir_name}')
    x11_volume = Volume(f'{os.getenv("HOME")}/.Xauthority')

    workspace_file = config.workspace_file
    config_files = [workspace_file]

    def __init__(self, container: Container,
                 volumes: Optional[List[Volume]] = None):
        self.container = container

        if volumes is None:
            volumes = []
        self.volumes = volumes + [self.workdir_volume, self.x11_volume]

        self.singularity = Singularity()

    @classmethod
    def from_yaml(cls, yaml_file):
        """Loads the configuration for the development environment using a yaml configuration file."""

        logging.info(f'Reading configuration from: {yaml_file}')

        yaml_config = yaml.safe_load(yaml_file)

        logging.debug(f"YAML for image: '{yaml_config['image']}")

        container = Container(Image(yaml_config['image']))
        logging.info(f'Container: {container}')

        volumes = []
        if yaml_config['volumes'] is not None:
            logging.debug(f"YAML for volumes: {yaml_config['volumes']}")
            volumes_config = (x.split(':') for x in yaml_config['volumes'])

            volumes = [Volume(source, dest) for source, dest in volumes_config]

        logging.info(f'Volumes: {volumes}')

        return cls(container, volumes)

    def build(self):
        logging.info('Building development environment.')

        try:
            os.mkdir(self.workdir_volume.source)
        except FileExistsError:
            logging.warning(f'The workspace directory {self.workdir_volume.source} already exists. It was not recreated.')

        self.singularity.build(self.container.image, self.container.path)

    def shell(self):
        logging.info('Creating a shell in the development environment.')
        self.singularity.shell(self.container.path, self.volumes)

    def run(self, command):
        logging.info('Running a command in the development environment.')
        self.singularity.run(self.container.path, self.volumes, command, self.workdir_volume.destination)

    @classmethod
    def initialize_workspace(cls, force):
        logging.info(f"Initializing a development environment at {os.getcwd()}")

        for file in cls.config_files:
            if os.path.exists(file):
                if force:
                    logging.info(f"File {file} exists and it was overridden.")
                else:
                    logging.warning(f"File {file} exists and force is off. Skipping it.")
                    continue

            src = config.project_root / 'default_yaml' / file
            shutil.copy(src, file)

            logging.debug(f"Copied {src} into {os.getcwd()}/{file}")

        logging.info(f"Successfully initialized the development environment at {os.getcwd()}")
