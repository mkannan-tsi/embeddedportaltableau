$(function() {
    $('#btnLogin').click(function() {
 
        $.ajax({
            url: '/login',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                top.location.href = "/"+response;             
                       },
            error: function(error) {
                console.log(error);
            }
        });
    });
});