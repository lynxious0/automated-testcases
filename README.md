# SauceDemo Automated Test Suite (Selenium + Python)

Automated test suite for https://www.saucedemo.com/ built with Selenium
WebDriver, Python's `unittest`, and the Page Object Model (POM).

Every test is mapped 1:1 to a test case ID from the source test case
docs (ULF = User Login Feature, GLB = Global login errors, PPF =
Product Feature, CCF = Cart & Checkout Feature) so coverage is
traceable back to those docs.

## Project structure

```
saucedemo-tests/
├── pages/                          # Page Object classes (one per page)
│   ├── base_page.py                # Shared wait/find/click helpers
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   ├── checkout_step_one_page.py
│   ├── checkout_step_two_page.py
│   └── checkout_complete_page.py
├── tests/
│   ├── config.py                   # Shared test users/passwords
│   ├── test_login.py               # ULF-001..020, GLB-001..003
│   ├── test_inventory.py           # PPF-001..006, PPF-014..017
│   ├── test_product_detail.py      # PPF-007..013
│   ├── test_cart.py                # CCF-001..010
│   └── test_checkout.py            # CCF-021..035
├── run_all_tests.py                # Runs entire suite with a summary report
├── requirements.txt
└── README.md
```

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
python -m unittest tests.test_login.LoginTests.test_ULF_006_login_button_success
```

## Test case coverage

| Doc ID range | File | Class | Notes |
|---|---|---|---|
| ULF-001..011, error-close | `test_login.py` | `LoginTests` | Field states, valid/invalid login, lockout, GLB-001..003 negative cases |
| ULF-012..020 | `test_login.py` | `LogoutTests` | Logout, direct-URL and back-button access after logout |
| PPF-001..006 | `test_inventory.py` | `ProductListTests` | Product list name/image/description/price/count |
| PPF-014..017 | `test_inventory.py` | `ProductFilterTests` | Sort A-Z/Z-A/price low-high/high-low |
| PPF-007..013 | `test_product_detail.py` | `ProductPageTests` | Detail page redirect, description, price, back button |
| CCF-001..010 | `test_cart.py` | `CartTests` | Cart icon, add/remove (list & detail page), cart contents |
| CCF-011..019 | `test_checkout.py` | `CheckoutStepOneTests` | Checkout info form + Continue/Back buttons |
| CCF-020..022 | `test_checkout.py` | `CheckoutConfirmationTests` | Order overview, pricing, Cancel/Finish |
| CCF-023..025 | `test_checkout.py` | `CheckoutCompleteTests` | Completion message + back-home button |

### Skipped test IDs (real site has no matching UI)

These IDs describe UI that doesn't exist on saucedemo.com. Rather than
faking a pass, they're implemented as `@unittest.skip(...)` with the
reason recorded, so they show up clearly in the test report instead of
silently disappearing:

| ID | Reason |
|---|---|
| ULF-014, ULF-015, ULF-016 | No logout confirmation dialog — clicking Logout logs out immediately |
| ULF-018 | No session-timeout/inactivity feature |
| PPF-005, PPF-011 | No star-rating element on the product list or product detail page |
| PPF-010 | Single currency (USD) only — nothing to localize |
| PPF-012 | No quantity stepper/selector on the product detail page |
| CCF-015 | Checkout form only has first name, last name, postal code — no payment field |

## Notes

- Tests use `standard_user` / `secret_sauce` by default (see `tests/config.py` for all test accounts).
- `problem_user`, `performance_glitch_user`, `error_user`, and `visual_user` intentionally have UI bugs baked into the site; the shared `LoginTests.test_ULF_006b_*` only checks that they can authenticate, not that their UI is bug-free.
- All waits use explicit `WebDriverWait` (15s, no `time.sleep()`) so tests stay stable across normal network conditions.
- Each test class runs against a fresh browser session (`setUp`/`tearDown`) for isolation.
- `type_text()` deliberately avoids `element.clear()`: on saucedemo's checkout form (React-controlled inputs), Selenium's native clear() can silently fail to update React's state, leaving the field looking empty even after "successful" typing. Select-all + Delete fires real keyboard events instead, which React picks up correctly.
- Login assertions wait for the `inventory.html` redirect rather than checking `current_url` immediately after the click — `performance_glitch_user` has a deliberate multi-second delay before redirecting and will otherwise lose that race.
- This suite drives the live saucedemo.com; occasional timeouts unrelated to the two bugs above are usually real network/site latency — a `Continue`/`Checkout` click timing out in isolation (with everything else passing) is worth a re-run before treating it as a regression.
