$(function(){

    var productCategoryList = [['스킨', 1], ['로션', 2], ['에센스', 5], ['비비크림, 선크림', 4], ['수분크림, 아이크림', 14], ['마스크/팩', 23], ['클렌징/스크럽', 3], ['립밤', 33], ['바디', 24], ['헤어', 22], ['향수', 25], ['기타', 26]];
    var setCategoryList = [['쿨가이 컬렉션', 18], ['꽃중년 컬렉션', 30], ['스포츠 컬렉션', 27], ['비즈니스맨 컬렉션', 28], ['계절 컬렉션', 31]];

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
        $('.tab-content').removeClass('tab-selected');
        $(target).addClass('tab-selected');

        if(target == '#productInfo'){
            $('.tab-btn').removeClass('selected-product-items-btn selected-product-rule-btn selected-product-info-btn');
            $(this).addClass('selected-product-info-btn');
        }else if(target == '#productItems'){
            $('.tab-btn').removeClass('selected-product-items-btn selected-product-rule-btn selected-product-info-btn');
            $(this).addClass('selected-product-items-btn');
        }else if(target == '#productRule'){
            $('.tab-btn').removeClass('selected-product-items-btn selected-product-rule-btn selected-product-info-btn');
            $(this).addClass('selected-product-rule-btn');
        }

   });

   var container = document.querySelector('.swiper-container');
   imagesLoaded(container, function() {	//when all images are loaded, it is triggered
      var mySwiper = $('.swiper-container').swiper({
          //Your options here:
          mode: 'horizontal',
          loop: false,
          calculateHeight: true,
          noSwiping : true
          //pagination: '.pagination',
          //paginationClickable: true
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
                  name.text(data.brandname +" "+ data.name);
                  desc.text(data.description);
                  btn.attr('href', '/mobile/product/'+id);

                  dialog.popup('open');
              },
              error:function(jqXHR, textStatus, errorThrown){

              }
		});

    });
});