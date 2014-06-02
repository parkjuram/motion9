/**
 * Created by Park-Kunbae on 14. 3. 31.
 */

$(function(){

    function getContextPath(){
        var offset=location.href.indexOf(location.host)+location.host.length;
        var ctxPath=location.href.substring(offset,location.href.indexOf('/',offset+1));
        return ctxPath;
    }
/*
    var closeSubMenu = function(){
        $('ul.header-main-sub-menu').each(function(idx, val){
           $(this).css({display :'none'});
        });
    };

    $('#header .has-sub-menu').hover(function(e){
        closeSubMenu();

        var subMenu = $(this).children('ul.header-main-sub-menu');
        subMenu.css({display : 'block'});
    });

    $('#header').hover(function(){

    }, function(e){
            closeSubMenu();
    });

*/
    var fixDiv = function() {
        var b = $(window).scrollTop();
        var d = $("#header").offset().top + 80;
        var c = $("#nav-top-btn");
        if (b > d) {
            c.css({position:"fixed", top:"90%", display:"block"});
        } else {
            c.css({position:"absolute",top:"0px", display : 'none'});
        }
    };

    $(window).scroll(fixDiv);

    $('.btn-for-interest').click(function(e){
        e.preventDefault();

        var btn = $(this);
        var productKey = btn.attr('data-product');
        var type = btn.attr('data-type')=='s'?'s':'p';
        var url = '';
        var done = btn.hasClass('btn-motion9-disable');

        if(!done)
            url = "/user/interest/add";
        else
            url = '/user/interest/del';

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
                            btn.addClass('btn-motion9-disable');
                          }else{
                              btn.removeClass('btn-motion9-disable');
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

        var howManySelectBox = $('#howManySelectBox');
        var howMany = 1;
        if(howManySelectBox.length != 0){
            howMany = howManySelectBox.val();
        }

        if(!confirm('장바구니에 추가 하시겠습니까?'))
            return;

        $.ajax({
				  url: "/cart/add",
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

});