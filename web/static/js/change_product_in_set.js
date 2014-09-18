/**
 * Created by Park-Kunbae on 14. 3. 27.
 */
var c_test;
$(function(){
    $('.changeable-collapse-btn').click(function(e){
        e.preventDefault();

        var collapsedMenu = $(this).parent().next('.list-collapsed');

        if(collapsedMenu.hasClass('list-collapsed-opened')){
            collapsedMenu.removeClass('list-collapsed-opened');
        }else{
            collapsedMenu.addClass('list-collapsed-opened');
        }
    });

    $('.view-description-btn').click(function(e){
        e.preventDefault();

        var description = $('#popup-product-description');
        var img = $('#popup-product-image');

        description.text( $(this).parent().attr('product-description') );
        img.attr("src", $(this).parent().attr('product-image-url') );

        var dialog = $('#product-description-dialog');
        dialog.popup('open');
    });

    $('.custom-product-btn').click(function(e){
        var selected_item = $(this).parent();

        var new_product_id = selected_item.attr('product-id');
        var original_product_id = selected_item.attr('original-product-id');
        var original_item = $(".change-list-wrapper[original-product-id='"+original_product_id+"']");
        c_test = original_item;

//        console.log(product_detail_in_json_url(new_product_id));
        $.ajax({
            url: product_detail_in_json_url(new_product_id),
            dataType: 'json',
            async: true,
            type: 'POST',
            success: function(data) {
//                original_item.find('.changeable-item-img img').attr('src', data.small_img_url);
                console.log(data)
                original_item.attr('product-id',data.id);
                original_item.find('#changeable-product-name').text(data.name);
                original_item.find('#changeable-product-price').text(data.discount_price);
            },
            error:function(jqXHR, textStatus, errorThrown){
                
            }
        });




//        original_item.find('.changeable-item-img img').attr('src', new_product_img_url);

    });

});