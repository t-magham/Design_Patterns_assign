## Before: The Original Architecture

```classDiagram
    class Customer {
        +name: str
        +age: int
        +shopping_cart: ShoppingCart
        +add_item_to_cart(item: CartItem)
        +get_discount(discount: str)
    }
    
    class ShoppingCart {
        +items: list~CartItem~
        -_totalPrice: float
        +add_item(item: CartItem)
        +apply_discount(discount: str)
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
    }

    Customer *-- ShoppingCart : has-a (Composition)
    ShoppingCart o-- CartItem : contains (Aggregation)
    CartItem --> Product : references
```

## After: Introducing Factories and Strategies

```classDiagram
    class Customer {
        +name: str
        +age: int
        +shopping_cart: ShoppingCart
        +add_item_to_cart(item: CartItem)
        +get_discount(discount: str)
    }
    
    class ShoppingCart {
        +items: list~CartItem~
        -_totalPrice: float
        +add_item(item: CartItem)
        +apply_discount(discount_type: str)
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
    }

    class Discount {
        <<interface>>
        +apply(price: float)* float
    }
    
    class StudentDiscount {
        +apply(price: float) float
    }
    
    class FirstTimeUserDiscount {
        +apply(price: float) float
    }
    
    class DiscountFactory {
        +create(discount_type: str)$ Discount
    }
    
    class ProductFactory {
        +create(type: str)$ Product
    }

    %% Core Relationships
    Customer *-- ShoppingCart : has-a
    ShoppingCart o-- CartItem : contains
    CartItem --> Product : references
    
    %% Discount Strategy & Factory Relationships
    Discount <|.. StudentDiscount : implements
    Discount <|.. FirstTimeUserDiscount : implements
    DiscountFactory ..> Discount : creates
    ShoppingCart ..> DiscountFactory : uses
    
    %% Product Factory Relationships
    ProductFactory ..> Product : creates
```