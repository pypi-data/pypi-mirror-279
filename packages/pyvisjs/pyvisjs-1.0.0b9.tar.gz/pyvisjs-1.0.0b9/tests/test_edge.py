from pyvisjs import Edge

def test_edge_init_default():
    # init
    START_ID = "1"
    END_ID = "2"

    # mock

    # call
    e = Edge(START_ID, END_ID)
    
    # assert
    assert e.start == START_ID
    assert e.end == END_ID

def test_edge_init_kwargs():
    # init
    START_ID = "1"
    END_ID = "2"
    NODE_CATEGORY = "category1"
    NODE_AMOUNT = 1009.4
    NODE_HASVALUE = False

    # mock

    # call
    e = Edge(START_ID, END_ID, category=NODE_CATEGORY, amount=NODE_AMOUNT, has_value=NODE_HASVALUE)
    
    # assert
    assert e.start == START_ID
    assert e.end == END_ID
    assert (e.category, e.amount, e.has_value) == (NODE_CATEGORY, NODE_AMOUNT, NODE_HASVALUE)


def test_edge_to_dict():
    # init
    START_ID = "A"
    END_ID = "B"
    EDGE_DICT = {
            "from": START_ID,
            "to": END_ID,
        }

    # mock

    # call
    e = Edge(START_ID, END_ID)
    
    # assert
    assert e.to_dict() == EDGE_DICT

def test_edge_update():
     # init
    e1 = Edge("A", "B")
    e2 = Edge("A", "C", color="green")
    e3 = Edge("A", "D", value=33)
    e4 = Edge("A", "E", id=1)
    
    # mock

    # call
    e1.update(color="red")
    e2.update(color="red")
    e3.update(value=12)
    e4.update(id=2, code=91827)
    
    # assert
    assert e1.to_dict() == {"from": "A", "to": "B", "color": "red"} 
    assert e2.to_dict() == {"from": "A", "to": "C", "color": "green"} 
    assert e3.to_dict() == {"from": "A", "to": "D", "value": 45} 
    assert e4.to_dict() == {"from": "A", "to": "E", "id": 2, "code": 91827} 