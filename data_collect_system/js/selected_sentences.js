function update_selected_sentence(sentences){
  var sentence_container = d3.selectAll('#selected_sentences_div')

  var width = document.getElementById('selected_sentences_div').clientWidth
  var height = document.getElementById('selected_sentences_div').clientHeight
  // console.log("sentence_show")
  sentence_container.selectAll(".selected_sentence").remove()

  var sentences = sentence_container.selectAll('.selected_sentence')
      .data(sentences)
      .enter()
      .append("div")
      .attr("class", "selected_sentence")
      .text(function(d){
        return d.sentence
      })
      .on("mouseover", function(d){
        d3.select(this).classed("hightlight", true)
        d3.selectAll('.elements')
          .each(function(q){
            var this_id = parseInt(d3.select(this).attr('id'))
            if (d.focus_id.includes(this_id)){
              this_element = d3.select(this)
              this_element.classed("focus", true)
              this_element.classed("compare", false)
              this_element.classed("none", false)
            }
            else if (d.compare_id.includes(this_id)){
              this_element = d3.select(this)
              this_element.classed("focus", false)
              this_element.classed("compare", true)
              this_element.classed("none", false)
            }
            else {
              this_element = d3.select(this)
              this_element.classed("focus", false)
              this_element.classed("compare", false)
              this_element.classed("none", true)
            }
          })
      })
      .on("mouseout", function(d){
        d3.select(this).classed("hightlight", false)
        refrush_all_element()

      })
      .on("click", function(d){
        // reload_selection()
      })
}
// function
