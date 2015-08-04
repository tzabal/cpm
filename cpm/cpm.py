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

import pickle

import networkx


class CriticalPathMethod(object):
    """Implementation of the Critical Path Method algorithm.

    Attributes:
        graph: a DiGraph object of the networkx library. It represents the network
            that the CPM algorithm will run on.
        snapshots: a list of pickled representations of the graph. As the network
            is getting solved, every iteration of cpm on the graph is stored here.
        paths: a list of lists of tuples. A list of the available paths, starting
            from the first node of the network, and arriving at the last node of it,
            where each path is composed of activities in the form of tuples.
    """

    def __init__(self, project):
        self.graph = networkx.DiGraph(indirect_cost=project['info']['indirect_cost'])
        self.graph.add_edges_from(project['activities'])
        self.snapshots = []
        self.paths = self.__find_all_simple_paths(source=self.graph.nodes()[0], target=self.graph.nodes()[-1])

    def __find_all_simple_paths(self, source, target):
        """Finds all the paths between two nodes of a graph.

        Args:
            source (int): the starting node
            target (int): the finishing node

        Returns:
            A list of lists of tuples. A list of the available paths, where
            each path is composed of activities in the form of tuples.
            For example: [ [(1,2), (2,3), (3,4)], [(1,2), (2,4)] ]
        """
        paths = []
        for i, path in enumerate(networkx.all_simple_paths(self.graph, source, target)):
            paths.append([])
            for j, elem in enumerate(path):
                if j+1 <= len(path)-1:
                    paths[i].append((path[j], path[j+1]))
        return paths

    def _calculate_cost_slope(self):
        """Calculates the cost slope of every activity in the network."""
        for node1, node2 in self.graph.edges():
            activity = self.graph.edge[node1][node2]
            try:
                activity['cost_slope'] = ((activity['crash_cost'] - activity['normal_cost']) /
                                          (activity['normal_duration'] - activity['crash_duration']))
            except ZeroDivisionError:
                # For imaginary activities
                activity['cost_slope'] = None

    def _solve_network(self, kw_duration='normal_duration'):
        self.__calculate_earliest_event_time(kw_duration)
        self.__calculate_latest_event_time(kw_duration)
        self.__calculate_total_float(kw_duration)

    def __calculate_earliest_event_time(self, kw_duration):
        for node in self.graph.nodes():
            max_eet = 0
            if self.graph.predecessors(node):
                for predecessor in self.graph.predecessors(node):
                    eet = self.graph.node[predecessor]['eet'] + self.graph.edge[predecessor][node][kw_duration]
                    if max_eet < eet:
                        max_eet = eet
            self.graph.node[node]['eet'] = max_eet

    def __calculate_latest_event_time(self, kw_duration):
        for node in reversed(self.graph.nodes()):
            if not self.graph.successors(node):
                self.graph.node[node]['let'] = self.graph.node[node]['eet']
            else:
                min_let = self.graph.node[self.graph.nodes()[-1]]['eet']
                for successor in self.graph.successors(node):
                    let = self.graph.node[successor]['let'] - self.graph.edge[node][successor][kw_duration]
                    if min_let > let:
                        min_let = let
                self.graph.node[node]['let'] = min_let

    def __calculate_total_float(self, kw_duration):
        for node1, node2 in self.graph.edges():
            activity = self.graph.edge[node1][node2]
            activity['total_float'] = (self.graph.node[node2]['let'] - self.graph.node[node1]['eet'] -
                                       activity[kw_duration])

    def _get_network_duration(self):
        return self.graph.node[self.graph.nodes()[-1]]['let']

    def _reduce_network_duration(self):
        critical_activities = self.__get_critical_activities()
        critical_paths = self.__get_critical_paths(critical_activities)
        for critical_path in critical_paths:
            critical_path = self.__remove_crashed_activities(critical_path)
            if len(critical_path) > 0:
                min_critical_activity = critical_path[0]
                min_cost_slope = self.graph.edge[min_critical_activity[0]][min_critical_activity[1]]['cost_slope']
                for critical_activity in critical_path[1:]:
                    if self.graph.edge[critical_activity[0]][critical_activity[1]]['cost_slope'] < min_cost_slope:
                        min_critical_activity = critical_activity
                        min_cost_slope = self.graph.edge[critical_activity[0]][critical_activity[1]]['cost_slope']
                self.graph.edge[min_critical_activity[0]][min_critical_activity[1]]['normal_duration'] -= 1
                self.graph.edge[min_critical_activity[0]][min_critical_activity[1]]['normal_cost'] += min_cost_slope

    def __get_critical_activities(self):
        """Finds all the critical activities of the network.

        Returns:
            A list of tuples. Every tuple represents a critical activity.
            For example: [ (1, 2), (2, 3), (2, 4), (3, 4) ]
        """
        critical_activities = []
        for node1, node2 in self.graph.edges():
            if self.graph.edge[node1][node2]['total_float'] == 0:
                critical_activities.append((node1, node2))
        return critical_activities

    def __get_critical_paths(self, critical_activities):
        """Finds all the critical paths of the network.

        A network may have more than one critical paths. Based on the critical activities,
        it constructs the critical path(s) of the network.

        Args:
            critical_activities: a list of tuples, where a tuple represents a critical activity.

        Returns:
            A list of list of tuples.
        """
        critical_paths = []
        for path in self.paths:
            if set(path) <= set(critical_activities):
                critical_paths.append(path)
        return critical_paths

    def __remove_crashed_activities(self, critical_path):
        return filter(lambda critical_activity:
                      self.graph.edge[critical_activity[0]][critical_activity[1]]['normal_duration'] >
                      self.graph.edge[critical_activity[0]][critical_activity[1]]['crash_duration'], critical_path)

    def __print_graph(self):
        # A method that helps with debugging the algorithm.
        # There is no actual use in the execution of cpm.
        print 'Nodes:'
        for node in self.graph.nodes():
            print str(node) + ': ' + str(self.graph.node[node])
        print 'Edges:'
        for edge in self.graph.edges():
            print str(edge) + ': ' + str(self.graph.edge[edge[0]][edge[1]])
        print 'Critical Activities:'
        critical_activities = []
        for node1, node2 in self.graph.edges():
            if self.graph.edge[node1][node2]['total_float'] == 0:
                critical_activities.append((node1, node2))
        print critical_activities

    def run_cpm(self):
        """The high-level actions of the CPM algorithm."""
        self._calculate_cost_slope()

        self._solve_network(kw_duration='crash_duration')
        crash_network_duration = self._get_network_duration()

        while True:
            self._solve_network()
            network_duration = self._get_network_duration()

            self.snapshots.append(pickle.dumps(self.graph))
            self._reduce_network_duration()

            if not network_duration > crash_network_duration:
                break
