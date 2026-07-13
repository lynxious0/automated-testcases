# SauceDemo Automated Test Suite (Selenium + Python)

Automated test suite covering the SauceDemo web app (https://www.saucedemo.com/)
using Selenium WebDriver and Python's built-in `unittest` framework, structured
with the Page Object Model (POM).

## Project structure

```
saucedemo_tests/
├── pages/                          # Page Object classes (one per page)
│   ├── base_page.py                # Shared wait/find/click helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   ├── checkout_step_one_page.py
│   ├── checkout_step_two_page.py
│   └── checkout_complete_page.py
├── tests/                          # Test cases (one file per feature area)
│   ├── config.py                   # Shared test users/passwords
│   ├── test_login.py               # 12 test cases
│   ├── test_inventory.py           # 13 test cases
│   ├── test_product_detail.py      # 4 test cases
│   ├── test_cart.py                # 5 test cases
│   └── test_checkout.py            # 11 test cases (step 1, step 2, complete)
├── run_all_tests.py                # Runs entire suite with a summary report
├── requirements.txt
└── README.md
```

Total: **45 automated test cases** covering login, inventory/sorting, product
detail, cart, and the full 3-step checkout flow.

## Setup

1. Install Python 3.8+ and make sure Chrome is installed.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   Selenium 4+ auto-manages the ChromeDriver binary — no manual driver setup needed.

## Running the tests

**Run everything at once (recommended):**
```
python run_all_tests.py
```

**Run a single test file:**
```
python -m unittest tests.test_login
```

**Run a single test case:**
```
python -m unittest tests.test_login.LoginTests.test_valid_login_standard_user
```

## What's covered

| Area | File | Cases |
|---|---|---|
| Login | `test_login.py` | Valid login for all 5 working users, locked-out user, wrong password, unregistered user, empty username/password/both, error dismissal |
| Inventory | `test_inventory.py` | Page load (6 items), sort A-Z/Z-A/price low-high/high-low, add/remove single & multiple items, cart badge count, item detail navigation, reset app state, about link, logout |
| Product detail | `test_product_detail.py` | Correct item loads, add/remove from detail page, back button |
| Cart | `test_cart.py` | Items listed correctly, empty cart, remove item, continue shopping, checkout navigation |
| Checkout | `test_checkout.py` | Step 1 valid submit + missing first name/last name/postal code errors + cancel; Step 2 item count, subtotal+tax=total, cancel, finish; Complete page confirmation message + back home |

## Notes

- Tests use `standard_user` / `secret_sauce` by default (see `tests/config.py` for all 6 test accounts SauceDemo provides).
- `problem_user` and `visual_user` intentionally have UI bugs — if you want to test *for* those bugs specifically, write assertions that expect the broken behavior (e.g., mismatched images) rather than reusing the standard test cases as-is.
- All waits use explicit `WebDriverWait` (no hardcoded `time.sleep()`), so tests should be stable across normal network conditions.
- Each test class runs against a fresh browser session (`setUp`/`tearDown`) for isolation.
