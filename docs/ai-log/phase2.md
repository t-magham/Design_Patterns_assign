**Question asked to AI:**

> "We have a `ShopFacade` class with static methods that coordinates `ProductFactory`, `CartItem`, `Customer`, and `ShoppingCart`. 
> We also considered Proxy as an alternative. What is the fundamental difference between Facade and Proxy, and how do I know which one fits our case?"

---

**ANSWER:**

Facade and Proxy are both structural patterns that wrap access to something, but they solve different problems.

- Facade is about **simplifying access to a complex subsystem**. It sits in front of multiple classes and provides a unified, simpler interface.
  The client doesn't need to know the subsystem exists. Facade doesn't restrict or modify what the subsystem does — it just makes it easier to reach.

- Proxy is about **controlling access to a single object**. It wraps one specific object and stands in for it — the client thinks it's talking to the real object,
  but the Proxy intercepts the call to add behavior like lazy loading, caching, logging, or access control. The Proxy and the real object share the same interface.

In your case, `ShopFacade` coordinates four different classes — `ProductFactory`, `CartItem`, `Customer`, `ShoppingCart`. 
That is a subsystem, not a single object. The goal is simplification, not access control. Facade is the correct choice.

---

**Criticism of ANSWER:**

One thing ANS gets right is the core distinction. But it is **incomplete in one important way**: it doesn't mention that `ShopFacade` uses `@staticmethod` throughout, 
which means it has no instance state. A real Facade often holds references to the subsystem objects it coordinates — for example `self.factory = ProductFactory()` — 
so it can manage their lifecycle. The current implementation just calls subsystem classes directly inside each method, which works but means the Facade provides 
no encapsulation of *which* subsystem implementations are used. If you wanted to swap `ProductFactory` for a database-backed version, you'd have to change the Facade's 
method bodies directly.