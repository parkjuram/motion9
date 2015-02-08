/*
<script type="text/javascript">
    var urlForSurveyAgain = "{% url 'survey_again' %}"
</script>

<script src="{% static 'user/js/survey.js' %}"></script>

class="btn-survey-again"

*/
(function() {
    $(function() {
        $('.btn-survey-again').click(function() {
            var currentDomObject = $(this);
            var item = "";
            $(".again-item:checked").each( function() {
               item += $(this).val() + "|";
            });
            var reason = $('#text-reason').text().trim();
            var comments = $('#text-comments').text().trim();

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
    });
})();