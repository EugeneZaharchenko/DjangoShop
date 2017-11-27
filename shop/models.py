from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='наименование')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='краткое наименование')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(verbose_name='Краткое описание' ,max_length=200, db_index=True)
    image = models.ImageField('Фото',upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(verbose_name='Описание товара' ,blank=True)
    price = models.DecimalField(verbose_name='цена',max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(verbose_name='акция')
    available = models.BooleanField(verbose_name='наличие' ,default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
