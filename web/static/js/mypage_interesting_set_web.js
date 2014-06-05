/**
 * Created by Park-Kunbae on 14. 3. 15.
 */
$(function(){

    $('.set-item-info').css({opacity:0.9});
    $('.set-item').hover(function(e){
        var infoBox = $(this).find('.set-item-info');
       var left = $(this).innerWidth() - infoBox.outerWidth();
       infoBox.animate({left : left+'px' }, { duration :'fast', easing: 'swing', queue: false});
    }, function(e){
       var infoBox = $(this).find('.set-item-info');
       var left = $(this).innerWidth();
       infoBox.animate({left : left+'px' }, { duration :'fast', easing: 'swing', queue: false});
    });


});