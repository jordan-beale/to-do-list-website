$().ready(function(){

$('#form').validate({

    rules : {
        username  : {
        required  : true,
        minlength : 3,
        maxlength : 16
        },
        password  : {
        required  : true,
        minlength : 3,
        maxlength : 16
        }
    },

    messages : {
        username  : {
        required  : "Please enter a username",
        minlength : "Your username must consist of at least 3 characters",
        maxlength : "Your username must consist of at most 16 characters"
        },
        password  : {
        required  : "Please enter a password",
        minlength : "Your password must be consist of at least 3 characters",
        maxlength : "Your username must consist of at most 16 characters"
        }
    }

})
});