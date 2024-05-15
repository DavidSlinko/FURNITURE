from random import randint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, CustomerForm, ShippingForm, EditProfileForm
from .utils import CartForAuthenticatedUser, get_cart_data
#import stripe
from furniture_project import settings


# Create your views here.

class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    template_name = 'pages/index.html'
    extra_context = {
        'title': 'LM'
    }

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories


# страница категорий товара
class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'pages/category.html'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = category.products.all()
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = category.products.all()

        prices = list(set([i.price for i in products]))

        context['prices'] = prices

        context['title'] = f'Товары категории: {category.title}'
        context['category'] = category

        return context


# Логин
def user_login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    messages.success(request, 'Вы вошли в аккаунт')
                    return redirect('index')
                else:
                    messages.error(request, 'Не верный логин или пароль')
                    return redirect('login')
            else:
                messages.error(request, 'Не верный логин или пароль')
                return redirect('login')

        else:
            form = LoginForm()

        context = {
            'title': 'Вход в аккаунт',
            'form': form
        }
        return render(request, 'pages/login.html', context)


# Выход
def user_logout_view(request):
    logout(request)
    messages.warning(request, 'Вы вышли с аккаунта')
    return redirect('index')


# Регистрация
def user_register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                messages.success(request, 'Вы успешно зарегистрировались. Войдите в аккаунт')
                return redirect('login')
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
                    return redirect('register')
        else:
            form = RegisterForm

        context = {
            'title': 'Регистрация',
            'form': form
        }
        return render(request, 'pages/register.html', context)


# Страница продукта
class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'pages/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'Товар {product.title}'

        products = Product.objects.filter(category=product.category)
        data = []
        for i in range(3):
            random_index = randint(0, len(products) - 1)  # Рандомный индекс
            p = products[random_index]  # Товары по рандомному индексу
            if p not in data and product != p:
                data.append(p)

        context['products'] = data

        return context


# Получения цвета
def get_product_by_color(request, model_product, color_code):
    product = Product.objects.get(model_product=model_product, color_code=color_code)

    products = Product.objects.filter(category=product.category)
    data = []
    for i in range(3):
        random_index = randint(0, len(products) - 1)
        p = products[random_index]
        if p not in data and product != p:
            data.append(p)

    context = {
        'title': f'Товар {product.title}',
        'product': product,
        'products': data
    }

    return render(request, 'pages/product.html', context)


# Избранное
def save_favorite_product(request, slug):
    if request.user.is_authenticated:


        user = request.user
        product = Product.objects.get(slug=slug)
        favorite_products = FavoriteProduct.objects.filter(user=user)


        if user:
            if product not in [i.product for i in favorite_products]:
                messages.success(request, 'Товар успешно добавлен в избранное')
                FavoriteProduct.objects.create(user=user, product=product)
            else:
                fav_product = FavoriteProduct.objects.get(user=user, product=product)
                messages.warning(request, 'Товар удален из избранного')
                fav_product.delete()

            page = request.META.get('HTTP_REFERER', 'index')
            return redirect(page)
    else:
        messages.warning(request, 'Для добавления товара в избранное войдите или зарегестрируйте аккаунт')
        return redirect('login')


# Страница избранного
class FavoriteProductView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    context_object_name = 'products'
    template_name = 'pages/favorite.html'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        favorite_products = FavoriteProduct.objects.filter(user=user)
        product = [i.product for i in favorite_products]
        return product


# добавление товара в корзину
def to_cart_view(request, slug, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, slug, action)
        page = request.META.get('HTTP_REFERER', 'index')

        return redirect(page)
    else:
        messages.warning(request, 'Пройдите регистрацию')
        return redirect('login')


# Страница корзины
def my_cart_view(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Моя корзина',
            'order': cart_info['order'],
            'products': cart_info['products']
        }
        return render(request, 'pages/my_cart.html', context)

    else:
        messages.warning(request, 'Пройдите регистрацию')
        return redirect('login')


# Оформление заказа
def checkout_view(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Оформление заказа',
            'order': cart_info['order'],
            'items': cart_info['products'],

            'customer_form': CustomerForm(),
            'shipping_form': ShippingForm()
        }
        return render(request, 'pages/checkout.html', context)
    else:
        return redirect('login')


# Оплата
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data['first_name']
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.email = customer_form.cleaned_data['email']
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()
        else:
            for field in shipping_form.errors:
                messages.error(request, shipping_form.errors[field].as_text())

        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Товары FURNITURE'
                    },
                    'unit_amount': int(total_price)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )
        return redirect(session.url, 303)


# Страница оплаты
def success_payment(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        if request.method == 'POST':
            form = EditProfileForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in cart_info:
                    OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                             quantity=item['quantity'])

        user_cart.clear()
        messages.success(request, 'Оплата прошла успешно')
        return render(request, 'pages/success.html')
    else:
        return redirect('index')


# Профиль
def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    user_orders = Order.objects.filter(user=request.user)
    user_order_item = OrderItem.objects.all()

    context = {
        'title': f'Профиль: {profile.user.username}',
        'profile': profile,
        'user_orders': user_orders,
        'user_order_item': user_order_item
    }
    return render(request, 'pages/profile.html', context)


# Изменения профиля
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            return redirect('profile', request.user.pk)  # Замените 'profile' на имя вашей страницы профиля
    else:
        edit_profile_form = EditProfileForm(instance=profile)

    return render(request, 'pages/edit_profile.html', {'edit_profile_form': edit_profile_form})
