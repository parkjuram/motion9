(function() {
    var analysisResultList;

    var selectedProductId;
    var totalAnalysedCount;

    var skinType = "";
    var feature = "no";

    function updateAnalysisTable(minCount, maxCount) {

        minCount = typeof minCount !== 'undefined' ? minCount : 0;
        maxCount = typeof maxCount !== 'undefined' ? maxCount : 999999;

        var result = "<tr><th>-</th><th>키워드</th><th>빈도</th><th>선택하기</th><tr>"
        var analysisResultItem;
        var i;
        for (i = 0; i < analysisResultList.length; i++) {
            analysisResultItem = analysisResultList[i];
            if ( analysisResultItem.count>=minCount && analysisResultItem.count<=maxCount) {
                result += "<tr><td><div class=\"checkbox\"><label><input class= \"is-apply\" type=\"checkbox\" value=\"\"></label></div></td><td>"
                + "<input class=\"text-keyword\" type=\"text\" value=\"" + analysisResultItem.keyword + "\"></td>"
                + "<td><input class=\"number-count\" type=\"number\" value=\"" + analysisResultItem.count + "\">"
                + "</td><td><label class=\"checkbox-inline\"><input class=\"checkbox-type\" type=\"checkbox\" value=\"skintype\">피부타입</label>"
                + "<label class=\"checkbox-inline\"><input class=\"checkbox-type\" type=\"checkbox\" value=\"feature\">특징</label>"
                + "<label class=\"checkbox-inline\"><input class=\"checkbox-type\" type=\"checkbox\" value=\"effect\">효과</label>"
                + "<label class=\"checkbox-inline\"><input class=\"checkbox-type\" type=\"checkbox\" value=\"etc\">기타</label></td></tr>";
            }
        }
        $('#table-analysis-result').html(result);
    }

    $(function() {
        var selectProduct = $('#select-product');
        var btnSelectProduct = $('#btn-select-product');
        var btnStartAnalysis = $('#btn-start-analysis');
        var btnApplyCountFilter = $('#btn-apply-count-filter');
        var btnEnterToDatabase = $('#btn-enter-to-database');


        selectProduct.change(function() {
            selectedProductId = undefined;
            btnStartAnalysis.attr("disabled","disabled");
        });
        btnSelectProduct.click(function() {
            selectedProductId = selectProduct.val();

            btnStartAnalysis.removeAttr("disabled");
            return false;
        });

        function update_progress(status_url) {
            $.getJSON(status_url, function (data) {
                percent = parseInt(data['current'] * 100 / data['total']);
                $('#text-analysis-status').text(percent + '%');

                if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
                    if ('result' in data) {
                        analysisResultList = data['result'];
                        totalAnalysedCount = analysisResultList.length;
                        updateAnalysisTable();
                    }
                }
                else {
                    // rerun in 2 seconds
                    setTimeout(function () {
                        update_progress(status_url);
                    }, 5000);
                }
            });
        }

        btnStartAnalysis.click(function() {
            $('#table-analysis-result').html("");
            $(this).button('loading');
            var queryConcatString = "";
            $('#query-str input').each( function ( index, object ) {
                var queryString = object.value.trim();
                if ( queryString.length !== 0 ) {
                    if ( queryConcatString.length === 0) {
                        queryConcatString += queryString;
                    } else {
                        queryConcatString += "@"+queryString;
                    }
                }
            } );

            $.ajax({
                url: urlForProductAnalysis,
                dataType: 'json',
                type: 'POST',
                data: {
                    queryConcatString: queryConcatString
                },
                success: function (data, status, request) {
                    $('#btn-start-analysis').button('reset');
                    status_url = request.getResponseHeader('Location');
                    update_progress(status_url);
                },
                error: function () {
                    alert('Unexpected error');
                    $('#btn-start-analysis').button('reset');
                }
            });
            return false;
        });

        btnApplyCountFilter.click(function() {
            var minCount = $('#min-count').val(), maxCount = $('#max-count').val();
            updateAnalysisTable(minCount, maxCount);
            return false;
        });

        btnEnterToDatabase.click(function() {
            var analysisDetailList = [];
            $('#table-analysis-result tr').each(function (index, object) {
                if ($(object).find(".is-apply:checked").length > 0) {
                    var keyword = $(object).find('.text-keyword').val();
                    var count = $(object).find('.number-count').val();

                    $(object).find('.checkbox-type:checked').each(function (index, object) {
                        var type = $(object).val();
                        analysisDetailList.push( {
                            'keyword': keyword,
                            'count': count,
                            'type': type
                        });
                    });
                }
            });
            var skinType ="";
            $('.checkbox-skin-type:checked').each( function(index, object) {
                skinType += object.value;
            });
            var feature = $('.radio-feature:checked').val();

            $.ajax({
                url: urlForProductAnalysis,
                dataType: 'json',
                type: 'POST',
                data: {
                    product_id: selectedProductId,
                    total_count: totalAnalysedCount,
                    skin_type: skinType,
                    feature: feature,
                    analysis_detail_list: JSON.stringify(analysisDetailList)
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