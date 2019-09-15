function initialize(){
  init_div()
  init_vis()
  init_svg()
  load_focus_compare()
  init_show_sentence()
}
function init_div(){
  var all = d3.select("#all")
  var width = $('#all')[0].clientWidth
  var height = $('#all')[0].clientHeight
  console.log("height", height)
  console.log("width", width)
  var left_percent = height * 1.1 / width * 100
  console.log(left_percent + "%")

  all.append("div")
      .attr("id", 'visualization_father')
      .attr("class", 'kuang')
      .style("position", "absolute")
      .style("top", '1%')
      .style("left", "1%")
      .style("width", left_percent + '%')
      .style("height", '98%')

  all.append("div")
      .attr("id", 'sentences_div')
      .attr("class", 'kuang')
      .style("position", "absolute")
      .style("top", '1%')
      .style("left", left_percent + 2 + '%')
      .style("width", 96 - left_percent + '%')
      .style("height", '58%')
      .style("overflow", "auto")


  var selected_sentences_div = all.append('div')
      .attr("id", 'selected_sentences_div')
      .attr('class', 'kuang')
      .style('position', 'absolute')
      .style('top', '60%')
      .style('height', '39%')
      .style('overflow','auto')
      .style("left", left_percent + 2 + '%')
      .style("width", 96 - left_percent + '%')
      .style("overflow", "auto")


  selected_sentences_div.append('button')
      .attr('id', 'submit')
      .text('Submit')

  selected_sentences_div.append('button')
      .attr('id', 'skip')
      .text('clear')
      .on('click',function(d){
        selected_sentences = []
        update_selected_sentence(selected_sentences)

      })

  d3.select("#submit")
      .on("click", function(d){
        if (selected_sentences.length === 0 )
        {
          reload_every_thing()
        }
        else{
          var svg_string = get_svg_string()
          var data_string = JSON.stringify(data_json)
          var sentences_string = JSON.stringify(selected_sentences)
          console.log(svg_string)
          console.log(data_string)
          console.log(sentences_string)
          send_data = {
            user_name: user_name,
            total_number: total_number,
            svg_string: svg_string,
            data_string: data_string,
            sentences_string: sentences_string,
            major_name: major_name,
            second_name: second_name
          }
          submit_answer(send_data)
          total_number ++
          var count_number = d3.select('#count_number')
            .text("第 " + total_number +" 个图表：")
          reload_every_thing()

        }
      })
}
function get_svg_string(){
  var svg = d3.select("#visualization_father").select("#visualization")
        .selectAll("svg")

  svg.select(".brush")
      .remove()

  var svg_string = svg._groups[0][0].outerHTML
  return svg_string
}

let a = function(){
  this.name = "newnewnew"
  console.log(this.name)


}

a.prototype.b = function(){
  console.log("hahhahaha")
}

function init_vis(){

  var width = document.getElementById("visualization_father").clientWidth
      height = document.getElementById("visualization_father").clientHeight

  var content_size = width

  var margin_rate = 0.025

  if (content_size > height){
      content_size = height
  }
  margin_size = content_size * margin_rate
  content_size = content_size * ( 1 - 2 * margin_rate)

  top_value = margin_size
  left_value = width - content_size - margin_size
  var visualization = d3.select("#visualization_father").append("div")
      .attr("id", "visualization")
      .attr("class", "kuang") // 这一行是要被注释掉的，谢谢，框你大爷。
      .style("position", "absolute")
      .style("left", left_value + "px")
      .style("top", top_value + "px")
      .style("width", content_size + 'px')
      .style("height", content_size + 'px')

  var focus_compare = d3.select("#visualization_father")
      .append("svg")
      .attr("id", "focus_compare")
      .attr("width", left_value)
      .attr("height", height)

}
function init_svg()
{
    var width = document.getElementById("visualization").clientWidth
        height = document.getElementById("visualization").clientHeight

    var vasulization = d3.select("#visualization")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("xmlns", "http://www.w3.org/2000/svg")
    reload_every_thing()
}
