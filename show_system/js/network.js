function send_data_and_setting(){

  var focus_id = new Array()
  var compare_id = new Array()
  element_num = element_status.length
  for (var i = 0; i < element_num; i ++ )
  {
    var status_of_i = get_status_by_id(i)
    if (status_of_i === 'focus')
    {
      focus_id.push(i)
    }
    else if (status_of_i === 'compare')
    {
      compare_id.push(i)
    }
  }

  if (focus_id.length > 0 )
  {

    var send_data = {
      data: JSON.stringify(data_json),
      focus_id: JSON.stringify(focus_id),
      compare_id: JSON.stringify(compare_id),
      major_name: major_name,
      second_name: second_name
    }
    // send_data["data"] = JSON.stringify(data_json)
    // send_data["focus_id"] = JSON.stringify(focus_id)
    // send_data["compare_id"] = JSON.stringify(compare_id)
    //console.log("send data:  ", send_data)
    get_sentence(send_data)
  }
}
function get_sentence(send_data){

  console.log()

  $.ajax({
      type: 'POST',
      url: "vis2description/getsentence",
      data: send_data,
      dataType: 'json',
      success: function(evt_data) {
          window._evt_data = evt_data
        //  console.log('sentence', evt_data)
          show_sentence(evt_data)

          // if (data_type === 'rule'){
          //   var this_sentences = []
          //   var length = evt_data.length
          //   for (var i = 0; i < length; i ++ )
          //   {
          //     if (evt_length[i].type === 'compare_trend'){
          //       this_sentences.append(evt_length[i])
          //     }
          //
          //   }
          //   console.log(this_sentences)
          //   show_sentence(this_sentences)
          // }
          // else {
          //   show_sentence(evt_data)
          // }
      },
      error: function(jqXHR) {
          // $('.loading').hide()
          alert('There is something wrong with our server')
      },
  })
}
function submit_answer(send_data){
  $.ajax({
      type: 'POST',
      url: "vis2description/submit_answer",
      data: send_data,
      dataType: 'json',
      success: function(evt_data) {
          // alert('Thank You! Submit Success!')
          // show_sentence(evt_data)
      },
      error: function(jqXHR) {
          // $('.loading').hide()
          alert('Submit Failed')
      },
  })
}
function get_data_json(send_data){
  $.ajax({
      type: 'POST',
      url: "vis2description/get_data_json",
      data: send_data,
      success: function(evt_data) {
        console.log(JSON.stringify(evt_data))
        console.log(evt_data)
        randomDraw(evt_data)
        SVG_string = d3.select('#visualization').node().innerHTML
        // send_data = {
        //   data_string: JSON.stringify(cur.data),
        //   svg_string: SVG_string,
        //   major_name: cur.major,
        //   second_name: cur.second
        // }
        // get_machine_answer(send_data)

        SVG_string = d3.select('#visualization').node().innerHTML
        send_data = {'svg_string': SVG_string}
        //console.log(send_data)
        get_modify_svg_from_server(send_data)
        // deal_with_data(evt_data)
        // alert('Thank You! Submit Success!')
          // show_sentence(evt_data)
      },
      error: function(jqXHR) {
          // $('.loading').hide()
          alert('Get data failed')
      },
  })
}
function get_machine_answer(send_data){
  $.ajax({
      type: 'POST',
      url: "vis2description/get_machine_answer",
      data: send_data,
      dataType: 'json',
      success: function(sentences) {
        //console.log(sentences)
        showSentences(sentences)
      },
      error: function(jqXHR) {
          // $('.loading').hide()
          alert('Submit Failed')
      },
  })
}
