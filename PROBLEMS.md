# Phase 0

## INITIAL DESIGN PROBLEMS:

1. ShoppingCart class is fat, it stores CartItems, applies discount, and calculates total:
    this broke the separation of concerns in the SRP, also we have the 'God class' code smell.
2. apply_discount(): if/else chain, when wanting to add new discount, we need to change the code,
    breaks the OCP
3. discount is passed as a string: very error-prone and unstable.
4. *def add_item(self, item: CartItem):* this makes the ShoppingCart class tightly coupled to the
    CartItem class, which breaks the DIP(Dependency inversion), the ShoppingCart class should not
    have to know about the internals of the CartItem class. Passing the Product and quantity
    directly is the better strategy.
5. ShoppingCart mixes business logic and UI: print(...) inside apply_discount() is a bad separation of concerns.

---

## AI RESPONSE: 
*PROMPT*: "What design cues are visible in this code? 
What design patterns could solve these problems? Write a brief description for each problem."

## Design Issues & Patterns

### 1. **No Input Validation** → *Decorator Pattern*
`set_price`, `CartItem`, and `Customer.__init__` accept any value — negative prices, zero quantities, invalid ages. A Decorator can wrap objects to add validation logic without modifying the core classes.

---

### 2. **Hardcoded Discount Logic** → *Strategy Pattern*
`apply_discount` uses chained `if/elif` — adding a new discount type means editing the class directly, violating the **Open/Closed Principle**. Strategy defines each discount as a separate interchangeable object, so new discounts are *added*, never *modified*.

---

### 3. **Cart Doesn't React to Price Changes** → *Observer Pattern*
`_totalPrice` is calculated at `add_item` time. If `p1.set_price(500)` is called later, the cart total is silently stale. Observer lets the cart *subscribe* to product price changes and recalculate automatically.

---

### 4. **No Controlled Object Creation** → *Factory Pattern*
`Product`, `CartItem`, and `Customer` are instantiated raw everywhere. A Factory centralises and standardises creation — useful when object setup grows more complex (e.g. loading from a database).

---

### 5. **One Cart Per Customer, Forever** → *Prototype Pattern*
`ShoppingCart` is hardcoded inside `Customer.__init__` — there's no way to clone, save, or reset a cart state. Prototype allows cloning an existing cart as a template (e.g. "reorder last cart").

---

### 6. **Scattered Cart Operations** → *Facade Pattern*
The caller must manually create `Product → CartItem → Customer → add_item_to_cart`. Facade wraps this pipeline behind a single clean interface like `store.purchase("iphone", qty=2, customer="jack")`.

## Comment on AI answer:

There is a huge difference between my initial response and AI response, it really discovers problems I didn't think about.

