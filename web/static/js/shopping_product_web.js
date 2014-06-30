/**
 * Created by Park-Kunbae on 14. 3. 15.
 */
$(function(){

    $( "#priceRange" ).slider({
      range: true,
      step : 30000,
      min: 5000,
      max: 500000,
      values: [ 70000, 140000 ],
      slide: function( event, ui ) {
          $( "#sPrice" ).text( ui.values[ 0 ]);
          $( "#fPrice" ).text( ui.values[ 1 ]);
      }
    });

    $( "#sPrice" ).text( $( "#priceRange" ).slider( "values", 0 ));
    $( "#fPrice" ).text( $( "#priceRange" ).slider( "values", 1 ));



    var container = document.querySelector('#productGrid');
    var msnry;


    imagesLoaded(container, function(){	//when all images are loaded, it is triggered
        var width = $('#productGrid').width()-2;
        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: 200,//parseInt(width/ 3),
          isResizeBound : false,
          gutter : 10,
          itemSelector: '.product-item'
        });
    });


    $('.product-item').hover(function(e){
        var id = $(this).attr('data-attr');
        $(this).find('.product-hover-area').css({display:'block'});
        $(this).find('.product-opacity-bg').animate({opacity:0.7},'fast');
        $(this).find('.product-item-info').addClass('product-expand-info-mode');
        $(this).find('.product-item-info-contents').hide();
        $(this).addClass('product-expand-mode');

    }, function(e){
        var hoverArea = $('.product-hover-area');
        hoverArea.css({display:'none'});
        $(this).find('.product-opacity-bg').css({opacity : 1});
        $(this).find('.product-item-info').removeClass('product-expand-info-mode');
        $(this).find('.product-item-info-contents').show();
        $(this).removeClass('product-expand-mode');
    });
});