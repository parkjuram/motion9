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
});