// ---------------- SANKEY START ----------------------
init_sankey({{ jinja.get("sankey", {})|tojson }})

function init_sankey(fig) {

    var data = {
        type: "sankey",
        domain: {
            x: [0,1],
            y: [0,1]
        },
        orientation: "h",
        valueformat: ".0f",
        valuesuffix: "TWh",
        node: {
            pad: 15,
            thickness: 15,
            line: {
                color: "black",
                width: 0.5
            },
                label: fig.data[0].node.label,
                //color: fig.data[0].node.color
            },

        link: {
            source: fig.data[0].link.source,
            target: fig.data[0].link.target,
            value: fig.data[0].link.value,
            //label: fig.data[0].link.label
        }
    }

    var data = [data]

    var layout = {
        title: "Sankey chart",
        width: 1118,
        height: 772,
        font: {
            size: 10
        }
    }

    Plotly.newPlot('myDiv', data, layout)
};
// ---------------- SANKEY END ----------------------