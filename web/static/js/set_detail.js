$(function(){

   $('a.tab-btn').click(function(e){
        e.preventDefault();

        var target = $(this).attr('href');
        console.log(target);
        $('.tab-content').removeClass('tab-selected');
        $(target).addClass('tab-selected');
   });

   var mySwiper = $('.swiper-container').swiper({
    //Your options here:
    mode:'horizontal',
    loop: true,
    calculateHeight : true,
    pagination: '.pagination',
    paginationClickable: true
    //etc..
  });
});