from pyvisjs.base_dictable import BaseDictable

def test_basedictable_init_default():
    # init
    class D(BaseDictable):
        def __init__(self):
            super().__init__()

    # mock

    # call
    d = D()
    
    # assert
    assert d.to_dict() == {}

def test_basedictable_dictable_attributes():
    # init
    class Person(BaseDictable):
        def __init__(self, name, age, parents):
            super().__init__()

            self.name = name
            self.age = age
            self.parents = parents


    NAME = "Andrey"
    AGE = 43
    PARENTS = [Person("Lydia", 63, None), Person("Mark", 64, None)]
    RESULT = {
        "name": NAME,
        "age": AGE,
        "parents": [
            { "name": "Lydia", "age": 63 },
            { "name": "Mark", "age": 64 },
        ]
    }
    # mock

    # call
    me = Person(NAME, AGE, PARENTS)
    
    # assert
    assert me.to_dict() == RESULT

def test_basedictable_instance_attr():
    # init
    class D(BaseDictable):
        def __init__(self):
            super().__init__()

    NAME = "AM"
    # mock

    # call
    d = D()
    d.name = NAME
    
    # assert
    assert d.to_dict() == {"name": NAME}

def test_basedictable_attr_filter_func():
    # init
    class ME(BaseDictable):
        def __init__(self, name, age):
            only_show_name_and_age = lambda attr: attr in ["name", "age"]
            super().__init__(attr_filter_func=only_show_name_and_age)

            self.name = name
            self.age = age
            self.country = "LV"
            self.city = "Jurmala"

    NAME = "AM"
    AGE = 44
    ME_DICT = {
        "name": NAME,
        "age": AGE,
    }

    # mock

    # call
    me = ME(NAME, AGE)
    
    # assert
    assert me.to_dict() == ME_DICT

def test_basedictable_attr_map_func():
    # init
    class ME(BaseDictable):
        def __init__(self, name, age, country, city):
            mapping = {
                "name": "firstname",
                "age": "age_years"
            }
            change_name_and_age = lambda attr: mapping.get(attr, attr)
            super().__init__(attr_map_func=change_name_and_age)

            self.name = name
            self.age = age
            self.country = country
            self.city = city

    NAME = "AM"
    AGE = 44
    COUNTRY = "LV"
    CITY = "Jurmala"
    ME_DICT = {
        "firstname": NAME,
        "age_years": AGE,
        "country": COUNTRY,
        "city": CITY
    }

    # mock

    # call
    me = ME(NAME, AGE, COUNTRY, CITY)
    
    # assert
    assert me.to_dict() == ME_DICT

def test_basedictable_update_dict_with_locals():
    # init
    class D(BaseDictable):
        def __init__(self):
            super().__init__()
            self.d1ct = {}

        def func(self, firstname:str=None, lastname:str=None, another_dict=None, empty_dict=None):
            self._update_dict_with_locals(self.d1ct, locals())

    FNAME = "Andrey"
    EMPTY_DICT={}
    ANOTHER_DICT = {
        "age": 43,
        "sex": "M"
    }
    RESULT = {
        "firstname": FNAME,
        # no lastname
        "another_dict": ANOTHER_DICT,
        "empty_dict": EMPTY_DICT,
    }
    # mock

    # call
    d = D()
    d.func(FNAME, another_dict=ANOTHER_DICT, empty_dict=EMPTY_DICT)
    
    # assert
    assert d.d1ct == RESULT