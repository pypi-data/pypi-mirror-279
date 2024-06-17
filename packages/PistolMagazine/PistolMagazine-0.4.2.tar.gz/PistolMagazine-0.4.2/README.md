# PistolMagazine 🎯
[![PyPI - Version](https://img.shields.io/pypi/v/PistolMagazine)](https://pypi.org/project/PistolMagazine/)


PistolMagazine is a data mocking tool designed to help you generate realistic data for testing and development purposes.

## Features ✨

- **Flexible Data Types** 📊: Supports various data types including integers, floats, strings, timestamps, and more.
- **Custom Providers** 🛠️: Easily create and integrate custom data providers.
- **Random Data Generation** 🎲: Generates realistic random data for testing.
- **Hook Functions** 🪝: Support for hook functions, allowing users to execute custom operations before or after generating mock data. These hooks can be utilized for:
  - **Logging**: Record relevant operations or data before or after data generation.
  - **Starting External Services**: Initiate external services or resources before generating data.
  - **Dynamic Data Modification**: Perform data validation or sanitization before generating mock data.
  - **Sending Data to Message Queues**: Transmit generated data to message queues for integration with other systems.
  - **Data Profiling**: Perform statistical analysis or monitoring post data generation.

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
from pistol_magazine.hooks.hooks import hook

# Create a custom provider
@provider
class MyProvider:
    def user_status(self):
        return choice(["ACTIVE", "INACTIVE"])
    
    
"""
Define hook functions
before_generate: Executes operations before generating all data. Suitable for tasks like logging or starting external services.
after_generate: Executes operations after generating each data entry but before final processing. Suitable for tasks like data validation or conditional modifications.
final_generate: Executes operations after generating and processing all data entries. Suitable for final data processing, sending data to message queues, or performing statistical analysis.
"""
@hook('pre_generate', order=1)
def pre_generate_first_hook(data):
    print("Start Mocking User Data")

@hook('pre_generate', order=2)
def pre_generate_second_hook(data):
    """
    Perform some preprocessing operations, such as starting external services.
    """

@hook('after_generate', order=1)
def after_generate_first_hook(data):
    data['user_status'] = 'ACTIVE' if data['user_age'] >= 18 else 'INACTIVE'
    return data

@hook('final_generate', order=1)
def final_generate_second_hook(data):
    """
    Suppose there is a function send_to_message_queue(data) to send data to the message queue
    """

# Use the custom provider
class UserInfoMocker(DataMocker):
    create_time: Timestamp = Timestamp(Timestamp.D_TIMEE10, days=2)
    user_name: Str = Str(data_type="name")
    user_email: Str = Str(data_type="email")
    user_age: Int = Int(byte_nums=6, unsigned=True)
    user_status: ProviderField = ProviderField(MyProvider().user_status)
    user_marriage: Bool = Bool()
    user_dict: Dict = Dict(
        {
            "a": Float(left=2, right=4, unsigned=True),
            "b": Timestamp(Timestamp.D_TIMEE10, days=2)
        }
    )
    user_list: List = List(
        [
            Datetime(Datetime.D_FORMAT_YMD_T, weeks=2),
            StrInt(byte_nums=6, unsigned=True)
        ]
    )

data = UserInfoMocker().mock(num_entries=2, to_json=True)
"""
e.g.
{"e09e74c4-b556-45ed-8c96-ec3f699c0efc": {"create_time": 1718452464, "user_name": "Melissa Bautista", "user_email": "hortonrachel@example.net", "user_age": 61, "user_status": "ACTIVE", "user_marriage": false, "user_dict": {"a": -19.7677, "b": 1718721164}, "user_list": ["2024-06-03T21:58:51", "21"]}, "22a1b460-c890-4f69-9c31-eabc494fce1b": {"create_time": 1718440430, "user_name": "Sherry Rodriguez", "user_email": "kristinramirez@example.org", "user_age": 46, "user_status": "ACTIVE", "user_marriage": false, "user_dict": {"a": 56.4705, "b": 1718609356}, "user_list": ["2024-06-22T14:17:46", "54"]}}
"""
print(data)

```

If you want more detailed instructions, you can refer to the examples and documentation in the [tests' directory](tests).


## Help PistolMagazine

If you find PistolMagazine useful, please ⭐️ Star it at GitHub

[Feature discussions](https://github.com/miyuki-shirogane/PistolMagazine/discussions) and [bug reports](https://github.com/miyuki-shirogane/PistolMagazine/issues) are also welcome!

**Happy Mocking!** 🎉🎉🎉