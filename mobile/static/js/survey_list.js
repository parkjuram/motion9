$(function() {

    $('a[is-analysis-finish="False"]').click( function() {
       alert('준비중입니다. 완료되면 이메일로 알려드리겠습니다');
       return false;
    });

});