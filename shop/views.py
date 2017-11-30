from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products_list = Product.objects.filter(available=True)
    paginator = Paginator(products_list, 2)


    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=category)

    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


# class EIndexView(View):
#     def get(self, request):
#
#         # Забираем все продукты отсортировав их по дате обновл-я
#         all_products = Product.objects.filter(available=True).order_by('-updated')
#         # Создаём Paginator, в который передаём продукты и указываем,
#         # что их будет 3 штук на одну страницу
#         current_page = Paginator(all_products, 3)
#
#         # Pagination в django_bootstrap3 посылает запрос вот в таком виде:
#         # "GET /?page=2 HTTP/1.0" 200,
#         # Поэтому нужно забрать page и попытаться передать его в Paginator,
#         # для нахождения страницы
#         page = request.GET.get('page')
#         try:
#             # Если существует, то выбираем эту страницу
#             context['article_lists'] = current_page.page(page)
#         except PageNotAnInteger:
#             # Если None, то выбираем первую страницу
#             context['article_lists'] = current_page.page(1)
#         except EmptyPage:
#             # Если вышли за последнюю страницу, то возвращаем последнюю
#             context['article_lists'] = current_page.page(current_page.num_pages)
#
#         return render_to_response('home/index.html', context)