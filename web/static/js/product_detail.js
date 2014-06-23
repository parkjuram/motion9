$(function(){

   $('a.tab-btn').click(function(e){
        e.preventDefault();

        var target = $(this).attr('href');
        console.log(target);
        $('.tab-content').removeClass('tab-selected');
        $(target).addClass('tab-selected');
   });

});