$(document).ready(function() {
    $('.event_btn').on('dblclick', function(event) {
        //trigger modal for editing / deleting
        var my_btn = $(this);
        $('#edit_dynamic_event').modal('show');
        $('#dynamic_event_title').val(my_btn.text());

        //get current date
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;
        var yyyy = today.getFullYear();
        if (dd<10) { dd = '0'+dd }
        if (mm<10) { mm = '0'+mm }
        today = yyyy + '-' + mm + '-' + dd;
        $('#dynamic_event_date').attr('min', today)
    })

    $('#add_dynamic_event_btn').on('click', function(event) {
        $('#add_dynamic_event').modal('show');
    })

    $('#add_dynamic_event_save').on('click', function(event) {
        
    })
})
