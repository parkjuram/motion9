/**
 * Created by Park-Kunbae on 14. 3. 27.
 */
$(function(){
    $('.changeable-collapse-btn').click(function(e){
        e.preventDefault();

        var collapsedMenu = $(this).parent().next('.list-collapsed');

        if(collapsedMenu.hasClass('list-collapsed-opened')){
            collapsedMenu.removeClass('list-collapsed-opened');
        }else{
            collapsedMenu.addClass('list-collapsed-opened');
        }
    });
});