#!/usr/bin/env python

import os
import sys
import shutil
from dotenv import dotenv_values
import psutil
import argparse
from colorama import init, Fore
import click
from pathlib import Path

env_path = os.path.join(Path().absolute().parent, '.env')
config = dotenv_values(env_path)

os.environ['RESOLVE_SCRIPT_API'] = config['RESOLVE_SCRIPT_API']
os.environ['RESOLVE_SCRIPT_LIB'] = config['RESOLVE_SCRIPT_LIB']
sys.path.append(os.path.join(os.environ['RESOLVE_SCRIPT_API'], 'Modules'))

# This has to be after setting the env variables for DaVinciResolveScript to work
from davincimator import Davincimator

init(autoreset=True)


def is_davinci_open() -> bool:
    for i in psutil.process_iter():
        if 'davinci' in i.name().lower():
            return True
    return False


def get_args():
    parser = argparse.ArgumentParser(description='Create DaVinci Resolve project and import media files')
    parser.add_argument('-b', '--base-project', help='Base project path to create a new one based on that')
    parser.add_argument('-c', '--copy-to', help='Copy media files to this directory if specified')
    parser.add_argument('-d', '--dir', help='Source media directory including media files')
    parser.add_argument('-f', '--file', help='Source media file')
    parser.add_argument('-p', '--project', required=True, help='DaVinci Resolve existing or new project name to create')
    parser.add_argument('-t', '--timeline', help='DaVinci Resolve existing or new timeline to create', default='master')
    return parser.parse_args()


def print_done():
    print(Fore.GREEN + 'Done!')


def main() -> None:
    if not is_davinci_open():
        print(Fore.RED + 'To run the script Davinci Resolve application must be running')
        sys.exit()

    args = get_args()
    directories = [args.dir, args.copy_to]
    for directory in directories:
        if directory is not None:
            if not os.path.isdir(directory):
                print(Fore.RED + f"Directory '{directory}' does not exist")
                sys.exit()

    davincimator = Davincimator()
    files = []
    if args.file:
        if not os.path.isfile(args.file):
            print(Fore.RED + f"File '{args.file}' does not exist")
            sys.exit()

        files.append(args.file)

    if args.dir:
        extensions = list(filter(None, config['MEDIA_EXTENSIONS_TO_IMPORT'].split(',')))
        if len(extensions) == 0:
            print(Fore.RED + 'MEDIA_EXTENSIONS_TO_IMPORT cannot be empty')
            sys.exit()

        temp_files = davincimator.find_files_source_dir(args.dir, extensions)
        files_num = len(temp_files)
        if files_num == 0:
            print(Fore.RED + f"There is no media file in {args.dir}")
            sys.exit()

        print(Fore.BLUE + f"Found {files_num} media file(s) in {args.dir}:")
        files.extend(temp_files)

        if len(files) == 0:
            print(Fore.YELLOW + 'Could not find any media file with the following extension: ' + ",".join(extensions))
            sys.exit()

    for file in files:
        print(Fore.CYAN + file)

    if not click.confirm('Would you like to continue?'):
        sys.exit()

    if args.copy_to:
        print(Fore.BLUE + f"'copy-to' dir is specified: {args.copy_to}")

        copy_to_dir = os.path.join(args.copy_to, args.project)
        print(Fore.BLUE + 'Copying files to: ' + copy_to_dir)

        davincimator.create_copy_to_dir(copy_to_dir)

        tmp_files = []
        for file in files:
            print(Fore.CYAN + f"Copying {file} ...", end=' ')
            new_file = shutil.copy2(file, copy_to_dir)
            tmp_files.append(new_file)
            print_done()

        # Because we now deal with the copied files
        files = tmp_files

    project_name = args.project
    if args.base_project:
        if not os.path.isfile(args.base_project):
            print(Fore.RED + f"Project path '{args.base_project}' does not exist")
            sys.exit()

        davincimator.project_manager.ImportProject(args.base_project, project_name)
        project = davincimator.project_manager.LoadProject(project_name)
    else:
        print(Fore.BLUE + f"Creating or loading existing '{project_name}' project ...", end=' ')
        project = davincimator.get_project_by_name(args.project)
        print_done()

        davincimator.setFPSforProjectTimline(project, files)

    print(Fore.BLUE + f"Adding files to the timeline '{args.timeline}' ...", end=' ')
    davincimator.add_files_to_timeline(project, args.timeline, files)
    print_done()


if __name__ == '__main__':
    main()
