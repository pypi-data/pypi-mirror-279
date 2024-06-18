from .base_dictable import BaseDictable
from typing import Dict, Self, List
from .edge import Edge
from .utils import dict_of_lists_to_list_of_dicts, list_of_dicts_to_dict_of_lists

# Options
# ├── set_configure
# ├── set_interaction
# ├── Nodes
# │   └── set_scaling
# ├── Edges
# │   ├── set
# │   ├── set_color
# │   └── set_smooth
# ├── Physics
# │   ├── set
# │   ├── set_barnesHutKV
# │   ├── set_barnesHut
# │   └── set_stabilization
# └── Extra (pyvisjs)
#     ├── set
#     ├── set_startAnimation
#     ├── set_dataTable
#     ├── set_filtering
#     ├── set_sankey
#     ├── for_jinja (add to tests)
#     └── for_js (add to tests)
#     └── to_dict (will be removed)





class Options(BaseDictable):
    def __init__(self, height:str=None, width:str=None, clickToUse:bool=None):
        is_not_pyvisjs = lambda attr: attr != "pyvisjs"
        super().__init__(attr_filter_func=is_not_pyvisjs)
        if height: self.height = height
        if width: self.width = width
        if clickToUse: self.clickToUse = clickToUse

        self.configure = {}
        self.interaction = {}

        self.nodes = Options.Nodes()
        self.edges = Options.Edges()
        self.physics = Options.Physics()
        self.pyvisjs = Options.PyvisjsExtra()

    def set_configure(self, enabled:bool=None) -> Self:
        self._update_dict_with_locals(self.configure, locals())
        return self

    def set_interaction(self, dragNodes:bool=None, dragView:bool=None, hideEdgesOnDrag:bool=None, hideEdgesOnZoom:bool=None, hideNodesOnDrag:bool=None, zoomView:bool=None) -> Self:
        self._update_dict_with_locals(self.interaction, locals())
        return self
    
    class PyvisjsExtra(BaseDictable):
        def __init__(self):
            super().__init__()
            self.title:str = None
            self.filtering = {}
            self.startAnimation = {}
            self.dataTables = {}
            self.sankey = {}

        def set_dataTable(self, position:str=None, columns=None, data=None):

            position = position or "bottom"

            self.dataTables[position] = {}
            
            self._update_dict_with_locals(self.dataTables[position], locals())        
            return self     

        def set_sankey(self, enabled:bool=None):
            
            self._update_dict_with_locals(self.sankey, locals())        
            return self          

        def set_filtering(self, enable_highlighting:bool=False, edge_filtering=None, node_filtering=None, dropdown_auto_close:bool=False) -> Self:
            self._update_dict_with_locals(self.filtering, locals())        
            return self  

        def set_startAnimation(self, zoom_factor:float=None, duration_ms:int=None) -> Self:
            self._update_dict_with_locals(self.startAnimation, locals())        
            return self  

        def set(self, title:str=None) -> Self:
            if title: self.title = title
            return self
        
        def for_js(self) -> Dict:
            result = {}

            if "enable_highlighting" in self.filtering:
                result["enable_highlighting"] = self.filtering["enable_highlighting"]

            if "dropdown_auto_close" in self.filtering:
                result["dropdown_auto_close"] = self.filtering["dropdown_auto_close"]

            return result

        def for_jinja(self, edges:List[Dict], nodes:List[Dict]) -> Dict:
            result = {}

            if self.filtering:
                result["filtering"] = {}
                
                # edges
                edge_filtering = None
                if "edge_filtering" in self.filtering:
                    edge_filtering = self.filtering["edge_filtering"]
                    if not isinstance(edge_filtering, list):
                        edge_filtering = [str(edge_filtering)]                 
                
                result["filtering"]["edges_lookup"] = list_of_dicts_to_dict_of_lists(edges, keys=edge_filtering, unique=True, sort=True)

                # nodes
                node_filtering = None
                if "node_filtering" in self.filtering:
                    node_filtering = self.filtering["node_filtering"]
                    if not isinstance(node_filtering, list):
                        node_filtering = [str(node_filtering)]
                
                result["filtering"]["nodes_lookup"] = list_of_dicts_to_dict_of_lists(nodes, keys=node_filtering, unique=True, sort=True)


            # trying to resolve "edges" and "nodes" placeholders in the data dict and handle defaults 
            if self.dataTables:
                tables = self.dataTables           
                for key in tables:
                    table = tables[key]

                    if "data" not in table:
                        table["data"] = "edges"
                    if "data" in table and str(table["data"]) == "edges":
                        if key == "bottom":
                            table["data"] = edges
                        elif key in ["left", "right"]:
                            table["data"] = [edge for edge in edges if "table" in edge and edge["table"] == key]
                    elif "data" in table and str(table["data"]) == "nodes":
                        if key == "bottom":
                            table["data"] = nodes
                        elif key in ["left", "right"]:
                            table["data"] = [node for node in nodes if "table" in node and node["table"] == key]
                    elif "data" in table and type(table["data"]).__name__ == "DataFrame":
                            table["data"] = dict_of_lists_to_list_of_dicts(table["data"].to_dict(orient="list"))
                    if "columns" not in table:
                        table["columns"] = [key for key in table["data"][0].keys() if key != "table"]

                result["tables"] = tables


            #sankey
            if self.sankey:
                result["sankey"] = {
                    "data": [
                        {
                            "node": list_of_dicts_to_dict_of_lists(nodes, keys=["label"]),
                            "link": list_of_dicts_to_dict_of_lists(edges, keys=["source", "target", "value"])
                        }
                    ]
                }

            if self.startAnimation:
                result["startAnimation"] = {
                    "zoom_factor": self.startAnimation.get("zoom_factor", None),
                    "duration_ms": self.startAnimation.get("duration_ms", None),
                }

            if self.title:
                result["title"] = self.title
            
            return result    

    class Nodes(BaseDictable):
        def __init__(self):
            super().__init__()
            self.scaling = {}
            self.font = {}

        def set_font(self, face:str=None) -> Self:
            self._update_dict_with_locals(self.font, locals())
            return self

        def set_scaling(self, min:int=None, max:int=None, label:bool=None) -> Self:
            self._update_dict_with_locals(self.scaling, locals())
            return self
        
    class Edges(BaseDictable):
        def __init__(self):
            super().__init__()

            self.arrows:str = None
            self.arrowStrikethrough:bool = None

            self.font = {}
            self.color = {}
            self.smooth = {}

        def set_font(self, face:str=None) -> Self:
            self._update_dict_with_locals(self.font, locals())
            return self

        def set(self, arrows:str=None, arrowStrikethrough:bool=False) -> Self:
            if arrows: self.arrows = arrows
            if arrowStrikethrough is not None: self.arrowStrikethrough = arrowStrikethrough

            return self
        
        def set_color(self, color:str=None, highlight:str=None, hover:str=None, inherit:str=None, opacity:float=None, dashes:bool=None) -> Self:
            self._update_dict_with_locals(self.color, locals())
            return self

        def set_smooth(self, enabled:bool=None, type:str=None, roundness:float=None) -> Self:
            self._update_dict_with_locals(self.smooth, locals())
            return self

    class Physics(BaseDictable):
        def __init__(self):
            super().__init__()

            self.enabled:bool = None
            self.minVelocity:float = None
            self.maxVelocity:float = None

            self.barnesHut = {}
            self.stabilization = {}

        def set(self, enabled:bool=None, minVelocity:float=None, maxVelocity:float=None) -> Self:
            if enabled is not None: self.enabled = enabled
            if minVelocity: self.minVelocity = minVelocity
            if maxVelocity: self.maxVelocity = maxVelocity

            return self

        def set_barnesHutKV(self, key:str, value):
            """
            You can use set_barnesHut function instead, if you dont know parameters names
            """
            self.barnesHut.update({ key: value })

        def set_barnesHut(self, theta:float=None, gravitationalConstant:int=None, centralGravity:float=None, springLength:int=None, springConstant:float=None, damping:float=None, avoidOverlap:float=None) -> Self:
            self._update_dict_with_locals(self.barnesHut, locals())
            return self

        def set_stabilization(self, enabled:bool=None, iterations:int=None, updateInterval:int=None, onlyDynamicEdges:bool=None, fit:bool=None) -> Self:
            self._update_dict_with_locals(self.stabilization, locals())
            return self

    


    