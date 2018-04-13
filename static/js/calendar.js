$(document).ready(function() {
    $('.event_btn').on('dblclick', function(event) {
        //trigger modal for editing / deleting
        var my_btn = $(this);
        $('#edit_dynamic_event').modal('show');
        $('#dynamic_event_title').val(my_btn.text());
        $('#dynamic_event_due_date').val(my_btn.attr('due_date'));
        $('#dynamic_event_duration').val(my_btn.attr('duration'));
        $('#edit_dynamic_event').attr('event_id', my_btn.attr('event_id'));
    })

    $('#update_dynamic_event').on('click', function(event) {
        var url_split = window.location.href.split('/');
        var user_id = url_split[url_split.length - 1];
        var event_id = $('#edit_dynamic_event').attr('event_id');
        var title = $('#dynamic_event_title').val();
        var due_date = $('#dynamic_event_due_date').val();
        var duration = $('#dynamic_event_duration').val();
        $.ajax({
            url: '/update_dynamic_event/' + user_id,
            method: 'put',
            data: {
                'event_id': event_id,
                'title': title,
                'due_date': due_date,
                'duration': duration
            },
            error: function(err) {
                console.log("got an error", err);
            },
            success: function(res) {
                $('#edit_dynamic_event').modal('hide');
            }
        })
    })

    $('#delete_dynamic_event').on('click', function(event) {
        var url_split = window.location.href.split('/');
        var user_id = url_split[url_split.length - 1];
        var event_id = $('#edit_dynamic_event').attr('event_id');
        $.ajax({
            url: '/delete_dynamic_event/' + user_id,
            method: 'delete',
            data: {
                'event_id': event_id
            },
            error: function(err) {
                console.log("got an error", err);
            },
            success: function(res) {
                $('#edit_dynamic_event').modal('hide');
            }
        })
    })

    $('#add_dynamic_event_btn').on('click', function(event) {
        $('#add_dynamic_event').modal('show');
        //get current date
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;
        var yyyy = today.getFullYear();
        if (dd<10) { dd = '0'+dd }
        if (mm<10) { mm = '0'+mm }
        today = yyyy + '-' + mm + '-' + dd;
        $('#add_dynamic_event_due_date').attr('min', today)
    })

    $('#add_dynamic_event_save').on('click', function(event) {
        var url_split = window.location.href.split('/');
        var user_id = url_split[url_split.length - 1];
        var title = $('#add_dynamic_event_title').val();
        var due_date = $('#add_dynamic_event_due_date').val();
        var duration = $('#add_dynamic_event_duration').val();
        $.ajax({
            url: '/add_dynamic_event/' + user_id,
            method: 'post',
            data: {
                'title': title,
                'due_date': due_date,
                'duration': duration
            },
            error: function(err) {
                console.log("got an error", err);
            },
            success: function(res) {
                $('#add_dynamic_event').modal('hide');
            }
        })
    })
})
