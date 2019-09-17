/*
    page init, event handler
*/
window.userStudyTotal = 2500;
let cur = new Data()
loadJsonData('../data/dataset/tmp/1.json')
// generate_pie_data()
get_line_chart_svg_data()
window.num = 0
$(document).ready(function(){
    $("#annotationDiv").css({
      'position': 'absolute',
      'display': 'block',
      'top': 0,
      'left': 0,
      // 'pointer-events': 'none'
    });
    let origin = d3.select('#visualization').select('svg')
    d3.select('#annotationDiv').select('svg').remove()
    let overlay = d3.select('#annotationDiv').append("svg")
    console.log(origin.attr('width'), origin.attr('height'), origin.attr('viewBox'))

    if (origin.attr("viewBox") === null){
      overlay.attr('width', origin.attr('width'))
        .attr('height', origin.attr('height'))
    }
    else {
      viewBox = origin.attr("viewBox")
      width = viewBox.split(" ")[2]
      height = viewBox.split(" ")[3]
      overlay.attr("width", width)
        .attr("height", height)


      overlay
        .attr('viewBox', origin.attr('viewBox'))
        .attr('preserveAspectRatio', origin.attr('preserveAspectRatio'))
      overlay.attr("width", origin.attr("width"))
        .attr("height", origin.attr('height'))
    }

    $('[data-toggle="popover"]').popover()
    document.getElementById('openFile')
            .addEventListener('change', function(){
                  d3.select('#visualization').selectAll('g').remove()
                  d3.select('#data-table').selectAll('tr').remove()
                  let f = this.files[0]
                  let p = new FileReader()
                  p.onload = function(e) {
                      remove_old_vis()
                      let SVG_string = e.target.result
                      // console.log(SVG_string)
                      changeSVG(SVG_string)
                      add_text_bbox()
                      SVG_string = d3.select('#visualization').node().innerHTML
                      send_data = {'svg_string': SVG_string}
                      get_modify_svg_open(send_data)
                  }
                 p.readAsText(f)
           })
      })

function generate_pie_data(){
  $.ajax({
      type: 'GET',
      url: "vis2description/get_file_name",
      success: function(data_pack) {
         window.directory = data_pack
         window.userStudyTotal = data_pack.length
         for(url of window.directory) {
           remove_old_vis()
           d3.json('../data/dataset/pie/'+url, function(d) {
               cur.init(d.data)
               cur.initChartFromJson()
               SVG_string = d3.select('#visualization').node().innerHTML
               send_data = {'svg': SVG_string, 'path': '../show_system/data/dataset/pie/'+d.user_name, 'save': '../show_system/data/dataset/pie_svg/'+d.user_name}
               $.ajax({
                   type: 'POST',
                   url:"vis2description/get_file_name",
                   data: send_data,
                   dataType: 'json',
                   success: function(data_pack) {
                   },
                   error: function(jqXHR) {
                       alert('There is something wrong with our server')
                   },
               })
             })
           }
         },
      error: function(jqXHR) {
      },
  })
}
// update data and svg
function get_line_chart_svg_data(){
  $.ajax({
      type: 'GET',
      url: "vis2description/get_file_name",
      success: function(data_pack) {
         //generate_svg_data(data_pack)
         window.directory = data_pack
         window.userStudyTotal = data_pack.length
      },
      error: function(jqXHR) {
      },
  })
}
function get_modify_svg_open(send_data){

  $.ajax({
      type: 'POST',
      url: "vis2description/get_svg_data",
      data: send_data,
      dataType: 'json',
      success: function(data_pack) {
        //  console.log(data_pack)
          frush_open_file(data_pack)
          // show_sentence(evt_data)
      },
      error: function(jqXHR) {
          // $('.loading').hide()
          alert('There is something wrong with our server')
      },
  })
}

function frush_open_file(data_pack){
  // svg_string = data_pack['svg_string']
  // sentences  = data_pack['sentences']
  // data = data_pack['data']
  // cur.init(data)
  // cur.drawTable()
  // // we update the data
  // // d3.select('#visualization').node().innerHTML = svg_string
  // changeSVG(svg_string)
  // // highLightShadow()
  // showSentences(sentences)
  // addDragging()
  // highLightText(data_pack)

  svg_string = data_pack['svg_string']
  sentences  = data_pack['sentences']
  data = data_pack['data']
  cur.init(data)
  cur.drawTable()
  // we update the data
  console.log("we change the svg string")
  d3.select('#visualization').node().innerHTML = svg_string
  // changeSVG(svg_string)
  highLightShadow()
  showSentences(sentences)
  addDragging()

  // console.log(data_pack)
  highLightText(data_pack)
}


// update data and svg
function get_modify_svg_from_server(send_data){

  $.ajax({
      type: 'POST',
      url: "vis2description/get_svg_data",
      //url:"vis2description/get_file_name",
      data: send_data,
      dataType: 'json',
      success: function(data_pack) {
        //  console.log(data_pack)
          frush(data_pack)

          // show_sentence(evt_data)
      },
      error: function(jqXHR) {
          // $('.loading').hide()
          alert('There is something wrong with our server')
      },
  })
}
function frush(data_pack){
  svg_string = data_pack['svg_string']
  sentences  = data_pack['sentences']
  data = data_pack['data']
  cur.init(data)
  cur.drawTable()
  // we update the data
  console.log("we change the svg string")
  d3.select('#visualization').node().innerHTML = svg_string
  // changeSVG(svg_string)
  highLightShadow()
  showSentences(sentences)
  addDragging()

  // console.log(data_pack)
  highLightText(data_pack)
}

// Do not update the svg chart
function get_modify_data_sentence_from_server(send_data){

  $.ajax({
      type: 'POST',
      url: "vis2description/get_svg_data",
      data: send_data,
      dataType: 'json',
      success: function(data_pack) {
        //  console.log(data_pack)
          frush_no_update_svg(data_pack)

          // show_sentence(evt_data)
      },
      error: function(jqXHR) {
          // $('.loading').hide()
          alert('There is something wrong with our server')
      },
  })
}

function frush_no_update_svg(data_pack){
  svg_string = data_pack['svg_string']
  sentences  = data_pack['sentences']
  data = data_pack['data']
  console.log(data, 'hello??????')
  cur.init(data)
  cur.drawTable()
  // console.log('LONG FRUSH!')
  // we do not update the data
  // d3.select('#visualization').node().innerHTML = svg_string
  // highLightShadow()
   showSentences(sentences)
  // addDragging()
}
