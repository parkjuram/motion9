from django.http.response import HttpResponse
from django.shortcuts import render
from motion9.const import *
from web.models import Product

# # def get_product_list(page_num=1, category_key=None):
# def getProductList(page_num=1, category_key=None):
#     stmt = g.db.session.query(Interest).filter(Interest.user_key == g.user.key if g.user else -1).subquery()
#
#     query = g.db.session.query(Product, Category.name.label('category_name'), stmt.c.key).\
#         outerjoin(stmt, Product.key == stmt.c.product_key).\
#         filter(Category.key == Product.category_key)
#
#     query = query.filter(Product.category_key == category_key) if category_key is not None else query
#
#     pager_indicator_total_length = int(math.ceil(float(query.count()) / ITEM_COUNT_PER_PAGE))
#     products_and_category_name_and_is_interested = \
#         query.order_by(Product.key).all() \
#         if page_num == 0 else \
#         query.order_by(Product.key).slice((page_num-1)*ITEM_COUNT_PER_PAGE, page_num*ITEM_COUNT_PER_PAGE).all()
#
#     product_list = []
#     for product, category_name, is_interested in products_and_category_name_and_is_interested:
#         product.category_name = category_name
#         product.is_interested = True if is_interested is not None else False
#
#         columns = get_table_columns(Product, ['category_name', 'is_interested'])
#         product_dict = get_dict_from_model(product, columns)
#         product_list.append(product_dict)
#
#     if page_num is not 0:
#         product_list = make_data_to_paging_format_dict(pager_indicator_total_length, page_num, product_list)
#     else:
#         product_list = {'data': product_list}
#
#     return product_list

def _get_product_list(category_id=None, page_num=1):
    product = Product.objects

    if category_id is not None:
        product.filter(category_id=category_id)

    products = product.all()


    print product


def shop_product_view(request, category_id=None, page_num=None):
    _get_product_list(category_id, page_num)

    return HttpResponse('good')
    # if page_num is None:



    # if pageNum == None:
    #     if category_key == None:
    #         products = getProductList(1)
    #     else :
    #         products = getProductList(1,category_key)
    # else :
    #     if category_key == None:
    #         products = getProductList(pageNum)
    #     else :
    #         products = getProductList(pageNum, category_key)
    #
    # categories = getCategoryList(False)
    # return render_template('shopping_product_web.html', products = products, current_page='shopping2', current_category=category_key, categories=categories)
    #
    # return HttpResponse(str(category_key))