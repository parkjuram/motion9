$(function () {

    $('#btn-request-survey-finish').on('click', survey_finish );

    function survey_finish(e) {
        e.preventDefault();
        var that = $(this);
        that.off('click');

        var options = [];
        var url = $(this).attr('url');

        $.each( $('fieldset[data-role="controlgroup"] :checked'), function( index ) {
           options.push( $(this).val() );
        });

        if(options.length < $(this).attr('survey_length')){
            alert('설문이 완료되지 않았습니다.');
            that.on('click', survey_finish);
        }else {
            $.ajax({
                url: urlRequestSurvey,
                dataType: 'json',
                type: 'POST',
                data: {
                    'survey_id': $(this).attr('survey_id'),
                    'preference_brand': $('#report-preference-brand').val().trim(),
                    'comments': $('#reportText').val().trim(),
                    'options': options
                },
                success: function (data) {
                    console.log(data);
                    if (data.success) {
                        alert('설문이 완료되었습니다.\n분석에는 1~2일이 소요됩니다.\n분석이 완료되면 이메일로 알려드리겠습니다.');
                        window.location.href = url;
                    }
                },
                complete: function( jqXHR, textStatus ) {
                    that.on('click', survey_finish);
                }
            });
        }

        return false;

    }

});