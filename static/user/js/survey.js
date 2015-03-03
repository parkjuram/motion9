/*
<script type="text/javascript">
    var urlForSurveyAgain = "{% url 'survey_again' %}"
</script>

<script src="{% static 'user/js/survey.js' %}"></script>

class="btn-survey-again"

*/
(function() {
    $(function() {

        $('.again-item[value="all"]').change(function() {
            var allChecked = $(this).is(":checked");
            $('.again-item').each( function() {
                $(this).prop('checked', allChecked);
            });
        });

        $('.again-item').change(function() {
            var isChecked = $(this).is(":checked");
            if ( !isChecked ) {
                $('.again-item[value="all"]').prop('checked', false);
            }
        });

        $('.btn-survey-again').click(function() {
            var currentDomObject = $(this);
            var item = "";
            $(".again-item:checked").each( function() {
               item += $(this).val() + "|";
            });
            var reason = $('#text-reason').val().trim();
            var comments = $('#text-comments').val().trim();

            $.ajax({
                url: urlForSurveyAgain,
                dataType: 'json',
                type: 'POST',
                data: {
                    user_survey_id: $(this).attr('user-survey-id'),
                    item: item,
                    reason: reason,
                    comments: comments
                },
                success: function(data) {
                    if ( data.success ) {
                        alert('Success');
                    } else {
                        alert('Fail');
                    }
                },
                error: function() {
                    alert('Fail');
                }
            });
        });

        $('.btn-request-more').click(function() {
            $.ajax({
                url: urlForMoreRequest,
                dataType: 'json',
                type: 'POST',
                data: {
                    user_survey_id: $(this).attr('user-survey-id'),
                    comments: $('#text-more-comments').val().trim()
                },
                success: function(data) {
                    if ( data.success ) {
                        alert('Success');
                    } else {
                        alert('Fail');
                    }
                },
                error: function() {
                    alert('Fail');
                }
            });
        });
    });
})();