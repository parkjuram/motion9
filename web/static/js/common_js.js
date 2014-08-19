/**
 * Created by Park-Kunbae on 14. 3. 31.
 */

/*
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/ko_KR/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

window.fbAsyncInit = function() {
    FB.init({
        appId: '1450591788523941',
        cookie: true,  // enable cookies to allow the server to access
        // the session
        xfbml: true,  // parse social plugins on this page
        version: 'v2.0' // use version 2.0
    });
}
*/

function numberFormatter(number){
    var digits = parseInt(number);
    var numberStr = ''+ digits;
    var length = numberStr.length;

    var result = '';
    for(var i = length-1 ; i >= 0; i--){
        result = numberStr.charAt(i) + result;

        if(i != 0 && (i == length-9 || i == length-6 || i == length-3))
           result = ',' + result;
    }

    return result;
}

function parsePrice(price){
    var parsedPrice = '';
    var numbers = price.split(',');
    for(var i = 0 ; i < numbers.length; i++){
        parsedPrice += numbers[i];
    }

    return parseInt(parsedPrice);
}


function getContextPath(){
    var offset=location.href.indexOf(location.host)+location.host.length;
    var ctxPath=location.href.substring(offset,location.href.indexOf('/',offset+1));
    return ctxPath;
}


$(function(){

    $.ajaxSetup({ cache: true });
      $.getScript('//connect.facebook.net/ko_kr/all.js', function(){
        FB.init({
          appId: '1450591788523941',
          cookie: true,  // enable cookies to allow the server to access
          // the session
          xfbml: true,  // parse social plugins on this page
          version: 'v2.0' // use version 2.0
        });

      });


    $('.btn-for-interest').click(function(e){
        e.preventDefault();

        var btn = $(this);
        var productKey = btn.attr('data-product');
        var type = btn.attr('data-type')=='s'?'s':'p';
        var url = '';
        var done = btn.hasClass('interest-done');

        if(!done)
            url = "/user/interest/add/";
        else
            url = '/user/interest/del/';

        $.ajax({
            url: url,
            dataType: 'json',
            async : true,
            type:'POST',
            data : {product_or_set_id : productKey, type : type},
            success: function(data){
                if(!data.success && data.message == 'login required'){
                    if(confirm('로그인이 필요 합니다. 로그인 하시겠습니까?'))
                        location.href= url_for_login_next;
                }else if(!data.success){
                    alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                }else{
                    if(!done){
                        btn.addClass('interest-done');
                        btn.text('관심취소');
                    }else{
                        btn.removeClass('interest-done');
                        btn.text('관심하기');
                    }
                }
            },
            error:function(jqXHR, textStatus, errorThrown){
                console.log(textStatus);
            }
		});
	});

    $('.btn-for-cart').click(function(e){
        e.preventDefault();
        var productKey = $(this).attr('data-product');
        var type = $(this).attr('data-type');
        if(type != 's' && type !='c')
            type = 'p';

        var howManySelectBox = $('#howMany');
        var howMany = 1;
        if(howManySelectBox.length != 0){
            howMany = howManySelectBox.val();
        }


        if(!confirm('장바구니에 추가 하시겠습니까?'))
            return;

        $.ajax({
				  url: "/user/cart/add/",
				  dataType: 'json',
				  async : true,
				  type:'POST',
				  data:{product_or_set_id : productKey, type : type, how_many : howMany},
				  success: function(data){
					  if(!data.success && data.message == 'login required'){
                          if(confirm('로그인이 필요 합니다. 로그인 하시겠습니까?'))
                            location.href= url_for_login_next;
                      }else if(!data.success){
                          alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                      }else{
                          alert('장바구니에 추가되었습니다.');
                      }
				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  console.log(textStatus);
				  }
		});
	});


    $('.btn-for-purchase').click(function(e){
        e.preventDefault();
        var isMobile = $(this).attr('data-mobile');
        var productKey = $(this).attr('data-product');
        var type = $(this).attr('data-type');
        if(type != 's' && type !='c')
            type = 'p';

        var howManySelectBox = $('#howMany');
        var howMany = 1;
        if(howManySelectBox.length != 0){
            howMany = howManySelectBox.val();
        }

        if(!confirm('바로 구매 하시겠습니까?'))
            return;

        $.ajax({
				  url: "/user/cart/add/",
				  dataType: 'json',
				  async : true,
				  type:'POST',
				  data:{product_or_set_id : productKey, type : type, how_many : howMany},
				  success: function(data){
					  if(!data.success && data.message == 'login required'){
                          if(confirm('로그인이 필요 합니다. 로그인 하시겠습니까?'))
                            location.href= url_for_login_next;
                      }else if(!data.success){
                          alert('에러가 발생하였습니다. 관리자에게 문의 해주세요.');
                      }else{
                          if(isMobile=='true')
                            location.href="/user/mobile/mypage/before_purchase/";
                          else
                            location.href="/user/mypage/cart/";
                      }
				  },
				  error:function(jqXHR, textStatus, errorThrown){
					  console.log(textStatus);
				  }
		});
	});

});