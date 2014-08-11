/**
 * Created by Park-Kunbae on 14. 4. 10.
 */


$(function(){

    var element = document.getElementById('addressLayer');
    $(element).jqm({modal:false});

    function closeDaumPostcode() {
        // iframe을 넣은 element를 안보이게 한다.
        element.style.display = 'none';
    }

    function showDaumPostcode() {
        new daum.Postcode({
            oncomplete: function(data) {
                // 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.
                // 우편번호와 주소 및 영문주소 정보를 해당 필드에 넣는다.
                $('#postalcode').val(data.postcode);
                $('#basicAddress').val(data.address);
                // iframe을 넣은 element를 안보이게 한다.
                $(element).jqmHide();
            },
            width : '100%',
            height : '100%'
        }).embed(element);



        $(element).jqmShow();
    }

    function closeDaumPostcode(){
        $(element).jqmHide();
    }

   $('#searchAddressBtn').click(function(e){
        showDaumPostcode();
   });


   $('select.cart-item-count').change(function(e){

        var sum=0;

       $('select.cart-item-count').each(function(i, v){
           var type = $(this).attr('data-type');
           var id = $(this).attr('data-id');
           var cnt = parseInt($(this).val());
           var price;
           var total;

           if(type == 's'){
              $('#cart-set-price-'+id).text();
              price = parsePrice($('#cart-set-price-'+id).text());
              total = price * cnt;
              $('#cart-set-total-price-'+id).text(numberFormatter(total));
           }else if(type == 'p'){
              price = parsePrice($('#cart-product-price-'+id).text());
              total = price * cnt;
              $('#cart-product-total-price-'+id).text(numberFormatter(total));
           }else{
              price = parsePrice($('#cart-custom-price-'+id).text());
              total = price * cnt;
              $('#cart-custom-total-price-'+id).text(numberFormatter(total));
           }
           sum+=total;
       });

       total_price=sum;
       $('#mileage').val(0);
       updateAmount(sum);
   });



   $('.del-item-btn').click(function(e){
      e.preventDefault();
      if(confirm('정말 삭제하시겠습니까?')){
        var id = $(this).attr('data-product-id');
        var type= $(this).attr('data-type');

        $.ajax({
              url: '/user/cart/del/',
              dataType: 'json',
              async : true,
              type:'POST',
              data : {product_or_set_id : id, type: type},
              success: function(data){
                  if(data.success){
                      location.href= '/user/mypage/cart';
                  }else if(!data.success){
                      alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                  }
              },
              error:function(jqXHR, textStatus, errorThrown){
                  console.log(textStatus);
              }
        });
      }
   });

    function getBrowserName() {
        var agent = navigator.userAgent.toLowerCase();
        if (agent.indexOf("firefox")!= -1) return 'Firefox';
        if (agent.indexOf("chrome")!= -1) return 'Chrome';
        if (agent.indexOf("safari")!= -1) return 'Safari';
        if (agent.indexOf("opera")!= -1) return 'Opera';
        if (agent.indexOf("msie")!= -1) return 'IE';
        else return navigator.userAgent;
    }

    function startPayment() {
        var browserName = getBrowserName();

        if(browserName != "Chrome" &&  browserName != "Safari" && browserName != "Firefox" && browserName != "Opera")
        {
            var payment_form = document.payment;
            payment_form.target = "payment";

    //                test payemnt url : http://tpay.billgate.net/credit/certify.jsp
    //                real payemnt url : https://pay.billgate.net/credit/certify.jsp
            payment_form.action = "https://pay.billgate.net/credit/certify.jsp";

            var popup_option ="width=500,height=477,toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=no,left=150,top=150";
            var popup_object = window.open("about:blank", "payment", popup_option);

            if ( popup_object == null ) {
                alert("팝업이 차단되어 있습니다.\n팝업차단을 해제하신 뒤 다시 시도하여 주십시오.");
            }

            payment_form.submit();
        } else {
            var payment_form = document.payment;
            if(plugin == null || plugin.VERSION == null)
            {
                alert("플러그인을 설치해주세요.");
                return;
            }
            ////// 수정 불가(필수 파라메터) //////////////////////
            plugin.SERVICE_ID           = payment_form.SERVICE_ID.value;
            plugin.ORDER_ID             = payment_form.ORDER_ID.value;
            plugin.ORDER_DATE           = payment_form.ORDER_DATE.value;

            plugin.USER_ID              = payment_form.USER_ID.value;
            plugin.USER_NAME            = payment_form.USER_NAME.value;
            plugin.USER_EMAIL           = payment_form.USER_EMAIL.value;
            plugin.ITEM_CODE            = payment_form.ITEM_CODE.value;
            plugin.ITEM_NAME            = payment_form.ITEM_NAME.value;
            plugin.USING_TYPE           = payment_form.USING_TYPE.value;
            plugin.CURRENCY             = payment_form.CURRENCY.value;
            plugin.CARD_TYPE            = payment_form.CARD_TYPE.value;
            plugin.DIRECT_USE           = '0000';
            plugin.AMOUNT               = payment_form.AMOUNT.value;
            plugin.INSTALLMENT_PERIOD   = payment_form.INSTALLMENT_PERIOD.value;
            plugin.RETURN_URL           = payment_form.RETURN_OPENBROWSER_URL.value;
            plugin.CHECK_SUM            = payment_form.CHECK_SUM.value;

            //결제페이지 URL
//            plugin.CERTIFY_URL          = "http://tpay.billgate.net/credit/certify.jsp";    //TEST
            plugin.CERTIFY_URL          = "https://pay.billgate.net/credit/certify.jsp";    //REAL

            ////// 수정 불가(필수 파라메터) //////////////////////

            if(plugin.Auth())
            {
                document.write(plugin.FORWARD_FORM);
                document.payform.submit();
            }

        }
    }

    $('.purchase-btn').click(function(e){

        $.ajax({
            url: url_profile_update,
            dataType: 'json',
            type:'POST',
            data: {
                'postcode': $('#postalcode').val(),
                'recent_phone': $('#phone1').val()+"-"+$('#phone2').val()+"-"+$('#phone3').val(),
                'basic_address': $('#basicAddress').val(),
                'detail_address': $('#detailAddress').val()
            },
            complete: function(jqXHR, textStatus) {
                startPayment();
            }
        });

   });

    $('#mileage').keydown(function(e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });

    $('#mileage').focusout(function(e){
        if ( $(this).val().length == 0 ) {
            $(this).val(0);
        } else {
            $(this).val( parseInt($(this).val()) );
            if ( parseInt($(this).val())%1000 != 0 ) {
                alert('천원단위로 사용 가능합니다.');
                $(this).val(0);
            } else if ( parseInt($(this).val()) > parseInt(user_mileage) ) {
                alert('보유한 적립금보다 많습니다.');
                $(this).val(0);
            } else if ( total_price-parseInt($(this).val()) < 0 ) {
                alert('상품금액보다 많은 적립금을 사용할 수 없습니다.');
                $(this).val(0);
            }
        }


        var result_total_price = total_price-parseInt($(this).val());

        if ( result_total_price != parseInt($('input[name="AMOUNT"]').val())) {
            updateAmount(result_total_price);
        }

    });

    function updateAmount(amount) {
        $.ajax({
            url: url_get_billgate_payment_checksum,
            dataType: 'json',
            type: 'POST',
            data: {
                service_id: service_id,
                order_id: order_id,
                amount: amount
            },
            success: function(data) {
                if ( data.success ) {
                    $('#cart-sum-price').text( numberWithCommas(amount) );
                    $('input[name="AMOUNT"]').val( amount );
                    $('input[name="CHECK_SUM"]').val( data.checksum );
                }
            }

        });


    }
    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

});