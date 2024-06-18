import os
from .base_dictable import BaseDictable
from .utils import open_file, save_file
from .node import Node
from .edge import Edge
from .options import Options
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import List, Dict, Self
from pathlib import Path

class Network(BaseDictable):
    def __init__(self, name="Network", nodes:List[Node]=None, edges:List[Edge]=None, options:Options=None):
        only_use_data_attr = lambda attr: attr == "_data"
        super().__init__(attr_filter_func=only_use_data_attr)
        self.name = name
        self._initialize_data(nodes, edges, options)
        self.env = Environment(
            loader=PackageLoader("pyvisjs"),
            autoescape=select_autoescape()
        )
        self.env.globals.update(isinstance=isinstance)

    @property
    def options(self) -> Options:
        opt = self._data["options"]   
        return opt if isinstance(opt, Options) else None
    
    @options.setter
    def options(self, val:Options):
        self._data["options"] = val
    
    @property
    def nodes(self) -> List[Node]: 
        return self._data["nodes"]  
    
    @property
    def edges(self) -> List[Edge]: 
        return self._data["edges"]  

    def _initialize_data(self, nodes:List[Node]=None, edges:List[Edge]=None, options:Options=None):
        default_data = {"nodes": [], "edges": [], "options": {}}

        if nodes:
            default_data.update({
                "nodes": nodes,
            })

        if edges:
            default_data.update({
                "edges": edges,
            })

        if options:
            default_data["options"] = options

        self._data = default_data

    def __repr__(self):
        return f"Network(\'{self.name}\')"
    
    def add_node(self, id:str, label=None, color=None, shape="dot", size=None, **kwargs) -> int:

        index = None
        search_result = [node for node in self.nodes if node.id == str(id)]
        if not search_result:
            index = len(self.nodes)
            self.nodes.append(Node(id, label, color, shape, size, **kwargs))
        else:
            index = self.nodes.index(search_result[0])
        
        return index

    def add_edge(self, fr0m:str, to:str, **kwargs) -> int:

        self.add_node(fr0m)
        self.add_node(to)

        index = None
        search_result = [edge for edge in self.edges if edge.start == str(fr0m) and edge.end == str(to)]
        if not search_result:
            index = len(self.edges)
            self.edges.append(Edge(fr0m, to, **kwargs))
        else:
            found_edge = search_result[0]
            found_edge.update(**kwargs)
            index = self.edges.index(found_edge)
        
        return index


    def to_dict(self):
        return super().to_dict()["_data"]

    def show(self, file_name:str=None):
        if file_name:
            self.render(open_in_browser=True, output_filename=file_name)
        else:
            self.render(open_in_browser=True)

    def render(self, open_in_browser=False, save_to_output=False, output_filename="default.html"):
        network_dict = self.to_dict()

        pyvisjs_dict = self.options.pyvisjs.for_js() if self.options else {}
        jinja_dict = self.options.pyvisjs.for_jinja(network_dict["edges"], network_dict["nodes"]) if self.options else {}
   
        template_filename = "container-template.html" if ("filtering" in jinja_dict or "tables" in jinja_dict) or "sankey" in jinja_dict else "basic-template.html"

        html_output = self.env \
            .get_template(template_filename) \
            .render(
                data=network_dict,
                pyvisjs=pyvisjs_dict, # available in the html file as a variable
                jinja=jinja_dict, # only used in jinja injections
            )

        if save_to_output or open_in_browser:
            file_path = save_file(output_filename, html_output)

        if open_in_browser:
            open_file(file_path)

        return html_output

    @classmethod
    def from_transactions(cls, meta:Dict, options:Options=None) -> Self:
        net = Network(options=options) if options else Network()
        edges_mapping = {}

        if "fields" in meta:
            fields = meta["fields"]

            # edges in fields
            if isinstance(fields, dict) and "edges" in fields:
                edges = fields["edges"]
                if isinstance(edges, list):
                    for edge in edges:
                        edges_mapping[edge] = (edge if edge != "from" else "fr0m")
                if isinstance(edges, dict):
                    for key, value in edges.items():
                        edges_mapping[key] = (value if value != "from" else "fr0m")

            # (todo) nodes in fields

        if "data" in meta:
            data = meta["data"]

            # list of dicts
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                first_row = data[0]

                if edges_mapping and "from" not in edges_mapping and "from" in first_row:
                    edges_mapping["from"] = "fr0m"
                if edges_mapping and "to" not in edges_mapping and "to" in first_row:
                    edges_mapping["to"] = "to"

                # if user doesnt provide fields we add all the fields to the edges
                if not edges_mapping:
                    columns = [col for col in first_row]
                    for col in columns:
                        edges_mapping[col] = col if col != "from" else "fr0m"

                for row in data:
                    edge_kwargs = {}
                    for key, value in edges_mapping.items():
                        edge_kwargs[value] = row[key]

                    if edge_kwargs:
                        net.add_edge(**edge_kwargs)

            # (todo) Dict of lists

        return net


    @classmethod
    def from_dir(cls, dir:str, options:Options=None, only_first_level=False) -> Self:
        net = Network(options=options) if options else Network()

        for path, subdirs, files in os.walk(dir):
            if ".venv" not in path \
                and "__pycache__" not in path \
                and "cachedir.tag" not in path \
                and ".pytest_cache" not in path \
                and ".git" not in path \
                and "node_modules" not in path \
                and "egg-info" not in path:
                curr_dir = (Path(os.getcwd()).stem).replace("-", "\n")
                net.add_node(
                    id = path, 
                    label = curr_dir, 
                    shape = "circle",
                    color = "orange",
                    font = {"color": "black"},
                    file_type = "dir",
                    file_ext = "",
                )

                for name in subdirs:
                    full_name = os.path.join(path, name)
                    net.add_node(
                        id = full_name, 
                        label = name, 
                        shape = "circle",
                        color = "#4eba3f",
                        font = {"color": "black"},
                        file_type = "dir",
                        file_ext = "",
                    )            
                    net.add_edge(path, full_name, label=f"dir:{subdirs.index(name)}")

                for name in files:
                    full_name = os.path.join(path, name)
                    ext = Path(name).suffix

                    if ext == ".py":
                        (color, font_color) = ("#54bede", "black")
                    elif ext == ".md":
                        (color, font_color) = ("#F02B4B", "black")
                    elif ext == ".txt":
                        (color, font_color) = ("#DF7DEC", "black")
                    elif ext == ".html":
                        (color, font_color) = ("#8f2d56", "white")
                    elif ext == ".js":
                        (color, font_color) = ("#da7422", "black")
                    else:
                        (color, font_color) = (None, "black")

                    net.add_node(
                        id = full_name, 
                        label = name, 
                        shape = "box",
                        color = color,
                        file_type = "file",
                        file_ext = ext,
                        font = {"color": font_color},
                    )            
                    net.add_edge(path, full_name, label=f"file:{files.index(name)}")

            if only_first_level:
                break
            
        return net
            