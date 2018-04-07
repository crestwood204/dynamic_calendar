$(document).ready(function() {
    $('#login').on('click', function(event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        $.ajax({
            url: '/login_post',
            method: 'post',
            data: {
                'username': username,
                'password': password,
            },
            error: function(err) {
                console.log("got an error", err);
            },
            success: function(res) {
                window.location = "/calendar"
            }
        })
    })
})
