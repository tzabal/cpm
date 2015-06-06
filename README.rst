====================
Critical Path Method
====================

The Critical Path Method (CPM) is an algorithm used in project management for scheduling a set of project activities.

This program (cpm) is an implementation of the Critical Path Method algorithm that can schedule a set of project activities at the minimum total cost with the optimum duration.


Installation
============

Theoretically, cpm can be installed in any platform that Python exists. However, detailed instructions are given only for the GNU/Linux distribution CentOS. Other Linux distributions and BSD flavors may follow the same procedure with small changes.


CentOS (and probably other RHEL-based distributions)
----------------------------------------------------

Firstly, download the packages that are required by the matplotlib dependency:

``yum -y install gcc gcc-c++ freetype-devel libpng-devel python-devel``

Add the EPEL repository and install pip:

| ``yum -y install epel-release``
| ``yum -y install python-pip``

With pip, install virtualenv, and then create an isolated environment for the installation of cpm:

| ``pip install virtualenv``
| ``virtualenv env-cpm``
| ``source env-cpm/bin/activate``


Now, having installed the required packages and prepared the environment, clone this repository and run the setup.py to automatically install cpm and its dependencies:

| ``git clone https://github.com/tzabal/cpm``
| ``cd cpm``
| ``python setup.py install``


Execution
=========

From inside the cpm local repository, simply run the following:

``cpm samples/two-activities-project.json``

In the current directory, a set of .png images and an HTML file will be generated. The HTML file is a report with the results.
