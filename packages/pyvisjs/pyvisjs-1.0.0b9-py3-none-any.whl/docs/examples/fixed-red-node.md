---
template: fixed-red-node.html
---

``` py
from pyvisjs import Network

network = Network()

# You can skip adding nodes to the network and just add edges
# nodes will be created automatically based on the node ids passed as arguments
for i in range(2, 11):
    network.add_edge(1, i)

# `add_node` function doesn't implement `fixed` parameter but it can be passwed
# to the vis.js Network's API through **kwargs

# adding 11th fixed red node and linking it with 1st node
network.add_node(id=11, label="fixed", color="red", fixed=True)
network.add_edge(1, 11)

network.show()
```
