var DRAG_HANDLER = 0
var INIT_HEIGHT = 0
var INIT_Y = 0
var TIME_LAST = 0
var TIME_NOW = 0
let highLightTableColor = '#fec44f'
let highLightRectColor = '#d95f0e'
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
   id =d3.select(this)
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
let update_sentence_data = function(){
    SVG_string = d3.select('#visualization').node().innerHTML
    send_data = {'svg_string': SVG_string}
    get_modify_data_sentence_from_server(send_data)
}
