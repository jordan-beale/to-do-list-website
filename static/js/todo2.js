$().ready(function(){


$('#addForm').submit(function(){
    var itemName = $("#itemName").val();
    var listName = $("#listName").val();

    //$('#'+listName).append("<li> <a>✗</a> <button>CLICK TO COMPLETE/ UNCOMPLETE</button></li>");

    $.post("/addItem",
        {itemName: itemName, listName, listName}
    );
})

});