$(function () {
    var element = document.getElementById('addressLayer');
    $(element).jqm({modal: false});

    function closeDaumPostcode() {
        // iframe을 넣은 element를 안보이게 한다.
        element.style.display = 'none';
    }

    function showDaumPostcode() {
        new daum.Postcode({
            oncomplete: function (data) {
                // 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.
                // 우편번호와 주소 및 영문주소 정보를 해당 필드에 넣는다.
                $('#postalcode').val(data.postcode);
                $('#basicAddress').val(data.address);
                // iframe을 넣은 element를 안보이게 한다.
                $(element).jqmHide();
            },
            width: '100%',
            height: '100%'
        }).embed(element);


        $(element).jqmShow();
    }

    function closeDaumPostcode() {
        $(element).jqmHide();
    }

    $('#searchAddressBtn').click(function (e) {
        showDaumPostcode();
    });


    $('select.cart-item-count').change(function (e) {

        var sumPrice = $('#cart-sum-price');
        var sum = 0;

        $('select.cart-item-count').each(function (i, v) {
            var type = $(this).attr('data-type');
            var id = $(this).attr('data-id');
            var cnt = parseInt($(this).val());
            var price;
            var total;

            if (type == 's') {
                $('#cart-set-price-' + id).text();
                price = parsePrice($('#cart-set-price-' + id).text());
                total = price * cnt;
                $('#cart-set-total-price-' + id).text(numberFormatter(total));
            } else if (type == 'p') {
                price = parsePrice($('#cart-product-price-' + id).text());
                total = price * cnt;
                $('#cart-product-total-price-' + id).text(numberFormatter(total));
            } else {
                price = parsePrice($('#cart-custom-price-' + id).text());
                total = price * cnt;
                $('#cart-custom-total-price-' + id).text(numberFormatter(total));
            }
            sum += total;
        });

        sumPrice.text(numberFormatter(sum));
    });

    function startPayment() {
        var payment_form = document.payment;
        //        payment_form.action = 'http://tpay.billgate.net/credit/smartphone/certify.jsp';  //test
        payment_form.action = 'https://pay.billgate.net/credit/smartphone/certify.jsp';  //real
        payment_form.submit();
    }

    $('.purchase-btn').click(function (e) {
        $.ajax({
            url: urlBeforePayment,
            dataType: 'json',
            type:'POST',
            data: {
                'order_id': $('input[name="ORDER_ID"]').val(),
                'name': $('#sendTo').val(),
                'phone': $('#phone1').val()+"-"+$('#phone2').val()+"-"+$('#phone3').val(),
                'postcode': $('#postalcode').val(),
                'basic_address': $('#basicAddress').val(),
                'detail_address': $('#detailAddress').val(),
                'shipping_requirement': $('#shippingRequirement').val(),
                'mileage': $('#mileage').val()
            },
            success: function (data) {
                if (data.success) {
                    startPayment();
                }
            }
        });
    });

    /*****  mileage usage relate part   *****/

    var mileage = $('#mileage');

    mileage.focusout( function(e){
        console.log('mileage.focusout');
        var self = $(this);
        var value = parseInt( self.val() );
        var errorMessage = null;
        var resultPrice = parseInt(totalPrice);

        if ( value == NaN ) {
            value = 0;
        } else if ( value%1000 != 0 ) {
            value = 0;
            errorMessage = '천원 단위로 사용 가능합니다.';
        } else if ( value > userMileage ) {
            value = 0;
            errorMessage = '보유한 적립금보다 많습니다.';
        } else if ( value > totalPrice ) {
            value = 0;
            errorMessage = '상품금액보다 많은 적립금을 사용할 수 없습니다.';
        } else {
            resultPrice = resultPrice - value;
        }

        self.val(numberWithCommas(value));
        updateResultPrice(resultPrice);
        if ( errorMessage != null ) {
            alert( errorMessage );
        }



    });

    // result price = total price - mileage
    function updateResultPrice(resultPrice) {
        $.ajax({
            url: urlGetBillgatePaymentChecksum,
            dataType: 'json',
            type: 'POST',
            data: {
                service_id: serviceId,
                order_id: orderId,
                amount: resultPrice
            },
            success: function (data) {
                if (data.success) {
                    $('#cart-sum-price').text(numberWithCommas(resultPrice));
                    $('input[name="AMOUNT"]').val(resultPrice);
//                    $('input[name="CHECK_SUM"]').val(data.checksum);
                }
            }
        });
    }

    function numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

});