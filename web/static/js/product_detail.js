$(function(){

   $('a.tab-btn').click(function(e){
        e.preventDefault();

        var target = $(this).attr('href');
        console.log(target);
        $('.tab-content').removeClass('tab-selected');
        $(target).addClass('tab-selected');
   });

  var container = document.querySelector('.swiper-container');
  imagesLoaded(container, function() {	//when all images are loaded, it is triggered
      var mySwiper = $('.swiper-container').swiper({
          //Your options here:
          mode: 'horizontal',
          loop: true,
          calculateHeight: true,
          pagination: '.pagination',
          paginationClickable: true
          //etc..
      });
  });
});