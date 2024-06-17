from .base_dictable import BaseDictable
from typing import Self

class Edge(BaseDictable):

    _attributes_mapping = {
        "start": "from",
        "end": "to"
    }

    @classmethod
    def convert_to_template_attribute(cls, attr):
        return cls._attributes_mapping.get(attr, attr)

    def __init__(self, start:str, end:str, **kwargs):
        convert_to_template_attribute = lambda attr: Edge.convert_to_template_attribute(attr)
        is_not_attributes_mapping = lambda attr: attr != "_attributes_mapping"
        super().__init__(attr_map_func = convert_to_template_attribute, attr_filter_func=is_not_attributes_mapping)
        self.start = str(start)
        self.end = str(end)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self, **kwargs) -> Self:
        for key, new_value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, new_value)
            elif key == "id":
                setattr(self, key, new_value)
            else:
                old_value = getattr(self, key)
                if isinstance(new_value, (float, int)) and isinstance(old_value, (float, int)):
                    setattr(self, key, old_value + new_value)

        return self

    def __repr__(self):
        return f"Edge(\'{self.start}\', \'{self.end}\')"