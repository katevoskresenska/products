# Необходимо создать модели работы со складскими запасами товаров и процесса оформления заказа этих товаров.
# Cписок требований:
# 1) Создайте товар с такими свойствами, как имя(name), подробные сведения(description or details),
# количество на складе(quantity), доступность(availability), цена(price).
# 2) Добавить товар на склад
# 3) Удалить товар со склада
# 4) Распечатать остаток товара по его имени
# 5) Распечатать остаток всех товаров
# 6) Товар может принадлежать к категории
# 7) Распечатать список товаров с заданной категорией
# 8 ) Корзина для покупок, в которой может быть много товаров с общей ценой.
# 9) Добавить товары в корзину (вы не можете добавлять товары, если их нет в наличии)
# 10) Распечатать элементы корзины покупок с ценой и общей суммой
# 11) Оформить заказ и распечатать детали заказа по его номеру
# 12) Позиция заказа, созданная после оформления заказа пользователем.
# Он будет иметь идентификатор заказа(order_id), дату покупки(date_purchased), товары(items), количество(quantity)
# 13) После оформления заказа количество товара уменьшается на количество товаров из заказа.

from datetime import datetime


class Price:

    def __get__(self, instance, owner):
        return instance._price * 1.2

    def __set__(self, instance, value):
        instance._price = value


class Product(object):
    price = Price()

    def __init__(self, name, description, quantity, price, category=None):
        self.name = name
        self.description = description
        self.quantity = quantity
        if self.quantity > 0:
            self.availability = True
        else:
            self.availability = False
        self._price = price
        self.category = category

    def __repr__(self):
        return self.name

    def get_info(self):
        return self.__dict__


class Stock(object):
    products = []

    def list_products(self):
        return self.products

    def add_product(self, product):
        if not self.products:
            self.products.append(product)
        else:
            for i in self.products:
                if i.name == product.name:
                    i.quantity += product.quantity
                    break
                else:
                    self.products.append(product)
                    break

    def remove_from_stock(self, name):
        self.products = [i for i in self.products if i.name != name]

    def in_stock_by_name(self, name):
        for i in self.products:
            if i.name == name:
                return {i.name: i.quantity}

    def in_stock(self):
        in_stock = {}
        for i in self.products:
            in_stock[i.name] = i.quantity
        return in_stock

    def in_stock_by_cat(self, cat):
        by_cat = {cat: []}
        for i in self.products:
            if i.category == cat:
                by_cat[cat].append(i)
        return by_cat


class Cart(Stock):
    order_id = 0
    orders = []

    def __init__(self):
        self.items = []
        self.total = 0
        super().__init__()

    def add_to_cart(self, name, quantity):
        if self.in_stock_by_name(name).get(name) >= quantity:
            price = [i.price for i in self.products if i.name == name]
            self.items.append({name: {'quantity': quantity, 'price': price[0]}})
            for item in self.products:
                if item.name == name:
                    item.quantity -= quantity
            return self.items
        else:
            print(f"Not enough items, {self.in_stock_by_name(name).get(name)} is available")

    def list_cart(self):
        total = 0
        for item in self.items:
            values = list(item.values())
            sum_ = values[0].get('quantity') * values[0].get('price')
            total += sum_
        return {'items': self.items, 'total': total}

    def place_order(self):
        order_id = self.order_id + 1
        order = self.list_cart()
        order_time = str(datetime.now())
        order = {'order_id': order_id, 'order_info': order, 'order_time': order_time}
        self.orders.append(order)

    def get_order_by_id(self, order_id):
        for item in self.orders:
            if item.get('order_id') == order_id:
                return item
            else:
                print("Nothing found by id")


stock = Stock()

pr1 = Product(name='item1', description='description1', quantity=5, price=5, category='cat1')
pr2 = Product(name='item2', description='description2', quantity=20, price=20, category='cat2')
pr3 = Product(name='item3', description='description3', quantity=5, price=10, category='cat3')
pr4 = Product(name='item4', description='description4', quantity=50,  price=15, category='cat1')
print(pr3.get_info())
# {'name': 'item3', 'description': 'description3', 'quantity': 5, 'availability': True, 'price': 10, 'category': 'cat3'}

stock.add_product(pr1)
stock.add_product(pr2)
stock.add_product(pr3)
stock.add_product(pr4)
print('list_products', stock.list_products())  # list_products [item1, item2, item3, item4]

print('remove_from_stock', stock.remove_from_stock('item2'))  # None
print('list_products', stock.list_products())  # list_products [item1, item3, item4]

stock.add_product(Product(name='item1', description='description1', quantity=15, price=5, category='cat1'))
print('list_products', stock.list_products())  # list_products [item1, item3, item4]

for j in stock.products:
    print('products', j.__dict__)
# products {'name': 'item1', 'description': 'description1', 'quantity': 20, 'availability': True, 'price': 5, 'category': 'cat1'}
# products {'name': 'item3', 'description': 'description3', 'quantity': 5, 'availability': True, 'price': 10, 'category': 'cat3'}
# products {'name': 'item4', 'description': 'description4', 'quantity': 50, 'availability': True, 'price': 15, 'category': 'cat1'}

print('in_stock_by_name', stock.in_stock_by_name('item1'))  # in_stock_by_name {'item1': 20}

print('in_stock', stock.in_stock())  # in_stock {'item1': 20, 'item3': 5, 'item4': 50}
print('in_stock_by_cat', stock.in_stock_by_cat('cat1'))  # in_stock_by_cat {'cat1': [item1, item4]}

cart = Cart()
print('in_stock', stock.in_stock())
# in_stock {'item1': 20, 'item3': 5, 'item4': 50}
print('add_to_cart', cart.add_to_cart('item1', 2))  # add_to_cart [{'item1': {'quantity': 2, 'price': 6.0}}]
print('add_to_cart', cart.add_to_cart('item4', 10))
# add_to_cart [{'item1': {'quantity': 2, 'price': 6.0}}, {'item4': {'quantity': 10, 'price': 18.0}}]
print('in_stock', stock.in_stock())
# in_stock {'item1': 18, 'item3': 5, 'item4': 40}

print('list_cart', cart.list_cart())
# list_cart {'items': [{'item1': {'quantity': 2, 'price': 6.0}}, {'item4': {'quantity': 10, 'price': 18.0}}], 'total': 192.0}
print('place_order', cart.place_order())  # None
print('get_order_by_id', cart.get_order_by_id(1))
# get_order_by_id {'order_id': 1, 'order_info': {'items': [{'item1': {'quantity': 2, 'price': 6.0}},
# {'item4': {'quantity': 10, 'price': 18.0}}], 'total': 192.0}, 'order_time': '2021-03-05 16:32:23.747957'}
