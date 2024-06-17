from pyvisjs import Node

def test_node_repr_id():
    # init
    NODE_ID = 1

    # mock

    # call
    n = Node(NODE_ID)
    
    # assert
    assert repr(n) == "Node('1', '1', 'None', 'dot', None)"

def test_node_repr_all_args():
    # init
    NODE_ID = 1
    LABEL = "node 1"
    COLOR = "lime"
    SHAPE = "circle"
    SIZE = 14
    # mock

    # call
    n = Node(NODE_ID, LABEL, COLOR, SHAPE, SIZE)
    
    # assert
    assert repr(n) == "Node('1', 'node 1', 'lime', 'circle', 14)"

def test_node_init_default():
    # init
    NODE_ID = 1

    # mock

    # call
    n = Node(NODE_ID)
    
    # assert
    assert n.id == str(NODE_ID)

def test_node_init_positional_args():
    # init
    NODE_ID = "X"
    NODE_LABEL = "label"
    NODE_COLOR = "lime"
    NODE_SHAPE = "circle"
    NODE_SIZE = 50

    # mock

    # call
    n = Node(NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE)
    
    # assert
    assert (n.id, n.label, n.color, n.shape, n.size) == (NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE)

def test_node_init_keyword_args():
    # init
    NODE_ID = "1"
    NODE_LABEL = "label"
    NODE_COLOR = "lime"
    NODE_SHAPE = "circle"
    NODE_SIZE = 50

    # mock

    # call
    n = Node(NODE_ID, label=NODE_LABEL, size=NODE_SIZE, shape=NODE_SHAPE, color=NODE_COLOR)
    
    # assert
    assert (n.id, n.label, n.color, n.shape, n.size) == (NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE)

def test_node_init_kwargs():
    # init
    NODE_ID = "hello_is_id"
    NODE_LABEL = "label"
    NODE_COLOR = "lime"
    NODE_SHAPE = "circle"
    NODE_SIZE = 50
    NODE_CATEGORY = "category1"
    NODE_AMOUNT = 1009.4
    NODE_HASVALUE = False

    # mock

    # call
    n = Node(NODE_ID, label=NODE_LABEL, size=NODE_SIZE, shape=NODE_SHAPE, color=NODE_COLOR
             , category=NODE_CATEGORY, amount=NODE_AMOUNT, has_value=NODE_HASVALUE)
    
    # assert
    assert (n.id, n.label, n.color, n.shape, n.size, n.category, n.amount, n.has_value) \
        == (NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE, NODE_CATEGORY, NODE_AMOUNT, NODE_HASVALUE)

def test_node_to_dict():
    # init
    NODE_ID = 1
    NODE_LABEL = "label"
    NODE_COLOR = "lime"
    NODE_SHAPE = "circle"
    NODE_SIZE = None
    NODE_DICT = {
            "id": str(NODE_ID),
            "label": NODE_LABEL,
            "color": NODE_COLOR,
            "shape": NODE_SHAPE,
            # no element for size, because it was set to None
        }

    # mock

    # call
    n = Node(NODE_ID, NODE_LABEL, NODE_COLOR, NODE_SHAPE, NODE_SIZE)
    
    # assert
    assert n.to_dict() == NODE_DICT
