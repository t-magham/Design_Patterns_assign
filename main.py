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

class Discount:
    def apply(self, price: float) -> float:
        raise NotImplementedError

class StudentDiscount(Discount):
    def apply(self, price: float) -> float:
        return price * 0.7

class FirstTimeUserDiscount(Discount):
    def apply(self, price: float) -> float:
        return price * 0.5

class DiscountFactory:
    @staticmethod
    def create(discount_type: str) -> Discount:
        if discount_type == "Student":
            return StudentDiscount()
        elif discount_type == "FirstTimeUser":
            return FirstTimeUserDiscount()
        raise ValueError(f"Unknown discount: {discount_type}")

class ShoppingCart:
    def __init__(self):
        self.items: list[CartItem] = []
        self._totalPrice = 0

    def add_item(self, item: CartItem): 
        self.items.append(item)
        self._totalPrice += item.get_price()

    def apply_discount(self, discount_type: str):
        try:
            # The Factory handles the logic. The Cart just uses the result!
            discount = DiscountFactory.create(discount_type)
            self._totalPrice = discount.apply(self._totalPrice)
            print(f"{discount_type} discount applied successfully!")
        except ValueError as e:
            print(e)

class Customer:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.shopping_cart = ShoppingCart()
    def add_item_to_cart(self, item: CartItem):
        self.shopping_cart.add_item(item)
    def get_discount(self, discount: str):
        self.shopping_cart.apply_discount(discount)

class ProductFactory:
    @staticmethod
    def create(type: str)-> Product:
        if type == "iphone":
            return Product("iphone", 999.99)
        elif type == "macbook":
            return Product("macbook", 1499.99)
        raise ValueError("Unexpected product type")

class ShopFacade:
    def add_to_cart(self, c: Customer, p_name: str, qnt: int):
        p = ProductFactory.create(p_name)
        ci = CartItem(p, qnt)
        c.add_item_to_cart(ci)
    def apply_discount(self, c: Customer, discount_type: str):
        c.get_discount(discount_type)

# now we can hide a lot of complexity
shop = ShopFacade()
c0 = Customer("Taregh", 20)
shop.add_to_cart(c0, "macbook", 3)
shop.apply_discount(c0, "Student")


p1 = ProductFactory.create("iphone")
p2 = ProductFactory.create("macbook")

ci1 = CartItem(p1, 2)
ci2 = CartItem(p2, 3)

c1 = Customer("jack", 18)
c1.add_item_to_cart(ci2)

