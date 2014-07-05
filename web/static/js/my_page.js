
$(function(){



  var mySwiper = $('.swiper-container').swiper({
    //Your options here:
    mode:'horizontal',
    loop: false,
    preventLinks : false,
    calculateHeight : true,
    noSwiping : true
    //etc..
  });


  $('#mypage-next-btn').click(function(e){
     e.preventDefault();
     mySwiper.swipeNext();
  });


  $('#mypage-prev-btn').click(function(e){
     e.preventDefault();
     mySwiper.swipePrev();
  });


  $('.mypage-interesting-del-btn').click(function(e){
        e.preventDefault();
        var type = $(this).attr('data-type');
        var id = $(this).attr('data-product');

        $.ajax({
              url: '/user/interest/del/',
              dataType: 'json',
              data : {product_or_set_id : id , type : type},
              async : true,
              type:'post',
              success: function(data){

                  location.reload();
              },
              error:function(jqXHR, textStatus, errorThrown){
                  console.log(textStatus);
              }
        });
    });

});