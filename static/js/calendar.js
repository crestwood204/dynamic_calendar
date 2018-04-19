$(document).ready(function() {
    // To-do-list functionality

    $('.event_btn_d').on('dblclick', function(event) {
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
                console.log(res)
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
                console.log(res)
            }
        })
    })

    //Calendar functionality

    $('#add_static_event_btn').on('click', function(event) {
        $('#add_static_event').modal('show');
        //get current date
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;
        var yyyy = today.getFullYear();
        var time = today.getTime();
        var hh = today.getHours();
        var min = today.getMinutes();
        if (dd<10) { dd = '0' + dd }
        if (mm<10) { mm = '0' + mm }
        if (hh<10) { hh = '0' + hh }
        if (min<10) { mm = '0' + mm}
        today = yyyy + '-' + mm + '-' + dd;
        time = hh + ':' + min
        console.log(today)
        console.log(time)
        $('#add_static_event_start_date').val(today)
        $('#add_static_event_start_time').val(time)

        if (hh == 23) {
            hh = 0;
            today.setDate(currentDate.getDate() + 1)
            dd = today.getDay();
            if (dd<10) { dd = '0' + dd }
            mm = today.getMonth() + 1;
            if (mm<10) { mm = '0' + mm }
            yyyy = today.getFullYear();
        } else {
            hh = parseInt(hh) + 1
        }

        if (hh<10) { hh = '0' + hh }
        today = yyyy + '-' + mm + '-' + dd;
        time = hh + ':' + min
        $('#add_static_event_end_date').val(today)
        $('#add_static_event_end_time').val(time)
    })

    $('#add_static_event_save').on('click', function(event) {
        var url_split = window.location.href.split('/');
        var user_id = url_split[url_split.length - 1];
        var title = $('#add_static_event_title').val();
        var start_date = $('#add_static_event_start_date').val();
        var start_time = $('#add_static_event_start_time').val();
        var end_date = $('#add_static_event_end_date').val();
        var end_time = $('#add_static_event_end_time').val();
        $.ajax({
            url: '/add_static_event/' + user_id,
            method: 'post',
            data: {
                'title': title,
                'start_date': start_date,
                'start_time': start_time,
                'end_date': end_date,
                'end_time': end_time
            },
            error: function(err) {
                console.log("got an error", err);
            },
            success: function(res) {
                $('#add_static_event').modal('hide');
            }
        })
    })

    $('.event_btn_s').on('dblclick', function(event) {
        var my_btn = $(this);
        if (my_btn.attr('event_type') == 'static') {
            $('#edit_static_event').modal('show')
            $('#edit_static_event_title').val(my_btn.attr('event_title'));
            $('#edit_static_event_start_date').val(my_btn.attr('start_date'));
            $('#edit_static_event_end_date').val(my_btn.attr('end_date'));
            $('#edit_static_event_start_time').val(my_btn.attr('start_time'));
            $('#edit_static_event_end_time').val(my_btn.attr('end_time'));
            $('#edit_static_event').attr('event_id', my_btn.attr('event_id'));
        }
    })

    $('#edit_static_event_save').on('click', function(event) {
        var url_split = window.location.href.split('/');
        var user_id = url_split[url_split.length - 1];
        var event_id = $('#edit_static_event').attr('event_id');
        var title = $('#edit_static_event_title').val();
        var start_date = $('#edit_static_event_start_date').val();
        var end_date = $('#edit_static_event_end_date').val();
        var start_time = $('#edit_static_event_start_time').val();
        var end_time = $('#edit_static_event_end_time').val();
        $.ajax({
            url: '/update_static_event/' + user_id,
            method: 'put',
            data: {
                'event_id': event_id,
                'title': title,
                'start_date': start_date,
                'end_date': end_date,
                'start_time': start_time,
                'end_time': end_time,
            },
            error: function(err) {
                console.log("got an error", err);
            },
            success: function(res) {
                $('#edit_static_event').modal('hide');
                console.log(res)
            }
        })
    })

    $('#delete_static_event').on('click', function(event) {
        var url_split = window.location.href.split('/');
        var user_id = url_split[url_split.length - 1];
        var event_id = $('#edit_static_event').attr('event_id');
        $.ajax({
            url: '/delete_static_event/' + user_id,
            method: 'delete',
            data: {
                'event_id': event_id
            },
            error: function(err) {
                console.log("got an error", err);
            },
            success: function(res) {
                $('#edit_static_event').modal('hide');
                console.log(res)
            }
        })
    })

})
