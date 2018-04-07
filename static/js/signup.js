$(document).ready(function() {
    $('#signup').on('click', function(event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        $.ajax({
            url: '/signup_post',
            method: 'post',
            data: {
                'username': username,
                'password': password,
            },
            error: function(err) {
                console.log("got an error", err);
            },
            success: function(res) {
                window.location = "/login"
            }
        })
    })
})
