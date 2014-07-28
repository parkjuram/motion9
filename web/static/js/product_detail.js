$(function(){

   $('a.tab-btn').click(function(e){
        e.preventDefault();

        var target = $(this).attr('href');
        console.log(target);
        $('.tab-content').removeClass('tab-selected');
        $(target).addClass('tab-selected');
   });

    var productCategoryList = [['스킨', 1],['로션', 2],['선크림, BB크림', 4],['에센스', 5],['수분크림, 아이크림', 14],['스페셜케어', 16],['클렌징, 스크럽', 3],['메이크업', 17], ['바디', 24], ['헤어', 22], ['향수', 25]];
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
        location.href='/mobile/shop/product/'+categoryId;
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
});