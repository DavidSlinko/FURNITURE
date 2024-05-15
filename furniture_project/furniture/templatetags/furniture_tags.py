from django import template
from furniture.models import Category, Slider, Product, FavoriteProduct

register = template.Library()


# Возвращает все категории на все страницы
@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=None)


# Возвращение нормальной цены
@register.simple_tag()
def get_normal_price(price):
    return f'{int(price):_}'.replace('_', ' ')


# Получение цвета и модели товара
@register.simple_tag()
def get_colors(model_product):
    products = Product.objects.filter(model_product=model_product)
    list_colors = [i.color_code for i in products]
    return list_colors


# Получение избранного товара
@register.simple_tag()
def get_favorite_products(user):
    fav_products = FavoriteProduct.objects.filter(user=user)
    products = [i.product for i in fav_products]
    return products


# Получаем все данные из модели Slider
@register.simple_tag()
def get_sliders():
    return Slider.objects.all()
