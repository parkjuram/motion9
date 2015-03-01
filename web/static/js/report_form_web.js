$(function () {

    $('#btn-request-survey-finish').click(function (e) {
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
                    'preference_brand': $('#report-preference-brand').val().trim(),
                    'comments': $('#reportText').val().trim(),
                    'options': options
                },
                success: function (data) {
                    console.log(data);
                    if (data.success) {
                        alert('설문이 완료되었습니다.\n분석에는 1~2일이 소요됩니다.\n분석이 완료되면 이메일로 알려드리겠습니다.');
                        location.href = url;
                    }
                }
            });
        }

    });

    $('.black-btn').click(function (e) {

        var btn_id = $(this).attr('id');
        var current_page_id = $('#'+$(this).attr('page_id'));
        var next_page_id = $('#page-num-'+btn_id);

        current_page_id.css('display',"none");
        next_page_id.css('display',"block");

    });



});

window.onload = function() {
    var page_id = $('#page-num-0');
    page_id.css('display',"block");
};