function load_bar_chart(){

    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = document.getElementById("visualization").clientWidth - margin.left - margin.right - margin.left - margin.right,
        height = document.getElementById("visualization").clientHeight - margin.left - margin.right - margin.top - margin.bottom;

    // set the ranges
    var x = d3.scaleBand()
            .range([0, width])
            .padding(0.1);
    var y = d3.scaleLinear()
            .range([height, 0]);

    // append the svg object to the body of the page
    // append a 'group' element to 'svg'
    // moves the 'group' element to the top left margin
    d3.select("#visualization").select("svg")
        .remove()

    var svg = d3.select("#visualization").append("svg")
        .attr("id", "visualization")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // get the data




    // format the data
    data.forEach(function(d) {
        d.value = +d.value;
    });

    // Scale the range of the data in the domains
    x.domain(data.map(function(d) { return d.name; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);

    // append the rectangles for the bar chart
    data_length = data.length
    max_value = 0
    for ( var i = 0 ; i < data_length; i ++ ){
      if (max_value < data[i].value){
        max_value = data[i].value
      }
    }
    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.name); })
        .attr("width", x.bandwidth())
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) { return height - y(d.value); })
        .attr("quantity0", function(d){
          return d.value/max_value
        })
        .attr("category0", function(d){
          var data_length = data.length
          for (var i = 0; i < data_length; i ++ ){
            if (data[i].value === d.value){
              return i
            }
          }
        })
        .attr("fill", function(d,i){
            var color = d3.color(i);
            console.log(color)
            return color;
        })

    // add the x Axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // add the y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

}
function build_data(name, value)
{
    select_thing = []
    my_assert(name.length === value.length, 'The length of the name did not match that of value!')
    var length = name.length;
    var data = new Array(length);
    for (var i = 0 ; i < length; i ++ ){
        data[i] = {"name": name[i], "value": value[i], "id": i}
        select_thing[i] = false;
    }
    console.log(select_thing)
    // print(data)
    return data;

}
function my_assert(a,b){
    print(a)
    if (!a){
        print(b)
    }
}
function download(){

 var html = d3.select("svg")
  .attr("version", 1.1)
  .attr("xmlns", "http://www.w3.org/2000/svg")
  .node().parentNode.innerHTML;
  //console.log(html);
 var imgsrc = 'data:image/svg+xml;base64,'+ btoa(html);
 var img = '<img src="'+imgsrc+'">';
 d3.select("#svgdataurl").html(img);

}
