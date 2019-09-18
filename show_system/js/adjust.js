var DRAG_HANDLER = 0
var INIT_HEIGHT = 0
var INIT_Y = 0
var TIME_LAST = 0
var TIME_NOW = 0
let highLightTableColor = '#fec44f'
let highLightRectColor = '#d95f0e'

// global
let xAxis
let yAxis
let legend
let is_vertical = true
let tick_value = []
let tick_value_x = []
let g_xAxis
let g_yAxis
let g_legend
let element_list

let highLightText = function (data_pack) {
  console.log("data_pack", data_pack)
  let textCollection = data_pack.data.text_collection
  let viewBox = d3.select('#visualization').select('svg').attr("viewBox").split(" ")


  let rel_width = parseFloat(viewBox[2])
  let rel_height = parseFloat(viewBox[3])
  is_vertical = data_pack.data.is_vertical

  d3.select('#annotationDiv').select('svg')
    .attr("viewBox", d3.select('#visualization').select('svg').attr("viewBox"))

  let this_svg = d3.select('#annotationDiv').select('svg')

  let g = d3.select('#annotationDiv').select('svg').append('g').attr('id', 'annotation')

  // let textCollection = {
  //   'yAxis': {'text': [{'x': 30, 'y': 20, 'w': 20, 'h': 10 }, {'x': 30, 'y': 80, 'w': 20, 'h': 10 }, {'x': 30, 'y': 140, 'w': 20, 'h': 10 }]},
  //   'xAxis': {'text': [{'x': 30, 'y': 500, 'w': 20, 'h': 10 }, {'x': 50, 'y': 500, 'w': 20, 'h': 10 }, {'x': 70, 'y': 500, 'w': 20, 'h': 10 }]},
  //   'legend': {'text': [{'x': 300, 'y': 10, 'w': 20, 'h': 10 }, {'x': 300, 'y': 30, 'w': 20, 'h': 10 }, {'x': 300, 'y': 5, 'w': 20, 'h': 10 }]},
  //   'unit': {'text': [{'x': 5, 'y': 10, 'w': 5, 'h': 30 }, {'x': 300, 'y': 500, 'w': 30, 'h': 5 }]},
  //   'title': {'text': [{'x': 100, 'y': 30, 'w': 100, 'h': 20 }]},
  //   'element': [] // 这里还要有元素的位置
  // }
  let colorList = ['#66c2a5','#fc8d62','#8da0cb', 'lightskyblue', 'lightpink']
  let attributeList = ['xAxis', 'yAxis', 'legend']
  let i = 0
  xAxis = textCollection.xAxis.text
  x_axis_y = xAxis[0].y
  yAxis = textCollection.yAxis.text
  y_axis_x = yAxis[0].x + yAxis[0].w

  tick_num = yAxis.length
  tick_value = new Array()
  for(let j = 0; j < tick_num; j ++){
    tick_value[j] = yAxis[j].y + yAxis[j].h / 2
  }
  console.log("tick_value", tick_value)

  tick_num = xAxis.length
  tick_value_x = new Array()
  for(let j = 0; j < tick_num; j ++){
    tick_value_x[j] = xAxis[j].x + xAxis[j].w / 2
  }
  console.log("tick_value x", tick_value_x)





  for (let attrName of attributeList) {
    let attribute_class = `g_${attrName}`
    let canvas = g.append('g').attr('id', attribute_class)

    let bbox_edge = 3

    canvas.selectAll("." + attribute_class)
      .data(textCollection[attrName].text)
      .enter()
      .append("rect")
      .attr('stroke', colorList[i])
      .attr('fill', colorList[i])
      .attr("class", "text_bbox")
      .attr("x", d => d.x - bbox_edge)
      .attr("y", d => d.y - bbox_edge)
      .attr("id", function(d, i){
        return attrName + "_" + i
      })
      .attr("width", d => d.w + 2 * bbox_edge)
      .attr("height", d => d.h + 2 * bbox_edge)
      .style('stroke-width', 3)
      // .style('stroke-opacity', 1)


    // for (let item of textCollection[attrName].text) {
    //   let x1 = item.x, x2 = item.x + item.w, y1 = item.y, y2 = item.y + item.h
    //   canvas.append('polygon')
    //     .attr('points', `${x1},${ y1} ${x2},${y1} ${x2},${y2} ${x1},${y2}`)
    //     .datum(item.content)
    //     .style('stroke-width', 3)
    //     .style('stroke', colorList[i])
    //     .style('fill-opacity', 0.1)
    //     .style('fill', colorList[i])
    //     .style('stroke-opacity', 1)
    //     .classed(`annotation_${attrName}`, true)
    //     .classed('annotation_normal', true)
    //     .classed('annotation_highlight', false)
    // }
    i++
  }

  g.append("line")
    .attr("id", "x_auxiliary_line")
    .attr("class", "auxiliary")
    .attr("x1", 0)
    .attr("y1", x_axis_y)
    .attr("x2", 0)
    .attr("y2", 0)
    // .attr("stroke-width", 2)
    .attr("stroke", colorList[0])
    .attr("opacity", 0)

  g.append("line")
    .attr("id", "y_auxiliary_line")
    .attr("class", "auxiliary")
    .attr("x1", y_axis_x)
    .attr("y1", 0)
    .attr("x2", 0)
    .attr("y2", 0)
    // .attr("stroke-width", 5)
    .attr("stroke", colorList[1])
    .attr("opacity", 0)

  g.append("circle")
    .attr("id", "auxiliary_circle")
    .attr("class", "auxiliary_circle")
    .attr("cx", 0)
    .attr("cy", x_axis_y)
    .attr("fill", colorList[2])
    .attr("r", 5)
    .attr("opacity", 0)

  // 添加一个透明大矩形：
  g.append("rect")
    .attr("width", rel_width)
    .attr("height", rel_height)
    .attr("fill", "black")
    .attr("opacity", 0.0)
    .on("mousemove", function(d){
      var coordinates = d3.mouse(this)
      let x = coordinates[0]
      let y = coordinates[1]
      // console.log(coordinates)
      // Draw_line(x, y)
      // highlight_y_tick(y)
      // highlight_x_tick(x)

    })
    .on("mouseover", function(d){

    })
    .on("mouseout", function(d){

    })

  g_xAxis = d3.select("#g_xAxis")
  g_yAxis = d3.select("#g_yAxis")
  g_legend = d3.select("#g_legend")

  element_list = data_pack.data.elements
  g.selectAll(".element")
      .data(element_list).enter()
      .append('rect')
      .attr('x', d => d.x)
      .attr('y', d => d.y)
      .attr('width', d => d.w)
      .attr('height', d => d.h)
      .style('opacity', 0)
      .style('fill', "red")
      .attr('id', (d, i) => "element_" + i)
      .classed('fake_element', true)
      .on('mouseover', function (d) {
        // d3.select("#x_auxiliary_line")
        //   .attr("opacity", 1)

        // d3.select("#y_auxiliary_line")
        //   .attr("opacity", 1)

        // d3.select("#auxiliary_circle")
        //   .attr("opacity", 1)

        console.log(d)
        if (is_vertical){
          x = d.x + d.w / 2
          y = d.y
        }
        else {
          x = d.x + d.w
          y = d.y + d.h / 2
        }
        Draw_line(x, y)
        if (is_vertical){
          g_xAxis.selectAll("rect")
            .classed("highlight", false)
          g_xAxis.select("#xAxis_" + d.x_axis_id)
            .classed("highlight", true)

          g_legend.selectAll("rect")
            .classed("highlight", false)
          g_legend.select("#legend_" + d.legend_id)
            .classed("highlight", true)

          highlight_y_tick(y)

        }
        else{
          // TODO
        }

        d3.select(this).classed("highlight", true)
        show_element_sentence(d)

      })
      .on('mouseout', function (d) {
        // g.select('#interaction_annotation').selectAll('line').remove()
         // stop highlight legend
         // no line
         fade_out_line()
         d3.select(this).classed("highlight", true)
      })

  add_trend(0, 4)
  add_trend(10, 14)
  add_trend(5, 9)
  // element_list.forEach(ele => {

  // })
}

function add_abs_sentence(abs_sentence, id){
  let new_sentence = {}
  new_sentence.sentence = abs_sentence
  new_sentence.focus_id = [id]
  new_sentence.compare_id = []
  new_sentence.strength = 1
  new_sentence.sure = true
  new_sentence.type = "abs"

  // sentences = data.

  console.log("sentences[0].type", sentences[0].type)

  if (sentences[0].type === "abs"){
      console.log("remove the first one")
      // sentences.shift()
      sentences[0] = new_sentence
  }
  else{
    sentences.splice(0, 0, new_sentence)
  }
  showSentences(sentences)
}

function show_element_sentence(d){
  abs_sentence = data.title + " of " + d.major + " in " + d.second + " is " + parseInt(d.value * 100)/100 + " " + data.unit + "." 
  add_abs_sentence(abs_sentence, d.id)
  console.log(abs_sentence)
}


function highlight_y_tick(value){
  tick_id = find_closest_y_tick(value)

  console.log(tick_id)

  g_yAxis.selectAll("rect")
    .classed("highlight", false)

  tick_id.forEach(function(id){
    g_yAxis.selectAll("#yAxis_" + id)
      .classed("highlight", true)
  })
}


function highlight_x_tick(value){
  tick_id = find_closest_x_tick(value)

  console.log(tick_id)

  g_yAxis.selectAll("rect")
    .classed("highlight", false)

  tick_id.forEach(function(id){
    g_xAxis.select("#xAxis_" + id)
      .classed("highlight", true)
  })
}

function find_closest_x_tick(value){
  console.log("value", value)
  let tick_num = tick_value_x.length

  if (value < tick_value_x[0] )
    return [0]
  if (value >= tick_value_x[tick_num - 1] )
    return [tick_num - 1]

  for (i = 0; i < tick_num - 1; i ++){
    if (value >= tick_value_x[i] && value < tick_value_x[i + 1] )
      return [i, i + 1]
  }
  return [0]


  // console.log(yAxis
  // return 0

}


function find_closest_y_tick(value){
  console.log("value", value)
  tick_num = tick_value.length

  if (value > tick_value[0] )
    return [0]
  if (value <= tick_value[tick_num - 1] )
    return [tick_num - 1]

  for (i = 0; i < tick_num - 1; i ++){
    if (value <= tick_value[i] && value > tick_value[i + 1] )
      return [i, i + 1]
  }
  return [0]



  // console.log(yAxis
  // return 0

}
// function draw_line()

function add_trend(begin_id, end_id){
  let begin_element = element_list[begin_id]
  let end_element = element_list[end_id]

  if (is_vertical)
  {
    let space = 20
    let trend = d3.select("#annotationDiv").select("#annotation")
      .append("g")

    trend.attr("class", "trend_arrow")
      .append("line")
      .attr("x1", begin_element.x + begin_element.w / 2 )
      .attr("y1", begin_element.y - space)
      .attr("x2", end_element.x + end_element.w / 2 )
      .attr("y2", end_element.y - space)

    // trend.append("path")
    //   .attr("d", )



  }
}


function fade_out_line(){

  let trans = d3.select("#annotationDiv")
    .transition()
    .duration(200)

  trans.select("#x_auxiliary_line")
    .attr("opacity", 0)

  trans.select("#y_auxiliary_line")
    .attr("opacity", 0)

  trans.select("#auxiliary_circle")
    .attr("opacity", 0)

  g_xAxis.selectAll("rect")
    .classed("highlight", false)

  g_yAxis.selectAll("rect")
    .classed("highlight", false)

  g_legend.selectAll("rect")
    .classed("highlight", false)


}

function Draw_line(x, y){

  let trans = d3.select("#annotationDiv")
    .transition()
    .duration(200)

  trans.select("#x_auxiliary_line")
    .attr("opacity", 1)
    .attr("x1", x)
    .attr("x2", x)
    .attr("y2", y)

  trans.select("#y_auxiliary_line")
    .attr("opacity", 1)
    .attr("y1", y)
    .attr("x2", x)
    .attr("y2", y)

  trans.select("#auxiliary_circle")
    .attr("opacity", 1)
    .attr("cx", x)
    .attr("cy", y)
}

// let highLightLine = function (x, y) {
//   d3.select('#annotationDiv').select('#interaction_annotation')
//     .append('line')
//     .attr('x1', xAxis[0].x )
//     .attr('y1', y)
//     .attr('x2', xAxis[xAxis.length - 1].x -  xAxis[xAxis.length - 1].w)
//     .attr('y2', y)
//     .style('stroke-dasharray', "10,10")
//     .style('stroke', 'black')

//   d3.select('#annotationDiv').select('#interaction_annotation')
//     .append('line')
//     .attr('x1', x)
//     .attr('y1', yAxis[0].y)
//     .attr('x2', x)
//     .attr('y2',  yAxis[yAxis.length - 1].y -  yAxis[yAxis.length - 1].h)
//     .style('stroke-dasharray', "10,10")
//     .style('stroke', 'black')

// }


let dragStart = function(d) {
    DRAG_HANDLER = d3.event.y
    INIT_HEIGHT = d3.select(this).attr('height')
    INIT_Y = parseFloat(d3.select(this).attr('y'))
    d3.select(this)
      .style("stroke", highLightRectColor)
      .style('stroke-width', '0.5vh')
    d3.select('#table-'+String(id))
      .style('background', highLightTableColor)
}

let dragging = function(d) {
    let yScale = cur.chart.yScale.invert
    let dy = d3.event.y - DRAG_HANDLER
    let newH = INIT_HEIGHT - dy
    let newY = INIT_Y + dy

    d3.select(this)
      .attr('height', newH)
      .attr('y', newY)
    let mydate = new Date()
    TIME_NOW = mydate.getTime()
    if (TIME_NOW - TIME_LAST > 200){
      update_sentence_data()
      TIME_LAST = TIME_NOW;
    }
    id = d3.select(this)
           .attr('id')
    d3.select('#table-'+String(id))
      .style('background', highLightTableColor)
}

let dragEnd = function(d) {
    let yScale = cur.chart.yScale.invert
    let dy = d3.event.y - DRAG_HANDLER
    let newH = INIT_HEIGHT - dy
    let newY = INIT_Y + dy

    d3.select(this)
      .attr('height', newH)
      .attr('y', newY)
      .style('stroke-width', 0)
    d3.select('#table-'+String(id))
      .style('background', null)
    update_sentence_data()
}

let mouseOver = function() {
    id = d3.select(this)
           .attr('id')
    d3.select('#table-'+String(id))
      .style('background', highLightTableColor)
    d3.select(this)
      .style("stroke", highLightRectColor)
      .style('stroke-width', '0.5vh')
}

let mouseOut = function() {
   id = d3.select(this)
         .attr('id')
   d3.select('#table-'+String(id))
     .style('background', null)
   d3.select(this)
     .style('stroke-width', 0)
}

let highLightRect = function() {
    id = d3.select(this).attr('customid')
    d3.select(this)
      .style('background', highLightTableColor)
    d3.select('.element_'+String(id))
      .style("stroke", highLightRectColor)
      .style('stroke-width', '0.5vh')

}

let normalRect = function() {
    id = d3.select(this).attr('customid')
    d3.select('.element_'+String(id))
      .style('stroke-width', 0)
    d3.select(this)
      .style('background', null)
}

let addDragging = function() {
    d3.selectAll('rect')
      .on('mouseover', mouseOver)
      .on('mouseout', mouseOut)
      .call(d3.drag()
              .on('start', dragStart)
              .on('drag', dragging)
              .on('end', dragEnd))
}

let update_sentence_data = function() {
    SVG_string = d3.select('#visualization').node().innerHTML
    send_data = {'svg_string': SVG_string}
    get_modify_data_sentence_from_server(send_data)
}
