/*
    fundamental functions for page.js, including dynamic elements
*/
window.CQQ_MODE = false
let USE_SERVER = false
let SERVER_ANSWER = true
const type_dict = {
  "all_trend": "trend",
  "compare_ave": "compare_abs",
  "sum_trend": "trend_sum",
  "local_trend": "trend_local",
  "local_sum_trend": "trend_local",
  "compare_trend": "compare_trend",
  "outlier": "outlier",
  "cluster":"cluster"
}
const type_name = {
  "all_trend": "Trend",
  "compare_ave": "Comparison",
  "sum_trend": "Trend on Sum",
  "local_trend": "Trend on local",
  "local_sum_trend": "Trend on local sum",
  "compare_trend": "Comparison on trend",
  "cluster": "Cluster",
  "outlier": "Outlier"
}
const color = ['#05668D','#A8DADC', '#00A896', '#FFF1D0', '#FFE5D9', '#FFA69E', '#FFCAD4']
const sweetcolor = ['#7cbff2', '#B2F7EF', '#d2f2cf', '#F7D6E0', '#F2B5D4', '#f2b6c4', '#7BDFF2','#EFF7F6']
let dropdownList = [{
      'text': 'Bar Chart (vertical)',
      'value': 'load_bar_chart_1d'
    }, {
      'text': 'Bar Chart (horizontal)',
      'value': 'load_bar_chart_1d_horizontal'
    }, {
      'text': 'Group Bar Chart (vertical)',
      'value': 'load_group_bar_chart'
    }, {
      'text': 'Group Bar Chart (horizontal)',
      'value': 'load_group_bar_chart_horizontal'
    },  {
      'text': 'Stack Bar Chart (vertical)',
      'value': 'load_stack_bar_chart'
    }, {
      'text': 'Stack Bar Chart (horizontal)',
      'value': 'load_stack_bar_chart_horizontal'
    }, {
      'text': 'Scatter Plot (vertical)',
      'value': 'load_scatter_plot'
    }, {
      'text': 'Scatter Plot (horizontal)',
      'value': 'load_scatter_plot_horizontal'
    }
]
function addColorPicker(rect) {
    let newobj = document.createElement('div')
}
let popoverInit = []

function changeSVG(SVG_string) {
     window.num = 0
     d3.select('#visualization').node().innerHTML = SVG_string
     let svg = d3.select('#visualization').select('svg').attr('id', 'mySvg')
     let windowWidth =  document.getElementById('visualization').clientWidth * 0.95
     let windowHeight = document.body.clientHeight * 0.8
     let width = svg.attr('width')
     let height = svg.attr('height')
     svg.attr('viewBox', '0 0 ' + String(width) + ' ' + String(height))
        .attr('preserveAspectRatio', "xMidYMid meet")
        .attr('height', windowHeight)
        .attr('width', windowWidth)
     highLightShadow()
}

function highLightShadow() {
    let svg = d3.select('#visualization')
                .select('svg')
    let defs = svg.append('defs')


    defs.append('filter')
       .attr('id', 'blue-shadow')
       .append('feDropShadow')
       .attr('dx', '3')
       .attr('dy', '3')
       .attr('stdDeviation', '3')
       .attr('flood-color', '#0080e0')
       .attr('flood-opacity', '50%')


    defs.append('filter')
      .attr('id', 'red-shadow')
      .append('feDropShadow')
      .attr('dx', '3')
      .attr('dy', '3')
      .attr('stdDeviation', '3')
      .attr('flood-color', '#fa1919')
      .attr('flood-opacity', '50%')

    defs.append('pattern')
      .attr("id", "pattern-blue")
      .attr("width", 4)
      .attr("height", 4)
      .attr("patternUnits", "userSpaceOnUse")
      .attr("patternTransform", "rotate(45)")
    .append("rect")
      .attr("width", 3)
      .attr("height", 4)
      .attr("fill", "white")
      .attr("transform", "translate(0,0)")

    defs.append('pattern')
      .attr("id", "pattern-red")
      .attr("width", 4)
      .attr("height", 4)
      .attr("patternUnits", "userSpaceOnUse")
      .attr("patternTransform", "rotate(-45)")
    .append("rect")
      .attr("width", 3)
      .attr("height", 4)
      .attr("fill", "white")
      .attr("transform", "translate(0,0)")

    defs.append("mask")
      .attr("id", "mask-blue")
    .append("rect")
      .attr("width", "100%")
      .attr("fill", "url(#pattern-blue)")

    defs.append("mask")
      .attr("id", "mask-red")
    .append("rect")
      .attr("width", "100%")
      .attr("fill", "url(#pattern-red)")
  //
  // defs = svg.append("defs");
  //
  // // create an svg element
  // var stripes = defs.append("pattern")
  //     .attr("id", "stripes")
  //     .attr("width", 15)
  //     .attr("height", 10)
  //     .attr("patternUnits", "userSpaceOnUse")
  //     .attr("patternTransform", "rotate(45 50 50)")
  //
  // stripes.append("line")
  //     .attr("stroke", "#d8d8d8")
  //     .attr("stroke-width", 10)
  //     .attr("y2", 20);
}
function showElementCQQ(element) {
  let oldhtml = element.innerHTML
  let newobj = document.createElement('input')
  newobj.type = 'text'
  // newobj.class = 'form-control form-control-sm'
  newobj.placeholder = oldhtml
  newobj.size = '1'
  /*为新增元素添加value值
   newobj.value = oldhtml*/
  //为新增元素添加光标离开事件
  newobj.onblur = function() {
      //当触发时判断新增元素值是否为空，为空则不修改，并返回原有值
      // element.innerHTML = this.value == '' ? oldhtml : this.value
      if(this.value === '') {
          element.innerHTML = oldhtml
      }
      else {
          let val = this.value
          element.innerHTML = val
          let id = element.getAttribute('customid')
          let role = element.getAttribute('customtype')
          let rowid = element.parentNode.getAttribute('row-id')
          switch(role) {
              case 'value':
                  if(id==0)
                  cur.data_array[rowid][cur.major] = val
                  else
                  cur.data_array[rowid][cur.second]=val
                  break
              default:
                  alert('ERROR in changing chart!')
          }
          remove_old_vis()
          window[cur.cType](...cur.cPara)
          SVG_string = d3.select('#visualization').node().innerHTML
          send_data = {'svg_string': SVG_string}
          get_modify_svg_from_server(send_data)

      }
      //当触发时设置父节点的双击事件为ShowElement
      // element.setAttribute("ondblclick", "ShowElement(this)")
  }
  //设置该标签的子节点为空
  element.innerHTML = ''
  //添加该标签的子节点，input对象
  element.appendChild(newobj)
  //设置选择文本的内容或设置光标位置（两个参数：start,end；start为开始位置，end为结束位置；如果开始位置和结束位置相同则就是光标位置）
  newobj.setSelectionRange(0, oldhtml.length)
  //设置获得光标
  newobj.focus()
  //设置父节点的双击事件为空
  // newobj.parentNode.setAttribute("ondblclick", "");

}

function showElement(element) {
    // change the value
    let oldhtml = element.innerHTML
    let newobj = document.createElement('input')
    newobj.type = 'text'
    // newobj.class = 'form-control form-control-sm'
    newobj.placeholder = oldhtml
    newobj.size = '1'
    /*为新增元素添加value值
     newobj.value = oldhtml*/
    //为新增元素添加光标离开事件
    newobj.onblur = function() {
        //当触发时判断新增元素值是否为空，为空则不修改，并返回原有值
        // element.innerHTML = this.value == '' ? oldhtml : this.value
        if(this.value === '') {
            element.innerHTML = oldhtml
        }
        else {
            let val = this.value

            element.innerHTML = val
            let id = element.getAttribute('customid')
            let role = element.getAttribute('customtype')
            switch(role) {
                case 'value':
                    cur.data_array[id][cur.quan] = val
                    break
                case 'major':
                    cur[cur.major][id] = val
                    break
                case 'second':
                    cur[cur.second][id] = val
                    break
                default:
                    alert('ERROR in changing chart!')
            }
            remove_old_vis()
            window[cur.cType](...cur.cPara)
            SVG_string = d3.select('#visualization').node().innerHTML
            send_data = {'svg_string': SVG_string}
            get_modify_svg_from_server(send_data)

        }
        //当触发时设置父节点的双击事件为ShowElement
        // element.setAttribute("ondblclick", "ShowElement(this)")
    }
    //设置该标签的子节点为空
    element.innerHTML = ''
    //添加该标签的子节点，input对象
    element.appendChild(newobj)
    //设置选择文本的内容或设置光标位置（两个参数：start,end；start为开始位置，end为结束位置；如果开始位置和结束位置相同则就是光标位置）
    newobj.setSelectionRange(0, oldhtml.length)
    //设置获得光标
    newobj.focus()
    //设置父节点的双击事件为空
    // newobj.parentNode.setAttribute("ondblclick", "");
}

function showSentences(data) {
   // data is the sentence array with index to focus & compare
    let textzone = d3.select('#sentences_div')
    textzone.selectAll('div').remove()
    textzone.selectAll('p').remove()
    // if(window.num !== 0) {
    //     textzone.append('p')
    //             .attr('class', 'm-2')
    //             .style('font', 'grey')
    //             .style('cursor', 'default')
    //             .text('Current Chart No: ' + String(window.num) )
    // }
    pzone = textzone.selectAll('div')
            .data(data)
            .enter()
            .append('div')
            .attr('class', 'row m-0 p-0 text_block')
            .on('mouseover', captionHighlight)
            .on('mouseout', back2normal)
   pzone.append('div')
        .attr('class', 'col-sm-1 m-0 p-0')
        .style('text-align', 'center')
        .style('vertical-align', 'middle')
        .style('height', '40px')
        .style('width', '40px')
        .style('top', '10px')
        .append('img')
        .attr('src', function(d){
          file_url = "vis2description/image/icon/" + type_dict[d.type] + ".png"
          return file_url
        })
        .attr('height', '32px')
        .attr('width', '32px')
        .attr('data-toggle', 'tooltip')
        .attr('data-placement', 'top')
        .attr('title', d => type_name[d.type])
        .style('vertical-align', 'middle')
        .style('display', 'inline-block')
        .style('opacity', d => d.strength)

   pzone.append('div')
        .attr('class', 'col-sm-11 m-0 p-0')
        .append('p')
        .style("opacity",d => d.strength)
        .attr('class', 'caption m-2 p-0')
        .text(d => d.sentence)
   $('[data-toggle=tooltip]').tooltip()
}

function back2normal(d, i) {
    d3.selectAll('rect')
      .classed('nobody', false)
      .classed('myfocus', false)
      .classed('mycompare', false)
      .classed('ordinary', true)
    d3.selectAll('circle')
      .classed('nobody', false)
      .classed('myfocus', false)
      .classed('mycompare', false)
      .classed('ordinary', true)
    d3.select("#data-table").selectAll(".table-cell").style("background", "white")
    // for (let k of d.compare_id){
    //   d3.select('.element_' + String(k)).style('fill', cur.color[cur.data_array[k]['c0']])
  //   if(cur.cType!="load_scatter_plot"){
  //     d3.select('.element_' + String(k)).style('fill', cur.color[cur.data_array[k]['c0']])
  //   }
  //   else{
  //   d3.select('.element_' + String(k)).style('fill', 'black')
  // }}



    // for (k of d.focus_id){
    //   if(cur.cType!="load_scatter_plot"){
    //     d3.select('.element_' + String(k)).style('fill', cur.color[cur.data_array[k]['c0']])
    //   }
    //   else{
    //   d3.select('.element_' + String(k)).style('fill', 'black')
    // }
    // }
}

function captionHighlight(d, i) {
    let total = cur.data_array.length
    let allid = Array.from(Array(total).keys())
    let fadeid = allid.map(v => true)
    for(let compid of d.compare_id) {
       d3.select('.element_' + String(compid))
         .raise()
         .classed('ordinary', false)
         .classed('mycompare', true)
         fadeid[compid] = false
      //d3.select('.element_' + String(compid)).style('fill', 'blue')
      d3.select("#data-table").select("#table-" + String(compid)).style("background", "#9ecae1")
    }
    for(let focusid of d.focus_id) {
       d3.select('.element_' + String(focusid))
         .raise()
         .classed('ordinary', false)
         .classed('myfocus', true)
       fadeid[focusid] = false
       // Tell me why!!!!!!!
      // d3.select('.element_' + String(focusid)).style('fill', 'red')
       d3.select("#data-table").select("#table-" + String(focusid)).style("background", "#fc9272")
     }
    for(let i in fadeid){
        if(fadeid[i] === true){
            let a = d3.select('.element_' + String(i))
                      .classed('ordinary', false)
                      .classed('nobody', true)
            d3.select("#data-table").select("#table-" + String(i)).style("background", "white")
        }

    }
}

let dropdownHandler = function(func, dataType) {
  // redraw the chart according to chart type and data type
  cur.cType = func
  remove_old_vis()
  window[func](...cur.cPara)
}

let dropdown = function(dataType) {
    let data
    let click = "dropdownHandler(d3.select(this).attr('value'),"
    switch(dataType) {
        case "ccq": {
          data = [2, 3, 4, 5]
          click += "'ccq')"
          break
        }
        case "ocq": {
          data = [2, 3, 4, 5]
          click += "'ocq')"
          break
        }
        case "oq": {
          data = [0, 1]
          click += "'oq')"
          break
        }
        case "cqq": {
           data = [6, 7]
           click += 'cqq)'
           break
        }
        default: alert('Invalid Data :-(')
    }
    d3.select('#chart-type')
      .selectAll('li')
      .remove()
    d3.select('#chart-type')
      .selectAll('li')
      .data(data)
      .enter()
      .append('li')
      .attr('class', 'nav-item')
      .style('text-align', 'center')
      .attr('onclick', click)
      .attr('value', v => dropdownList[v].value)
          .append('a')
          .attr('href', '#')
          .attr('class', 'dropdown-item')
          .text(v => dropdownList[v].text)
    d3.select('#chart-type')
      .append('li')
      .attr('role', 'seperator')
      .attr('class', 'dropdown-divider')
    d3.select('#chart-type')
      .append('li')
      .attr('class', 'nav-item')
      .text('Select Chart Type')
      .style('text-align', 'center')
}

let Data = function() {
}

Data.prototype.drawTitle = function() {
    d3.select('#chart-title').text(this.title)
}

Data.prototype.translateList = function() {
    let first = this.major
    let second = this.second
    let q = this.quan
    let len1 = this[first].length
    let len2 = second == undefined? 1 : this[second].length
    let matrix = new Array(len2)
    for(let i = 0; i < len2; ++i) matrix[i] = new Array(len1)
    if(this.dType.length === 2) {
        for (let v of this.data_array)
            matrix[0][v[first]] = {'value': v[q], 'id': v.id}
    }
    else {
      if(CQQ_MODE==1||this.dType=='cqq'){
        for (let v of this.data_array) {
            let row = v[second]
            let col = 0
            for (let oid in this.o0){
              if(Number(v[first])==Number(this.o0[oid])){
                col = oid
              }
            }
            matrix[row][col] = {'value': v[q], 'id': v.id}
        }
      }
        else{
          for (let v of this.data_array) {
              let row = v[second]
              let col = v[first]
              matrix[row][col] = {'value': v[q], 'id': v.id}
          }
        }
    }

    return matrix
}

Data.prototype.init = function(data, filename) {
    if("vis_type"in data && data.vis_type=='load_scatter_line_plot'){
       data  = CCQ2CQQ(data)
       if(filename){
         this.filename = filename.slice(14)
         console.log('Data Obj from file: ', filename)
       }
       this.dType = 'cqq'
    }
    else{
      this.dType = data.type
    }
    this.title = data.title
    this.c0 = data.c0
    this.c1 = data.c1
    this.o0 = data.o0
    this.data = data
    this.data_array = data.data_array
    this.unit = data.unit
    this.unit1 = data.unit1
    this.unit2 = data.unit2
    let tmpColor = this.color || sweetcolor
    this.color = data.color || tmpColor
    this.cType = data.vis_type || null
    this.major = data.major_name
    this.second = data.second_name
    this.quan = 'q0'
    if(this.cType == "load_scatter_line_plot") {
      this.cPara = [this, this.second, this.major, this.quan]
    }
    else if(this.cType=="load_scatter_plot") {
      this.cPara = [this, null, this.major, this.second]
    }
    else{this.cPara = [this, this.major, this.second, this.quan]}
}

Data.prototype.initChartFromJson = function() {
    remove_old_vis()
    window[this.cType](...this.cPara)
}

Data.prototype.initChart = function() {
      remove_old_vis()
      switch (this.dType) {
          case "ccq":
              load_group_bar_chart(this, 'c0', 'c1', 'q0')
              this.major = 'c0'
              this.second = 'c1'
              this.quan = 'q0'
              this.cType = 'load_group_bar_chart'
              this.cPara = [this, 'c0', 'c1', 'q0']
              break
          case "ocq":
              load_group_bar_chart(this, 'c0', 'o0', 'q0')
              this.major = 'c0'
              this.second = 'o0'
              this.quan = 'q0'
              this.cType = 'load_group_bar_chart'
              this.cPara = [this, 'o0', 'c0', 'q0']
              break
          case "cq":
              load_pie_chart(this, 'c0', undefined, 'q0')
              this.major = 'c0'
              this.second = null
              this.quan = 'q0'
              this.cType = 'load_bar_chart_1d'
              break
          case "oq":
              load_bar_chart_1d(this, 'o0', undefined, 'q0')
              this.major = 'o0'
              this.second = null
              this.quan = 'q0'
              this.cType = 'load_bar_chart_1d'
              this.cPara = [this, 'c0', null, 'q0']
          case "cqq":
              this.major = 'o0'
              this.second = 'c0'
              this.cType = 'load_scatter_plot'
              this.quan = 'q0'
              window[this.cType](...this.cPara)
              break
        default:
          alert("Invalid Data :-(")
    }
}
Data.prototype.drawQQTableXY = function(){
  let table = d3.select('#data-table')
  table.selectAll('tr').remove()
  tabledata = this.data_array.map((d) => [d[this.major], d[this.quan]])
  table.select('thead')
            .append('tr')
            .selectAll('th')
            .data(['id', 'x', 'y'])
            .enter()
            .append('th')
            .attr('scope', 'col')
            .attr('customtype', 'XY')
            .attr('customid', (d, i) => i-1)
            .attr('ondblclick', 'showElementCQQ(this)')
            .text(d => d)
  let tableBody = table.select('tbody')
                       .selectAll('tr')
                       .data(tabledata)
                       .enter()
                       .append('tr')
                       .attr('row-id', (d,i)=>i)

  tableBody.append('th')
           .attr('scope', 'row')
           .attr('customtype', 'id-indicator')
           .attr('customid', (d, i) => i)
           .text((d,i)=>i)

  tableBody.selectAll('td')
           .data(d => d)
           .enter()
           .append('td')
           .attr('ondblclick', 'showElementCQQ(this)')
           .attr('customid', (d,i)=> i)
           .attr('customtype', 'value')
           .text(d => parseInt(d* 100)/100)
}

Data.prototype.drawQQTable = function() {
  let table = d3.select('#data-table')
  table.selectAll('tr').remove()
  let majorRow = [' ', ' ', ...this[this.major]]

  let secondRow = this[this.second]
  let colorlen = this[this.second].length
  let matrix = this.translateList()
  table.select('thead')
            .append('tr')
            .selectAll('th')
            .data(majorRow)
            .enter()
            .append('th')
            .attr('scope', 'col')
            .attr('customtype', 'major')
            .attr('customid', (d, i) => i - 2)
            .attr('ondblclick', 'showElement(this)')
            .text(d => d)
  let tableBody = table.select('tbody')
                       .selectAll('tr')
                       .data(matrix)
                       .enter()
                       .append('tr')
  tableBody.append('th')
           .attr('scope', 'row')
           .attr('ondblclick', 'showElement(this)')
           .attr('customtype', 'second')
           .attr('customid', (d, i) => i)
           .text((d, i) => secondRow[i])

 tableBody.append('th')
          .attr('scope', 'row color-picker-th')
          .append('span')
          .attr('class', 'colorpicker-input-addon')
          .append('i')
          .style('background-color', (d, i) => cur.color[i])
          .attr('class', 'popover-icon')
          .attr('id', (d, i) => 'popover-icon-' + String(i))
          .attr('data-toggle', 'popover')
          .attr('data-placement', 'right')

  tableBody.selectAll('td')
           .data(d => d)
           .enter()
           .append('td')
           .attr('customid', (d,i) => d.id)
           .attr('id', (d, i) =>'table-'+String(d.id))
           .attr("class", "table-cell")
           .attr('customtype', 'value')
           .on('mouseover', highLightRect)
           .on('mouseout', normalRect)
           .text(d => parseInt(d.value * 100)/100)
          .attr('ondblclick', 'showElement(this)')
  }

Data.prototype.drawTable = function() {
  if (this.cType == 'load_scatter_line_plot') {
       this.drawQQTable()
       return
  }
  else if (this.cType=='load_scatter_plot') {
      this.drawQQTableXY()
      return
  }
    let table = d3.select('#data-table')
    table.selectAll('tr').remove()
    let majorRow = [' ', ' ', ...this[this.major]]

    let secondRow = this[this.second]
    let colorlen = this[this.second].length
    let matrix = this.translateList()
    table.select('thead')
              .append('tr')
              .selectAll('th')
              .data(majorRow)
              .enter()
              .append('th')
              .attr('scope', 'col')
              .attr('customtype', 'major')
              .attr('customid', (d, i) => i - 2)
              .attr('ondblclick', 'showElement(this)')
              .text(d => d)
    let tableBody = table.select('tbody')
                         .selectAll('tr')
                         .data(matrix)
                         .enter()
                         .append('tr')
    tableBody.append('th')
             .attr('scope', 'row')
             .attr('ondblclick', 'showElement(this)')
             .attr('customtype', 'second')
             .attr('customid', (d, i) => i)
             .text((d, i) => secondRow[i])

   tableBody.append('th')
            .attr('scope', 'row color-picker-th')
            .append('span')
            .attr('class', 'colorpicker-input-addon')
            .append('i')
            .style('background-color', (d, i) => cur.color[i])
            .attr('class', 'popover-icon')
            .attr('id', (d, i) => 'popover-icon-' + String(i))
            .attr('data-toggle', 'popover')
            .attr('data-placement', 'right')

    tableBody.selectAll('td')
             .data(d => d)
             .enter()
             .append('td')
             .attr('customid', (d,i) => d.id)
             .attr('id', (d, i) =>'table-'+String(d.id))
             .attr("class", "table-cell")
             .attr('customtype', 'value')
             .on('mouseover', highLightRect)
             .on('mouseout', normalRect)
             .text(d => parseInt(d.value * 100)/100)
            .attr('ondblclick', 'showElement(this)')

    // for(let i = 0; i < colorlen; ++i) {
    //       let id = '#popover-div-' + String(i)
    //       d3.select('body')
    //         .append('div')
    //         .attr('class', 'popover-div')
    //         .attr('id', 'popover-div-' + String(i))
    //         .attr('data-color', cur.color[i])
    //
    //       popoverInit.push({
    //         html: true,
    //         content: () => $('#popover-div-' + String(i)).html()
    //       })
    // }
}

Data.prototype.DEBUG = function() {
    console.log(this.data_array)
    console.log(this.translateList())
    console.log(this)
}

let loadJsonData = function(fileName='.data/0018.json') {
    d3.json(fileName, function(d) {
      loadJsonDataByData(d, fileName)
   })
}

let loadJsonDataByData = function(data, fileName){
  console.log(data)
  cur.init(data, fileName)
  cur.initChart()
  //cur.drawTitle()
  SVG_string = d3.select('#visualization').node().innerHTML
  send_data = {'svg_string': SVG_string}
  get_modify_svg_from_server(send_data)
  // cur.drawTable()
  // dropdown(cur.dType)
  showSentences(data.sentences)
  addDragging()
}

let randomDraw = function(d) {
     cur.init(d)
     cur.initChartFromJson()
     cur.drawTable()
     dropdown(cur.dType)
     addDragging()
}
let reloadJsonFromFile = function() {
      remove_old_vis()
      if(window.num === userStudyTotal) {
        window.num = 1
      //  alert("You've finished the user study! Thank you for your cooperation :-)")
      }
      else window.num += 1
      // let url = 'vis2description/data/userStudyNew/' + String(window.num) +'.json'
      // let url = 'vis2description/data/train/'+window.directory[window.num]
      let url = 'vis2description/data/dataset/tmp/'+window.directory[window.num]
       console.log(url)
       d3.json(url, function(d) {
         if (SERVER_ANSWER){
           console.log(d)
           cur.init(d) //d.data
           cur.initChartFromJson()
          // cur.drawTable()
           //cur.drawTitle()
           SVG_string = d3.select('#visualization').node().innerHTML
           send_data = {'svg_string': SVG_string}
            get_modify_svg_from_server(send_data)
         }
         else{
           cur.init(d)
           cur.initChartFromJson()
           cur.drawTable()
           dropdown(cur.dType)
           showSentences(d.sentences)
           addDragging()
           highLightShadow()
         }
      })
    }
let reloadJson = function() {
    if (! USE_SERVER){
      reloadJsonFromFile()
      return
    }
    else{
      remove_old_vis()
      get_data_json( {data_type: 'rule'})
      addDragging()
      return
    }
}
