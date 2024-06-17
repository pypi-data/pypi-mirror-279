---
template: filtering-example.html
---
``` py
from pyvisjs import Network, Options

options = Options("500px", "100%")
options.edges.set(arrows="to")
options.set_interaction(
    dragView=False,
    zoomView=False,
)
options.pyvisjs \
    .set(title="pyvisjs filtering example") \
    .set_filtering()

net = Network.from_dir(".", options, only_first_level=True)
net.show()
```