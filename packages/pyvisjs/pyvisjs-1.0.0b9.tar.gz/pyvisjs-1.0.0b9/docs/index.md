---
template: index.html
title: Python Wrapper for vis.js
---

(under construction)  
### Installation
As a package user you can install it from pip

``` sh
# Installation for a package user
# this script installs package from pip

py -m venv .venv
.venv\\Scripts\\activate
py -m pip install pyvisjs
```

Or if you want to contribute you can clone the repo and install the package in the editable mode

``` sh
# Installation for a package developer  
# this script installs package from the local files in the editable mode

git clone https://gitlab.com/22kittens/pyvisjs.git
cd pyvisjs
git checkout dev
py -m venv .venv
.venv\\Scripts\\activate
py -m pip install -r requirements.txt
py -m pip install -e .
```

### Configuration
Next you need to provide <a href="https://visjs.github.io/vis-network/docs/network/#modules" target="_blank">Vis.js' specific objects</a> like nodes, edges and (optional) options.  
For example you can create a simple network of two nodes using the code below (link to the example)

``` py
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

If you don't want to add any extra node attributes except the mandatory node id, the pyvisjs package allows you to skip adding the nodes and just add edges using desired ids. Corresponding nodes in this case will be added automatically (<a href="examples/basic-example/" target="blank_">see example</a>)

``` py
from pyvisjs import Network

network = Network()

# You can skip adding nodes to the network and just add edges
# nodes will be created automatically based on the node ids passed as arguments
for i in range(2, 51):
    network.add_edge(1, i)

network.show("dandelion.html")
```

Python wrappers for Vis.js' Node and Edge classes implement only some extent of all available attributes - the major ones such as label, color, shape and size for nodes and start and end ids for edges. If you want to use any other attributes from Vis.js set of APIs you can just pass them as **kwargs.  
If for example you've found in the Vis.js' <a href="https://visjs.github.io/vis-network/docs/network/nodes.html#" target="_blank">nodes module documentation</a> that Node can have `fixed` attribute and you want to apply this property to one of your nodes.  
To do so you just need to pass `fixed=True` in the end of the parameters list of the [`add_node`](nodes.md) method (<a href="examples/fixed-red-node/" target="blank_">see example</a>) 


``` py
from pyvisjs import Network

network = Network()

for i in range(2, 11):
    network.add_edge(1, i)

# `add_node` function doesn't implement `fixed` parameter but it can be passwed
# to the vis.js Network's API through **kwargs

# adding 11th fixed red node and linking it with 1st node
network.add_node(id=11, label="fixed", color="red", fixed=True)
network.add_edge(1, 11)

network.show()
```

Or, as a more complex example of how not implemented attributes can be passed to the Vis.js' API, lets assume you want to node's label background color set to `lime` which requires to pass an object instead of just a single value. So from the Vis.js' <a href="https://visjs.github.io/vis-network/docs/network/nodes.html#" target="_blank">nodes module documentation</a> you've learned you need to specify the `font` object with the `background` attribute set to the `color` value you need.    
To do so you need to pass `font={"background": "lime"}` in the end of the parameters list of the [`add_node`](nodes.md) method (see example) 

``` py
from pyvisjs import Network

# Create a Network instance
network = Network()

# You can skip adding nodes to the network and just add edges
# nodes will be created automatically based on the node ids passed as arguments
for i in range(2, 11):
    network.add_edge(1, i)

# adding 11th fixed red node and link it with 1st node
network.add_node(11, "fixed", "red", font={"background": "lime"})
network.add_edge(1, 11)

# Display the network
network.show()
```

using attributes through **kwargs + examples  
pyvisjs-specific options + filtering  

### Usage examples
standalone html  
flask


