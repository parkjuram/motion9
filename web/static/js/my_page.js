
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


});