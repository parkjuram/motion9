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

   $('.view-product-btn').click(function(e){
        e.preventDefault();
        var id = $(this).attr('data-product');
        var dialog = $('#productDetailDialog');
        var img = $('#popupDetailImg').find('img');
        var name = $('#popupDetailName');
        var desc = $('#popupDetailDesc');
        var btn = $('#popupDetailBtn');

        $.ajax({
              url: '/mobile/product/'+id+'/json/',
              dataType: 'json',
              async : true,
              type:'POST',
              success: function(data){
                  console.log(data);
                  img.attr('src', data.big_img_url);
                  name.text(data.name);
                  desc.text(data.description);
                  btn.attr('href', '/mobile/product/'+id);

                  dialog.popup('open');
              },
              error:function(jqXHR, textStatus, errorThrown){

              }
		});

    });
});