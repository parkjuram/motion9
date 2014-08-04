/**
 * Created by Park-Kunbae on 14. 4. 10.
 */


function onPaymentSuccess(payment_id) {
    window.location.replace( url_payment_complete + "?payment_id" + payment_id );
}

function onPaymentFail() {
    alert("payment fail!!!");
}

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

        var sumPrice = $('#cart-sum-price');
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

       sumPrice.text(numberFormatter(sum));
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

    $('.purchase-btn').click(function(e){
        var payment_form = document.payment;
        payment_form.target = "payment";

//                test payemnt url : http://tpay.billgate.net/credit/certify.jsp
//                real payemnt url : https://pay.billgate.net/credit/certify.jsp
        payment_form.action = "http://tpay.billgate.net/credit/certify.jsp";

        var popup_option ="width=500,height=477,toolbar=no,location=no,status=no,menubar=no,scrollbars=no,resizable=no,left=150,top=150";
        var popup_object = window.open("about:blank", "payment", popup_option);

        if ( popup_object == null ) {
            alert("팝업이 차단되어 있습니다.\n팝업차단을 해제하신 뒤 다시 시도하여 주십시오.");
        }

        payment_form.submit();
   });

});