$(document).on('pageshow', '.ui-page',function(event){
    setTimeout(function () {
        $('.selector').popup('open');
    }, 3000);
});