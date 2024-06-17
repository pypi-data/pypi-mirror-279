from pyvisjs import Network

network = Network()

# You can skip adding nodes to the network and just add edges
# nodes will be created automatically based on the node ids passed as arguments
for i in range(2, 51):
    network.add_edge(1, i)

network.show("dandelion.html")