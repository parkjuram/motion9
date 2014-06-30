/**
 * Created by Park-Kunbae on 14. 3. 15.
 */
$(function(){

    var container = document.querySelector('#productGrid');
    var msnry;


    imagesLoaded(container, function(){	//when all images are loaded, it is triggered
        var width = $('#productGrid').width()-2;

        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: 200,
          isResizeBound : false,
          gutter : 10,
          itemSelector: '.product-item'
        })
    });

    $('.product-item').hover(function(e){
        var id = $(this).attr('data-attr');
        $(this).addClass('product-item-hover');
        $(this).find('.product-hover-area').css({display:'block'});
        $(this).find('.product-opacity-bg').animate({backgroundColor:'#393939', opacity:0.7},'slow',function(){
            console.log('done');
        });

    }, function(e){
        $(this).removeClass('product-item-hover');
        var hoverArea = $(this).find('.product-hover-area');
        $(this).find('.product-opacity-bg').css({opacity : 1});
        hoverArea.css({display:'none'});
    });

});