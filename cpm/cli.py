# Copyright 2015 Tzanetos Balitsaris
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os.path
import sys

import prettytable

import cpm


def process_arguments():
    description = ('A program that implements the Critical Path Method '
                   'algorithm in order to schedule a set of project activities '
                   'at the minimum total cost with the optimum duration.')
    parser = argparse.ArgumentParser(description=description)
    arg_help = 'a file that describes the project in JSON format'
    parser.add_argument('project_file', help=arg_help)
    arg_help = 'a directory that the generated images will be placed in'
    parser.add_argument('-o', '--images-dir', help=arg_help)

    arguments = parser.parse_args()
    if not os.path.isfile(arguments.project_file):
        sys.stderr.write('The project_file is not an existing regular file.\n')
        sys.exit(1)
    if arguments.images_dir and not os.path.isdir(arguments.images_dir):
        sys.stderr.write('The images_dir is not an existing directory.\n')
        sys.exit(1)

    return arguments


def main():
    arguments = process_arguments()

    try:
        project = cpm.validate(arguments.project_file)
    except cpm.ProjectValidationException as exc:
        sys.stderr.write(str(exc) + '\n')
        sys.exit(1)
    images_dir = arguments.images_dir + '/' if arguments.images_dir else ''

    cpmnet = cpm.CriticalPathMethod(project)
    cpmnet.run_cpm()
    results, images = cpmnet.get_results(images_dir)

    results_table = prettytable.PrettyTable([
        "Project Duration", "Critical Path(s)", "Direct Cost", "Indirect Cost", "Total Cost"
    ])
    for result in results:
        results_table.add_row([
            result['project_duration'], result['critical_paths'],
            result['direct_cost'], result['indirect_cost'], result['total_cost']
        ])
    print results_table

if __name__ == '__main__':
    main()
