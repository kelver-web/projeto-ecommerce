from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """Vai inicializar o carrinho de compras"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            """Salvar um carrinho de compras vazio na sessão do user"""
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Vai adicinar um produto no carrinho de  compras ou atualizar a quantidade"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] =  {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Irá marcar uma sessão como modificada para que seja salva"""
        self.session.modified = True

    def remove(self, product):
        """Remove os produtos"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Irá iterar pelos itens e obter os produtos do banco de dados"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Conta a quantidade de itens que estão no carrinho de compras"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """Remover o carrinho de compras"""
        del self.session[settings.CART_SESSION_ID]
        self.save()