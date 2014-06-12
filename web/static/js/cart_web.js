/**
 * Created by Park-Kunbae on 14. 4. 10.
 */
$(function(){
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