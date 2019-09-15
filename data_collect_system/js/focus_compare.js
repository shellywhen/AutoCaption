function load_focus_compare(){
  var color = ['red','blue','#7570b3']
  var name = [{name:"focus"},{name:"compare"},{name:"clear"}]
  var focus_compare_svg = d3.select("#focus_compare")

  var width = parseFloat(focus_compare_svg.attr("width"))
  var height = parseFloat(focus_compare_svg.attr("height"))

  var button_width = width
  var button_height = height / 10

  var button_left = (width - button_width ) / 2
  var button_top = (height - (name.length * 2 - 1) * button_height) / 2

  var margin_rate = 0.1
  var button_margin = {left: button_width * margin_rate, right: button_width * margin_rate, top: button_height * margin_rate, bottom: button_height * margin_rate}

  var button = focus_compare_svg.selectAll(".button")
      .data(name)
      .enter()
      .append("g")
      .attr("id", function(d){
        return d.name;
      })
      .attr("class", "button")
      .attr("transform", function(d,i){
        this_top = button_top + i * 2 * button_height
        console.log(this_top)

        return "translate(" + button_left + "," + this_top + ")"
      })
  button.append("rect")
      .attr("width", button_width - button_margin.left - button_margin.right)
      .attr("height", button_height - button_margin.top - button_margin.bottom)
      .attr("x", button_margin.left)
      .attr("y", button_margin.top)
      .attr("stroke", function(d, i ){
        return color[i]
      })

  var font_size = button_height/4
  button.append("text")
      .attr("text-anchor", "middle")
      .attr("x", button_width/2)
      .attr("y", button_height/2 + font_size/4)
      .attr("font-size", font_size)
      .text(function(d){
        return d.name
      })

  focus_compare_svg.select("#focus")
      .classed("select", true)
      .on("click", function(d){
        console.log("click on focus")
        if (current_select != 'focus')
        {
          current_select = 'focus'
        }
        refresh_focus_compare()
      })
  focus_compare_svg.select("#compare")
      .on("click", function(d){
        if (current_select != "compare")
        {
          current_select = "compare"
        }
        refresh_focus_compare()
      })
  focus_compare_svg.select("#clear")
      .on("click", function(d){
        reload_selection()
      })

  focus_compare_svg.append("text")
      .attr("id", "count_number")
      .text("第 " + total_number +" 个图表：")
      .attr('y', font_size)

}

function refresh_focus_compare(){
  var focus = d3.select("#focus")
  var compare = d3.select("#compare")
  var num_of_none = 0
  if (current_select === "focus")
  {
    focus.classed("select", true)
    compare.classed("select", false)
  }
  else if (current_select === "compare")
  {
    focus.classed("select", false)
    compare.classed("select", true)
  }
  
}
