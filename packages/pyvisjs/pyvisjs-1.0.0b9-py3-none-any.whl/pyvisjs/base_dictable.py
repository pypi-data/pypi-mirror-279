from typing import Dict

class BaseDictable:

    def __init__(self, attr_filter_func=None, attr_map_func=None):
        self.attr_filter_func = attr_filter_func or (lambda x: x)
        self.attr_map_func = attr_map_func or (lambda x: x)

    def _update_dict_with_locals(self, _dict:Dict, _locals:Dict):
        for attr_name, attr_value in _locals.items():
            if attr_value is not None and attr_name != "self":
                if attr_name == "kwargs":
                    for kwargs_key, kwargs_value in attr_value.items():
                        _dict.update({kwargs_key: kwargs_value})
                else:
                    _dict.update({attr_name: attr_value})

    def to_dict(self):
        """Converts object to dictionary.  
        Used to pass network, nodes and edges to the underlying html
        """
        result = {}

        def has_to_dict(attr):
            return hasattr(attr, "to_dict") and callable(getattr(attr, "to_dict"))
        
        def process_attr(attr):
            return attr.to_dict() if has_to_dict(attr) else attr
        
        def process_list(lst):
            return [process_attr(item) for item in lst]
        
        def process_dict(dict):
            return {key: process_list(value) if isinstance(value, list) else process_attr(value) for (key, value) in attr_value.items()}
        


        for attr_name in list(filter(self.attr_filter_func, dir(self))):
            if not attr_name.startswith("__"):
                attr_value = getattr(self, attr_name)
                attr_name = self.attr_map_func(attr_name)
                if callable(attr_value):
                    continue
                elif isinstance(attr_value, list):
                    result[attr_name] = process_list(attr_value)
                elif isinstance(attr_value, dict):
                    if not attr_value: continue
                    result[attr_name] = process_dict(attr_value)
                elif has_to_dict(attr_value):
                    obj_dict = attr_value.to_dict()
                    if not obj_dict: continue
                    result[attr_name] = obj_dict
                else:
                    if attr_value is None: continue
                    result[attr_name] = attr_value
                    
        return result