function init_change_vis(){
  // var margin = {top: 20, right: 20, bottom: 20, left: 20 }
  var width = document.getElementById("change_vis").clientWidth
  var height = document.getElementById("change_vis").clientHeight
  var margin_value = width / 20
  var margin = {top: margin_value, right: margin_value, bottom: margin_value, left: margin_value }
  width = width - margin.left - margin.right
  height = height - margin.top - margin.bottom
  var svg = d3.select("#change_vis").append("svg")
      .attr("id", "change_button")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .on("click",function(d){
        change_vis()
      })
  change_data()
}
function change_vis(){
  change_data()
  load_bar_chart()
}
function change_data(){
  var number = Math.floor(Math.random() * 7) + 3;
  var name = ["Africa","Banama","China","Dutch","England","France","Ganna","Holand","Ireland","Russia"]
        .slice(0,number)

  var value = new Array();
  for (var i = 0; i < number; i ++ ){
    value[i] = Math.random() * 100
  }

  data = build_data(name, value);
}
