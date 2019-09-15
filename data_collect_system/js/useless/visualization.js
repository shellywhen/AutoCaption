function load_line_chart(){
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = document.getElementById("visualization").clientWidth - margin.left - margin.right - margin.left - margin.right,
        height = document.getElementById("visualization").clientHeight - margin.left - margin.right - margin.top - margin.bottom;

    // 7. d3's line generator
    // apply smoothing to the line

    // 8. An array of objects of length N. Each object has key -> value pair, the key being "y" and the value is a random number

    var name = ["Aasdf","Bfff","C","D","E"]
    // console.log(name)
    var value = new Array(123, 123, 3, 234, 12)
    var data = build_data(name, value);


    // var xScale = d3.scaleLinear()
    //     .domain([0, data.length - 1]) // input
    //     .range([0, width]); // output

    var xScale = d3.scaleBand()
        .range([0, width])
        .domain(data.map(function(d) { return d.name; }))
        .padding(1)

    var yScale = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return d.value; })]) // input
        .range([height, 0]); // output

    var line = d3.line()
        .x(function(d, i) { return xScale(d.name); }) // set the x values for the line generator
        .y(function(d) { return yScale(d.value); }) // set the y values for the line generator
        .curve(d3.curveMonotoneX)


    // 1. Add the SVG to the page and employ #2
    var svg = d3.select("#visualization").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");



    // var rect =  svg.append("rect")
    //     .attr("width", width)
    //     .attr("height",height)
    // console.log(rect)

    // 3. Call the x axis in a group tag
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

    // 4. Call the y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft

    // 9. Append the path, bind the data, and call the line generator
    svg.append("path")
        .datum(data) // 10. Binds data to the line
        .attr("class", "line") // Assign a class for styling
        .attr("d", line) // 11. Calls the line generator
        .attr("fill", "none")
        .attr("stroke","#ffab00")
        .attr("stroke-width",3)

    // 12. Appends a circle for each datapoint
    svg.selectAll(".dot")
        .data(data)
    .enter().append("circle") // Uses the enter().append() method
        .attr("class", "dot") // Assign a class for styling
        .style("cx", function(d, i) { return xScale(d.name) })
        .style("cy", function(d) { return yScale(d.value) })
        .style("fill", "blue")
        .attr("r", 5);

    window._xScale = xScale;

    svg.selectAll("circle")
        .attr("class", "dot")
        .on("click",Select_element)

}
function Select_element(d){
    var this_circle = d3.select(this)
    if (this_circle.classed("choose")){
        this_circle.classed("choose", false)
        select_thing[d.id] = false;

    }
    else{
        this_circle.classed("choose", true)
        select_thing[d.id] = true;
    }
    console.log(select_thing)

}
