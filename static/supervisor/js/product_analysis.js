(function() {
    var analysisResultList;
    var selectedProductId;
    var totalAnalysedCount;

    function updateAnalysisTable(minCount, maxCount) {

        minCount = typeof minCount !== 'undefined' ? minCount : 0;
        maxCount = typeof maxCount !== 'undefined' ? maxCount : 999999;

        var result = "<tr><th>-</th><th>키워드</th><th>빈도</th><th>선택하기</th><tr>"
        var analysisResultItem;
        for (i = 0; i < analysisResultList.length; i++) {
            analysisResultItem = analysisResultList[i];
            if ( analysisResultItem.count>=minCount && analysisResultItem.count<=maxCount) {
                result += "<tr><td><div class=\"checkbox\"><label><input type=\"checkbox\" value=\"\"></label></div></td><td>"
                + "<input type=\"text\" value=\"" + analysisResultItem.keyword + "\"></td>"
                + "<td><input type=\"number\" value=\"" + analysisResultItem.count + "\">"
                + "</td><td><label class=\"checkbox-inline\"><input type=\"checkbox\" id=\"inlineCheckbox1\" value=\"option1\">피부타입</label>"
                + "<label class=\"checkbox-inline\"><input type=\"checkbox\" id=\"inlineCheckbox2\" value=\"option2\">특징</label>"
                + "<label class=\"checkbox-inline\"><input type=\"checkbox\" id=\"inlineCheckbox2\" value=\"option2\">효과</label>"
                + "<label class=\"checkbox-inline\"><input type=\"checkbox\" id=\"inlineCheckbox2\" value=\"option2\">기타</label></td></tr>";
            }
        }
        $('#table-analysis-result').html(result);
    }

    $(function() {
        var selectProduct = $('#select-product');
        var btnSelectProduct = $('#btn-select-product');
        var btnStartAnalysis = $('#btn-start-analysis');
        var btnApplyCountFilter = $('#btn-apply-count-filter');


        selectProduct.change(function() {
            selectedProductId = undefined;
            btnStartAnalysis.attr("disabled","disabled");
        });
        btnSelectProduct.click(function() {
            selectedProductId = selectProduct.val();
            console.log(selectedProductId);

            btnStartAnalysis.removeAttr("disabled");
            return false;
        });
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
                success: function(data) {
                    if ( data.success ) {
                        analysisResultList = data.analysis_result_list;
                        totalAnalysedCount = analysisResultList.length;
                        console.log( totalAnalysedCount );
                        updateAnalysisTable();
                        $('#btn-start-analysis').button('reset');
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
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
    });


})();