class Product:
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    def get_price(self) -> float:
        return self._price

    def set_price(self, new_price: float):
        self._price = new_price

class CartItem(object):
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def get_price(self):
        return self.product.get_price() * self.quantity

class ShoppingCart:
    def __init__(self):
        self.items: list[CartItem] = []
        self._totalPrice = 0

    def add_item(self, item: CartItem): 
        self.items.append(item)
        self._totalPrice += item.get_price()

    def apply_discount(self, discount: str):
        if discount == "First Time User":
            print(f"50% discount on your fist order!")
            self._totalPrice *= 0.5
        elif discount == "Student":
            print(f"30% discount for students")
            self._totalPrice *= 0.7
        else:
            print("invalid discount!")

class Customer:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.shopping_cart = ShoppingCart()
    def add_item_to_cart(self, item: CartItem):
        self.shopping_cart.add_item(item)
    def get_discount(self, discount: str):
        self.shopping_cart.apply_discount(discount)

p1 = Product("iphone", 999.99)
p2 = Product("macbook", 1499.99)

ci1 = CartItem(p1, 2)
ci2 = CartItem(p2, 3)

c1 = Customer("jack", 18)
c1.add_item_to_cart(ci2)

