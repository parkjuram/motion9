$(function(){
     $('.product-info-btn').click(function(e){
        e.preventDefault();
        $('#product-detail-modal').modal('show');
    });

//     $('.available-product').hover(function(e){
//       $(this).children('.available-product-hover-menu').show();
//    },function(e){
//       $(this).children('.available-product-hover-menu').hide();
//    });

//     $('.available-item').hover(function(e){
//       $(this).children('.available-item-hover-menu').show();
//    },function(e){
//       $(this).children('.available-item-hover-menu').hide();
//    });

    var fixDiv = function() {
        var b = $(window).scrollTop();
        var d = $("#changeProductWrapper").offset().top;
        var c = $("#originProductWrapper");
        if (b > d-20) {
            c.css({position:"fixed",top:"20px"})
        } else {
            c.css({position:"absolute",top:"0px"})
        }
    };

    $('.available-product-btn').click(function(e){
        e.preventDefault();
        var target = $(this).attr('data-target');

        if($(target).css('display') == 'block'){
            $(target).hide();
        }else{
            $(target).show();
        }
    })

    var updateCustomView = function(product, originalKey, newKey){
         var target = $('#customSetTableItem-'+originalKey);
         target.attr('data-new-key', newKey);
         target.find('.set-table-item-img img').attr('src', product.big_img_url);
         target.find('.set-table-item-category').text(product.category_name)
        var productName = product.name;
        if(productName.length > 16)
            productName = productName.substr(0,16)+'..';
         target.find('.set-table-item-info').text(productName);
    };

    $('.available-item-btn').click(function(e){
        e.preventDefault();
        var originalKey = $(this).attr('data-original-key');
        var newKey = $(this).attr('data-product');

         $.ajax({
				  url: '/product/'+newKey+'/json/',
				  dataType: 'json',
				  async : true,
				  type:'POST',
				  success: function(data){
                      var product = data;
					  if(product != null){
                          updateCustomView(product, originalKey, newKey);
                      }else{
                          alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                      }
				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
				  }
		});
    });

    var preForSubmit = function(setKey){

        var params = {set_id : setKey, custom_lists : [], changedCnt : 0};
        var changedCnt = 0;
        $('.custom-set-item-tr').each(function(idx, val){
            var originalKey = $(this).attr('data-original-key');
            var newKey = $(this).attr('data-new-key');
            if(newKey != originalKey)
                changedCnt++;
            params.custom_lists.push({original_id : originalKey, new_id : newKey});
        });
        params.changedCnt = changedCnt;

        return params;
    };

    var submitCustomSet = function(setKey, addToCart){
        var param = preForSubmit(setKey);
        if(param.changedCnt == 0){
            alert('커스터 마이징 한 제품이 없습니다.');
            return ;
        }
        $.ajax({
				  url: '/customize/set/save/',
				  dataType: 'json',
                  data: {'data' : JSON.stringify(param), 'addToCart': addToCart},
				  async : true,
				  type:'POST',
				  success: function(data){
                      var result = data;
					  if(result['success'] == true){
                          if(addToCart)
                            alert('장바구니에 추가 되었습니다.');
                          else
                            alert('My Collection에 저장 되었습니다.');
                      }else{
                          alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                      }
				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
				  }
		});
    };

    $('#submitCustomBtn').click(function(e){
        e.preventDefault();
        var setKey = $(this).attr('data-set');
        submitCustomSet(setKey, true);
    });

    $('#addCustomBtn').click(function(e){
        e.preventDefault();
        var setKey = $(this).attr('data-set');
        submitCustomSet(setKey, false);
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


   //$(window).scroll(fixDiv);
   //fixDiv();
});