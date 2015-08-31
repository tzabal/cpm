====================
Critical Path Method
====================

The Critical Path Method (CPM) is an algorithm that is used in project management for scheduling a set of project activities.

This program (cpm) is an implementation of the Critical Path Method algorithm that can schedule a set of project activities at the minimum total cost with the optimum duration.


Architecture
============

The core component is the cpm.py module. This module implements the Critical Path Method algorithm and it is designed to act as a library.

There are two user interfaces that utilize the cpm.py module. The first is the cli.py module which implements a command-line interface using the standard argparse Python module, and the second is the web.py module which implements a web interface using the Flask web framework.

The input of the program is a file that describes a project in JSON format with a structure that is defined by a JSON Schema. The *samples* directory of this project contains a list of project files that can be used as input. The output of the program is a table (columns: project duration, critical path(s), direct cost, indirect cost, total cost) that lists every iteration of the CPM algorithm on the given project, and a set of images that depict the state of the network in every iteration.


Installation
============

Theoretically, cpm can be installed in any platform that Python exists. However, detailed instructions are given only for the Linux distribution CentOS. Other GNU/Linux distributions and BSD flavors may follow the same procedure with small deviations and install successfully the program.


CentOS
------

The procedure described here assumes a fresh installation of CentOS 7.1 (or an older release) with nothing but only the minimum installed packages in order to cover any possible installation scenario.

First, install the system packages that are required by the matplotlib dependency::

  yum -y install gcc gcc-c++ freetype-devel libpng-devel python-devel

Add the EPEL repository and install git and pip::

  yum -y install epel-release
  yum -y install git python-pip

With pip, install virtualenv, and then create an isolated environment for the installation of cpm::

  pip install virtualenv
  virtualenv venv-cpm
  source venv-cpm/bin/activate
  cd venv-cpm

Having installed the required packages and prepared the environment, clone this repository and run the setup.py to automatically install cpm and its dependencies::

  git clone https://github.com/tzabal/cpm
  cd cpm && python setup.py install


Execute using the command-line interface
========================================

The command-line interface is accessible via the *cpm* command. It accepts two command-line arguments. The first one is required, as it is the file that describes the project, and the second one is optional, as it is the directory that the generated images will be placed in (if not specified, the current directory is used).

Run CPM on the project file two-activities-project.json that describes a project with two activities, with the cpm command::

  cpm ~/venv-cpm/cpm/samples/two-activities-project.json

A nicely formatted ASCII table with the results is printed on the screen, along with a set of images generated in the current directory.


Execute using the web interface
===============================

In order to use the web interface, use the following command to start serving the application::

  python cpm/web.py

Open a web browser and visit the http://127.0.0.1:5000/ address.