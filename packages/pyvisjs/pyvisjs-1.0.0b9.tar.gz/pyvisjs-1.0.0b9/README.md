[![pipeline status](https://gitlab.com/22kittens/pyvisjs/badges/main/pipeline.svg)](https://gitlab.com/22kittens/pyvisjs/-/commits/main)
[![PyPI - Version](https://img.shields.io/pypi/v/pyvisjs)](https://pypi.org/project/pyvisjs)
[![Documentation](https://img.shields.io/badge/ref-Documentation-blue)](https://22kittens.gitlab.io/pyvisjs/)
[![coverage](https://gitlab.com/22kittens/pyvisjs/badges/dev/coverage.svg?job=pytest_job)](https://gitlab.com/22kittens/pyvisjs/-/commits/main)


# ![logo](https://gitlab.com/uploads/-/system/project/avatar/56819743/favicon-32x32.png) - pyvisjs
Python wrapper for vis.js Network

> :warning: **Beta version disclaimer** Please note that this package is in a **beta** version and backwards-incompatible changes might be introduced in future releases.


pyvisjs is a Python package designed to provide seamless interaction with [vis.js](https://visjs.org) network visualizations, allowing users to manipulate and visualize network data using Python.

## Usage workflow

1. Create a network using python
2. Apply standard vis.js options such as colors, shapes or physics
3. Apply pyvisjs specific options such as node/edge filtering or highlighting
4. Show or generate html file
5. Enjoy network interactions in your browser

## Installation

You can install PyVisjs via pip:

```bash
pip install pyvisjs
```

## Usage example

```python
from pyvisjs import Network

# Create a Network instance
net = Network()

# Add nodes and edges
net.add_node(1)
net.add_node(2)
net.add_edge(1, 2)

# Display the network
net.show("example.html")
```

For more examples and detailed usage, please refer to the [documentation](https://22kittens.gitlab.io/pyvisjs).

## Contributing

Contributions are welcome! If you have suggestions, feature requests, or find any bugs, please open an issue or submit a pull request. Make sure to follow the [contribution guidelines](https://22kittens.gitlab.io/pyvisjs/CONTRIBUTING).

## Acknowledgments

This project is inspired by the [pyvis](https://github.com/WestHealth/pyvis) Python package and the [visNetwork](https://github.com/datastorm-open/visNetwork) R-language package.

## License

This project is licensed under the [MIT License](https://22kittens.gitlab.io/pyvisjs/LICENSE).