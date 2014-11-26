$(function () {

    $('#report-btn').click(function (e) {
        e.preventDefault();

        var options = [];
        var url = $(this).attr('url');

        $.each( $('fieldset[data-role="controlgroup"] :checked'), function( index ) {
           options.push( $(this).val() );
        });

        if(options.length < $(this).attr('survey_length')){
            alert('설문이 완료되지 않았습니다.');

        }else {
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
                        alert('보고서 요청이 완료되었습니다.');
                        location.href = url;
                    }
                }
            });
        }

    });

});