"""
================================================================================
 Assignment 03 — Refactor the Messy Store System
 192-201 Advanced Computer Programming with Generative AI
 Week 5 — OOP Design & Refactoring
================================================================================
"""

import io
import contextlib


# ==============================================================================
# LEGACY STORE SYSTEM — DO NOT EDIT THIS SECTION
# ==============================================================================

PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]

TAXRATE = 0.07
foodtax = 0.0

ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]


def calc(o):
    global TAXRATE

    n = o[0]
    t = o[1]
    items = o[2]

    sub = 0.0
    tax = 0.0

    print("Receipt for " + n + " (" + t + ")")
    print("-" * 40)

    for it in items:
        pi = it[0]
        q = it[1]

        p = PRODUCTS[pi][1]
        nm = PRODUCTS[pi][0]
        cat = PRODUCTS[pi][2]

        line = p * q
        sub = sub + line

        if cat == "food":
            tax = tax + line * foodtax
        else:
            tax = tax + line * TAXRATE

        print(nm + " x" + str(q) + " = " + str(line))

    d = 0.0

    if t == "none":
        d = 0.0
    elif t == "silver":
        if sub > 100:
            d = sub * 0.05
        else:
            d = sub * 0.02
    elif t == "gold":
        if sub > 100:
            d = sub * 0.10
        else:
            d = sub * 0.05
    elif t == "platinum":
        if sub > 100:
            d = sub * 0.15
        else:
            d = sub * 0.10

    totalqty = 0

    for it in items:
        totalqty = totalqty + it[1]

    if totalqty >= 10:
        d = d + sub * 0.03

    total = sub - d + tax

    pts = 0

    if t == "none":
        pts = int(total // 10)
    elif t == "silver":
        pts = int(total // 10) * 2
    elif t == "gold":
        pts = int(total // 10) * 3
    elif t == "platinum":
        pts = int(total // 10) * 5

    print("-" * 40)
    print("Subtotal: " + str(round(sub, 2)))
    print("Discount: " + str(round(d, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(pts))
    print("")

    return total


def legacy_main():
    grand = 0.0

    for o in ORDERS:
        grand = grand + calc(o)

    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


# ==============================================================================
# BEHAVIOUR LOCK — DO NOT EDIT
# ==============================================================================

def capture(fn):
    """Run fn() and return everything it printed, as a string."""
    buf = io.StringIO()

    with contextlib.redirect_stdout(buf):
        fn()

    return buf.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)


# ==============================================================================
# YOUR REFACTORED SOLUTION
# ==============================================================================

# ------------------------------------------------------------------------------
# Named constants
# ------------------------------------------------------------------------------

TAX_RATE = 0.07
FOOD_TAX_RATE = 0.0

FOOD_CATEGORY = "food"

DISCOUNT_THRESHOLD = 100

BULK_QTY_THRESHOLD = 10
BULK_DISCOUNT_RATE = 0.03

POINTS_DIVISOR = 10


# ------------------------------------------------------------------------------
# Product
# ------------------------------------------------------------------------------

class Product:
    """Represents a product sold by the store."""

    def __init__(self, name, price, category):
        if not name:
            raise ValueError("Product name cannot be empty.")

        if price < 0:
            raise ValueError("Product price cannot be negative.")

        if not category:
            raise ValueError("Product category cannot be empty.")

        self.name = name
        self.price = price
        self.category = category

    def tax_rate(self):
        """Return the tax rate for this product."""
        if self.category == FOOD_CATEGORY:
            return FOOD_TAX_RATE

        return TAX_RATE

    def tax_for(self, amount):
        """Calculate tax for a given amount of this product."""
        return amount * self.tax_rate()


# ------------------------------------------------------------------------------
# OrderItem
# ------------------------------------------------------------------------------

class OrderItem:
    """Represents one product and its quantity in an order."""

    def __init__(self, product, quantity):
        if not isinstance(product, Product):
            raise TypeError("product must be a Product.")

        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")

        self.product = product
        self.quantity = quantity

    def line_total(self):
        """Return the total price for this order item."""
        return self.product.price * self.quantity

    def tax(self):
        """Return the tax for this order item."""
        return self.product.tax_for(self.line_total())


# ------------------------------------------------------------------------------
# Customer hierarchy
# ------------------------------------------------------------------------------

class Customer:
    """Base customer membership tier."""

    def discount_rate(self, subtotal):
        """Return the membership discount rate."""
        return 0.0

    def points_multiplier(self):
        """Return the points multiplier."""
        return 1

    def __str__(self):
        return "none"


class SilverCustomer(Customer):
    """Silver membership customer."""

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_THRESHOLD:
            return 0.05

        return 0.02

    def points_multiplier(self):
        return 2

    def __str__(self):
        return "silver"


class GoldCustomer(Customer):
    """Gold membership customer."""

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_THRESHOLD:
            return 0.10

        return 0.05

    def points_multiplier(self):
        return 3

    def __str__(self):
        return "gold"


class PlatinumCustomer(Customer):
    """Platinum membership customer."""

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_THRESHOLD:
            return 0.15

        return 0.10

    def points_multiplier(self):
        return 5

    def __str__(self):
        return "platinum"


# ------------------------------------------------------------------------------
# Order
# ------------------------------------------------------------------------------

class Order:
    """An order has one customer and many order items."""

    def __init__(self, customer_name, customer, items):
        if not customer_name:
            raise ValueError("Customer name cannot be empty.")

        if not isinstance(customer, Customer):
            raise TypeError("customer must be a Customer.")

        if not items:
            raise ValueError("Order must contain at least one item.")

        self.customer_name = customer_name
        self.customer = customer
        self.items = list(items)

    def subtotal(self):
        """Return the order subtotal."""
        return sum(item.line_total() for item in self.items)

    def tax(self):
        """Return the total tax for the order."""
        return sum(item.tax() for item in self.items)

    def total_quantity(self):
        """Return the total quantity of products."""
        return sum(item.quantity for item in self.items)

    def membership_discount(self):
        """Return the membership discount."""
        subtotal = self.subtotal()

        return subtotal * self.customer.discount_rate(subtotal)

    def bulk_discount(self):
        """Return the bulk discount."""
        if self.total_quantity() >= BULK_QTY_THRESHOLD:
            return self.subtotal() * BULK_DISCOUNT_RATE

        return 0.0

    def discount(self):
        """Return the total discount."""
        return self.membership_discount() + self.bulk_discount()

    def total(self):
        """Return the final order total."""
        return self.subtotal() - self.discount() + self.tax()

    def points(self):
        """Return the loyalty points earned."""
        return (
            int(self.total() // POINTS_DIVISOR)
            * self.customer.points_multiplier()
        )

    def receipt(self):
        """
        Build the receipt text.

        This method only prepares the output.
        It does not print anything.
        """

        lines = []

        lines.append(
            "Receipt for "
            + self.customer_name
            + " ("
            + str(self.customer)
            + ")"
        )

        lines.append("-" * 40)

        for item in self.items:
            lines.append(
                item.product.name
                + " x"
                + str(item.quantity)
                + " = "
                + str(item.line_total())
            )

        lines.append("-" * 40)

        lines.append(
            "Subtotal: "
            + str(round(self.subtotal(), 2))
        )

        lines.append(
            "Discount: "
            + str(round(self.discount(), 2))
        )

        lines.append(
            "Tax: "
            + str(round(self.tax(), 2))
        )

        lines.append(
            "Total: "
            + str(round(self.total(), 2))
        )


        lines.append(
            "Points earned: "
            + str(self.points())
        )

        lines.append("")
        lines.append("")

        return "\n".join(lines)



# ------------------------------------------------------------------------------
# Factory for membership tiers
# ------------------------------------------------------------------------------

def create_customer(tier):
    """Create the appropriate customer subclass."""

    customer_types = {
        "none": Customer,
        "silver": SilverCustomer,
        "gold": GoldCustomer,
        "platinum": PlatinumCustomer,
    }

    try:
        customer_type = customer_types[tier]
    except KeyError:
        raise ValueError("Unknown customer tier.")

    return customer_type()


# ------------------------------------------------------------------------------
# Convert legacy product data into Product objects
# ------------------------------------------------------------------------------

def create_products(product_data):
    """Convert product tuples into Product objects."""

    return [
        Product(name, price, category)
        for name, price, category in product_data
    ]


# ------------------------------------------------------------------------------
# Convert legacy order data into Order objects
# ------------------------------------------------------------------------------

def create_orders(order_data, products):
    """Convert order tuples into Order objects."""

    orders = []

    for customer_name, tier, raw_items in order_data:
        customer = create_customer(tier)

        items = [
            OrderItem(
                products[product_index],
                quantity
            )
            for product_index, quantity in raw_items
        ]

        orders.append(
            Order(
                customer_name,
                customer,
                items
            )
        )

    return orders


# ------------------------------------------------------------------------------
# Refactored main
# ------------------------------------------------------------------------------

def refactored_main():
    """Print every receipt and the grand total."""

    products = create_products(PRODUCTS)

    orders = create_orders(
        ORDERS,
        products
    )

    grand = 0.0

    for order in orders:
        print(order.receipt(), end="")

        grand = grand + order.total()

    print(
        "GRAND TOTAL (all orders): "
        + str(round(grand, 2))
    )


# ==============================================================================
# SELF-TEST — DO NOT EDIT
# ==============================================================================

def _check():
    try:
        your_output = capture(refactored_main)

    except NotImplementedError:
        print("Solution not implemented yet.\n")
        print(
            "Below is the TARGET output your refactor "
            "must reproduce exactly:\n"
        )
        print(GOLDEN_OUTPUT)
        return

    if your_output == GOLDEN_OUTPUT:
        print(
            "PASS - behaviour is unchanged. "
            "Your refactor is safe.\n"
        )

    else:
        print(
            "FAIL - the output changed, so this is not "
            "yet a valid refactor.\n"
        )

        g = GOLDEN_OUTPUT.splitlines()
        y = your_output.splitlines()

        for i in range(max(len(g), len(y))):
            gl = g[i] if i < len(g) else "<no line>"
            yl = y[i] if i < len(y) else "<no line>"

            if gl != yl:
                print(
                    "First difference at line "
                    + str(i + 1)
                    + ":"
                )

                print(
                    "  expected: "
                    + repr(gl)
                )

                print(
                    "  yours:    "
                    + repr(yl)
                )

                break


if __name__ == "__main__":
    _check()


# ==============================================================================
# RUBRIC
# ==============================================================================
#
# Behaviour preserved (self-test PASS) .................. 2
# Domain modelling & composition ....................... 2
# Polymorphism (tier discount & points, no if/elif) .... 1.5
# Pure calculation vs I/O separation ................... 1.5
# Encapsulation & validation ........................... 1
# Clean code (names, no magic numbers, DRY, no global).. 1
# CHANGES.md explanation (per-change, before->after) ... 0.5
# CHANGES.md prompt log (Level-2) ...................... 0.5
#
# ==============================================================================
