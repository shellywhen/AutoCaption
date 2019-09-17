var DRAG_HANDLER = 0
var INIT_HEIGHT = 0
var INIT_Y = 0
var TIME_LAST = 0
var TIME_NOW = 0
let highLightTableColor = '#fec44f'
let highLightRectColor = '#d95f0e'

let highLightText = function (data_pack) {
  console.log("data_pack", data_pack)
  let textCollection = data_pack.data.text_collection
  d3.select('#annotationDiv').select('svg')
    .attr("viewBox", d3.select('#visualization').select('svg').attr("viewBox"))

  let g = d3.select('#annotationDiv').select('svg').append('g').attr('id', 'annotation')
  let colorList = ['blanchedalmond', 'palegreen', 'mediumpurple', 'lightskyblue', 'lightpink']
  let attributeList = ['xAxis', 'yAxis', 'legend']
  let i = 0
  return
  xAxis = textCollection.xAxis.text
  yAxis = textCollection.yAxis.text
  for (let attrName of attributeList) {
    let canvas = g.append('g').attr('id', `g_${attrName}`)
    for (let item of textCollection[attrName].text) {
      let x1 = item.x, x2 = item.x + item.w, y1 = item.y, y2 = item.y + item.h
      canvas.append('polygon')
        .attr('points', `${x1},${ y1} ${x2},${y1} ${x2},${y2} ${x1},${y2}`)
        .datum(item.content)
        .style('stroke-width', 3)
        .style('stroke', colorList[i])
        .style('fill-opacity', 0.1)
        .style('fill', colorList[i])
        .style('stroke-opacity', 1)
        .classed(`annotation_${attrName}`, true)
        .classed('annotation_normal', true)
        .classed('annotation_highlight', false)
    }
    i++
  }
  element_list = data_pack.data.elements
  element_list.forEach(ele => {
    g.append('rect')
      .datum(ele)
      .attr('x', ele.x)
      .attr('y', ele.y)
      .attr('width', ele.w)
      .attr('height', ele.h)
      .style('opacity', 0.1)
      .style('fill', "red")
      .attr('id', ele.id)
      .classed('fake_element', true)
      .on('mouseover', function (d) {
        console.log(d)
      })
      .on('mouseout', function (d) {
        g.select('#interaction_annotation').selectAll('line').remove()
         // stop highlight legend
         // no line

      })
  })
}

let highLightLine = function (x, y) {
  d3.select('#annotationDiv').select('#interaction_annotation')
    .append('line')
    .attr('x1', xAxis[0].x )
    .attr('y1', y)
    .attr('x2', xAxis[xAxis.length - 1].x -  xAxis[xAxis.length - 1].w)
    .attr('y2', y)
    .style('stroke-dasharray', "10,10")
    .style('stroke', 'black')

  d3.select('#annotationDiv').select('#interaction_annotation')
    .append('line')
    .attr('x1', x)
    .attr('y1', yAxis[0].y)
    .attr('x2', x)
    .attr('y2',  yAxis[yAxis.length - 1].y -  yAxis[yAxis.length - 1].h)
    .style('stroke-dasharray', "10,10")
    .style('stroke', 'black')

}

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
