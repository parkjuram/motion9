$(function () {

    $('#report-btn').click(function (e) {
        e.preventDefault();

        var options = [];
        var dialog = $('#productDetailDialog');

        $.each( $('fieldset[data-role="controlgroup"] :checked'), function( index ) {
           options.push( $(this).val() );
        });

        $.ajax({
            url: urlRequestSurvey,
            dataType: 'json',
            type: 'POST',
            data: {
                'survey_id': $(this).attr('survey_id'),
                'comments': $('#reportText').val().trim(),
                'options': options
            },
            success: function (data) {
               console.log(data);
                if (data.success) {
                   dialog.popup('open');
                   alert('test');
                }
            }
        });

    });

});