class Product:
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    def get_price(self) -> float:
        return self._price

    def set_price(self, new_price: float):
        self._price = new_price
    def get_name(self):
        return self._name
    def set_name(self, new_name: str):
        self._name = new_name

class CartItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def get_price(self):
        return self.product.get_price() * self.quantity

class Discount:
    def apply(self, price: float) -> float:
        raise NotImplementedError

class NoDiscount(Discount):
    def apply(self, price: float) -> float:
        return price # base case for our decorator

class DiscountDecorator(Discount):
    def __init__(self, discount: Discount):
        self.wrapped_discount = discount

class StudentDiscount(DiscountDecorator):
    def apply(self, price: float) -> float:
        price = self.wrapped_discount.apply(price)
        return price * 0.7

class FirstTimeUserDiscount(DiscountDecorator):
    def apply(self, price: float) -> float:
        price = self.wrapped_discount.apply(price)
        return price * 0.5

class DiscountFactory:
    @staticmethod
    def create(discount_types: list[str]) -> Discount:
        discount = NoDiscount()
        for t in discount_types:
            if t == "Student":
                discount = StudentDiscount(discount)
            elif t == "FirstTimeUser":
                discount = FirstTimeUserDiscount(discount)
            else:
                raise ValueError(f"Unknown discount: {t}")
        return discount

class ShoppingCart:
    def __init__(self):
        self.items: list[CartItem] = []

    def add_item(self, item: CartItem): 
        self.items.append(item)

    def get_total(self):
        return sum(item.get_price() for item in self.items)

    def apply_discount(self, discount_type: list[str]):
        try:
            # The Factory handles the logic. The Cart just uses the result!
            discount = DiscountFactory.create(discount_type)
            return discount.apply(self.get_total())
        except ValueError as e:
            print(e)

class Customer:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.shopping_cart = ShoppingCart()
    def add_item_to_cart(self, item: CartItem):
        self.shopping_cart.add_item(item)

class ProductFactory:
    @staticmethod
    def create(product_type: str)-> Product:
        if product_type == "iphone":
            return Product("iphone", 999.99)
        elif product_type == "macbook":
            return Product("macbook", 1499.99)
        raise ValueError("Unexpected product type")

class ShopFacade:
    @staticmethod
    def add_to_cart(c: Customer, p_name: str, qnt: int):
        p = ProductFactory.create(p_name)
        ci = CartItem(p, qnt)
        c.add_item_to_cart(ci)
    @staticmethod
    def apply_discount(c: Customer, discount_type: list[str]):
        return c.shopping_cart.apply_discount(discount_type)
    @staticmethod
    def get_total(c: Customer):
        return c.shopping_cart.get_total()

# now we can hide a lot of complexity
c0 = Customer("Taregh", 20)
ShopFacade.add_to_cart(c0, "macbook", 3)
price_b4_discount = ShopFacade.get_total(c0)
discounted_price = ShopFacade.apply_discount(c0, ["Student", "FirstTimeUser"])


p1 = ProductFactory.create("iphone")
p2 = ProductFactory.create("macbook")

ci1 = CartItem(p1, 2)
ci2 = CartItem(p2, 3)

c1 = Customer("jack", 18)
c1.add_item_to_cart(ci2)

