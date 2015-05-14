$(function() {

    //survey list중에서 아직 분석이 되지 않은 아이템을 클릭하면 불리는 function
    $('a[is-analysis-finish="False"]').click( function() {
       alert('현재 분석중입니다. 완료되면 이메일로 알려드리겠습니다');
       return false;
    });

});