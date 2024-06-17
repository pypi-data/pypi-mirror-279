# Packege-specific options

These options are extra (compared to vis.js) options provided by the pyvisjs package.
They can be set up using config functions of the `options.pyvisjs` object

<table>
<thead>
    <tr>
        <td>Config functions</td>
    </tr>
    <tr>
        <th>Option name</th>
        <th>Configuration function</th>
        <th>Effect</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>General settings</td>
        <td><code>set</code></td>
        <td>So far you can only set up <code>Title</code> here</td>
    </tr>
    <tr>
        <td><a href="#filtering">Filtering</a></td>
        <td><code>set_filtering</code></td>
        <td>Adds a <a href="https://tom-select.js.org/" target="_blank">Tom-Select</a> control above the Network area</td>
    </tr>
    <tr>
        <td><a href="#data-tables">Data Tables</a></td>
        <td><code>set_dataTable</code></td>
        <td>Adds up to 3 <a href="https://datatables.net/" target="_blank">DataTable</a> controls just below the Network area</td>
    </tr>
    <tr>
        <td><a href="#sankey-chart">Sankey Chart</a></td>
        <td><code>set_sankey</code></td>
        <td>Adds a <a href="https://plotly.com/python/sankey-diagram/" target="_blank">Sankey</a> diagram below the Network area</td>
    </tr>
</tbody>
</table>


## Filtering

Filtering adds a <a href="https://tom-select.js.org/" target="_blank">Tom-Select</a> control above the Network area
which allows filtering the Network by Node or Edge attributes.  
You can enable and configure filtering using `set_filtering` function of the `options.pyvisjs` object:
``` py
from pyvisjs import Network, Options

options = Options("800px", "1300px")
options.pyvisjs.set_filtering(
        enable_highlighting=True,
        node_filtering=["file_type", "file_ext", "label"],
        edge_filtering=[],
        dropdown_auto_close=True,
    )

net = Network(options=options)
```

### How it works
By default, i.e. passing no arguments to the `options.pyvisjs.set_filtering()`, the Tom-Select control will be added above the Network area 
and ALL Node and Edge distinct attribute values will be added to the drop-down list. Attribute values will be visually groupped by node.`attribute_name` or edge.`attribute_name` correspondingly. Selection of the item from the list will 
filter the corresponding Network elements. Filtering in this case means - hide all other elements, except selected. By defailt, drop-down list will stay open allowing to select multiple items.  
(<a href="../examples/filtering-example/" target="blank_">see example</a>)


### Parameters

<table>
<thead>
    <tr>
        <th width=300px>Setting</th>
        <th>Description</th>
        <th>Type</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td><code>enable_highlighting</code></td>
        <td>
``` py
from pyvisjs import Network, Options

options = Options("800px", "1300px")
options.pyvisjs.set_filtering(
        enable_highlighting=True,
        node_filtering=["file_type", "file_ext", "label"],
        edge_filtering=[],
        dropdown_auto_close=True,
    )

net = Network(options=options)
```
        </td>
        <td><code>bool</code></td>
    </tr>

    <tr>
        <td><code>node_filtering</code></td>
        <td></td>
        <td><code>list</code></td>
    </tr>

    <tr>
        <td><code>edge_filtering</code></td>
        <td></td>
        <td><code>list</code></td>
    </tr>

    <tr>
        <td><code>dropdown_auto_close</code></td>
        <td></td>
        <td><code>bool</code></td>
    </tr>
</tbody>
</table>

## Data Tables

## Sankey Chart