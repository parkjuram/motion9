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

   var fixDiv = function() {
        var b = $(window).scrollTop();
        var d = $("#cartPageWrapper").offset().top;
        var c = $("#puchaseInfoBox");
        if (b > d-50) {
            c.css({position:"fixed",top:"70px"})
        } else {
            c.css({position:"absolute",top:"20px"})
        }
    };
   $(window).scroll(fixDiv);
   fixDiv();

   $('#setAllCheck').click(function(e){
      var isChecked = $(this).is(':checked');
      if(!isChecked)
        $('.set-checkbox').prop('checked',false);
      else
        $('.set-checkbox').prop('checked',true);
   });

   $('#productAllCheck').click(function(){
      var isChecked = $(this).is(':checked');
      if(!isChecked)
        $('.product-checkbox').prop('checked',false);
      else
        $('.product-checkbox').prop('checked',true);
   });

   $('#delProductBtn').click(function(e){
      e.preventDefault();
      if(confirm('정말 삭제하시겠습니까?')){
        var keys = '';
        $('.product-checkbox').each(function(idx, val){
             if($(this).is(':checked') == true){
                 if(keys != '')
                    keys += ',';
                 keys+=$(this).attr('data-product-key');
             }
        });
        $.ajax({
              url: '/cart/del',
              dataType: 'json',
              async : true,
              type:'POST',
              data : {product_keys : keys, type: 'p'},
              success: function(data){
                  if(data.success){
                      location.href= '/cart';
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


    $('#delSetBtn').click(function(e){
        e.preventDefault();
        if(confirm('정말 삭제하시겠습니까?')){
        var keys = '';
        $('.set-checkbox').each(function(idx, val){
             if($(this).is(':checked') == true){
                 if(keys != '')
                    keys += ',';
                 keys+=$(this).attr('data-product-key');
             }
        });
        $.ajax({
              url: '/cart/del',
              dataType: 'json',
              async : true,
              type:'POST',
              data : {product_keys : keys, type: 's'},
              success: function(data){
                  if(data.success){
                      location.href= '/cart';
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