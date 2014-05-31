/**
 * Created by Park-Kunbae on 14. 3. 15.
 */
$(function(){

    var setItemWidth = function(){
        var width = $('#productGrid').width();
        $('.product-item').css({width : '306px'});
    };

    var container = document.querySelector('#productGrid');
    var msnry;


    imagesLoaded(container, function(){	//when all images are loaded, it is triggered
        //var width = $('#productGrid').width()-2;
        setItemWidth();
        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: 306,
          isResizeBound : false,
          gutter : 0,
          itemSelector: '.product-item'
        });
    });

    $('.product-item').hover(function(e){
        var id = $(this).attr('data-attr');

        $('#addCartBtn').attr('data-product', id);
        $('#cancelInterestBtn').attr('href', '/interest/del/set/'+id);

        var hoverArea = $('#productHoverArea');
        hoverArea.appendTo($('#item-'+id));

        hoverArea.css({position : 'absolute', top : 0, left: 0});
        $('#opacityBg').css({opacity:0.7});

        hoverArea.css({display:'block'});

    }, function(e){
        var hoverArea = $('#productHoverArea');
        hoverArea.appendTo($('body'));
        hoverArea.css({display:'none'});
    })
});