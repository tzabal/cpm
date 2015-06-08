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
import json
import os.path
import pickle
import sys

import jsonschema
from mako.template import Template
import matplotlib.pyplot
import networkx
import prettytable

import cpm

PROJECT_SCHEMA = {
    "title": "Project Activities",
    "description": "The JSON schema of project activities file",
    "$schema": "http://json-schema.org/draft-04/schema",
    "type": "object",
    "properties": {
        "info": {
            "type": "object",
            "properties": {
                "indirect_cost": {
                    "type": "integer"
                }
            }
        },
        "activities": {
            "type": "array",
            "minItems": 1,
            "items": [
                {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "items": [
                        {
                            "type": "integer"
                        },
                        {
                            "type": "integer"
                        },
                        {
                            "type": "object",
                            "properties": {
                                "normal_duration": {
                                    "type": "integer"
                                },
                                "normal_cost": {
                                    "type": "integer"
                                },
                                "crash_duration": {
                                    "type": "integer"
                                },
                                "crash_cost": {
                                    "type": "integer"
                                }
                            },
                            "required": ["normal_duration", "normal_cost", "crash_duration", "crash_cost"],
                            "additionalItems": False
                        }
                    ]
                }
            ]
        }
    }
}


def generate_html_report(output_dir, results_table, images):
    template = Template(filename='templates/report.mako')
    report = output_dir + 'report.html'
    with open(report, 'w') as f:
        f.write(template.render(results_table=results_table.get_html_string(), images=images))


def draw_network(graph, pos, output_dir, iteration):
    node_labels = dict((n, str(str(n) + '(' + str(d['eet']) + ',' + str(d['let']) + ')')) for n, d in graph.nodes(data=True))
    edge_labels = dict([((u, v), graph.edge[u][v]['normal_duration']) for u, v in graph.edges()])
    networkx.draw_networkx_labels(graph, pos, labels=node_labels)
    networkx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    networkx.draw_networkx(graph, pos=pos, with_labels=False, node_size=3000, node_color='c', node_shape='o')
    matplotlib.pyplot.axis('off')
    image = output_dir + 'network-' + str(iteration) + '.png'
    matplotlib.pyplot.savefig(image)
    matplotlib.pyplot.close()
    return image


def _get_project_duration(graph):
    return graph.node[graph.nodes()[-1]]['let']


def _get_critical_path(graph):
    critical_path = []
    for node1, node2 in graph.edges():
        if graph[node1][node2]['total_float'] == 0:
            critical_path.append((node1, node2))
    return critical_path


def _get_direct_cost(graph, kw_cost):
    direct_cost = 0
    for node1, node2 in graph.edges():
        direct_cost += graph.edge[node1][node2][kw_cost]
    return direct_cost


def collect_results(graph, kw_cost):
    project_duration = _get_project_duration(graph)
    critical_path = _get_critical_path(graph)
    direct_cost = _get_direct_cost(graph, kw_cost)
    indirect_cost = project_duration * graph.graph['indirect_cost']
    total_cost = direct_cost + indirect_cost
    return {'project_duration': project_duration,
            'critical_path': critical_path,
            'direct_cost': direct_cost,
            'indirect_cost': indirect_cost,
            'total_cost': total_cost}


def validate(project_file):
    with open(project_file) as f:
        try:
            project = json.load(f)
            jsonschema.validate(project, PROJECT_SCHEMA)
        except ValueError as value_error:
            sys.stderr.write('The project file is not a valid JSON file.\n')
            sys.stderr.write(value_error)
            sys.exit(1)
        except jsonschema.ValidationError as validation_error:
            sys.stderr.write('The project file does not comply with the needed JSON schema.\n')
            sys.stderr.write(validation_error)
            sys.exit(1)
        return project


def process_arguments():
    description = ('A program that implements the Critical Path Method '
                   'algorithm in order to schedule a set of project activities '
                   'at the minimum total cost with the optimum duration.')
    parser = argparse.ArgumentParser(description=description)
    arg_help = 'a file that describes the project in JSON format'
    parser.add_argument('project_file', help=arg_help)
    arg_help = 'a directory that the results will be placed in'
    parser.add_argument('-o', '--output-dir', help=arg_help)

    arguments = parser.parse_args()
    if not os.path.isfile(arguments.project_file):
        sys.stderr.write('The project_file is not an existing regular file.\n')
        sys.exit(1)
    if arguments.output_dir and not os.path.isdir(arguments.output_dir):
        sys.stderr.write('The output_dir is not an existing directory.\n')
        sys.exit(1)

    return arguments


def main():
    arguments = process_arguments()
    project = validate(arguments.project_file)
    output_dir = '' if not arguments.output_dir else arguments.output_dir + '/'

    cpmnet = cpm.CriticalPathMethod(project)
    cpmnet.run_cpm()

    pos = None
    images = []
    results_table = prettytable.PrettyTable(["Project Duration", "Critical Path", "Direct Cost", "Indirect Cost", "Total Cost"])
    for iteration, snapshot in enumerate(cpmnet.snapshots):
        graph = pickle.loads(snapshot)
        results = collect_results(graph, 'normal_cost')
        results_table.add_row([results['project_duration'], results['critical_path'], results['direct_cost'], results['indirect_cost'], results['total_cost']])

        if iteration == 0:
            pos = networkx.fruchterman_reingold_layout(graph)
        images.append(draw_network(graph, pos, output_dir, iteration))
    generate_html_report(output_dir, results_table, images)


if __name__ == '__main__':
    main()
