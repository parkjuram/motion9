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
        $(this).find('.product-hover-area').css({display:'block'});
        $(this).find('.product-opacity-bg').animate({backgroundColor: 'white', opacity:0.7},'slow');
        $(this).find('.product-item-info').addClass('product-expand-info-mode');
        $(this).find('.product-item-info-contents').hide();
        $(this).addClass('product-expand-mode');

    }, function(e){
        var hoverArea = $('.product-hover-area');
        hoverArea.css({display:'none'});
        $(this).find('.product-opacity-bg').css({backgroundColor: 'white', opacity : 0});
        $(this).find('.product-item-info').removeClass('product-expand-info-mode');
        $(this).find('.product-item-info-contents').show();
        $(this).removeClass('product-expand-mode');
    });

});