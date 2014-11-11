$(function () {

    $('#report-btn').click(function (e) {
        e.preventDefault();

        var errorMessage = null;

        var options = [];

        $.each($('fieldset[data-role="controlgroup"] :checked'), function (index) {
            options.push($(this).val());
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
                if (data.success) {
                    alert('request success!');
                }
            }

        });

    });
});