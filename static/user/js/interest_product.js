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
                        alert('관심되었습니다.');
                    } else {
                        //alert('ERROR!');
                    }
                },
                error: function() {
                    alert('ERROR!');
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
                        alert('관심 취소되었습니다.');
                        location.reload();
                    } else {
                        //alert('ERROR!');
                    }
                },
                error: function() {
                    alert('ERROR!');
                }
            });
        });
    });
})();