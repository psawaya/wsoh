document.addEventListener("DOMContentLoaded", function () {
    var w = 960,
        h = 960,
        format = d3.format(",d");

    var pack = d3.layout.pack()
        .size([w - 4, h - 4])
        .children(function(d) { return d.group; })
        .value(function(d) { return 100; });

    var vis = d3.select("#chart").append("svg:svg")
                                 .attr("width", w)
                                 .attr("height", h)
                                 .attr("class", "pack")
                                .append("svg:g");

    var infoDisplay = document.getElementById("info");

    function renderGraph(json) {
        var selection = vis.data([{ group: json }])
                        .selectAll("g.node")
                        .data(pack.nodes, function(d) {
                            if (d.name)
                                return d.name;
                            // XXX if group use ID
                            return Math.random();
                        });

        selection.exit().remove();

        var newNodes = selection
            .enter().append("svg:g")
            .attr("class", function(d) { return d.group ? "node" : "leaf node"; })
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

        newNodes.append("svg:circle")
            .attr("r", function(d) { return d.r; });

        newNodes.filter(function(d) { return !d.group; }).append("svg:text");

        newNodes.filter(function(d) { return !d.group; })
            .on("mouseover", function(d, i) {
                infoDisplay.innerHTML = d.name;
            });

        var textAnchors = vis.selectAll("g.node").selectAll("text");

        textAnchors.attr("text-anchor", "middle")
            .attr("dy", ".3em")
            .text(function(d) {
                return d.name.substring(0, d.r / 3);
            })
    }

    d3.json("sample.json", renderGraph);

    setTimeout(function(){
        // renderGraph([{
        //     group: [
        //         {
        //             name:"hi",
        //         },
        //         {
        //             name: "blah",
        //         },
        //     ],
        // }]);
        d3.json("http://localhost:5000/fetch/9b24b06a-b51a-11e0-b0ec-e0f8473df42e/8",renderGraph);
    }, 1000);
}, true);
