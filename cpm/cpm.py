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

    def __init__(self, project):
        self.graph = networkx.DiGraph(indirect_cost=project['info']['indirect_cost'])
        self.graph.add_edges_from(project['activities'])
        self.snapshots = []

    def _calculate_cost_slope(self):
        for node1, node2 in self.graph.edges():
            activity = self.graph.edge[node1][node2]
            try:
                activity['cost_slope'] = (activity['crash_cost'] - activity['normal_cost']) / (activity['normal_duration'] - activity['crash_duration'])
            except ZeroDivisionError:
                # For imaginary activities
                activity['cost_slope'] = None

    def _is_network_crashable(self):
        for node1, node2 in self.graph.edges():
            activity = self.graph.edge[node1][node2]
            if activity['normal_duration'] > activity['crash_duration']:
                return True
        return

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
            activity['total_float'] = self.graph.node[node2]['let'] - self.graph.node[node1]['eet'] - activity[kw_duration]

    def _reduce_network_duration(self):
        critical_activities = self.__get_critical_activities()
        critical_activities = self.__remove_crashed_activities(critical_activities)
        if len(critical_activities) > 0:
            min_critical_activity = critical_activities[0]
            min_cost_slope = min_critical_activity['cost_slope']
            for critical_activity in critical_activities[1:]:
                if critical_activity['cost_slope'] < min_cost_slope:
                    min_critical_activity = critical_activity
                    min_cost_slope = critical_activity['cost_slope']
            min_critical_activity['normal_duration'] -= 1
            min_critical_activity['normal_cost'] += min_cost_slope

    def __get_critical_activities(self):
        # Returns a list of dictionaries
        critical_activities = []
        for node1, node2 in self.graph.edges():
            if self.graph.edge[node1][node2]['total_float'] == 0:
                critical_activities.append(self.graph.edge[node1][node2])
        return critical_activities

    def __remove_crashed_activities(self, critical_activities):
        return filter(lambda critical_activity: critical_activity['normal_duration'] > critical_activity['crash_duration'], critical_activities)

    def run_cpm(self):
        self._calculate_cost_slope()
        while self._is_network_crashable():
            self._solve_network()
            self.snapshots.append(pickle.dumps(self.graph))
            self._reduce_network_duration()
        self._solve_network()
        self.snapshots.append(pickle.dumps(self.graph))
