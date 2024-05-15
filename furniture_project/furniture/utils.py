from .models import Order, OrderProduct, Customer, Product
from django.contrib import messages


class CartForAuthenticatedUser:
    def __init__(self, request, slug=None, action=None):
        self.user = request.user
        self.request = request

        if slug and action:
            self.add_or_delete(slug, action)

    # получени инфы о корзине
    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user)

        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.orderproduct_set.all()

        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'order': order,
            'products': order_products
        }

    # Добавления и удаление из корзины
    def add_or_delete(self, slug, action):
        order = self.get_cart_info()['order']
        product = Product.objects.get(slug=slug)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1
            messages.success(self.request, f'Товар {product.title} добавлен в козину')
        else:
            order_product.quantity -= 1
            product.quantity += 1
            messages.warning(self.request, f'Товар {product.title} удален из корзины')

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    # Очищение корзины после оплаты
    def clear(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            product.delete()
        order.save()


# будет возвращать инфу о корзине
def get_cart_data(request):
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()
    return cart_info
