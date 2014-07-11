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


    $('.set-item-info').css({opacity:0.9});
    $('.set-item').hover(function(e){
        var infoBox = $(this).find('.set-item-info');
       var left = $(this).innerWidth() - infoBox.outerWidth() + 1;
       infoBox.animate({left : left+'px' }, { duration :'fast', easing: 'swing', queue: false});
    }, function(e){
       var infoBox = $(this).find('.set-item-info');
       var left = $(this).innerWidth();
       infoBox.animate({left : left+'px' }, { duration :'fast', easing: 'swing', queue: false});
    });
});