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

from setuptools import setup

setup(
    name='cpm',
    description='An implementation of the Critical Path Method algorithm',
    url='https://github.com/tzabal/cpm',
    author='Tzanetos Balitsaris',
    author_email='tzabal@freebsd.org',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD :: FreeBSD',
    ],
    packages=['cpm'],
    package_data = {
        'cpm': ['templates/*.mako']
    },
    install_requires=[
        'jsonschema',
        'mako',
        'matplotlib',
        'networkx',
        'PrettyTable'
    ],
    entry_points={
        'console_scripts': [
            'cpm = cpm.main:main',
        ]
    }
)
