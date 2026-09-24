# Assignment 03 — CHANGES

**Name:** HEIN_LWIN_OO **Student ID:** 6705140006

This is the written part of your submission. Explain **what you changed and why**, then record your **prompt log**. Keep before/after snippets to a line or two.

---

## 1 · What I changed

#	Code smell in the original	What I changed it to	OOP concept applied	How I verified behaviour was unchanged
1	Products were stored as bare tuples such as ("Laptop", 1200.0, "electronics").	Created a Product class with name, price, and category attributes.	Classes / Encapsulation	Ran python Assignment_03.py and checked that the self-test printed PASS.
2	Order items were stored as (product_index, quantity) tuples.	Created an OrderItem class containing a Product object and a quantity.	Composition	Ran the self-test and checked that all receipt lines remained identical.
3	The calc() function contained repeated if/elif checks for each membership tier.	Created Customer, SilverCustomer, GoldCustomer, and PlatinumCustomer classes with their own discount and points methods.	Inheritance / Polymorphism	Checked that the self-test printed PASS and reviewed each tier's discount and points rules.
4	The original calc() function calculated values and printed the receipt at the same time.	Moved calculations into methods such as subtotal(), discount(), tax(), total(), and points(), while receipt() handles the receipt text.	Separation of calculation and I/O	Compared the refactored output with the behaviour lock until the self-test printed PASS.
5	Magic numbers and a mutable global TAXRATE were used in the calculation.	Created named constants such as TAX_RATE, BULK_QTY_THRESHOLD, BULK_DISCOUNT_RATE, and POINTS_DIVISOR, and removed the global mutation.	Clean code / Encapsulation	Ran the complete program and verified that the final output matched the legacy output exactly.
6	Tax calculation checked the product category inside the order calculation.	Made Product responsible for determining its own tax rate through tax_rate() and tax_for().	Composition / Encapsulation	Ran the self-test and checked that food remained tax-free while other products used the 7% rate.
7	Raw data had no validation when creating objects.	Added constructor validation for product values, quantities, customer names, customers, and orders.	Encapsulation / Validation	Reviewed the constructors and confirmed that valid legacy data still produced the same output.

## 2 · Short reflection (4–6 sentences)

Which change improved the code the most, and why? Where did keeping the behaviour identical force you to be careful?

> _The change that improved the code the most was replacing the membership-tier if/elif chains with a family of customer classes. Each tier now contains its own discount and points behaviour, which makes the Order class easier to understand. Separating calculations from receipt printing also made the program cleaner because the calculation methods return values instead of producing output. Keeping the behaviour identical required me to be careful about the exact receipt formatting, including the blank line between receipts. I used the supplied self-test to compare the refactored output with the original output. When the test initially failed, I used the reported first difference to find and fix the missing blank line._

---

## 3 · Prompt log (Level 2 — required)

Record **every** prompt where AI helped. If you wrote a part yourself, say so in one row. AI-shaped code with an empty log does **not** meet the Level-2 policy.

#	My prompt to the AI	What it suggested (summary)	Accept / reject / edited	How I checked it
1	I provided the assignment and asked for help refactoring the messy store system into an object-oriented design.	Suggested Product, OrderItem, Customer, and Order classes, named constants, validation, and separate calculation methods.	Edited and integrated the suggested design into my assignment.	Read the code and ran the self-test.
2	I reported the error PRODUCTS not defined ORDERS not defined after copying the refactored code.	Explained that the original PRODUCTS and ORDERS definitions needed to remain in the legacy section.	Accepted and kept the original legacy data.	Ran the complete file again.
3	I asked for the complete Assignment_03.py code.	Provided a complete version containing the original legacy section, behaviour lock, refactored classes, and self-test.	Edited the code as needed and tested it.	Ran python Assignment_03.py.
4	I reported the output difference at line 12 where a blank line was missing before Bob's receipt.	Identified that the legacy program printed an additional blank line after each receipt.	Accepted the explanation and edited receipt() to preserve the exact output.	Ran the self-test again and checked for PASS.

**Ownership statement.** *By submitting, I confirm I understand and can explain every line of code I submitted, and that this prompt log reflects my actual AI use.*

---

## 4 · Before-you-submit checklist

- [ ] `python Assignment_03.py` prints **PASS**.
- [ ] No tuples / parallel lists left — products, orders, and items are objects.
- [ ] No `if tier == ...` chains — tiers are a class family.
- [ ] Calculation methods **return** values and do not `print`; printing is separate.
- [ ] Constructors validate state; no leftover `global`; magic numbers are named.
- [ ] The change table and reflection above are filled in.
- [ ] The prompt log is complete and the ownership statement is signed.
