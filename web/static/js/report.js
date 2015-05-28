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
        var blog_summary = $('.blog-product-item-contents-summary');
        var blog_summary_detail = $('.blog-product-item-contents-summary-detail');

        if ( blog_summary.css('display') == 'none' ) {
            blog_summary.css('display',"block");
            blog_summary_detail.css('display',"none");
//            magazine_fold.scrollView();
            $(this).text('자세히 보기');
        } else {
            blog_summary.css('display',"none");
            blog_summary_detail.css('display', "block");
            $(this).text('닫기');
//            $(".magazine-wrapper").scrollView();
        }
        $(this).scroll();
    });

     $('.view-title-btn').click(function(e){
        e.preventDefault();

        var contents = $('.report-main-title-contents');
//        var more_btn = $('.report-main-title-more')

        if ( contents.css('height') == '50px') {
            contents.css('height',"auto");
//            magazine_fold.scrollView();
            $(this).text('닫기');
        } else {
            contents.css('height',"50px");
            $(this).text('더보기');
//            $(".magazine-wrapper").scrollView();
        }
        $(this).scroll();

     });


        var modalOnloadHandler = function(hash){
        $('#modalProductImgGallery').magnificPopup({
            delegate: 'a',
            type: 'image',
            tLoading: 'Loading image #%curr%...',
            mainClass: 'mfp-img-mobile',
            gallery: {
                enabled: true,
                navigateByImgClick: true,
                preload: [0,1] // Will preload 0 - before current, and 1 after the current image
            },
            image: {
                tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
            }
        });

        $('#modalCntSpinner').spinner({value:1, min : 1, afterChange: function(val){
            console.log('hello' + val);
        }});

        $('body').css({overflow:'hidden'});

        $('.btn-for-cart').click(function(e) {
            func_add_to_cart(e, this);
        });
    };

    var onHideHandler = function(hash){
        hash.w.hide();
        hash.o.remove();
        $('body').css({overflow: 'visible'});
    };

    $('#reportDetailModal').jqm({modal:false, ajaxText:'불러오는중..', trigger: '.view-report-detail-btn',ajax:'@href', onLoad : modalOnloadHandler, onHide:onHideHandler});

});