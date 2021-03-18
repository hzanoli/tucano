#!/usr/bin/env python3

import subprocess
import argparse
import os

sandbox_image_path = '/project/alice/users/hezanoli/o2/o2'
local_building_dir = '/project/alice/users/hezanoli/o2/alice'
build_dir_in_sandbox = '/alice'
singularity_bin = '/cvmfs/oasis.opensciencegrid.org/mis/singularity/bin/singularity'

parser = argparse.ArgumentParser()

parser.add_argument('--image', '-i', default=sandbox_image_path,
                    help='Path to the image (sandbox).')

parser.add_argument('--host_folder', '-l', default=local_building_dir,
                    help='Path in the host filesystem where the software will be built.')

parser.add_argument('--image_folder', '-if', default=build_dir_in_sandbox,
                    help='Path in the image filesystem where the software will be built.')

parser.add_argument('--package', '-p', default='O2',
                    help='Path in the image filesystem where the software will be built.')

parser.add_argument('--branch', '-b', default='dev',
                    help='branch to checkout the ')

parser.add_argument('--defaults', '-d', default='o2',
                    help='Redirects to the defaults parameter to be passed to aliBuild.')

parser.add_argument('--singularity', '-s', default=singularity_bin,
                    help='location of the singularity binary')

parser.add_argument('--dry_run', '-dr', default=False, action='store_true',
                    help='Do not actually run the build, but prints the build command')

parser.add_argument('--clean', '-c', default=False, action='store_true',
                    help='call aliBuild clean --agressive-cleanup to make save space.')

if __name__ == '__main__':
    args = parser.parse_args()
    executable = [f'{args.singularity}', 'exec']

    temp_dir = os.getenv('TMPDIR')
    if temp_dir is None:
        temp_dir = '/tmp/'

    mounts = ['-B', f'{args.host_folder}:{args.image_folder},{temp_dir}:{temp_dir}']

    singularity_command = executable + mounts + [args.image]

    print(f'Executing singularity with the command: {" ".join(singularity_command)}')

    build_in_container = f"source /root/.bashrc && cd {args.image_folder} "
    build_in_container += f"&& aliBuild init {args.package}@{args.branch} --defaults {args.defaults} "
    build_in_container += f"&& aliBuild build {args.package} --defaults {args.defaults} --debug "

    if args.clean:
        build_in_container += "&& aliBuild clean --aggressive-cleanup"

    build_command = ['bash', '-c', build_in_container]

    print(f'Build command will be: {" ".join(build_command)}')

    command = singularity_command + build_command

    if args.dry_run:
        print(f'The total command array is is: {command}')
        print(f'Which should run as {" ".join(command)}')

    else:
        with open(f'build_{args.package}.log', 'w') as opt_file:
            process = subprocess.run(command, stdout=opt_file, stderr=subprocess.STDOUT)
