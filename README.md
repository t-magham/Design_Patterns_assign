# 🛒 E-Commerce Shopping Cart — Design Patterns Assignment

A shopping cart system built in Python, developed across 3 phases as part of a university design patterns course. The project intentionally starts with poorly structured code (Phase 0) and evolves through creational, structural, and behavioral patterns — each phase fixing real design problems identified in the previous one.

---

## What It Does

- Add products to a customer's shopping cart
- Stack multiple discount types on top of each other
- React to cart events (item added, discount applied, checkout) via observers
- Hide subsystem complexity behind a single Facade interface

---

## Patterns Used

### Creational
| Pattern | Where | Why |
|---|---|---|
| **Factory Method** | `DiscountFactory`, `ProductFactory` | Centralizes object creation. Callers never instantiate products or discounts directly — they request them by type string. Adding a new type requires no changes to calling code. |

### Structural
| Pattern | Where | Why |
|---|---|---|
| **Decorator** | `DiscountDecorator`, `StudentDiscount`, `FirstTimeUserDiscount`, `SeasonalDiscount` | Allows stacking multiple discounts without modifying existing classes. Each decorator wraps another `Discount` and delegates inward before applying its own rate. |
| **Facade** | `ShopFacade` | Hides the coordination of `ProductFactory`, `CartItem`, `Customer`, and `ShoppingCart` behind a single entry point. Callers never interact with subsystem classes directly. |

### Behavioral
| Pattern | Where | Why |
|---|---|---|
| **Strategy** | `Discount` (ABC), all discount subclasses | Each discount type encapsulates its own calculation algorithm. `Discount` is a formal abstract base class — Python enforces that every concrete discount implements `apply()`. |
| **Observer** | `Observer` (ABC), `Logger`, `EmailNotifier`, `InventoryTracker` | `ShoppingCart` notifies all attached observers on cart events. New reactions (logging, email, inventory) are added as new classes — `ShoppingCart` is never modified. |

---

## Architecture Diagram

```mermaid
classDiagram
    class Customer {
        +name: str
        +age: int
        +shopping_cart: ShoppingCart
        +add_item_to_cart(item: CartItem)
    }

    class ShoppingCart {
        +items: list~CartItem~
        +_observers: list~Observer~
        +attach(observer: Observer)
        +add_item(item: CartItem)
        +get_total(): float
        +apply_discount(discount_types: list~str~): float
        +checkout()
    }

    class CartItem {
        +product: Product
        +quantity: int
        +get_price(): float
    }

    class Product {
        -_name: str
        -_price: float
        +get_price(): float
        +set_price(new_price: float)
        +get_name(): str
        +set_name(new_name: str)
    }

    class Discount {
        <<abstract>>
        +apply(price: float)* float
    }

    class NoDiscount {
        +apply(price: float) float
    }

    class DiscountDecorator {
        +wrapped_discount: Discount
        +__init__(discount: Discount)
    }

    class StudentDiscount {
        +apply(price: float) float
    }

    class FirstTimeUserDiscount {
        +apply(price: float) float
    }

    class SeasonalDiscount {
        +apply(price: float) float
    }

    class DiscountFactory {
        +create(discount_types: list~str~)$ Discount
    }

    class ProductFactory {
        +create(product_type: str)$ Product
    }

    class ShopFacade {
        +add_to_cart(c: Customer, p_name: str, qnt: int)$
        +apply_discount(c: Customer, discount_type: list~str~)$
        +get_total(c: Customer)$
        +attach_observer(c: Customer, observer: Observer)$
        +checkout(c: Customer)$
    }

    class Observer {
        <<abstract>>
        +update(event: str, cart: ShoppingCart)*
    }

    class Logger {
        +update(event: str, cart: ShoppingCart)
    }

    class EmailNotifier {
        +update(event: str, cart: ShoppingCart)
    }

    class InventoryTracker {
        +update(event: str, cart: ShoppingCart)
    }

    %% Core
    Customer *-- ShoppingCart : has-a
    ShoppingCart o-- CartItem : contains
    CartItem --> Product : references

    %% Strategy + Decorator
    Discount <|.. NoDiscount : implements
    Discount <|.. DiscountDecorator : implements
    DiscountDecorator o-- Discount : wraps
    DiscountDecorator <|-- StudentDiscount : extends
    DiscountDecorator <|-- FirstTimeUserDiscount : extends
    DiscountDecorator <|-- SeasonalDiscount : extends

    %% Factory
    DiscountFactory ..> Discount : creates
    ProductFactory ..> Product : creates
    ShoppingCart ..> DiscountFactory : uses

    %% Observer
    Observer <|.. Logger : implements
    Observer <|.. EmailNotifier : implements
    Observer <|.. InventoryTracker : implements
    ShoppingCart o-- Observer : notifies

    %% Facade
    ShopFacade ..> Customer : coordinates
    ShopFacade ..> ProductFactory : delegates
    ShopFacade ..> CartItem : orchestrates
    ShopFacade ..> ShoppingCart : delegates
```

---

## How It Works

A customer's cart is managed entirely through `ShopFacade`. When `add_to_cart` is called, the Facade creates a `Product` via `ProductFactory`, wraps it in a `CartItem`, and adds it to the customer's `ShoppingCart`. The cart then fires an `"item_added"` event to all attached observers.

When `apply_discount` is called with a list of discount type strings, `DiscountFactory` builds a chain of Decorator objects — each wrapping the previous one — and calls `apply()` on the outermost, which delegates inward. The result is the final discounted price. A `"discount_applied"` event is fired after.

When `checkout` is called, a `"checkout"` event fires — `EmailNotifier` reacts to this and sends a confirmation.

---

## How to Run

No dependencies outside the Python standard library.

```bash
# Clone the repo
git clone <your-repo-url>
cd <repo-folder>

# Run 
python main.py
```

Expected output:
```
[LOG] item_added
[INVENTORY] macbook — 3 unit(s) reserved
[LOG] item_added
[INVENTORY] iphone — 1 unit(s) reserved
[LOG] discount_applied
[EMAIL] Sending order confirmation — total: $4499.97
```

---

## Project Structure

```
├── README.md                  
├── PATTERNS.md               ← Documenting patterns per phase
├── PROBLEMS.md               ← initial code analysis (Faz 0)
├── main.py                       ← source code
├── docs/
│   ├── diagrams/              ← UML diagrams
│   └── ai-log/
│       ├── phase1.md
│       ├── phase2.md
│       └── phase3.md
└── .github/workflows/ci.yml 
```
