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


   $('select.product-num').change(function(e){
       var productPrice = 0;
       var deliveryPrice = 0;
       var totalProductPrice =  $('#totalProductPrice');
       var totalPurchasePrice = $('#totalPurchasePrice');

       $('select.product-num').each(function(i, v){
           var num = parseInt($(this).val());
           var isSet = $(this).attr('data-isSet');
           var key = $(this).attr('data-attr');
           var price = 0;
           if(isSet=='true'){
               price = parseInt($('#setPrice-'+key).text());
               productPrice += (price * num);
           }else{
               price = parseInt($('#productPrice-'+key).text());
               productPrice += (price * num);
           }
       });

       totalProductPrice.text(productPrice);
       totalPurchasePrice.text(productPrice + deliveryPrice);
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

});