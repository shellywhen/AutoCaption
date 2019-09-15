function init_show_sentence(){
  var width = document.getElementById("sentences_div").clientWidth
      height = document.getElementById("sentences_div").clientHeight

}

function show_sentence(sentences){
  var sentence_container = d3.selectAll('#sentences_div')

  var width = document.getElementById('sentences_div').clientWidth
  var height = document.getElementById('sentences_div').clientHeight
  // console.log("sentence_show")
  sentence_container.selectAll(".sentence").remove()

  var sentences = sentence_container.selectAll('.sentence')
      .data(sentences)
      .enter()
      .append("div")
      .attr("class", "sentence")
      .text(function(d){
        return d.sentence
      })
      .on("mouseover", function(d){
        d3.select(this).classed("hightlight", true)
        d3.selectAll('.elements')
          .each(function(q){
            this_element = d3.select(this)
            this_id = parseInt(this_element.attr('id'))
            if (d.focus_id.includes(this_id)){
              this_element.classed("focus", true)
              this_element.classed("compare", false)
              this_element.classed("none", false)
            }
            else if (d.compare_id.includes(this_id)){
              this_element.classed("focus", false)
              this_element.classed("compare", true)
              this_element.classed("none", false)
            }
            else {
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
        selected_sentences.push(d)
        reload_selection()
        update_selected_sentence(selected_sentences)
      })

}
