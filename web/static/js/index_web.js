/**
 * Created by Park-Kunbae on 14. 3. 15.
 */
$(function(){
   $('.index-content-img').hover(function(){
        $(this).css({opacity : 1});
   }, function(){
       $(this).css({opacity : 0.4});
   });
});