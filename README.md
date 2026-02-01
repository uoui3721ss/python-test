# python-test
python test for ai agent

## UAE Telephone Number Ordering

This repository includes a function for ordering UAE telephone numbers according to local people's preferences.

### Features

The `uae_phone_ordering.py` module provides functionality to sort UAE phone numbers based on:

- **Premium carrier prefixes**: Mobile numbers with prefixes like 50, 55, 56 are preferred
- **Repeating digits**: Numbers with repeating digits (e.g., 777-7777) are highly valued
- **Sequential patterns**: Numbers with sequential digits (e.g., 123-4567) get bonus points
- **Lucky numbers**: Numbers containing 7 and 8 are considered lucky
- **Round numbers**: Numbers ending in 00, 000, etc. are preferred
- **Avoiding unlucky numbers**: Numbers with many 4s are slightly penalized

### Usage

```python
from uae_phone_ordering import order_uae_phones

# Example: Order a list of UAE phone numbers
phones = [
    '+971 50 123 4567',
    '+971 55 777 7777',
    '+971 52 234 5678',
    '+971 56 888 8888',
    # ... more numbers
]

ordered_phones = order_uae_phones(phones)
```

### Running the Example

To see an example of ordering 50 UAE telephone numbers:

```bash
python uae_phone_ordering.py
```

### Running Tests

To run the test suite:

```bash
python -m unittest test_uae_phone_ordering -v
```
