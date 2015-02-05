(function() {
    $(function() {
        $('#btn-interest').click(function() {
            $.ajax({
                url: urlForDoInterest,
                dataType: 'json',
                type: 'POST',
                data: {
                    product_id: $(this).attr('product-id'),
                    user_survey_id: $(this).attr('user-survey-id')
                },
                success: function(data) {
                    alert('success');
                },
                error: function() {
                    alert('error');
                }
            });
        });
    });
})();