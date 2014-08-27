/**
 * Created by Park-Kunbae on 14. 4. 3.
 */



$(function(){

    $('.product-info-btn').click(function(e){
        e.preventDefault();

        var productKey =$(this).attr('data-product');
        var productImg = $('#productModalImg');
        var productName = $('#productModalName');
        var productPrice = $('#productModalPrice');
        var cartBtn = $('#productModalCartBtn');
        var interestBtn = $('#productModalInterestBtn');

         $.ajax({
				  url: '/product/json/'+productKey,
				  dataType: 'json',
				  async : true,
				  type:'POST',
				  success: function(data){
                      var product = data.data;
					  if(product != null){
                          productImg.attr('src', product.big_img_url);
                          productName.text(product.name);
                          productPrice.text(product.discount_price);
                          cartBtn.attr('data-product', product.key);
                          interestBtn.attr('data-product', product.key);

                          $('#product-detail-modal').modal('show');
                      }else{
                          alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                      }
				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
				  }
		});


    });

/*
    $('.set-img-gallery').magnificPopup({
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
*/

    var hoverBg = $(this).find('.set-img-opacity-bg');
    var hoverContents = $(this).find('.set-img-opacity-contents');
    $('.set-img-container').hover(function(e) {
        hoverBg.css({display:'block'});
        hoverContents.css({display:'block'});
    }, function(e) {
        hoverBg.css({display:'none'});
        hoverContents.css({display:'none'});
    });

    $('.belong-to-set-item').hover(function(e){
        var id = $(this).attr('data-attr');
        $(this).find('.product-hover-area').css({display:'block'});
        $('.product-opacity-bg').css({opacity:0.9});
        //hoverArea.css({display:'block'});

    }, function(e){
        var hoverArea = $(this).find('.product-hover-area');
        //hoverArea.appendTo($('body'));
        hoverArea.css({display:'none'});
    });

    $('.cnt-spinner').spinner({value:1, min : 1, afterChange: function(val){
        var price = parsePrice($('#productPrice').text());
        var final = price * parseInt(val);
        $('#productFinalPrice').text(numberFormatter(final));
    }});

    $("#setTabs").easyResponsiveTabs({
        type: 'default', //Types: default, vertical, accordion
        width: 'auto', //auto or any custom width
        fit: true,   // 100% fits in a container
        activate: function() {}  // Callback function, gets called if tab is switched
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

$('#productDetailModal').jqm({modal:false, ajaxText:'불러오는중..', trigger: '.view-product-detail-btn',ajax:'@href', onLoad : modalOnloadHandler, onHide:onHideHandler});
    //$('#productDetailModal').jqm({ajax : '@href'});


/*    $('.view-product-detail-btn').click(function(e){
        e.preventDefault();
        var id = $(this).attr('data-product');

        $('#productDetailModal').jqmShow();
    });
*/


});