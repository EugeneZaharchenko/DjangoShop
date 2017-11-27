from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='фамилия')
    last_name = models.CharField(max_length=50,verbose_name='имя')
    email = models.EmailField(verbose_name='электронная почта')
    address = models.CharField(max_length=250, verbose_name='адрес')
    postal_code = models.CharField(max_length=20, verbose_name='почтовый индекс')
    city = models.CharField(max_length=100, verbose_name='город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(verbose_name='Цена',max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='количество' , default=1)


    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
