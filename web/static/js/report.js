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

    imagesLoaded(container, function(){	//when all images are loaded, it is triggered

        msnry = new Masonry( container, {	// api for displaying images as a grid
          // options
          columnWidth: '.product-detail',
          isResizeBound : false,
          gutter : 0,
          itemSelector: '.product-detail'
        });
    });

    $('.btn-detail').click(function(e) {
        e.preventDefault();

       var test =  $(this).parent;


        var magazine_fold = $('.blog-product-item-contents-summary');
        if ( magazine_fold.css('display') == 'none' ) {
            magazine_fold.css('display',"block");
//            magazine_fold.scrollView();
            $(this).text('자세히 보기');
        } else {
            magazine_fold.css('display',"none");
            $(this).text('닫기');
//            $(".magazine-wrapper").scrollView();
        }
        $(this).scroll();
    });

});