import logging
import subprocess
from typing import List

from ..container import Image, Volume


class Singularity:
    """"Interface with Singularity"""

    def __init__(self, bin_path='/cvmfs/oasis.opensciencegrid.org/mis/singularity/bin/singularity'):
        self.bin = bin_path

    def execute_command(self, arguments, **kwargs):
        """Execute a command in Singularity."""
        args = [self.bin] + arguments

        logging.debug(f'Executing the command: {" ".join(args)}')
        subprocess.run(args, **kwargs)

    def build(self, source_image: Image, destination: str, sandbox: bool = True, fix_perms: bool = True):
        """Uses Singularity to build image into a destination.

        Args:
            source_image: The image to be built.
            destination: folder/file to save the image.
            sandbox: whether to create the image as a sandbox (chroot directory). You probably to keep it true
                unless you would like to build SIF images. Those are slower when running rootless, because
            fix_perms: when running rootless, Singularity can create folders that the user cannot delete. To avoid
                this problems, always run fix_perms if running rootless.
        """
        logging.info(f'Building image: {source_image} into {destination}.')
        cli_arguments = ['build']

        if fix_perms:
            cli_arguments += ['--fix-perms']

        if sandbox:
            cli_arguments += ['--sandbox']

        cli_arguments += [destination, source_image.uri]

        logging.debug(f'Singularity build arguments: {cli_arguments}')

        self.execute_command(cli_arguments)

    def shell(self, container_path, volumes: List[Volume]):
        """Opens a shell in the container."""
        cli_arguments = ['shell']
        cli_arguments += self.get_mounts(volumes)
        cli_arguments += [container_path]

        logging.debug(f'Singularity shell arguments: {cli_arguments}')

        self.execute_command(cli_arguments)

    @staticmethod
    def get_mounts(volumes):
        return ['-B', ','.join(volume.mount for volume in volumes)]

    def run(self, container_path, volumes, command, root_path='~'):
        """Runs a command in the container."""
        cli_arguments = ['run']
        cli_arguments += self.get_mounts(volumes)
        cli_arguments += [container_path, '/bin/bash', '-c']
        cli_arguments += [f'cd {root_path} && {command}']
        logging.debug(f'Singularity run arguments: {cli_arguments}')
        self.execute_command(cli_arguments)
