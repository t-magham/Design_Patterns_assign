from abc import ABC, abstractmethod

# Discount is now a formal abstract base class — each subclass is a Strategy
class Discount(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass

class NoDiscount(Discount):
    def apply(self, price: float) -> float:
        return price

class DiscountDecorator(Discount, ABC):
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

# OCP demonstration — new discount, zero existing code changed
class SeasonalDiscount(DiscountDecorator):
    def apply(self, price: float) -> float:
        price = self.wrapped_discount.apply(price)
        return price * 0.85

class DiscountFactory:
    @staticmethod
    def create(discount_types: list[str]) -> Discount:
        discount = NoDiscount()
        for t in discount_types:
            if t == "Student":
                discount = StudentDiscount(discount)
            elif t == "FirstTimeUser":
                discount = FirstTimeUserDiscount(discount)
            elif t == "Seasonal":
                discount = SeasonalDiscount(discount)
            else:
                raise ValueError(f"Unknown discount: {t}")
        return discount
    
# introduce observers
class Observer(ABC):
    @abstractmethod
    def update(self, event: str, cart: "ShoppingCart"):
        pass

class Logger(Observer):
    def update(self, event: str, cart: "ShoppingCart"):
        print(f"[LOG] {event}")

class EmailNotifier(Observer):
    def update(self, event: str, cart: "ShoppingCart"):
        if event == "checkout":
            print(f"[EMAIL] Sending order confirmation — total: ${cart.get_total():.2f}")

class InventoryTracker(Observer):
    def update(self, event: str, cart: "ShoppingCart"):
        if event == "item_added":
            last = cart.items[-1]
            print(f"[INVENTORY] {last.product.get_name()} — {last.quantity} unit(s) reserved")

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

class ShoppingCart:
    def __init__(self):
        self.items: list[CartItem] = []
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def _notify(self, event: str):
        for obs in self._observers:
            obs.update(event, self)

    def add_item(self, item: CartItem):
        self.items.append(item)
        self._notify("item_added")

    def get_total(self):
        return sum(item.get_price() for item in self.items)

    def apply_discount(self, discount_types: list[str]):
        try:
            discount = DiscountFactory.create(discount_types)
            result = discount.apply(self.get_total())
            self._notify("discount_applied")
            return result
        except ValueError as e:
            print(e)

    def checkout(self):
        self._notify("checkout")


class Customer:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.shopping_cart = ShoppingCart()

    def add_item_to_cart(self, item: CartItem):
        self.shopping_cart.add_item(item)


class ProductFactory:
    @staticmethod
    def create(product_type: str) -> Product:
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

    @staticmethod
    def attach_observer(c: Customer, observer: Observer):
        c.shopping_cart.attach(observer)

    @staticmethod
    def checkout(c: Customer):
        c.shopping_cart.checkout()



c0 = Customer("Taregh", 20)

ShopFacade.attach_observer(c0, Logger())
ShopFacade.attach_observer(c0, EmailNotifier())
ShopFacade.attach_observer(c0, InventoryTracker())

ShopFacade.add_to_cart(c0, "macbook", 3)
ShopFacade.add_to_cart(c0, "iphone", 1)

price_before = ShopFacade.get_total(c0)
discounted_price = ShopFacade.apply_discount(c0, ["Student", "Seasonal"])

ShopFacade.checkout(c0)