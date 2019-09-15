function upload_information(){
    // $.ajax({
    //     url: "http://localhost:5000/",
    //     type: "GET",
    //     // dataType: 'JSONP',
    //     success:function(result){
    //     console.log(result)
    // }});
    content = d3.select("svg")._groups[0][0].outerHTML
    svg_content = {name: "svg", content: content }
    print(svg_content)

    $.ajax({
        type: 'POST',
        url: "heiheihei",
        data: svg_content,
        dataType: 'json',
        success: function(evt_data) {
            window._evt_data = evt_data
            console.log(evt_data)
            // alert(evt_data)
            // self.parseData(data)
        },
        error: function(jqXHR) {
            // $('.loading').hide()
            alert('hhhh')
        },
    })
}
