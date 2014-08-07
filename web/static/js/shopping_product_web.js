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
          $( "#sPrice" ).text( numberFormatter(ui.values[ 0 ]));
          $( "#fPrice" ).text( numberFormatter(ui.values[ 1 ]));
      }
    });

    $( "#sPrice" ).text( numberFormatter($( "#priceRange" ).slider( "values", 0 )));
    $( "#fPrice" ).text( numberFormatter($( "#priceRange" ).slider( "values", 1 )));

    $('.filter-btn').click(function(e){
        e.preventDefault();
        var min = $( "#priceRange" ).slider( "values", 0 );
        var max = $( "#priceRange" ).slider( "values", 1 );

        var url = location.href;
        var qIdx;
        if((qIdx = url.indexOf('?')) != -1){
           url = url.substring(0, qIdx-1);
           url += '?price_max='+max+'&price_min='+min;
        }else{
           url += '?price_max='+max+'&price_min='+min;
        }
        location.href = url;
    });


    var container = document.querySelector('#productGrid');
    var msnry;


    imagesLoaded(container, function(){	//when all images are loaded, it is triggered
        var width = $('#productGrid').width()-2;
        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: 200,//parseInt(width/ 3),
          isResizeBound : false,
          gutter : 20,
          itemSelector: '.product-item'
        });
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