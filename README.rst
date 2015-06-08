====================
Critical Path Method
====================

The Critical Path Method (CPM) is an algorithm used in project management for scheduling a set of project activities.

This program (cpm) is an implementation of the Critical Path Method algorithm that can schedule a set of project activities at the minimum total cost with the optimum duration.


Installation
============

Theoretically, cpm can be installed in any platform that Python exists. However, detailed instructions are given only for the GNU/Linux distribution CentOS. Other Linux distributions and BSD flavors may follow the same procedure with small changes and install successfully the program.


CentOS (and other RHEL-based distributions)
-------------------------------------------

First, install the system packages that are required by the *matplotlib* dependency::

  yum -y install gcc gcc-c++ freetype-devel libpng-devel python-devel

Add the EPEL repository and install git and pip::

  yum -y install epel-release
  yum -y install git python-pip

With pip, install virtualenv, and then create an isolated environment for the installation of cpm::

  pip install virtualenv
  virtualenv env-cpm
  source env-cpm/bin/activate

Finally, having installed the required packages and prepared the environment, clone this repository and run the *setup.py* to automatically install cpm and its dependencies::

  git clone https://github.com/tzabal/cpm
  cd cpm && python setup.py install


Execution
=========

cpm exposes a command-line interface. It accepts only two command-line arguments. The first one is required, as it is the file that describes the project (input), and the second one is optional, as it is the directory that the results (output) will be placed in (if not specified, the current directory is assumed).

Specifically::

  usage: cpm [-h] [-o OUTPUT_DIR] project_file

  A program that implements the Critical Path Method algorithm in order to
  schedule a set of project activities at the minimum total cost with the
  optimum duration.

  positional arguments:
    project_file          a file that describes the project in JSON format

  optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                          a directory that the results will be placed in

Example
-------

The *samples* directory contains a sample input project_file. It describes a project with two activities. Execute cpm simply by running::

  cpm ~/cpm/samples/two-activities-project.json

In the current directory, a set of *.png* images and an *HTML* file will be generated. The *HTML* file is a report with the results.

To specify where to output the results, use the *-o* argument::

  cpm ~/cpm/samples/two-activities-project.json -o ~/cpm-results/

Note that the *~/cpm-results* should exist prior executing the command.
