# PistolMagazine 🎯
[![PyPI - Version](https://img.shields.io/pypi/v/PistolMagazine)](https://pypi.org/project/PistolMagazine/)


PistolMagazine is a data mocking tool designed to help you generate realistic data for testing and development purposes.

## Features ✨

- **Flexible Data Types** 📊: Supports various data types including integers, floats, strings, timestamps, and more.
- **Custom Providers** 🛠️: Easily create and integrate custom data providers.
- **Random Data Generation** 🎲: Generates realistic random data for testing.

## Installation 📦

Install PistolMagazine using pip:

```bash
pip install pistolmagazine
```

## Quick Start 🚀

Here’s a quick example to get you started:

```python
from pistol_magazine import *
from random import choice

# Define your data structure
expect_format = {
        "a": Float(left=2, right=4, unsigned=True),
        "b": Timestamp(Timestamp.D_TIMEE10, days=2),
        "C": List(
            [
                Datetime(Datetime.D_FORMAT_YMD_T, weeks=2),
                StrInt(byte_nums=6, unsigned=True)
            ]
        )
    }
# Generate mock data, e.g. {'a': -54.9438, 'b': 1717673498, 'C': ['2024-06-15T04:50:46', '5']}
print(Dict(expect_format).mock())


# Create a custom provider
@provider
class MyProvider:
    def symbol(self):
        return choice(["BTC", "ETH"])

# Use the custom provider, e.g. "ETH"
class UserInfoMocker(DataMocker):
    create_time: Timestamp = Timestamp(Timestamp.D_TIMEE10, days=2)
    user_name: Str = Str(data_type="name")
    user_email: Str = Str(data_type="email")
    user_age: Int = Int(byte_nums=6, unsigned=True)
    user_symbol: ProviderField = ProviderField(MyProvider().symbol)

data = UserInfoMocker().mock(to_json=True)
"""
e.g.
{
    "create_time": 1717747583,
    "user_name": "Christine Woods",
    "user_email": "hlyons@example.com",
    "user_age": 44,
    "user_symbol": "ETH"
}
"""
print(data)

```

If you want more detailed instructions, you can refer to the examples and documentation in the [tests' directory](tests).


## Help PistolMagazine

If you find PistolMagazine useful, please ⭐️ Star it at GitHub

[Feature discussions](https://github.com/miyuki-shirogane/PistolMagazine/discussions) and [bug reports](https://github.com/miyuki-shirogane/PistolMagazine/issues) are also welcome!

**Happy Mocking!** 🎉🎉🎉