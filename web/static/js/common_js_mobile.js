/**
 * Created by Park-Kunbae on 14. 3. 31.
 */

$(function(){
    var renderCart = function(target, data){
        var keys = ['sets', 'products', 'custom_sets'];

        target = $(target);
        var imgUrl;
        var productName;
        var productPrice;
        var howMany;

        var html = '';


        for(var j = 0; j < keys.length ; j++){
            var list =  data[keys[j]];
            for(var i = 0 ; i < list.length ; i++){
                html = '';
                productPrice = list[i].discount_price;
                productName = list[i].name;
                imgUrl = list[i].big_img_url;
                howMany = list[i].item_count;


                var htmlPrepend = "<li>"
                    + "<div class='cart-item-img'>"
                    +   "<img src='"+imgUrl+"'/>"
                    + "</div>"
                    + "<div class='cart-item-info'>"
                    +       productName
                    + "     <div class='cart-select-box-wrapper'>"
                    + "         <lable>수량 : </lable>"
                    + "         <select data-shadow='false' data-corner='false'>";

                var htmlPost = '</select>'
                    + '     </div>'
                    + '     <div class="clearfix"></div>'
                    + '가격 : '
                    + productPrice + '원'
                    + '</div>'
                    + '<div class="clearfix"></div>'
                    + '</li>';

                html += htmlPrepend;
                for(var k = 0 ; k < howMany + 3 ; k++){
                    if(k == howMany)
                        html += '<option selected="selected">'+k+'</option>';
                    else
                        html += '<option>'+k+'</option>';
                }
                html += htmlPost;
                target.append($(html));
            }
        }
    };



    $('#cartPanel').on('panelopen', function(){
        var target = $('#cartPanel .custom-menu-list');

        if(false && target.length != 0){
            target.html('');
            $.ajax({
                  url: '/user/mypage/cart/json/',
                  dataType: 'json',
                  async : true,
                  type:'get',

                  success: function(data){

                      renderCart('#cartPanel .custom-menu-list', data);
                      $.mobile.loading('hide');
                      $(window).scroll();

                  },
                  error:function(jqXHR, textStatus, errorThrown){
                      console.log(textStatus);
                  }
            });
        }
    });


    $('#testBtn').click(function(e){
        e.preventDefault();
        $.mobile.loading('show');
        var target = $('#cartPanel .custom-menu-list');

        if(target.length != 0){
            target.html('');
            $.ajax({
                  url: '/user/mypage/cart/json/',
                  dataType: 'json',
                  async : true,
                  type:'get',
                  success: function(data){

                      renderCart('#cartPanel .custom-menu-list', data);
                      $.mobile.loading('hide');
                      $('#cartPanel').panel('open');
                  },
                  error:function(jqXHR, textStatus, errorThrown){
                      console.log(textStatus);
                  }
            });
        }
        });
});