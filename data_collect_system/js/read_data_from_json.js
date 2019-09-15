const marginRate = .2
const spaceRatio = .3
const fontRatio = .03
const legendHeightRatio = .04
const paddingValue = .2

function load_json_data(){
  json_name = "json/Ielts_new_principle/ielts_data/0002.json"
  console.log(json_name)
  d3.json(json_name, function(d){
    print(d)
    data_json = d
    init_element_status(d)
    data_type = judge_type(d)
    switch (data_type) {
      case "ccq":
        deal_with_ccq(d)
        break;
      case "ocq":
        deal_with_ocq(d)
      default:
        console.log("I can not handle this kind of data!")
    }

  })
}
function reload_every_thing(){
  remove_old_vis()
  var count_number = d3.select('#count_number')
    .text("第 " + total_number +" 个图表：")
  send_data = {data_type: data_type}
  update_selected_sentence([])
  current_select = 'focus'
  refresh_focus_compare()
  get_data_json(send_data)
  // selected_sentences = []
  // show_sentence([])
}
function deal_with_data(d) {
  data_json = d
  init_element_status(d)
  // console.log('element initial',element_status)
  switch (d['type']) {
    case "ccq":
      deal_with_ccq(d)
      break;
    case "ocq":
      deal_with_ocq(d)
      break;
    case 'cq':
      deal_with_cq(d)
      break;
    case 'oq':
      deal_with_oq(d)
      break;
    default:
      console.log("I can not handle this kind of data!")
  }
  if (is_show){
    sent_data = { data_string: JSON.stringify(data_json),
                  svg_string: get_svg_string,
                  major_name: major_name,
                  second_name: second_name
                }
    get_machine_answer(sent_data)
    selected_sentences = []
  }
  else if (data_json.hasOwnProperty('sentences')){
    selected_sentences = data_json['sentences']
    update_selected_sentence(selected_sentences)
  }
  if (super_limit){
    if (total_number < 3000){
      $("#submit").click()
    }
  }
}
function judge_type(data) {
      d = data.data_array[0]
      var o0 = d.hasOwnProperty("o0")
      var o1 = d.hasOwnProperty("01")
      var c0 = d.hasOwnProperty("c0")
      var c1 = d.hasOwnProperty("c1")
      var q0 = d.hasOwnProperty("q0")
      var q1 = d.hasOwnProperty("q1")

      if (o0 && c0 && q0 && !o1 && !c1 && !q1){
        return "ocq"
      }
      else if (c0 && c1 && q0 && !o0 && !o1 && !q1){
        return "ccq"
      }
      else if (c0 && !c1 && q0 && !o0 && !o1 && !q1){
        return "cq"
      }
      else if (!c0 && !c1 && q0 && o0 && !o1 && !q1){
        return "oq"
      }

  // console.log(d.hasOwnProperty("c0"))
}
function deal_with_oq(data){
    if (Math.random() > 0.5)
    {
      load_bar_chart_1d(data, 'o0', '', 'q0')
    }
    else{
      load_bar_chart_1d_horizontal(data, 'o0', '', 'q0')
    }
    major_name = 'o0'
    second_name = ''
    add_click_action()
    add_brush_action()
}
function deal_with_cq(data){
    if (Math.random() > 0.5)
    {
      load_bar_chart_1d(data, 'c0', 'c1', 'q0')
    }
    else{
      load_bar_chart_1d_horizontal(data, 'c0', 'c1', 'q0')
    }
    major_name = 'c0'
    second_name = 'c1'
    add_click_action()
    add_brush_action()
}
function deal_with_ccq(data){
      if (false){
        load_group_bar_chart(data, "c0", "c1", "q0")
        major_name = 'c0'
        second_name = 'c1'
      }
      else {
        load_group_bar_chart(data, 'c1', 'c0', 'q0')
        major_name = 'c1'
        second_name = 'c0'
      }
//
//      load_stack_bar_chart(data, 'c0', 'c1', 'q0')
//      load_stack_bar_chart_verticle(data, 'c0', 'c1', 'q0')
      add_click_action()
      add_brush_action()
}
function deal_with_ocq(data){
      console.log(data.vis_type)
      if (data.vis_type === 'load_group_bar_chart')
      {
        major_name = data.major_name
        second_name = data.second_name

        load_group_bar_chart(data, major_name, second_name, 'q0')
      }
      else if (data.vis_type === 'load_stack_bar_chart')
      {
        major_name = data.major_name
        second_name = data.second_name
        load_stack_bar_chart(data, major_name, second_name, 'q0')
      }
      else if (data.vis_type === 'load_stack_bar_chart_horizontal')
      {
        major_name = data.major_name
        second_name = data.second_name
        load_stack_bar_chart_horizontal(data, major_name, second_name, 'q0')
      }
      else if (data.vis_type === 'load_group_bar_chart_horizontal')
      {
        major_name = data.major_name
        second_name = data.second_name
        load_group_bar_chart_horizontal(data, major_name, second_name, 'q0')
      }
      else if (Math.random() > 0.5)
      {

        load_group_bar_chart(data, "c0", "o0", "q0")
        major_name = 'c0'
        second_name = 'o0'
      }
      else {
        load_stack_bar_chart_horizontal(data, 'o0', 'c0', 'q0')
        major_name = 'o0'
        second_name = 'c0'
      }
      add_click_action()
      add_brush_action()

}

function add_click_action(){
      d3.select("#visualization")
        .select("svg")
        .selectAll("rect")
        .on("click", function(d){
          click_on_id(parseInt(d3.select(this).attr("id")))
          send_data_and_setting()
          refrush_all_element()
        })
}
function add_brush_action(){
      d3.select("#visualization")
        .selectAll("svg")
        .selectAll(".brush")
        .call(d3.brush()
                .on('end', brushed))
}
function remove_old_vis(){
    var svg = d3.selectAll("#visualization")
      .selectAll("svg").selectAll("g").remove()
}

function brushed(d){
      console.log(d3.event)
      if(!d3.event.selection){
        return
      }
      var selection = d3.event.selection
      x1 = selection[0][0]
      y1 = selection[0][1]
      x2 = selection[1][0]
      y2 = selection[1][1]

      d3.selectAll(".elements")
        .each(function(d){
          var this_element = d3.select(this)
          var x = parseFloat(this_element.attr('x'))
          var y = parseFloat(this_element.attr('y'))
          var width = parseFloat(this_element.attr('width'))
          var height = parseFloat(this_element.attr("height"))
          x1_r = x
          y1_r = y
          x2_r = x + width
          y2_r = y + height
          var this_id = parseInt(d3.select(this).attr('id'))
          if (x2 < x1_r || x1 > x2_r || y1_r > y2 || y1 > y2_r){

            element_status[this_id][current_select] = false
          }
          else {
            element_status[this_id][current_select] = true;
          }
        })
      refrush_all_element()
      send_data_and_setting()
      // console.log(d3.event.selection)
}



let extent = function (array, key) {
      let yMin = Infinity
      let yMax = -Infinity
      for (v of array) {
          yMin = Math.min(yMin, v[key])
          yMax = Math.max(yMax, v[key])
      }
      return [yMin, yMax]
}

function CQ(data, cat_position, cat_color, quantity, position = 'vertical') {
    // initial chart set up
        this.svg = d3.selectAll('#visualization').selectAll('svg')
        this.height = this.svg.attr('height')
        this.width = this.svg.attr('width')
        this.g = this.svg.append('g')
                         .attr('transform', 'translate(' + this.width * marginRate + ',' + this.height * marginRate + ')')
        this.g.append('g')
                  .attr('class', 'brush')
   // database set up
        this.position = position
        this.data = data
        this.majorName = cat_position
        this.secondName = cat_color
        this.quantity = quantity
   // scale set up
        this.scaleHeight = [this.height * (1 - 2 * marginRate), 0]
        this.scaleWidth = [0, this.width * (1 - 2 * marginRate)]
        this.xScale = d3.scaleBand()
                        .padding(paddingValue)
                        .domain(this.data[this.majorName])
        this.yScale = d3.scaleLinear()
        if(this.position === 'horizontal') {
            this.xScale.rangeRound(this.scaleHeight)
            this.yScale.rangeRound(this.scaleWidth)
        }
        else {
            this.xScale.rangeRound(this.scaleWidth)
            this.yScale.rangeRound(this.scaleHeight)
        }
}

CQ.prototype.drawBarChart = function(){
    if(this.position === 'horizontal') {
         this.drawBarChart_Horizontal()
         return
    }
    this.xScale.domain(this.data[this.majorName])
    let yMin = Infinity
    let yMax = -Infinity
    for (v of this.data.data_array) {
        yMin = 0
        yMax = Math.max(yMax, v[this.quantity])
    }
    this.yScale.domain([0, yMax])

    this.g.selectAll('.bar')
        .data(this.data.data_array)
        .enter().append('rect')
        .attr('class', 'bar')
        .classed('elements', true)
        .attr('id', d => d['id'])
        .attr(this.quantity, d => d[this.quantity])
        .attr(this.majorName, d => d[this.majorName])
        .attr('x', d => this.xScale(this.data[this.majorName][d[this.majorName]]))
        .attr('y', d => this.yScale(d[this.quantity]))
        .attr('fill', (d, i) => this.data.color[i])   // 普通柱形图 按顺序赋色
        .attr('width', this.xScale.bandwidth())
        .attr('height', d => this.scaleHeight[0] - this.yScale(d[this.quantity]))

    this.g.append('g')
      .attr('class', 'axis axis--x')
      .attr('transform', 'translate(0,' + this.scaleHeight[0] + ')')
      .call(d3.axisBottom(this.xScale))

    this.g.append('g')
      .attr('class', 'axis axis--y')
      .call(d3.axisLeft(this.yScale))
    .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 6)
      .attr('dy', '0.71em')
      .attr('text-anchor', 'end')
      .text(this.data.unit)
}

CQ.prototype.drawBarChart_Horizontal = function () {
    this.xScale.domain(this.data[this.majorName])
    let yMin = Infinity
    let yMax = -Infinity
    for (v of this.data.data_array) {
        yMin = 0
        yMax = Math.max(yMax, v[this.quantity])
    }
    this.yScale.domain([0, yMax])
    this.g.selectAll('.bar')
      .data(this.data.data_array)
      .enter().append('rect')
        .attr('class', 'bar')
        .classed('elements', true)
        .attr('y', d => this.xScale(this.data[this.majorName][d[this.majorName]]))
        .attr('x', d => 0)
        .attr('id', d => d['id'])
        .attr(this.quantity, d => d[this.quantity])
        .attr(this.majorName, d => d[this.majorName])
        .attr('fill', (d, i) => this.data.color[i])
        .attr('height', this.xScale.bandwidth())
        .attr('width', d => this.yScale(d[this.quantity]))

    this.g.append('g')
      .attr('class', 'axis axis--x')
      .call(d3.axisLeft(this.xScale))

    this.g.append('g')
      .attr('class', 'axis axis--y')
      // .attr('transform', 'translate(0,' + this.scaleHeight[0] + ')')

      .call(d3.axisTop(this.yScale))
    this.g.append('text')
        .attr('transform', 'translate(' + String(this.scaleWidth[1]) + ',0)')
        .attr('dy', '-1.2rem')
        .attr('text-anchor', 'end')
        .attr('font-size', this.height * (1 - 2 * marginRate) * fontRatio)
        .text(this.data.unit);
}

CQ.prototype.drawTitle = function (title) {
    let canvasHeight = this.height * (1 - 2 * marginRate)
    let canvasWidth = this.width * (1 - 2* marginRate)
    let fontSize = canvasHeight * fontRatio
    this.g.append('text')
          .attr('class', 'title')
          .attr('text-anchor', 'middle')
          .attr('font-size', fontSize * 1.5)
          .attr('x', canvasWidth / 2)
          .attr('y', - 2 * fontSize)
          .text(title)
    return this
}

function CCQ(data, cat_position, cat_color, quantity, position = 'vertical') {
    // initial chart set up
        this.svg = d3.selectAll('#visualization').selectAll('svg')
        this.height = this.svg.attr('height')
        this.width = this.svg.attr('width')
        this.g = this.svg.append('g')
                         .attr('transform', 'translate(' + this.width * marginRate + ',' + this.height * marginRate + ')')
        this.g.append('g')
                  .attr('class', 'brush')
   // database set up
        this.position = position
        this.data = data
        this.majorName = cat_position
        this.secondName = cat_color
        this.quantity = quantity
   // scale set up
        this.scaleHeight = [this.height * (1 - 2 * marginRate), 0]
        this.scaleWidth = [0, this.width * (1 - 2 * marginRate)]
        this.xScale = d3.scaleBand()
                        .padding(paddingValue)
                        .domain(this.data[this.majorName])
        this.yScale = d3.scaleLinear()
        if(this.position === 'horizontal') {
            this.xScale.rangeRound(this.scaleHeight)
            this.yScale.rangeRound(this.scaleWidth)
        }
        else {
            this.xScale.rangeRound(this.scaleWidth)
            this.yScale.rangeRound(this.scaleHeight)
        }
}

CCQ.prototype.drawAxis = function() {
    if (this.position === 'horizontal') {
        this.g.append('g')
              .attr('class', 'axis')
              .call(d3.axisLeft(this.xScale))

        this.g.append('g')
              .attr('class', 'axis')
              .attr('transform', 'translate(0,' + this.height * (1 - 2 * marginRate) + ')')
              .call(d3.axisBottom(this.yScale))
        this.g.append('text')
                  .attr('transform', 'translate(' + String(this.scaleWidth[1]) + ',' + this.scaleHeight[0] + ')')
                  .attr('dy', '-.2rem')
                  .attr('text-anchor', 'end')
                  .attr('font-size', this.height * (1 - 2 * marginRate) * fontRatio)
                  .text(this.data.unit)
        return this
      }
      this.g.append('g')
            .attr('class', 'axis')
            .attr('transform', 'translate(0,' + this.height * (1 - 2 * marginRate) + ')')
            .call(d3.axisBottom(this.xScale))

      this.g.append('g')
            .attr('class', 'axis')
            .call(d3.axisLeft(this.yScale))
      this.g.append('text')
                .attr('transform', 'rotate(-90)')
                .attr('y', 6)
                .attr('dy', '0.71em')
                .attr('text-anchor', 'end')
                .attr('font-size', this.height * (1 - 2 * marginRate) * fontRatio)
                .text(this.data.unit)
      return this
}



CCQ.prototype.drawStackBarChart = function(key) {
    // pre-processing for rect position
        let data = this.data[this.majorName].map(v => { return {[this.majorName]: v} })
        // let index = this.data[this.majorName].map(v => {return {}} )
        let index = {}
        let value = {}
        for (let majorName of this.data[this.majorName]) {
            index[majorName] = {}
            value[majorName] = {}
            for (let secondName of this.data[this.secondName]) {
                index[majorName][secondName] = null
                value[majorName][secondName] = null
            }
        }
        for (let d of this.data.data_array) {
              data[d[this.majorName]][this.data[this.secondName][d[this.secondName]]] = d[this.quantity]
              let majorIdx = d[this.majorName]
              let secondIdx = d[this.secondName]
              let majorName = this.data[this.majorName][majorIdx]
              let secondName = this.data[this.secondName][secondIdx]
              index[majorName][secondName] = d.id
              value[majorName][secondName] = d[this.quantity]
        }
    //    console.log(index,'LOG INDEX')
        let stack = d3.stack().keys(this.data[this.secondName]).order(d3.stackOrderNone).offset(d3.stackOffsetNone)
        let series = stack(data)
        let right = []
        let i = 0
       for (let second of series) {
            right.push([])
            for (let first of second) {
                right[i].push({'array': first, [this.majorName]: first.data[this.majorName], [this.secondName]: second.key})
            }
            ++i
       }
       // console.log(right, 'new Data')
    // scale domain
        let total = data.map(v => {
            let sum = 0
            this.data[this.secondName]
                .forEach(name => {
                  sum += v[name] })
                return sum})
        let maximum = d3.max(total)

        this.yScale.domain([0, maximum])

    // draw stack bar chart
        if (this.position === 'horizontal') {
            this.g.append('g')
                  .selectAll('g')
                  .data(right)
                  .enter()
                  .append('g')
                      .attr('fill', (d, i) => this.data.color[i])
                  .selectAll('rect')
                  .data(d => d)
                  .enter()
                  .append('rect')
                      .classed('bar', true)
                      .classed('elements', true)
                      .attr('id', d => String(index[d[this.majorName]][d[this.secondName]]))
                      .attr(this.majorName, d => this.data[this.majorName].indexOf(d[this.majorName]))
                      .attr(this.secondName, d => this.data[this.secondName].indexOf(d[this.secondName]))
                      .attr(this.quantity, d => value[d[this.majorName]][d[this.secondName]])
                      .attr('y', (d, i) => this.xScale(d[this.majorName]))
                      .attr('x', d => this.yScale(d.array[0]))
                      .attr('width', d => this.yScale(d.array[1]) - this.yScale(d.array[0]))
                      .attr('height',this.xScale.bandwidth())
            return this
        }
        else {
            this.g.append('g')
                  .selectAll('g')
                  .data(right)
                  .enter()
                  .append('g')
                      .attr('fill', (d, i) => this.data.color[i])
                  .selectAll('rect')
                  .data(d => d)
                  .enter()
                  .append('rect')
                      .classed('bar', true)
                      .classed('elements', true)
                      .attr('id', d => { return String(index[d[this.majorName]][d[this.secondName]])})
                      .attr(this.majorName, d => this.data[this.majorName].indexOf(d[this.majorName]))
                      .attr(this.secondName, d => this.data[this.secondName].indexOf(d[this.secondName]))
                      .attr(this.quantity, d => value[d[this.majorName]][d[this.secondName]])
                      .attr('x', (d, i) => this.xScale(d[this.majorName]))
                      .attr('y', d => this.yScale(d.array[1]))
                      .attr('height', d => this.yScale(d.array[0]) - this.yScale(d.array[1]))
                      .attr('width',this.xScale.bandwidth())
            return this
        }

}


CCQ.prototype.drawGroupBarChart = function() {
      let innerScale = d3.scaleBand().domain(this.data[this.secondName]).rangeRound([0,this.xScale.bandwidth()])
      let yMin = Infinity
      let yMax = -Infinity
      for (v of this.data.data_array) {
          yMin = 0
          yMax = Math.max(yMax, v[this.quantity])
      }
      console.log(yMax)
      console.log(yMin)
      this.yScale.domain([0, yMax])
      window.yScale = this.yScale
      // window.yScale.domain([yMin, yMax])
      // this.yScale.domain(extent(this.data.data_array, this.quantity))
      if (this.position === 'horizontal') {
            this.yScale.domain([0, yMax])
            this.g.append('g').attr('class', 'bars').selectAll('rect')
                  .data(this.data.data_array)
                  .enter()
                  .append('rect')
                    .attr('transform', d => 'translate(0,' + String(innerScale(this.data[this.secondName][d[this.secondName]])) + ')')
                    .attr('fill', (d, i) => this.data.color[d[this.secondName]])
                    .attr('id', d => d.id)
                    .attr(this.majorName, d => d[this.majorName])
                    .attr(this.secondName, d => d[this.secondName])
                    .attr(this.quantity, d => d[this.quantity])
                    .classed('bar', true)
                    .classed('elements', true)
                        .attr('x', 0)
                        .attr('y', d => this.xScale(this.data[this.majorName][d[this.majorName]]))
                        .attr('width', d => this.yScale(d[this.quantity]))
                        .attr('height', innerScale.bandwidth())
            return this
      }


      this.g.append('g').attr('class', 'bars').selectAll('rect')
            .data(this.data.data_array)
            .enter()
            .append('rect')
              .attr('transform', d => 'translate(' + String(innerScale(this.data[this.secondName][d[this.secondName]])) + ',0)')
              .attr('fill', (d, i) => this.data.color[d[this.secondName]])
              .attr('id', d => d.id)
              .attr(this.majorName, d => d[this.majorName])
              .attr(this.secondName, d => d[this.secondName])
              .attr(this.quantity, d => d[this.quantity])
              .classed('bar', true)
              .classed('elements', true)
                  .attr('x', d => this.xScale(this.data[this.majorName][d[this.majorName]]))
                  .attr('y', d => this.yScale(d[this.quantity]))
                  .attr('height', d => this.scaleHeight[0] - this.yScale(d[this.quantity]))
                  .attr('width', innerScale.bandwidth())

      return this
}

CCQ.prototype.drawTitle = function (title) {
    let canvasHeight = this.height * (1 - 2 * marginRate)
    let canvasWidth = this.width * (1 - 2* marginRate)
    let fontSize = canvasHeight * fontRatio
    this.g.append('text')
          .attr('class', 'title')
          .attr('text-anchor', 'middle')
          .attr('font-size', fontSize * 1.5)
          .attr('x', canvasWidth / 2)
          .attr('y', - fontSize / 2)
          .text(title)
    return this
}

CCQ.prototype.drawLegend = function (cat_color) {
        let canvasHeight = this.height * (1 - 2 * marginRate)
        let canvasWidth = this.width * (1 - 2 * marginRate)
        let legendHeight = canvasHeight * legendHeightRatio
        let fontSize = canvasHeight * fontRatio
        let rectHeight = legendHeight * .9
        let rectWidth = canvasWidth * .03
        let cell = this.data[cat_color].map((d, i) => ({'name': d, 'color': this.data.color[i]}))
        let canvas =  this.g.append('g')
                        .attr('transform', 'translate(' + canvasWidth + ',0)')
                        .attr('class', 'legend-wrap')
        let legends = canvas.selectAll('.legend')
                            .data(cell)
                            .enter()
                            .append('g')
                            .attr('transform', (d, i) => 'translate(0,' + i * legendHeight + ')' )
        legends.append('rect')
              .attr('width', rectWidth)
              .attr('height', rectHeight)
              .attr('fill', d => d.color)
        legends.append('text')
              .attr('x', rectWidth + .2 * fontSize)
              .attr('y', fontSize)
              .attr('text-anchor', 'start')
              .attr('font-size', fontSize)
              .text(d => d.name)
        return canvas
}

function load_stack_bar_chart (data, cat_position, cat_color, quantity) {
    chart = new CCQ(data, cat_position, cat_color, quantity)
    chart.drawStackBarChart(cat_color)
    chart.drawTitle(data.title)
    chart.drawLegend(cat_color)
    chart.drawAxis()
}

function load_stack_bar_chart_horizontal (data, cat_position, cat_color, quantity) {
    chart = new CCQ(data, cat_position, cat_color, quantity, 'horizontal')
    console.log(chart.data)
    chart.drawStackBarChart(cat_color)
    chart.drawTitle(data.title)
    chart.drawLegend(cat_color)
    chart.drawAxis()
}

function load_bar_chart_1d(data, cat_position, cat_color, quantity) {
    let chart = new CQ(data, cat_position, cat_color, quantity)
    chart.drawBarChart()
    chart.drawTitle(data.title)
}

function load_bar_chart_1d_horizontal(data, cat_position, cat_color, quantity) {
    let chart = new CQ(data, cat_position, cat_color, quantity, 'horizontal')
    chart.drawBarChart()
    chart.drawTitle(data.title)
}

function load_group_bar_chart(data, cat_position, cat_color, quantity) {
    chart = new CCQ(data, cat_position, cat_color, quantity)
    chart.drawGroupBarChart()
    chart.drawTitle(data.title)
    chart.drawLegend(cat_color)
    chart.drawAxis()
}

function load_group_bar_chart_horizontal (data, cat_position, cat_color, quantity) {
    chart = new CCQ(data, cat_position, cat_color, quantity, 'horizontal')
    chart.drawGroupBarChart()
    chart.drawTitle(data.title)
    chart.drawLegend(cat_color)
    chart.drawAxis()
}
