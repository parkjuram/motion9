$(function(){

    var productCategoryList = [['스킨', 1],['로션', 2],['선크림, BB크림', 4],['에센스', 5],['모이스춰라이저', 12],['수분크림, 아이크림', 14],['스페셜케어', 16],['클렌징, 스크럽', 3],['메이크업', 17]];

    var setCategoryList = [['라이프 스타일', 18],['계절', 19],['피부상태', 20],['프리미엄', 21]];

    $('#mainCategoryList').change(function(e){
       var target = $('#subCategoryList');
        var list;
        if($(this).val() == '#subProductCategory'){
            list = productCategoryList;
        }else{
            list = setCategoryList;
        }

        target.children().each(function(){
            $(this).remove();
        });

        for(var i = 0 ; i < list.length; i++){
            var option = $('<option value="'+list[i][1]+'">'+list[i][0]+'</option>');
            target.append(option);
        }

        target.selectmenu( "refresh", true );
    });

    $('#subCategoryList').change(function(e){
        var categoryId = $(this).val();
        location.href='/mobile/shop/set/'+categoryId;
    });

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
          loop: false,
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