$().ready(function(){

$(function() {

    $(".button").click(function( event ) {
        var id = $(this).attr("id");
        if ($("#"+id+"text").html() == "✗"){
            $("#"+id+"text").html("✓");
            $.get("/changeItem?q=" + "✓ " + id);
        }else{
            $("#"+id+"text").html("✗");
            $.get("/changeItem?q=" + "✗ " + id);
        }
    })

})
});