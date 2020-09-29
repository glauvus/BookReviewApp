//on load
$(function () {
    //if enter key is pressed, make a get request
    //passing the text from the search field
    $("#searchField").keyup(function(e){
        if(e.keyCode==13) {
            var textToSearch = $(this).val();
            $.getJSON("/"+textToSearch, function(data) {
                createBookTable(data);
            })
        }
    });
});

//function to render a table from the response json data
function createBookTable(data) {
    $("#tableHead").empty();
    $("#tableBody").empty();
    if(data.length<1) {
        $("#noResultsAlert").html("No books found!");
    } else {
        $("#noResultsAlert").empty();
        $("#tableHead").html("<tr><th scope=\"col\">ISBN</th> \
                            <th scope=\"col\">Title</th> \
                            <th scope=\"col\">Author</th> \
                            <th scope=\"col\">Year</th></tr>");
        for(var i=0; i<data.length; i++) {
            var isbn = data[i].isbn;
            var title = data[i].title;
            var author = data[i].author;
            var year = data[i].year;
        
            $("#tableBody").append("<tr><td>"+isbn+"</td> \
                                        <td>"+title+"</td> \
                                        <td>"+author+"</td> \
                                        <td>"+year+"</td></tr>");
        }
    }
}