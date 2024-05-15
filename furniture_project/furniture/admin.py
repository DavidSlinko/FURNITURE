from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .forms import CategoryForm


# Register your models here.


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'get_count_products', 'get_image_category')
    prepopulated_fields = {'slug': ['title']}
    form = CategoryForm

    # Метод для получени картинки категории
    def get_image_category(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="50" > ')
            except:
                return '-'
        else:
            return '-'

    # Метод для получения количества товара категории
    def get_count_products(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_image_category.short_description = 'Картинка'
    get_count_products.short_description = 'Количество товара'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'price', 'quantity', 'created_at', 'get_image_product')
    list_display_links = ('pk', 'title')
    prepopulated_fields = {'slug': ['title']}
    inlines = [GalleryInline]
    list_editable = ('price', 'quantity')

    def get_image_product(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75" > ')
            except:
                return '-'
        else:
            return '-'

    get_image_product.short_description = 'Картинка'


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'get_image_slider')
    list_display_links = ('pk', 'title')

    # Метод для получения картинки
    def get_image_slider(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_image_slider.short_description = 'Картинка'


admin.site.register(Gallery)
admin.site.register(FavoriteProduct)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
admin.site.register(City)
admin.site.register(Profile)
admin.site.register(OrderItem)


