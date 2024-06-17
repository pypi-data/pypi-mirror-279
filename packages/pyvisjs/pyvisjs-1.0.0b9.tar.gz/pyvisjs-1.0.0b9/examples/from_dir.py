from pyvisjs import Network, Options

options = Options("500px", "100%")
options.edges.set(arrows="to")
options.pyvisjs \
    .set(title="pyvisjs filtering example") \
    .set_filtering(
        enable_highlighting=True,
        node_filtering=["file_type", "file_ext", "label"],
        dropdown_auto_close=True,
    )

net = Network.from_dir(".", options)
net.show()