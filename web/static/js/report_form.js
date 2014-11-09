$(function(){

    $('.report-btn').click(function (e) {

        var errorMessage = null;

//        if($('#postalcode').val()=='' || $('#basicAddress').val()==''){
//            errorMessage = '주소를 입력해 주십시오.';
//        }else if($('#sendTo').val()==''){
//            errorMessage = '수취인 이름을 입력해 주십시오.';
//        }else if($('#phone1').val()=='' || $('#phone2').val()=='' || $('#phone3').val()==''){
//            errorMessage = '수취인 전화번호를 입력해 주십시오.';
//        }else if($('#cart-sum-price').text()==''){
//            errorMessage = '결제금액 1000원 미만은 결제되지 않습니다.'
//        }
//
//        if ( errorMessage != null ) {
//            alert( errorMessage );
//        }else{
            $.ajax({
                url: urlReportForm,
                dataType: 'json',
                async : true,
                type:'POST',
                data: {
                    'survey_id': $('').val(),
                    'comments': $('#phone1').val()+"-"+$('#phone2').val()+"-"+$('#phone3').val(),
                    'options': $('#postalcode').val()
                },

                success: function (data) {
                    if (data.success) {
                        startPayment();
                    }
                }

            });
//        }

    });
});