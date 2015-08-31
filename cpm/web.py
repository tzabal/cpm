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

import time

from flask import Flask
from flask import Markup
from flask import render_template
from flask import request
import prettytable

import cpm


app = Flask(__name__)


def _get_html_results_table(results):
    results_table = prettytable.PrettyTable([
        "Project Duration", "Critical Path(s)", "Direct Cost", "Indirect Cost", "Total Cost"
    ])
    for result in results:
        results_table.add_row([
            result['project_duration'], result['critical_paths'],
            result['direct_cost'], result['indirect_cost'], result['total_cost']
        ])
    return results_table.get_html_string()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        project_file = request.files['project_file']
        if project_file:
            try:
                project = cpm.validate(project_file)
            except cpm.ProjectValidationException as exc:
                return render_template('index.html', error=exc)
            cpmnet = cpm.CriticalPathMethod(project)
            cpmnet.run_cpm()
            results, images, optimum_solution = cpmnet.get_results('static/results/')
            return render_template('results.html',
                                   results_table=Markup(_get_html_results_table(results)),
                                   images=zip(images, range(0, len(images))),
                                   force_reload=str(time.time()),
                                   optimum_total_cost=optimum_solution[0],
                                   optimum_project_duration=optimum_solution[1])
        else:
            return render_template('index.html', error='No project file has been uploaded.')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
