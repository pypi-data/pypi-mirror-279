from pyvisjs import Options

def test_options_init_default():
    # init
    DEFAULT_DICT = {}

    # mock

    # call
    options = Options()
    
    # assert
    assert options
    assert options.to_dict() == DEFAULT_DICT 

def test_options_physics_set_barnesHut():
    # init
    EXPECTED_DICT = {
        'physics': {
            'barnesHut': {
                'gravitationalConstant': -2750, 
                'centralGravity': 0.3, 
                'springLength': 250, 
                'springConstant': 0, 
                'damping': 1
            }
        }
    }

    # mock

    # call
    options = Options()

    options.physics.set_barnesHut(
        gravitationalConstant=-2750,
        centralGravity=0.3,
        springConstant=0,
        springLength=250,
        damping=1
    )
    
    # assert
    assert options
    assert options.to_dict() == EXPECTED_DICT 

def test_options_edges_nodes_physics():
    # init
    SCALING_MIN = 10
    SCALING_MAX = 30
    COLOR = "LIME"
    SMOOTH = False
    GR_CONSTANT = -30000
    ST_ITERATIONS = 2500
    OPTIONS_DICT = {
        'edges': {
            'color': {
                'color': COLOR
            }, 
            'smooth': {
                'enabled': SMOOTH
            }
        }, 
        'nodes': {
            'scaling': {
                'min': SCALING_MIN, 
                'max': SCALING_MAX
            }
        }, 
        'physics': {
            'barnesHut': {
                'gravitationalConstant': GR_CONSTANT
            }, 
            'stabilization': {
                'iterations': ST_ITERATIONS
            }
        }
    }

    # mock

    # call
    options = Options()
    options.nodes.set_scaling(min = SCALING_MIN, max = SCALING_MAX)
    options.edges.set_color(color = COLOR)
    options.edges.set_smooth(enabled = SMOOTH)
    options.physics.set_barnesHut(gravitationalConstant=GR_CONSTANT)
    options.physics.set_stabilization(iterations=ST_ITERATIONS)
    
    # assert
    assert options.to_dict() == OPTIONS_DICT

def test_options_bluor_use_case():
    # init
    OPTIONS_DICT = {
        "configure": {
            "enabled": False
        },
        "edges": {
            "arrows": "to",
            "arrowStrikethrough": False,
            "color": {
                "inherit": True
            },
            "smooth": {
                "enabled": True,
                "type": "dynamic"
            }
        },
        "interaction": {
            "dragNodes": True,
            "hideEdgesOnDrag": False,
            "hideNodesOnDrag": False
        },
        "physics": {
            "barnesHut": {
                "avoidOverlap": 0,
                "centralGravity": 0.3,
                "damping": 1, #is_gummy=0.09
                "gravitationalConstant": -2750,
                "springConstant": 0, #is_gummy=0.05
                "springLength": 250
            },
            "enabled": True,
            "stabilization": {
                "enabled": True,
                "fit": True,
                "iterations": 1000,
                "onlyDynamicEdges": False,
                "updateInterval": 50
            }
        }
    }

    # mock

    # call
    options = Options()
    options \
        .set_configure(enabled=False) \
        .set_interaction(dragNodes=True, hideEdgesOnDrag=False, hideNodesOnDrag=False)
    options.edges \
        .set_color(inherit=True) \
        .set_smooth(type="dynamic", enabled=True) \
        .set(arrows="to", arrowStrikethrough=False)
    options.physics \
        .set(enabled=True) \
        .set_barnesHut(avoidOverlap=0, centralGravity=0.3, damping=1, gravitationalConstant=-2750, springConstant=0, springLength=250) \
        .set_stabilization(enabled=True, fit=True, iterations=1000, onlyDynamicEdges=False, updateInterval=50)
    
    # assert
    assert options.to_dict() == OPTIONS_DICT

def test_option_pyvisjs_set_dataTable_default():
    # init
    DATA_TABLES = {
        "bottom": {
            "position": "bottom",
        }
    }

    # mock

    # call
    options = Options().pyvisjs.set_dataTable()
    
    # assert
    assert options
    assert options.dataTables == DATA_TABLES     

def test_option_pyvisjs_for_jinja_tables():
    # init
    NODES = [
        {"id": 1, "label": "node1", "color": "black", "table": "left"},
        {"id": 2, "label": "node2", "color": "white", "table": "right"},
    ]
    EDGES = [
        {"from": 1, "to": 2, "label": "purchase", "value": 100, "table": "left"},
        {"from": 2, "to": 1, "label": "refund", "value": 95, "table": "right"}
    ]
    TABLES_EXPECTED = {
        "tables": {
            "left": {
                "position": "left",
                "columns": [
                    {"field": "from", "label": "Partner"}, 
                    {"field": "label", "label": "Type"}, 
                    {"field": "value"},
                ],
                "data": [{"from": 1, "to": 2, "label": "purchase", "value": 100, "table": "left"}]
            },
            "right": {
                "position": "right",
                "columns": ["id", "label", "color"], # no "table"
                "data": [{"id": 2, "label": "node2", "color": "white", "table": "right"}]
            },
            "bottom": {
                "position": "bottom",
                "columns": ["id", "class"],
                "data": [
                    {"id": 1, "name": "h1", "class": "v3"},
                    {"id": 2, "name": "h2", "class": "v8"},
                ]
            }
        }
    }

    # mock

    # call
    options = Options()
    options.pyvisjs \
        .set_dataTable(
            "left",
            [
                {"field": "from", "label": "Partner"}, 
                {"field": "label", "label": "Type"}, 
                {"field": "value"},
            ],
            "edges") \
        .set_dataTable(
            "right",
            # no columns specified,
            data = "nodes") \
        .set_dataTable(
            position = "bottom",
            columns = ["id", "class"],
            data = [
                {"id": 1, "name": "h1", "class": "v3"},
                {"id": 2, "name": "h2", "class": "v8"},
            ])
        
    tables_actual = options.pyvisjs.for_jinja(EDGES, NODES)
    
    # assert
    assert tables_actual == TABLES_EXPECTED

def test_option_pyvisjs_set_filtering_default():
    # init
    FILTERING_EXPECTED = {
        "enable_highlighting": False,
        "dropdown_auto_close": False,
    }

    # mock

    # call
    options = Options()
    options.pyvisjs.set_filtering()
    
    # assert
    assert options.pyvisjs.filtering == FILTERING_EXPECTED

def test_option_pyvisjs_for_jinja_filtering_node_filtering_only():
    # init
    NODES = [
        {"id": 1, "label": "node1", "color": "black", "table": "left"},
        {"id": 2, "label": "node2", "color": "white", "table": "right"},
    ]
    EDGES = [
        {"from": 1, "to": 2},
        {"from": 2, "to": 1}
    ]
    TABLES_EXPECTED = {
        "filtering": {
            "nodes_lookup": {
                "label": ["node1", "node2"],
                "wrong_field": [None]
            },
            "edges_lookup": {
                "from": [1, 2],
                "to": [1, 2], # sorting
            }
        }
    }

    # mock

    # call
    options = Options()
    options.pyvisjs \
        .set_filtering(
            enable_highlighting=True,
            node_filtering=["label", "wrong_field"],
            dropdown_auto_close=True,
        )
        
    tables_actual = options.pyvisjs.for_jinja(EDGES, NODES)
    
    # assert
    assert tables_actual == TABLES_EXPECTED   

def test_option_pyvisjs_for_jinja_filtering_edge_filtering_empty_list():
    # init
    NODES = [
        {"id": 1, "label": "node1", "color": "black", "table": "left"},
        {"id": 2, "label": "node2", "color": "white", "table": "right"},
    ]
    EDGES = [
        {"from": 1, "to": 2},
        {"from": 2, "to": 1}
    ]
    TABLES_EXPECTED = {
        "filtering": {
            "nodes_lookup": {
                "label": ["node1", "node2"],
            },
            "edges_lookup": {}
        }
    }

    # mock

    # call
    options = Options()
    options.pyvisjs \
        .set_filtering(
            enable_highlighting=True,
            node_filtering=["label"],
            edge_filtering=[],
            dropdown_auto_close=True,
        )
        
    tables_actual = options.pyvisjs.for_jinja(EDGES, NODES)
    
    # assert
    assert tables_actual == TABLES_EXPECTED   

def test_option_pyvisjs_for_jinja_filtering_edge_filtering_str():
    # init
    NODES = [
        {"id": 1, "label": "node1", "color": "black", "table": "left"},
        {"id": 2, "label": "node2", "color": "white", "table": "right"},
    ]
    EDGES = [
        {"from": 1, "to": 2},
        {"from": 2, "to": 1}
    ]
    TABLES_EXPECTED = {
        "filtering": {
            "nodes_lookup": {
                "label": ["node1", "node2"],
            },
            "edges_lookup": {
                "from": [1, 2],
            }
        }
    }

    # mock

    # call
    options = Options()
    options.pyvisjs \
        .set_filtering(
            enable_highlighting=True,
            node_filtering="label",
            edge_filtering="from",
            dropdown_auto_close=True,
        )
        
    tables_actual = options.pyvisjs.for_jinja(EDGES, NODES)
    
    # assert
    assert tables_actual == TABLES_EXPECTED   