$(function(){

    var container = document.querySelector('#productGrid');
    var msnry;


    imagesLoaded(container, function(){	//when all images are loaded, it is triggered

        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: '.product-item',
          isResizeBound : false,
          gutter : 0,
          itemSelector: '.product-item'
        });
    });
});