/*
<script type="text/javascript">
    var urlForDoInterest = "{% url 'do_interest_product' %}";
    var urlForUndoInterest = "{% url 'undo_interest_product' %}";
</script>

<script src="{% static 'user/js/interest_product.js' %}"></script>
*/
(function() {
    $(function() {
        $('.btn-interest').click(function() {
            var currentDomObject = $(this);
            $.ajax({
                url: urlForDoInterest,
                dataType: 'json',
                type: 'POST',
                data: {
                    product_id: $(this).attr('product-id'),
                    user_survey_id: $(this).attr('user-survey-id')
                },
                success: function(data) {
                    if ( data.success ) {
                        currentDomObject.text("관심완료");
                        alert('Interest Success');
                    } else {
                        alert('Interest Fail');
                    }
                },
                error: function() {
                    alert('Interest Fail');
                }
            });
        });

        $('.btn-undo-interest').click(function() {
            var currentDomObject = $(this);
            $.ajax({
                url: urlForUndoInterest,
                dataType: 'json',
                type: 'POST',
                data: {
                    interest_id: $(this).attr('interest-id'),
                },
                success: function(data) {
                    if ( data.success ) {
                        alert('Undo Success');
                        location.reload();
                    } else {
                        alert('Undo Fail');
                    }
                },
                error: function() {
                    alert('Undo Fail');
                }
            });
        });
    });
})();