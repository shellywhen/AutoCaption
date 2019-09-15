function storyline_view(){
    var color = ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854']
    var time_happen = new Array(7)
    time_happen[0] = new Array( -1,     -1,     11678,  -1,     -1)
    time_happen[1] = new Array( 6931,   -1,     12406,  -1,     -1)
    time_happen[2] = new Array( 5335,   -1,     13804,  -1,     -1)
    time_happen[3] = new Array( -1,     8948,   -1,     15159,  36170)
    time_happen[4] = new Array( 7892,   8915,   -1,     15079,  36132)
    time_happen[5] = new Array( 5789,   9113,   -1,     13768,  36053)
    time_happen[6] = new Array( -1,     32207,  -1,     35387,  45008)
    console.log(time_happen)

    event_name = ["Asteroids airbursts","Asteroids hit the ocean","Pressure Wave arrive sea level","Shock Wave Arriving Seabed","Water Jet and Rim Waves"]
    

    var margin = {top: 20, right: 20, bottom: 20, left: 20 }
    var width = document.getElementById("story_line").clientWidth - margin.left - margin.right
    var height = document.getElementById("story_line").clientHeight - margin.top - margin.bottom   
    console.log("open js")
    var svg = d3.select("#story_line").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    line_x = [0,1,2,3,4,5,6];
    text = ["45 degre, d=100m, Airburst=0km"]
    var line_container = svg.selectAll(".line_container")
        .data(line_x)
        .enter().append("g")
        .attr("class","line_container")
        .attr("transform",function(d,i){
            transform = "translate(0," + height * ( d + 1.5 ) / 8 + ")"
            return transform 
        })
    line_container.append("rect")   
        .attr("class","line")
        .attr("width",width )
        .attr("height",height/100)

    // line_container.append("g")
    //     .attr("class","description")
    //     .attr("width",width * 0.15)
    //     .attr("height",height/10)
    //     .attr("transform",function(d,i){
    //         height_transform = - height / 20
    //         transform = "translate(" + width * 0.825 + "," + height_transform + ")"
    //         return transform;
    //     })

    for (var i = 0 ; i < 5 ; i ++ ){
        line_container.append("rect")
            .attr("width", width/30)
            .attr("height", height/10)
            .attr("transform", function(d){
                console.log(time_happen[d][i])
                if (time_happen[d][i] < 0 ){
                    return "translate("+ 2 * width +",0)";
                }
                else{
                    var x_change = time_happen[d][i] * width / 50000;
                    var y_change = - height/20;
                    return "translate(" + x_change + "," + y_change + ")";
                }
            })
            .attr("fill", color[i])
    }
        

        // .attr("stroke-width", 1 )
        // .attr("fill","#ddd")


    // airbursts 0 ,  stroke_arrive_seabed, hit ocean , 
}
