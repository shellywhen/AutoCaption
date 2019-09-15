function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo() {
  await sleep(40000);
}

let load_save = function(data, path) {
  let filename = path.slice(14)
  if (data['data']['vis_type'] == "load_stack_bar_chart" || data['data']['vis_type']=="load_stack_bar_chart_horizontal") {
      return;
  }
  cur.init(data.data)
  cur.initChart()
  SVG_string = d3.select('svg').node().outerHTML
  let send_data = {
    'svg': SVG_string,
    'path': '../show_system/data/train/'+ filename,
    'save': '../show_system/data/SVG/'+ filename
  }
  $.ajax({
      type: 'POST',
      url: "vis2description/get_file_name",
      data: send_data,
      dataType: 'json',
      success: function(d) {
          console.log('Successfully saving'+ send_data)
      },
      error: function(e) {
          console.log('ERROR!')
      },
  })
}

let generate_svg_data = function(fileList) {
    // fileList = fileList.slice(0, 12)
    task = d3.queue()
    for(filename of fileList) {
        let path = '../data/train/' + filename
        task.defer(d3.json, path, d => load_save(d, path))
     }
}

function show_result(page, interval) {
  $.ajax({
      type: 'GET',
      url: "vis2description/get_file_name",
      success: function(data_pack) {
        fileList = data_pack.slice(page, page+interval)
        let task = d3.queue()
        for(filename of fileList) {
            let path = '../data/SVG/' + filename
            task.defer(d3.json, path, function(d) {
              let filename = path.slice(12)
              console.log('hey!!!', path)
              if (d['vis_type'] == "load_stack_bar_chart") {
                  return;
              }
              let svg_string = d['svg_string']
                $('svg').prop('outerHTML', svg_string)
            })
        }
      },
      error: function(jqXHR) {
          alert('WHAT THE HECK IS WRONG WITH SHOW RESULT?')
      },
})
}

function show(svg) {
    $('svg').prop("outerHTML", svg)
}
