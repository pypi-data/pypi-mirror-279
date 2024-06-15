# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepbench',
 'deepbench.astro_object',
 'deepbench.collection',
 'deepbench.image',
 'deepbench.physics_object',
 'deepbench.shapes']

package_data = \
{'': ['*'], 'deepbench': ['settings/*']}

install_requires = \
['astropy>=5.2.2,<6.0.0',
 'autograd>=1.5,<2.0',
 'h5py>=3.9.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.25.0,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'scikit-image>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'deepbench',
    'version': '0.2.3',
    'description': 'Physics Benchmark Dataset Generator',
    'long_description': '![GitHub Workflow Status](https://github.com/deepskies/DeepBench/actions/workflows/test-bench.yml/badge.svg?label=test)\n[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n [![PyPI version](https://badge.fury.io/py/deepbench.svg)](https://badge.fury.io/py/deepbench)\n[![Documentation Status](https://readthedocs.org/projects/deepbench/badge/?version=latest)](https://deepbench.readthedocs.io/en/latest/?badge=latest)\n\n### What is it?\nSimulation library for very simple simulations to *benchmark* machine learning algorithms.\n\n### Why do we need it? Why is it useful?\n1. There are very universally recognized scientifically meaningful benchmark data sets, or methods with which to generate them.\n2. A very simple data set will have objects, patterns, and signals that are intuitively quanitifiable and will be fast to generate.\n3. A very simple data set will be a great testing ground for new networks and for newcomers to practice with the technology.\n\n## Documentation\n\n#### [ReadTheDocs](https://deepbench.readthedocs.io/en/latest/)\n\n#### To build from source\n```\npip install sphinx\ncd docs\nmake html\n```\n\nThe folder `docs/_build/html` will be populated with the documentation. Navigate to `file:///<Path To DeepBench>/docs/_build/html/index.html` in any web browser to view.\n\n## Requirements\n* python = ">=3.8,<3.11,"\n* numpy = "^1.24.3"\n* matplotlib = "^3.7.1"\n* scikit-image = "^0.20.0"\n* astropy = "^5.2.2"\n* autograd = "^1.5"\n* pyyaml = "^6.0"\n\n\n\n## Install\n\n### From PyPi\n```\npip install deepbench\n```\n\n### From Source\n\n```\ngit clone https://github.com/deepskies/DeepBench.git\npip install poetry\npoetry shell\npoetry install\npoetry run pytest --cov\n```\n\n## General Features\n1. very fast to generate\n2. Mimics in a very basic / toy way what is in astro images\n3. Be fully controllable parametrically\n\n![DeepBench Logo](docs/repository_support/DeepBench.png)\n\n### Included Simulations\n\n1. Astronomy Objects - simple astronomical object simulation\n- Galaxy, Spiral Galaxy, Star\n\n2. Shapes - simple 2D geometric shapes\n- Rectangle, Regular Polygon, Arc, Line, Ellipse\n\n3. Physics Objects - simple physics simulations\n- Neutonian Pendulum, Hamiltonian Pendulum\n\n## Example\n\n### Standalone\n* Produce 3 instance of a pendulum over 10 different times with some level of noise.\n```\nimport numpy as np\nfrom deepbench.collection import Collection\n\nconfiguration = {\n\t"object_type": "physics",\n\t"object_name": "Pendulum",\n\t"total_runs": 3,\n\t"parameter_noise": 0.2,\n\t"image_parameters": {\n\t\t"pendulum_arm_length": 2,\n\t\t"starting_angle_radians": 0.25,\n\t\t"acceleration_due_to_gravity": 9.8,\n\t\t"noise_std_percent":{\n\t\t\t"acceleration_due_to_gravity": 0\n\t},\n\t"object_parameters":{\n\t\t"time": np.linspace(0, 1, 10)\n\t}\n}\n\nphy_objects = Collection(configuration)()\n\nobjects = phy_objects.objects\nparameters = phy_objects.object_parameters\n```\n\n* Produce a noisy shape image with a rectangle and an arc\n\n```\nimport numpy as np\nfrom deepbench.collection import Collection\n\nconfiguration = {\n\t"object_type": "shape",\n\t"object_name": "ShapeImage",\n\n\t"total_runs": 1,\n\t"image_parameters": {\n\t\t"image_shape": (28, 28),\n\t\t"object_noise_level": 0.6\n\t},\n\n\t"object_parameters": {\n\t\t[\n\t\t"rectangle": {\n\t\t\t"object": {\n\t\t\t\t"width": np.random.default_rng().integers(2, 28),\n\t\t\t\t"height": np.random.default_rng().integers(2, 28),\n\t\t\t\t"fill": True\n\t\t\t},\n\t\t\t"instance": {}\n\t\t},\n\t\t"arc":{\n\t\t\t"object": {\n\t\t\t\t"radius": np.random.default_rng().integers(2, 28),\n\t\t\t\t"theta1":np.random.default_rng().integers(0, 20),\n\t\t\t\t"theta2":np.random.default_rng().integers(21, 180)\n\t\t\t},\n\t\t\t"instance":{}\n\t\t}\n\n\t\t]\n\t}\n}\n\nshape_image = Collection(configuration)()\n\nobjects = shape_image.objects\nparameters = shape_image.object_parameters\n```\n\n\n### Fine-Grained Control\n* Make a whole bunch of stars\n```\nfrom deepbench.astro_object import StarObject\nimport numpy as np\n\nstar = StarObject(\n        image_dimensions = (28,28),\n        noise = 0.3,\n        radius= 0.8,\n        amplitude = 1.0\n    )\n\ngenerated_stars = []\nx_position, y_position = np.random.default_rng().uniform(low=1, high=27, size=(2, 50))\nfor x_pos, y_pos in zip(x_position, y_position):\n\tgenerated-stars.append(star.create_object(x_pos, y_pos))\n```\n\n\n## Contributions\n### Original Team\n1. Craig Brechmos\n2. Renee Hlozek\n3. Brian Nord\n\n### Refactor and Deployment\n1. Ashia Livaudais\n2. M. Voetberg\n\n### Pendulum Team\n1. Becky Nevin\n2. Omari Paul\n\n## Contributing\n[Please view the deepskies contribution guidelines before submitting a code addition](https://github.com/deepskies/.github/blob/main/CONTRIBUTING.md)\n\n## Acknowledgement\n\n\nThis work was produced by Fermi Research Alliance, LLC under Contract No. DE-AC02-07CH11359 with the U.S. Department of Energy. Publisher acknowledges the U.S. Government license to provide public access under the DOE Public Access Plan DOE Public Access Plan.\nNeither the United States nor the United States Department of Energy, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any data, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights.\n\nWe acknowledge the Deep Skies Lab as a community of multi-domain experts and collaborators who’ve facilitated an environment of open discussion, idea-generation, and collaboration. This community was important for the development of this project.\n\n',
    'author': 'M. Voetberg',
    'author_email': 'maggiev@fnal.gov',
    'maintainer': 'M. Voetberg',
    'maintainer_email': 'maggiev@fnal.gov',
    'url': 'https://github.com/deepskies/DeepBench',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
