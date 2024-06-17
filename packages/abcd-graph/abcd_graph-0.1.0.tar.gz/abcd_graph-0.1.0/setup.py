# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['abcd_graph', 'abcd_graph.api', 'abcd_graph.core']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.26.4,<2.0.0',
 'pydantic>=2.6.4,<3.0.0',
 'typing-extensions>=4.10.0,<5.0.0']

extras_require = \
{'all': ['pre-commit>=3.7.0,<4.0.0',
         'pytest>=8.1.1,<9.0.0',
         'pytest-cov>=5.0.0,<6.0.0',
         'networkx>=3.3,<4.0',
         'igraph',
         'matplotlib>=3.9.0,<4.0.0'],
 'dev': ['pre-commit>=3.7.0,<4.0.0',
         'pytest>=8.1.1,<9.0.0',
         'pytest-cov>=5.0.0,<6.0.0'],
 'igraph': ['igraph'],
 'matplotlib': ['matplotlib>=3.9.0,<4.0.0'],
 'networkx': ['networkx>=3.3,<4.0']}

setup_kwargs = {
    'name': 'abcd-graph',
    'version': '0.1.0',
    'description': '',
    'long_description': '# abcd-graph\nA python library for generating ABCD graphs.\n\n## Installation\n```bash\npip install abcd-graph\n```\n\n## Usage\n```python\nfrom abcd_graph import Graph, ABCDParams\n\nparams = ABCDParams()\ngraph = Graph(params).build()\n```\n\n### Parameters\n\n- `params`: An instance of `ABCDParams` class.\n- `n`: Number of nodes in the graph.\n- `logger` A boolean to enable or disable logging to the console. Default is `False` - no logs are shown.\n\n\n### Exporting\n\nThe graph object can be exported to `networkx.Graph` object using the `to_networkx` method.\n\n```python\nfrom abcd_graph import Graph, ABCDParams\n\nparams = ABCDParams()\ngraph = Graph(params).build().to_networkx()\n```\n\nThis requires the `networkx` library to be installed.\n```bash\npip install abcd-graph[networkx]\n```\n\nAnother option is an `igraph.Graph` object.\n\n```python\nfrom abcd_graph import Graph, ABCDParams\n\nparams = ABCDParams()\ngraph = Graph(params).build().to_igraph()\n```\n\nThis requires the `igraph` library to be installed.\n```bash\npip install abcd-graph[igraph]\n```\n\nFinally, the graph can be exported to a `numpy.ndarray` object that represents the `adjacency matrix`.\n\n```python\nfrom abcd_graph import Graph, ABCDParams\n\nparams = ABCDParams()\ngraph = Graph(params).build().adj_matrix\n```\n\n> [!IMPORTANT]\n> If the `build()` method is not run before calling any of the export methods, a `RuntimeError` will be raised.\n\n> [!NOTE]\n> The `numpy` array is of type `numpy.bool_`. If the graph was not properly generated (loops or multi-edges),\n> a `MalformedGraphError` will be raised.\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
