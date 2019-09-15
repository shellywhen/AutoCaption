
function loggin(event){
  var name = document.getElementById("name").value
  if (name.length === 0 )
  {
    return false
  }
  else {
    user_name = name
    user_name_array = user_name.split('_')
    d3.select("#all").selectAll("#form").remove()
    if (user_name_array.indexOf('oq') > -1){
      data_type = 'oq'
    }
    if (user_name_array.indexOf('ocq') > -1){
      data_type = 'ocq'
    }
    if (user_name_array.indexOf('super') > -1){
      super_limit = true
    }
    if (user_name_array.indexOf('rule') > -1){
      data_type = 'rule'
    }
    if (user_name_array.indexOf('admin') > -1){
      is_show = true
    }
    initialize()
  }
  return false
}
