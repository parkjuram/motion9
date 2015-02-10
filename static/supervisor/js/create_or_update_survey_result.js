(function() {

    $(function() {
        var btnEnterToDatabase = $('#btn-enter-to-database');

        btnEnterToDatabase.click(function() {
            var selectedProductList = [];
            $('#table-product-list tr').each(function (index, object) {
                if ($(object).find(".is-apply:checked").length > 0) {
                    var productId = $(object).attr("product-id");
                    var type = $(object).attr("select-type");

                    selectedProductList.push( {
                        'product-id': productId,
                        'type': type
                    });
                }
            });

            var generalReview = $('#textarea-general-review').val();
            var budgetMin = $('#budget-min').val();
            var budgetMax = $('#budget-max').val();
            var additionalComment = $('#textarea-additional-comment').val();

            $.ajax({
                url: urlForCreateOrUpdateSurveyResult,
                dataType: 'json',
                type: 'POST',
                data: {
                    general_review: generalReview,
                    budget_min: budgetMin,
                    budget_max: budgetMax,
                    additional_comment: additionalComment,
                    selected_product_list: JSON.stringify(selectedProductList)
                },
                success: function(data) {
                    if ( data.success ) {
                        alert('success');
                    } else {
                        alert('fail');
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    alert('fail');
                }
            });
        });
    });


})();