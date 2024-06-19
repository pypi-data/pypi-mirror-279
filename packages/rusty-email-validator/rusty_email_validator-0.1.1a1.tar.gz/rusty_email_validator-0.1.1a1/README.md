# Rusty Email Validator

This project provides a simple email validation library written in Rust, with Python bindings using PyO3. The library uses the [`validator`](https://github.com/Keats/validator) crate to validate email addresses.

## Features

- Validate email addresses using Python.

## Requirements

- Python 3.6 or higher

## Installation

You can install the package directly from PyPI:

```sh
pip install rusty-email-validator
```

## Usage

Here's an example of how to use the email validation function in Python:

```python
from rusty_email_validator import validate

email = "example@example.com"
is_valid = validate(email)
print(f"Is valid: {is_valid}")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PyO3](https://github.com/PyO3/pyo3) for providing the Rust bindings for Python.
- [Validator](https://github.com/Keats/validator) for the email validation functionality.