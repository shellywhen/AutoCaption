var select_thing = [];
var data;
var data_json;
var element_status;
var current_select = "focus";
var selected_sentences = new Array();
var major_name;
var second_name;
var user_name;
var total_number = 0;
var is_show = false
var need_login = true
var data_type = 'ocq'
var super_limit = false 

function init_element_status(data){
  data_number = data.data_array.length
  element_status = new Array()
  for (var i = 0; i < data_number; i ++ )
  {
    var element = new Array()
    element['id'] = i
    element['focus'] = false
    element['compare'] = false
    element_status[i] = element
  }
}
function click_on_id(id){
  if (element_status[id][current_select]){
    element_status[id][current_select] = false
  }
  else{
    element_status[id][current_select] = true
  }
}
function get_status_by_id(id){
  if (element_status[id]["focus"])
  {
    return "focus"
  }
  else if( element_status[id]['compare'])
  {
    return 'compare'
  }
  return "none"
}
function refrush_all_element(){

  var number_elements = element_status.length
  var number_hightlight = 0
  for( var i = 0; i < number_elements; i ++ )
  {
    var status = get_status_by_id(i)
    if (status == 'focus' ||  status == 'compare')
    {
      number_hightlight ++
    }
  }
  if (number_hightlight === 0 )
  {
    d3.selectAll(".elements")
      .classed("focus", false)
      .classed("compare", false)
      .classed("none", false)
  }
  else{
    d3.selectAll(".elements")
      .each(function(d){
        var this_element = d3.select(this)
        var this_id = parseInt(this_element.attr("id"))
        if (get_status_by_id(this_id) == "focus"){
          this_element.classed("focus", true)
          this_element.classed("compare", false)
          this_element.classed("none", false)
          // d3.select(this).classed("none", false)
        }
        else if (get_status_by_id(this_id) == "compare"){
          this_element.classed("focus", false)
          this_element.classed("compare", true)
          this_element.classed("none", false)
          // d3.select(this).classed("none", false)
        }
        else{
          this_element.classed("focus", false)
          this_element.classed("compare", false)
          this_element.classed("none", true)
        }
      })
  }
}
function reload_selection(){
  var element_num = element_status.length
  for (var i = 0; i < element_num; i ++ ){
    element_status[i]['id'] = i
    element_status[i]['focus'] = false
    element_status[i]['compare'] = false
  }
  current_select = 'focus'
  refresh_focus_compare()
  d3.selectAll(".elements")
    .classed("focus", false)
    .classed("compare", false)
    .classed("none", false)

  d3.selectAll('#sentences_div')
    .selectAll('.sentence')
    .remove()
  // send_data_and_setting()
}
