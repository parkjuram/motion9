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