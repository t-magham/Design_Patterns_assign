# AI Log — Phase 3 Pair Programming Session

**Date:** 2025  
**Duration:** ~35 minutes  
**Tool:** Claude (Anthropic)

---

## Session Summary

### Opening — Pattern Selection (min 0–8)

I opened by showing the Phase 2 code and asking which behavioral patterns made sense for the system.

**Me:** Phase 3 requires at least 2 behavioral patterns. Looking at my code, I have the Discount hierarchy already — does that count as Strategy?

**AI:** Structurally yes, but not formally. Right now `Discount` is a plain base class using `raise NotImplementedError` — that's a convention, not a contract. Python doesn't stop anyone from instantiating `Discount` directly. To make it a proper Strategy, it needs to become an `ABC` with `@abstractmethod`. That one change is also your OCP demonstration — `SeasonalDiscount` can be added as a new class with zero changes to existing code.

**Me:** What's the second pattern?

**AI:** Observer fits naturally. Right now nothing reacts when items are added or discounts are applied. In a real e-commerce system you'd want logging, email notifications, inventory tracking — all triggered by cart events. `ShoppingCart` becomes the subject, observers subscribe to it, and adding new behavior means adding a new class — `ShoppingCart` never changes.

---

### ABC Discussion (min 8–15)

**Me:** What is ABC exactly, and why does it matter here?

**AI:** `ABC` stands for Abstract Base Class. Without it, `Discount` is just a regular class — subclasses override `apply` by convention but nothing enforces it. With `ABC` and `@abstractmethod`, Python raises a `TypeError` immediately if you try to instantiate the abstract class or any subclass that forgot to implement `apply`.

**Me:** Should `DiscountDecorator` also be abstract? It doesn't implement `apply` either.

**AI:** Correct — it shouldn't be instantiable. Add `ABC` to its inheritance: `class DiscountDecorator(Discount, ABC)`. Since it doesn't re-declare `@abstractmethod apply`, the explicit `ABC` is what signals to Python that this class itself cannot be instantiated.

**Me:** So the hierarchy becomes: `Discount` (abstract) → `DiscountDecorator` (abstract) → concrete subclasses?

**AI:** Exactly. Every class that can't stand alone is abstract. Every class you actually use is concrete. That's the correct design.

---

### Observer Implementation (min 15–25)

**Me:** Who should subscribe to `ShoppingCart`?

**AI:** Three things fit naturally: `Logger` reacts to all events, `EmailNotifier` reacts only to checkout, `InventoryTracker` reacts only to item_added. `ShoppingCart` only knows about the abstract `Observer` — it never imports any of the concrete classes.

We then wired `_observers: list[Observer]` into `ShoppingCart`, added `attach()` and `_notify()`, and called `_notify` from `add_item`, `apply_discount`, and a new `checkout` method. `ShopFacade` got `attach_observer` and `checkout` static methods so the caller never touches the cart directly.

**Me:** Should the observer receive the event name and the cart itself?

**AI:** Yes — passing both gives observers full context. `EmailNotifier` needs `cart.get_total()` to build the confirmation message. `InventoryTracker` needs `cart.items[-1]` to know what was just added. Without passing the cart, observers would need their own state tracking which creates coupling.

---

### OCP Demonstration (min 25–32)

**Me:** How do I demonstrate OCP clearly for the grader?

**AI:** `SeasonalDiscount` is your proof. Add it as a new class inheriting `DiscountDecorator`, implement `apply`, add one `elif` in `DiscountFactory` — done. Point to it explicitly in your PR description: "no existing class was modified to add this behavior." That single example satisfies the requirement cleanly.

---

## What the AI Got Right

- Correctly identified that `Discount` was Strategy in structure but not in contract, and that formalizing it with `ABC` was the right move
- The Observer subscriber question was answered with concrete, domain-appropriate examples rather than generic ones
- Caught that `DiscountDecorator` also needed `ABC` when questioned — did not suggest this proactively

## Where the AI Fell Short

- Initially suggested `@abstractmethod apply` on `DiscountDecorator` as the fix, which would have worked but was less explicit than `(Discount, ABC)`. Only arrived at the cleaner solution after I pushed back.
- Did not proactively mention that passing `cart` to `observer.update()` was necessary — I had to ask whether observers should receive context. A more complete answer would have flagged this upfront.
- The AI did not mention that `_notify` in `apply_discount` fires after the discount is calculated but the cart total hasn't changed — observers receiving `"discount_applied"` still see the pre-discount total from `get_total()`. This is a real limitation worth noting.

---

## Reflection

**How long would this phase have taken without AI?**  
Pattern selection alone would have taken 1–2 hours of reading. Implementing `ABC` correctly, understanding the difference between `raise NotImplementedError` and `@abstractmethod`, and wiring Observer without introducing coupling would realistically have taken a full afternoon — 3 to 4 hours total. With AI the implementation took about 35 minutes.

**Where did AI fail?**  
The `DiscountDecorator` / `ABC` issue required me to push back to get the right answer. The Observer context-passing issue required me to ask the right question. AI is good at answering questions you know to ask — it's weaker at spotting the things you don't know you're missing.