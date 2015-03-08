var test;
(function() {

    $(function() {
        var btnEnterToDatabase = $('#btn-enter-to-database');

        btnEnterToDatabase.click(function() {
            var selectedProductList = [];
            $('#table-product-list tr').each(function (index, object) {
                if ($(object).find(".checkbox-enter-product:checked").length > 0) {
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

        $(".checkbox-enter-product").change(function() {
            var selectedItemList = $('#selected-item-list');
            selectedItemList.html("");
            var totalPrice = 0;
            $('.product-list tr input.checkbox-enter-product:checked').each(function(index, item) {
                var name = $(item).attr('product-name')
                var price = $(item).attr('product-price')
                totalPrice += parseInt(price);
                selectedItemList.append("<div>" + name + "</div>");
            });
            $('#total-price').text(totalPrice);
        });

        //$(".brand-list input[type='checkbox']").change(function() {
        //    var checkedBrandNameList = [];
        //    $(".brand-list input[type='checkbox']:checked").each(function(index, item) {
        //        checkedBrandNameList.push(item.value);
        //    });
        //});

    });

    this.applyFilter = function() {
        var checkedBrandNameList = [];
        $(".brand-list input[type='checkbox']:checked").each( function(index, item) {
            checkedBrandNameList.push(item.value);
        });
        var checkedCategoryIdList = [];
        $(".category-list input[type='checkbox']:checked").each( function(index, item) {
            checkedCategoryIdList.push(item.value);
        });
        var skinType = "";
        $(".skin-type-list input[type='checkbox']:checked").each( function(index, item) {
            skinType += item.value;
        });

        var minPrice = parseInt($('#min-price').val());
        var maxPrice = parseInt($('#max-price').val());

        $('.product-list tr').each(function(index, item) {
            $(item).css('display', 'table-row');
            if (parseInt($(item).attr('product-price'))<minPrice || maxPrice<parseInt($(item).attr('product-price'))) {
                $(item).css('display', 'none');
            }
        });


        $('.product-list tr').each(function(index, item) {
            if ( $.inArray( $(item).attr('brand'), checkedBrandNameList ) == -1 ) {
                $(item).css('display', 'none');
            }
            var productSkinType = $(item).attr('skin-type');
            var isIn = false;

            for( i=0; i<skinType.length; i++ ) {
                for ( j=0; j<productSkinType.length; j++ ) {
                    if ( skinType[i] == productSkinType[j] ) {
                        isIn = true;
                        break;
                    }
                }
                if ( isIn ) break;
            }

            if ( !isIn ) {
                $(item).css('display', 'none');
            }

            if ( $.inArray( $(item).attr('category-id'), checkedCategoryIdList ) == -1 ) {
                $(item).css('display', 'none');
            }
        });
    };

})();