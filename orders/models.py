from django.db import models
from shop.models import Product

# Create your models here.


class Order(models.Model):
    first_name = models.CharField('Nome', max_length=100)
    last_name = models.CharField('Sobrenome', max_length=100)
    email = models.EmailField()
    address = models.CharField('Endereço', max_length=250)
    postal_code = models.CharField('Código postal', max_length=20)
    city = models.CharField('Cidade', max_length=100)
    created = models.DateTimeField('Criado', auto_now_add=True)
    updated = models.DateTimeField('Modificado', auto_now=True)
    paid = models.BooleanField('Pago', default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Order {self.id}"
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Produto')
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Quantidade', default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity