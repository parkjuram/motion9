/**
 * Created by Park-Kunbae on 14. 3. 31.
 */

$(function(){
    var renderCart = function(target, data){
        var keys = ['sets', 'products', 'custom_sets'];
        var imgUrl;
        var productName;
        var productPrice;
        var howMany;

        var html = '';
        var htmlPrepend = "<li>"
                    + "<div class='cart-item-img'>"
                    +   "<img src='"+imgUrl+"'/>"
                    + "</div>"
                    + "<div class='cart-item-info'>"
                    +   productName
                    + "</div>"
                    + "<div class='cart-select-box-wrapper'>"
                    + "     <lable>수량 : </lable>"
                    + "     <select data-shadow='false' data-corner='false'>";

        var htmlPost = '    </select>'
                    + '     <div class="clearfix"></div>'
                    + '</div>
                    + '가격 : '
                    + productPrice
                    + '원 <div class="clearfix"></div>'
                    + '</li>';

        for(var j = 0; j < keys.length ; j++){
            var list =  data[keys[i]];
            for(var i = 0 ; i < list.length ; i++){
                html = '';
                productPrice = list[i].discount_price;
                productName = list[i].name;
                imgUrl = list[i].big_img_url;

                html += htmlPrepend;

                html += htmlPost;
                target.append($(html));
            }
        }
    };

    $('#cartPanel').on('panelopen', function(){
        $.ajax({
              url: '/user/mypage/cart/json/',
              dataType: 'json',
              async : true,
              type:'POST',

              success: function(data){
                  renderCart('#cartPanel .custom-menu-list', data);
              },
              error:function(jqXHR, textStatus, errorThrown){
                  console.log(textStatus);
              }
		});
    });
});