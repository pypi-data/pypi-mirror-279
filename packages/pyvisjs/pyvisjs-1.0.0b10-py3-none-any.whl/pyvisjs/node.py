from .base_dictable import BaseDictable

class Node(BaseDictable):
    def __init__(self, id:str, label:str=None, color:str=None, shape:str="dot", size=None, **kwargs):
        super().__init__()
        self.id = str(id)
        self.label = label or str(id)
        self.color = color
        self.shape = shape
        self.size = size

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"{self.__class__.__name__}(\'{self.id}\', \'{self.label}\', \'{self.color}\', \'{self.shape}\', {self.size})"