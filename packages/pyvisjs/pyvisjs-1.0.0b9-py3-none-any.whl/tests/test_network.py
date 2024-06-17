import os
from unittest.mock import patch, ANY
from pyvisjs import Network, Node, Edge, Options

# Network
# ├── __init__ (name, nodes, edges, options)
# ├── _initialize_data
# ├── get_options
# ├── set_options
# ├── get_nodes
# ├── get_edges
# ├── add_node
# ├── add_edge
# ├── show
# ├── render
# ├── from_dir
# └── to_dict

def test_network_init_default_params():
    # init
    DEFAULT_DICT = {
        "nodes": [],
        "edges": [],
        "options": {}
    }
    # mock


    # call
    n = Network("Network2")
    
    # assert
    assert n.name == "Network2"
    assert n.env is not None
    assert n._data == DEFAULT_DICT # result of calling _initialize_data
    assert n.attr_filter_func # from the base class
    assert n.to_dict() == DEFAULT_DICT

def test_network_init_with_data():
    # init
    TITLE = "My network"
    PHYSICS_ENABLED = False
    NETWORK_DICT = {
        "nodes": [
            { "id": "1", "label": "node 1", "shape": "dot" },
            { "id": "2", "label": "node 2", "shape": "dot" },
            { "id": "3", "label": "node 3", "shape": "dot" },
        ],
        "edges": [
            { "from": "1", "to": "2" },
            { "from": "2", "to": "3" },
            { "from": "3", "to": "4" }
        ],
        "options": {
            "physics": {
                "enabled": PHYSICS_ENABLED
            }
        }
    }
    # mock


    # call
    nd1 = Node(1, "node 1")
    nd2 = Node(2, "node 2")
    nd3 = Node(3, "node 3")

    eg1 = Edge(1, 2)
    eg2 = Edge(2, 3)
    eg3 = Edge(3, 4)

    opt = Options()
    opt.pyvisjs.set(title=TITLE)
    opt.physics.set(enabled=PHYSICS_ENABLED)

    n = Network("Network2", [nd1, nd2, nd3], [eg1, eg2, eg3], opt)
    
    # assert
    assert n.name == "Network2"
    assert n.env is not None
    assert n.to_dict() == NETWORK_DICT

def test_network_initialize_data():
    # init
    DEFAULT_DICT = {
        "nodes": [],
        "edges": [],
        "options": {}
    }

    NODES = [Node(1), Node(2)]
    EDGES = [Edge(1, 2)]
    OPT = Options("100%", "100%")

    INITIALIZED_DICT = {
        "nodes": NODES,
        "edges": EDGES,
        "options": OPT
    }
    # mock

    # call
    n = Network("Network2")
    n_data_before_init = n._data
    n._initialize_data(NODES, EDGES, OPT) 

    # assert
    assert n_data_before_init == DEFAULT_DICT
    assert n._data == INITIALIZED_DICT

def test_network_get_options_default():
    # init

    # mock

    # call
    n = Network("Network2")
     
    # assert
    assert n.options == None

def test_network_get_options():
    # init
    TITLE = "Network title"
    PHYSICS_ENABLED = True
    # mock

    # call
    opt = Options()
    opt.pyvisjs.set(title=TITLE)
    opt.physics.set(enabled=PHYSICS_ENABLED)
    n = Network("Network2", options=opt)
     
    # assert
    assert n.options.pyvisjs.title == TITLE
    assert n.options.physics.enabled == PHYSICS_ENABLED

def test_network_set_options():
    # init
    ZOOM_VIEW = True
    DRAG_NODES = False
    # mock

    # call
    n = Network("Network2")
    n_default_options = n.options
    n.options = Options().set_interaction(dragNodes=DRAG_NODES, zoomView=ZOOM_VIEW)

    # assert
    assert n_default_options == None
    assert n.options.interaction["dragNodes"] == DRAG_NODES
    assert n.options.interaction["zoomView"] == ZOOM_VIEW

def test_network_get_nodes_and_edges():
    # init

    # mock

    # call
    nd1 = Node(1, "node 1")
    nd2 = Node(2, "node 2")
    nd3 = Node(3, "node 3")

    eg1 = Edge(1, 2)
    eg2 = Edge(2, 3)
    eg3 = Edge(3, 4)

    n = Network("Network2", [nd1, nd2], [eg1])
    n.nodes.append(nd3)
    n.edges.append(eg2)
    n.edges.append(eg3)

    # assert
    assert n.nodes == [nd1, nd2, nd3]
    assert n.edges == [eg1, eg2, eg3]

def test_network_add_node():
    # init

    # mock

    # call
    n = Network("Network1")
    n.add_node(1)
    n.add_node(2, "name2")
    n.add_node(2) # duplicate node
    n.add_node(3, "hello", "red", "circle", None, category="high")
    
    # assert
    assert len(n.nodes) == 3
    assert n.nodes[0].id == "1"
    assert n.nodes[0].label == "1"
    assert n.nodes[1].id == "2"
    assert n.nodes[1].label == "name2"
    assert n.nodes[2].category == "high"

def test_network_add_node_return_value():
    # init

    # mock

    # call
    n = Network("Network1")
    node1_index = n.add_node(1)
    node2_index = n.add_node(2, "name2")
    node2_index_dup = n.add_node(2) # duplicate node
    node3_index = n.add_node(3, "hello", "red", "circle", None, category="high")
    
    # assert
    assert node1_index == 0
    assert node2_index == 1
    assert node2_index_dup == 1 # dup has been found
    assert node3_index == 2

def test_network_add_edge():
    # init
    n = Network("Network1")
    n.add_node(1)
    n.add_node(2, "name2")

    # mock

    # call
    n.add_edge(1, 2) # both nodes exist
    n.add_edge(2, 3, country="LV") # one node missing
    n.add_edge(2, 3) # duplicate edge
    
    # assert
    assert n.nodes[0].id == "1"
    assert n.nodes[1].id == "2"
    assert n.nodes[2].id == "3"

    assert len(n.edges) == 2
    assert n.edges[0].start == "1"
    assert n.edges[0].end == "2"
    assert n.edges[1].start == "2"
    assert n.edges[1].end == "3"
    assert n.edges[1].country == "LV"

def test_network_add_edge_return_value():
    # init
    n = Network("Network1")
    n.add_node(1)
    n.add_node(2, "name2")

    # mock

    # call
    edge1_index = n.add_edge(1, 2) # both nodes exist
    edge2_index = n.add_edge(2, 3, country="LV") # one node missing
    edge2_index_dup = n.add_edge(2, 3) # duplicate edge
    
    # assert
    assert edge1_index == 0
    assert edge2_index == 1
    assert edge2_index_dup == 1

def test_network_to_dict():
    # init
    TITLE = "Title1"
    PHYSICS_ENABLED = True

    NETWORK_DICT = {
        "nodes": [
            { "id": "1", "label": "1", "shape": "dot" },
            { "id": "2", "label": "name2", "shape": "dot" },
            { "id": "3", "label": "3", "shape": "dot" },
        ],
        "edges": [
            { "from": "1", "to": "2" },
            { "from": "2", "to": "3" }
        ],
        "options": {
            "physics": {
                "enabled": PHYSICS_ENABLED
            }
        }
    }

    # mock

    # call
    opt = Options()
    opt.pyvisjs.set(title=TITLE) # pyvisjs key is not going to options.to_dict()
    opt.physics.set(enabled=PHYSICS_ENABLED) 

    n = Network("Network1", options=opt)
    n.add_node(1)
    n.add_node(2, "name2")
    n.add_edge(1, 2) # both nodes exist
    n.add_edge(2, 3) # one node missing
    n.add_edge(2, 3) # duplicate edge
    
    # assert
    assert n.to_dict() == NETWORK_DICT

@patch('pyvisjs.network.Environment')
def test_network_render_default_params(mock_Environment):
    # init
    DATA = { "nodes": [], "edges": [], "options": {} }
    PYVISJS = {}
    JINJA = {}
    TEMPLATE_FILENAME = "basic-template.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    network = Network("Test Network")
    html_output = network.render()

    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_render_all_pyvisjs_options_no_data(mock_Environment):
    # init
    DATA={"nodes": [], "edges": [], "options": {}}
    TITLE="network title"
    TEMPLATE_FILENAME="container-template.html"
    ENABLE_HIGHLIGHTING=True
    DROPDOWN_AUTO_CLOSE=False
    ZOOM_FACTOR=2
    DURATION_MS=3050
    TABLE_POSITION="bottom"
    PYVISJS={
        "enable_highlighting": ENABLE_HIGHLIGHTING,
        "dropdown_auto_close": DROPDOWN_AUTO_CLOSE,
    }
    JINJA={
        "tables": {
            'bottom': {
                'position': TABLE_POSITION, 
                'columns': ["id", "name"], 
                'data': [{"id": 1, "name": "name1"}]
            }
        },
        "startAnimation": {
            "zoom_factor": ZOOM_FACTOR,
            "duration_ms": DURATION_MS,
        },
        "filtering": {
            "edges_lookup": {},
            "nodes_lookup": {},
        },
        "sankey": {
            "data": [{ "node": {}, "link": {} }]
        },
        "title": TITLE,
    }
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    options = Options()
    options.pyvisjs \
        .set(title=TITLE) \
        .set_sankey(enabled=True) \
        .set_filtering(
            enable_highlighting=ENABLE_HIGHLIGHTING,
            dropdown_auto_close=DROPDOWN_AUTO_CLOSE
        ) \
        .set_startAnimation(
            zoom_factor=ZOOM_FACTOR,
            duration_ms=DURATION_MS,
        ) \
        .set_dataTable(
            position=TABLE_POSITION,
            columns=["id", "name"],
            data=[{"id": 1, "name": "name1"}]
        )

    network = Network("Test Network", options=options)
    network.render() # <--------------------

    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_render_pyvisjs_options_only_defaults(mock_Environment):
    # init
    DATA={ "nodes": [], "edges": [], "options": {} }
    TITLE="network title"
    TEMPLATE_FILENAME="basic-template.html"
    PYVISJS={}
    JINJA={
        "title": TITLE,
    }
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    options = Options()
    options.pyvisjs.set(title=TITLE)
    network = Network("Test Network", options=options)
    network.render() # <--------------------

    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_render_edge_filtering_unique_values(mock_Environment):
    # init
    DATA={
        'nodes': [
            {'id': '1', 'label': '1', 'shape': 'dot'}, 
            {'id': '2', 'label': '2', 'shape': 'dot'}, 
            {'id': '3', 'label': '3', 'shape': 'dot'}], 
        'edges': [
            {'to': '2', 'field1': 'AM', 'from': '1'}, 
            {'to': '3', 'field1': 'AM', 'from': '1'}, 
            {'to': '3', 'field1': 'JL', 'from': '2'}], 
        'options': {}
    }
    TEMPLATE_FILENAME="container-template.html"
    ENABLE_HIGHLIGHTING=True
    DROPDOWN_AUTOCLOSE=True
    EDGE_FILTERING=["field1", "field2"]
    NODE_FILTERING=["label", "shape"]
    PYVISJS={
        "enable_highlighting": ENABLE_HIGHLIGHTING,
        "dropdown_auto_close": DROPDOWN_AUTOCLOSE,
    }
    JINJA={
        "filtering": {
            "edges_lookup": {"field1": ["AM", "JL"], "field2": [None]},
            "nodes_lookup": {"label": ["1", "2", "3"], "shape": ["dot"]},
        }
    }
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    options = Options()
    options.pyvisjs.set_filtering(
        enable_highlighting=ENABLE_HIGHLIGHTING, 
        edge_filtering=EDGE_FILTERING,
        node_filtering=NODE_FILTERING,
        dropdown_auto_close=DROPDOWN_AUTOCLOSE,
    )
    net = Network("Network1", options=options)
    net.add_edge(1, 2, field1="AM")
    net.add_edge(1, 3, field1="AM")
    net.add_edge(2, 3, field1="JL")
    net.render()


    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_render_tom_template_edge_filtering_int(mock_Environment):
    # init
    TEMPLATE_FILENAME="container-template.html"
    ENABLE_HIGHLIGHTING=True
    EDGE_FILTERING=34
    NODE_FILTERING=22
    PYVISJS={
        "enable_highlighting": ENABLE_HIGHLIGHTING,
        "dropdown_auto_close": False, # default value
    }
    JINJA={
        "filtering": {
            "edges_lookup": {"34": [None]},
            "nodes_lookup": {"22": [None]},
        }
    }
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    options = Options()
    options.pyvisjs.set_filtering(
        enable_highlighting=ENABLE_HIGHLIGHTING, 
        edge_filtering=EDGE_FILTERING,
        node_filtering=NODE_FILTERING
    )
    net = Network("Network1", options=options)
    net.add_edge(1, 2)
    net.render()
 

    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=ANY, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_network_render_default_template_and_return_value(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    DEFAULT_TEMPLATE_FILENAME = "basic-template.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT

    # call
    network = Network("Test Network")
    html_output = network.render() # <--------------------

    # assert
    mock_get_template.assert_called_once_with(DEFAULT_TEMPLATE_FILENAME)
    mock_save_file.assert_not_called()
    mock_open_file.assert_not_called()
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_network_render_template_with_open_in_browser(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    TEMPLATE_FILENAME = "basic-template.html"
    DEFAULT_OUTPUT_FILENAME = "default.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT
    mock_save_file.return_value = DEFAULT_OUTPUT_FILENAME

    # call
    network = Network("Test Network")
    html_output = network.render(open_in_browser=True) # <--------------------

    #assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME)
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_network_render_template_with_save_to_output(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    TEMPLATE_FILENAME = "basic-template.html"
    DEFAULT_OUTPUT_FILENAME = "default.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT

    # call
    network = Network("Test Network")
    html_output = network.render(save_to_output=True) # <--------------------

    #assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(DEFAULT_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_not_called()
    assert html_output == RENDER_RESULT


@patch('pyvisjs.network.open_file')
@patch('pyvisjs.network.save_file')
@patch('pyvisjs.network.Environment')
def test_network_render_template_with_open_and_save_no_defaults(mock_Environment, mock_save_file, mock_open_file):
    # init
    RENDER_RESULT = "<html>template</html>"
    TEMPLATE_FILENAME = "basic-template.html"
    CUSTOM_OUTPUT_FILENAME = "custom_output.html"
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_render.return_value = RENDER_RESULT
    mock_save_file.return_value = CUSTOM_OUTPUT_FILENAME

    # call
    network = Network("Test Network")
    html_output = network.render( # <--------------------
        open_in_browser=True, 
        save_to_output=True, 
        output_filename=CUSTOM_OUTPUT_FILENAME)

    #assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_save_file.assert_called_once_with(CUSTOM_OUTPUT_FILENAME, RENDER_RESULT)
    mock_open_file.assert_called_once_with(CUSTOM_OUTPUT_FILENAME)
    assert html_output == RENDER_RESULT

@patch('pyvisjs.network.Network.render')
def test_network_show_default_params(mock_render):
    # init
    # mock
    # call
    net = Network("Network")
    net.show()

    # assert
    mock_render.assert_called_once_with(open_in_browser=True)

@patch('pyvisjs.network.Network.render')
def test_network_show(mock_render):
    # init
    FILE_NAME = "output1.html"
    # mock
    # call
    net = Network("Network")
    net.show(FILE_NAME)

    # assert
    mock_render.assert_called_once_with(open_in_browser=True, output_filename=FILE_NAME)


# .
# ├── file1.txt
# ├── file2
# └── subdir1
#     ├── file3
#     └── file4
@patch("os.getcwd")
@patch("os.walk")
@patch('pyvisjs.network.Environment')
def test_network_from_dir_no_options(mock_Environment, mock_os_walk, mock_os_getcwd):
    # init
    TEMPLATE_FILENAME="basic-template.html"
    ROOT_COLOR="orange"
    FOLDER_COLOR="#4eba3f"
    TXT_COLOR="#DF7DEC"
    JS_COLOR="#da7422"
    FOLDER_SHAPE="circle"
    FILE_SHAPE="box"
    FONT={"color": "black"}
    DATA= {
        "nodes": [
            { "id": ".", "label": "working_dir", "shape": "circle", "color": ROOT_COLOR, "file_ext": "", "file_type": "dir", "shape": FOLDER_SHAPE, "font": FONT },
            { "id": f".{os.sep}subdir1", "label": "subdir1", "shape": "circle", "color": FOLDER_COLOR, "file_ext": "", "file_type": "dir", "shape": FOLDER_SHAPE, "font": FONT },
            { "id": f".{os.sep}subdir2", "label": "subdir2", "shape": "circle", "color": FOLDER_COLOR, "file_ext": "", "file_type": "dir", "shape": FOLDER_SHAPE, "font": FONT },
            { "id": f".{os.sep}file1.txt", "label": "file1.txt", "shape": "circle", "color": TXT_COLOR, "file_ext": ".txt", "file_type": "file", "shape": FILE_SHAPE, "font": FONT },
            { "id": f".{os.sep}file2.js", "label": "file2.js", "shape": "circle", "color": JS_COLOR, "file_ext": ".js", "file_type": "file", "shape": FILE_SHAPE, "font": FONT },
        ],
        "edges": [
            { "from": ".", "to": f".{os.sep}subdir1", "label": "dir:0" },
            { "from": ".", "to": f".{os.sep}subdir2", "label": "dir:1" },
            { "from": ".", "to": f".{os.sep}file1.txt", "label": "file:0" },
            { "from": ".", "to": f".{os.sep}file2.js", "label": "file:1" },
        ],
        "options": {}
    }
    PYVISJS={}
    JINJA={}
    
    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render
    mock_os_getcwd.return_value = "working_dir"

    # path, subdirs, files
    mock_os_walk.return_value = [
        (".", ["subdir1", "subdir2"], ["file1.txt", "file2.js"]),
    ]

    # call
    net = Network.from_dir(".")
    net.render()

    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_pyvisjs_dataTables_default(mock_Environment):
    # init
    TEMPLATE_FILENAME = "container-template.html"
    PYVISJS={}
    DATA = {
        "nodes": [
            {'id': 'AM', 'label': 'AM', 'shape': 'dot'},
            {'id': 'JL', 'label': 'JL', 'shape': 'dot'},                     
            {'id': 'DM', 'label': 'DM', 'shape': 'dot'},  
        ], 
        "edges": [
            {'category': 'pers', 'direction': 'out', 'to': 'JL', 'label': '200', 'from': 'AM'},
            {'category': 'pers', 'direction': 'out', 'to': 'DM', 'label': '20', 'from': 'AM'},           
        ],
        "options": {}
    }
    JINJA = {
        'tables': {
            'bottom': {
                'position': 'bottom', 
                'columns': ['category', 'direction', 'to', 'label', 'from'], 
                'data': [
                    {'category': 'pers', 'direction': 'out', 'to': 'JL', 'label': '200', 'from': 'AM'},
                    {'category': 'pers', 'direction': 'out', 'to': 'DM', 'label': '20', 'from': 'AM'},
                ]
            }
        }
    }

    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    opt = Options()
    opt.pyvisjs.set_dataTable()

    net = Network(options=opt)
    net.add_edge("AM", "JL", label="200", category="pers", direction="out")
    net.add_edge("AM", "DM", label="20", category="pers", direction="out")
    net.render()
    
    # assert
    assert len(net.options.pyvisjs.dataTables) == 1
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_pyvisjs_dataTables_all_tables(mock_Environment):
    # init
    BOTTOM_DATA = [
        {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
        {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
        {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
        {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
        {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
        {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
        {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
    ]
    TEMPLATE_FILENAME = "container-template.html"
    DATA = {
        "nodes": [
            {'id': 'AM', 'label': 'AM', 'shape': 'dot'},
            {'id': 'JL', 'label': 'JL', 'shape': 'dot'},                     
            {'id': 'DM', 'label': 'DM', 'shape': 'dot'},
            {'id': 'Hypo', 'label': 'Hypo', 'shape': 'dot'},
            {'id': 'McDnlds', 'label': 'McDnlds', 'shape': 'dot'},
            {'id': 'LMT', 'label': 'LMT', 'shape': 'dot'}, 
        ], 
        "edges": [
            {'category': 'pers', 'table': 'left', 'to': 'JL', 'label': '200', 'from': 'AM'},
            {'category': 'pers', 'table': 'left', 'to': 'DM', 'label': '20', 'from': 'AM'},
            {'category': 'hypo', 'to': 'Hypo', 'label': '150', 'from': 'JL'},
            {'category': 'food', 'to': 'McDnlds', 'label': '5', 'from': 'DM'},
            {'category': 'tele', 'table': 'left', 'to': 'LMT', 'label': '33', 'from': 'AM'},       
            {'category': 'pers', 'table': 'right', 'to': 'AM', 'label': '50', 'from': 'JL'},           
        ],
        "options": {}
    }
    PYVISJS={}
    JINJA = {
        'tables': {
            'left': {
                'position': 'left', 
                'columns': [
                    {'name': 'from', 'label': 'Partner'}, 
                    {'name': 'label', 'label': 'Amount'}, 
                    {'name': 'category'}
                ], 
                'data': [
                    {'category': 'pers', 'to': 'JL', 'label': '200', 'from': 'AM', 'table': 'left'},
                    {'category': 'pers', 'to': 'DM', 'label': '20', 'from': 'AM', 'table': 'left'},
                    {'category': 'tele', 'to': 'LMT', 'label': '33', 'from': 'AM', 'table': 'left'},              
                ]
            }, 
            'right': {
                'position': 'right', 
                'columns': [
                    {'name': 'to', 'label': 'Partner'}, 
                    {'name': 'label', 'label': 'Amount'}, 
                    {'name': 'category', 'label': 'Class.'}
                ], 
                'data': [                
                    {'category': 'pers', 'to': 'AM', 'label': '50', 'from': 'JL', 'table': 'right'},
                ]
            }, 
            'bottom': {
                'position': 'bottom', 
                'columns': ['id', 'from', 'to', 'amount', 'country', 'class'], 
                'data': [
                    {'id': 1, 'from': 'AM', 'to': 'JL', 'amount': 100, 'country': 'LV', 'class': 'pers'}, 
                    {'id': 2, 'from': 'AM', 'to': 'JL', 'amount': 100, 'country': 'LV', 'class': 'pers'}, 
                    {'id': 3, 'from': 'AM', 'to': 'DM', 'amount': 20, 'country': 'EE', 'class': 'pers'}, 
                    {'id': 4, 'from': 'JL', 'to': 'Hypo', 'amount': 150, 'country': 'GB', 'class': 'hypo'}, 
                    {'id': 5, 'from': 'JL', 'to': 'AM', 'amount':50, 'country': 'LV', 'class': 'pers'}, 
                    {'id': 6, 'from': 'AM', 'to': 'LMT', 'amount': 33, 'country': 'LV', 'class': 'tele'}, 
                    {'id': 7, 'from': 'DM', 'to': 'McDnlds', 'amount': 5, 'country': 'US', 'class': 'food'}
                ]
            }
        }
    }

    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    opt = Options()
    opt.pyvisjs \
        .set_dataTable(
            "left",
            [
                {"name": "from", "label": "Partner"}, 
                {"name": "label", "label": "Amount"}, 
                {"name": "category"}
            ],
            "edges") \
        .set_dataTable(
            "right",
            [
                {"name": "to", "label": "Partner"}, 
                {"name": "label", "label": "Amount"}, 
                {"name": "category", "label": "Class."}
            ],
            "edges") \
        .set_dataTable(
            "bottom",
            ["id", "from", "to", "amount", "country", "class"],
            BOTTOM_DATA)

    # out -> left
    net = Network(options=opt)
    net.add_edge("AM", "JL", label="200", category="pers", table="left")
    net.add_edge("AM", "DM", label="20", category="pers", table="left")
    net.add_edge("JL", "Hypo", label="150", category="hypo")
    net.add_edge("DM", "McDnlds", label="5", category="food")
    net.add_edge("AM", "LMT", label="33", category="tele", table="left")
    net.add_edge("JL", "AM", label="50", category="pers", table="right")
    net.render()
    
    # assert
    assert len(net.options.pyvisjs.dataTables) == 3
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_from_transactions_LoD_fields_edges_list(mock_Environment):
    # init
    TRANS = {
        "data": [
            {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
            {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
            {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
            {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
            {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
        ],
        "fields": {
            "edges": ["from", "to", "amount"],
        },
    }
    TEMPLATE_FILENAME = "basic-template.html"
    DATA = {
        "nodes": [
            { "id": "AM", "label": "AM", "shape": "dot" },
            { "id": "JL", "label": "JL", "shape": "dot" },
            { "id": "DM", "label": "DM", "shape": "dot" },
            { "id": "Hypo", "label": "Hypo", "shape": "dot" },
            { "id": "LMT", "label": "LMT", "shape": "dot" },
            { "id": "McDnlds", "label": "McDnlds", "shape": "dot" },
        ],
        "edges": [
            { "from": "AM", "to": "JL", "amount": 200 },
            { "from": "AM", "to": "DM", "amount": 20 },
            { "from": "JL", "to": "Hypo", "amount": 150 },
            { "from": "JL", "to": "AM", "amount": 50 },
            { "from": "AM", "to": "LMT", "amount": 33 },
            { "from": "DM", "to": "McDnlds", "amount": 5 },
        ],
        "options": {}
    }
    PYVISJS = {}
    JINJA = {}

    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    net = Network.from_transactions(TRANS)
    net.render()
    
    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_from_transactions_LoD_no_fields(mock_Environment):
    # init
    TRANS = {
        "data": [
            {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
            {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
            {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
            {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
            {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
        ],
    }
    TEMPLATE_FILENAME = "basic-template.html"
    DATA = {
        "nodes": [
            { "id": "AM", "label": "AM", "shape": "dot" },
            { "id": "JL", "label": "JL", "shape": "dot" },
            { "id": "DM", "label": "DM", "shape": "dot" },
            { "id": "Hypo", "label": "Hypo", "shape": "dot" },
            { "id": "LMT", "label": "LMT", "shape": "dot" },
            { "id": "McDnlds", "label": "McDnlds", "shape": "dot" },
        ],
        "edges": [
            {"id": 2, "from": "AM", "to": "JL", "amount": 200, "country": "LV", "class": "pers"},
            {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
            {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
            {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
            {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
            {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
        ],
        "options": {}
    }
    PYVISJS = {}
    JINJA = {}

    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    net = Network.from_transactions(TRANS)
    net.render()
    
    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_from_transactions_LoD_fields_edges_dict_fr0m(mock_Environment):
    # init
    TRANS = {
        "data": [
            {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
            {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
            {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
            {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
            {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
        ],
        "fields": {
            "edges": {"from": "fr0m", "to": "to", "amount": "money"},
        },
    }
    TEMPLATE_FILENAME = "basic-template.html"
    DATA = {
        "nodes": [
            { "id": "AM", "label": "AM", "shape": "dot" },
            { "id": "JL", "label": "JL", "shape": "dot" },
            { "id": "DM", "label": "DM", "shape": "dot" },
            { "id": "Hypo", "label": "Hypo", "shape": "dot" },
            { "id": "LMT", "label": "LMT", "shape": "dot" },
            { "id": "McDnlds", "label": "McDnlds", "shape": "dot" },
        ],
        "edges": [
            { "from": "AM", "to": "JL", "money": 200 },
            { "from": "AM", "to": "DM", "money": 20 },
            { "from": "JL", "to": "Hypo", "money": 150 },
            { "from": "JL", "to": "AM", "money": 50 },
            { "from": "AM", "to": "LMT", "money": 33 },
            { "from": "DM", "to": "McDnlds", "money": 5 },
        ],
        "options": {}
    }
    PYVISJS = {}
    JINJA = {}

    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    net = Network.from_transactions(TRANS)
    net.render()
    
    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_from_transactions_LoD_fields_edges_dict(mock_Environment):
    # init
    TRANS = {
        "data": [
            {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
            {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
            {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
            {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
            {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
        ],
        "fields": {
            "edges": {"from": "from", "to": "to", "amount": "money"},
        },
    }
    TEMPLATE_FILENAME = "basic-template.html"
    DATA = {
        "nodes": [
            { "id": "AM", "label": "AM", "shape": "dot" },
            { "id": "JL", "label": "JL", "shape": "dot" },
            { "id": "DM", "label": "DM", "shape": "dot" },
            { "id": "Hypo", "label": "Hypo", "shape": "dot" },
            { "id": "LMT", "label": "LMT", "shape": "dot" },
            { "id": "McDnlds", "label": "McDnlds", "shape": "dot" },
        ],
        "edges": [
            { "from": "AM", "to": "JL", "money": 200 },
            { "from": "AM", "to": "DM", "money": 20 },
            { "from": "JL", "to": "Hypo", "money": 150 },
            { "from": "JL", "to": "AM", "money": 50 },
            { "from": "AM", "to": "LMT", "money": 33 },
            { "from": "DM", "to": "McDnlds", "money": 5 },
        ],
        "options": {}
    }
    PYVISJS = {}
    JINJA = {}

    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    net = Network.from_transactions(TRANS)
    net.render()
    
    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_from_transactions_LoD_fields_edges_dict_skipping_from_and_to(mock_Environment):
    # init
    TRANS = {
        "data": [
            {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
            {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
            {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
            {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
            {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
        ],
        "fields": {
            "edges": {"amount": "money"},
        },
    }
    TEMPLATE_FILENAME = "basic-template.html"
    DATA = {
        "nodes": [
            { "id": "AM", "label": "AM", "shape": "dot" },
            { "id": "JL", "label": "JL", "shape": "dot" },
            { "id": "DM", "label": "DM", "shape": "dot" },
            { "id": "Hypo", "label": "Hypo", "shape": "dot" },
            { "id": "LMT", "label": "LMT", "shape": "dot" },
            { "id": "McDnlds", "label": "McDnlds", "shape": "dot" },
        ],
        "edges": [
            { "from": "AM", "to": "JL", "money": 200 },
            { "from": "AM", "to": "DM", "money": 20 },
            { "from": "JL", "to": "Hypo", "money": 150 },
            { "from": "JL", "to": "AM", "money": 50 },
            { "from": "AM", "to": "LMT", "money": 33 },
            { "from": "DM", "to": "McDnlds", "money": 5 },
        ],
        "options": {}
    }
    PYVISJS = {}
    JINJA = {}

    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    net = Network.from_transactions(TRANS)
    net.render()
    
    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)

@patch('pyvisjs.network.Environment')
def test_network_from_transactions_LoD_fields_edges_list_skipping_from_and_to(mock_Environment):
    # init
    TRANS = {
        "data": [
            {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
            {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
            {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
            {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
            {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
            {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
        ],
        "fields": {
            "edges": ["amount", "country", "class"],
        },
    }
    TEMPLATE_FILENAME = "basic-template.html"
    DATA = {
        "nodes": [
            { "id": "AM", "label": "AM", "shape": "dot" },
            { "id": "JL", "label": "JL", "shape": "dot" },
            { "id": "DM", "label": "DM", "shape": "dot" },
            { "id": "Hypo", "label": "Hypo", "shape": "dot" },
            { "id": "LMT", "label": "LMT", "shape": "dot" },
            { "id": "McDnlds", "label": "McDnlds", "shape": "dot" },
        ],
        "edges": [
            {"from": "AM", "to": "JL", "amount": 200, "country": "LV", "class": "pers"},
            {"from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
            {"from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
            {"from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
            {"from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
            {"from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
        ],
        "options": {}
    }
    PYVISJS = {}
    JINJA = {}

    # mock
    mock_get_template = mock_Environment.return_value.get_template
    mock_render = mock_get_template.return_value.render

    # call
    net = Network.from_transactions(TRANS)
    net.render()
    
    # assert
    mock_get_template.assert_called_once_with(TEMPLATE_FILENAME)
    mock_render.assert_called_once_with(data=DATA, pyvisjs=PYVISJS, jinja=JINJA)