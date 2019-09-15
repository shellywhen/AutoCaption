function load_show_choose(){
    var margin = {top: 20, right: 20, bottom: 20, left: 20 }
    var width = document.getElementById("show_choose").clientWidth - margin.left - margin.right
    var height = document.getElementById("show_choose").clientHeight - margin.top - margin.bottom
    // console.log("The width is: " + document.getElementById("show_choose").clientWidth)
    print(width)
    print(height)
    // console.log("The height is: " + document.getElementById("show_choose").clientHeight)

    console.log("open js")
    var svg = d3.select("#show_choose").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("w", width)
        .attr("h", height)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.select("rect")
        .on("click",function(d){
            print("d")
        })
        // .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    console.log("Now the select thing is: ", select_thing)
    var select_bar_height = height/10;
    var select_bar_width = width;
    var select_bar_container = svg.append("g")
        .attr("class", "select")
        .attr("transform", "translate(0," + (height - select_bar_height)/2 + ")")

    console.log("length of select-thing:", select_thing.length)
    if (select_thing.length > 0 ){
        select_bar_width = width/(select_thing.length)
        select_bar_container.select("select_bar")
            .data(select_thing)
        .enter()
            .append("rect")
            .attr("height", select_bar_height)
            .attr("width", function(d,i){
                return select_bar_width * i
            })
            .attr("x",function(d,i){
                return i * select_bar_width;
            })
            .attr("fill", function(d){
                if (d){
                    return "red"
                }
                else {
                    return "blue"
                }
            })

    }
}

function print(content){
    console.log(content)
}
