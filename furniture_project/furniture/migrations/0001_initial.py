# Generated by Django 5.0.2 on 2024-02-10 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='Краткоео описание к слайдеру')),
                ('description', models.CharField(max_length=400, verbose_name='Под описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images_slider/', verbose_name='Картинка для слайдера')),
            ],
            options={
                'verbose_name': 'Слайдер',
                'verbose_name_plural': 'Слайдер',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название категории')),
                ('images', models.ImageField(upload_to='categories/', verbose_name='Иконка категории')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='furniture.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название товара')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание к товару')),
                ('price', models.FloatField(verbose_name='Цена товара')),
                ('quantity', models.IntegerField(verbose_name='Количество на складе')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('color_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Название цвета')),
                ('color_code', models.CharField(blank=True, max_length=150, null=True, verbose_name='Код цвета')),
                ('model_product', models.CharField(blank=True, max_length=100, null=True, verbose_name='Модель товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='furniture.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Картинка товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='furniture.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Картинка товара',
                'verbose_name_plural': 'Картинки товара',
            },
        ),
    ]
