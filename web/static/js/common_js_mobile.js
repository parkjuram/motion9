/**
 * Created by Park-Kunbae on 14. 3. 31.
 */

$(function(){
    var renderCart = function(target, data){
        var keys = ['sets', 'products', 'custom_sets'];

        target = $(target);
        var imgUrl;
        var productId;
        var productName;
        var productPrice;
        var howMany;
        var type;

        var html = '';


        for(var j = 0; j < keys.length ; j++){
            var list =  data[keys[j]];
            var preHiddenEl = "";
            var postHiddenEl = "";
            var name="";
            if(keys[j] == 'sets') {
                type = 's';
                preHiddenEl = "<input type='hidden' name='set_id[";
                postHiddenEl = "]' value='";
                name="name='set_cnt[";
            }else if(keys[j] =='products') {
                type = 'p';
                preHiddenEl = "<input type='hidden' name='product_id[";
                postHiddenEl = "]' value='";
                name="name='product_cnt[";
            }else if(keys[j] == 'custom_sets') {
                type = 'c';
                preHiddenEl = "<input type='hidden' name='custom_set_id[";
                postHiddenEl = "]' value='";
                name="name='custom_set_cnt[";
            }

            for(var i = 0 ; i < list.length ; i++){
                html = '';
                productId = list[i].id;
                productPrice = list[i].discount_price;
                productName = list[i].name;
                imgUrl = list[i].big_img_url;
                howMany = list[i].item_count;

                var htmlPrepend = "<li>"
                    + "<a class='cart-delete-btn' data-type='"+type+"' data-id='"+productId+"' href='#' >X</a>"
                    + "<div class='cart-item-img'>"
                    +   "<img src='"+imgUrl+"'/>"
                    + "</div>"
                    + preHiddenEl + i + postHiddenEl+ productId+"'/>"
                    + "<div class='cart-item-info'>"
                    +       productName
                    + "     <div class='cart-select-box-wrapper'>"
                    + "         <lable>수량 : </lable>"
                    + "         <select class='cart-item-count' "+name+i+"]' data-id='"+productId+"' data-shadow='false' data-corner='false'>";

                var htmlPost = '</select>'
                    + '     </div>'
                    + '     <div class="clearfix"></div>'
                    + '가격 : <span id="cart-item-' + productId + '">'
                    + numberFormatter(productPrice) + '</span>원'
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

            $('select.cart-item-count').change(function(e){
                var sumPrice = $('#cartTotalPrice');
                var sum=0;

               $('select.cart-item-count').each(function(i, v){
                   var id = $(this).attr('data-id');
                   var cnt = parseInt($(this).val());
                   var price;
                   var total;

                   price = parsePrice($('#cart-item-'+id).text());
                   total = price * cnt;
                   sum+=total;
               });

               sumPrice.text(numberFormatter(sum));
           });

        }




        $('.cart-delete-btn').click(function(e){
            e.preventDefault();

            if(confirm('이 제품을 장바구니에서 삭제 하시겠습니까?')){

                var type = $(this).attr('data-type');
                var id = $(this).attr('data-id');

                $.ajax({
                      url: '/user/cart/del/',
                      dataType: 'json',
                      data : {product_or_set_id : id , type : type},
                      async : true,
                      type:'post',
                      success: function(data){

                          location.reload();
                      },
                      error:function(jqXHR, textStatus, errorThrown){
                          console.log(textStatus);
                      }
                });

            }
        });
    };



    $('a.collapse-btn').click(function(e){
        e.preventDefault();
        var collapsedMenu = $(this).next('.list-collapsed');

        if(collapsedMenu.hasClass('list-collapsed-opened')){
            collapsedMenu.removeClass('list-collapsed-opened');
        }else{
            collapsedMenu.addClass('list-collapsed-opened');
        }
    });





    $('#openCartBtn').click(function(e){
        e.preventDefault();
        $.mobile.loading('show');
        var target = $('#cartPanel .custom-menu-list');

        if(target.length != 0){
            target.html('');
            if($('.cart-delete-btn').length > 0){
                $('.cart-delete-btn').unbind('click');
            }

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
        }else{
            $.mobile.loading('hide');
            $('#cartPanel').panel('open');
        }
    });

    $('#cartBuyBtn').click(function(e){
        e.preventDefault();
        console.log('here');
        $('#cartBuyForm').submit();
    });

});