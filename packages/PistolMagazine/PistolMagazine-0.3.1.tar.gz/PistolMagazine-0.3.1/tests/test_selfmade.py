from pprint import pprint
from random import choice
from pistol_magazine import DataMocker, provider, Str, Int, Timestamp, Bool
from pistol_magazine.self_made import ProviderField


def test_model_data_conversion():
    """
    Use it when your mock requirements are not that precise.
    In this case, you cannot use `kwargs` to pass custom arguments such as instances of the `Timestamp` class.
    Only the default rules for keyword arguments can be used.
    If you want to use `kwargs`, refer to the test functions in files like `test_dict` and `test_list` for guidance.
    :return:
    """
    data = {
        "a": {
            "1": "2022-01-01T00:00:00",
            "2": "20.22",
            "3": 20.22,
            "4": 100,
        },
        "b": 1680441525,
        "c": 1680441525000,
        "d": "i am strong",
        "e": ["1680441525000000", "2022-01-01T00:00:001",
              {
                  "f": 1000,
                  "g": "10000"
              }]
    }
    models = {
        'a': {'1': 'Datetime_%Y-%m-%dT%H:%M:%S', '2': 'StrFloat', '3': 'Float', '4': 'Int'},
        'b': 'Timestamp_0', 'c': 'Timestamp_3', 'd': 'Str',
        'e': ['StrTimestamp_3', 'Str', {'f': 'Int', "g": "StrInt"}]
    }
    data_mocker1 = DataMocker.data_to_model(data)
    data_mocker2 = DataMocker.model_to_data(models)
    # Input raw data ---------> Data format
    pprint(data_mocker1.get_datatype())
    # Input raw data ---------> New mock data in the same format
    pprint(data_mocker1.mock())
    # Input model data ---------> Mock data in the given format
    pprint(data_mocker2.mock())


@provider
class MyProvider:
    def symbol(self):
        return choice(["BTC", "ETH"])


def test_provider():
    print(DataMocker().symbols())  # e.g. "BTC"


def test_data_mocker():
    """
    :return: e.g.
    {
        "create_time": 1717747583,
        "user_name": "Christine Woods",
        "user_email": "hlyons@example.com",
        "user_age": 44,
        "user_symbol": "ETH"
    }
    """
    class UserInfoMocker(DataMocker):
        create_time: Timestamp = Timestamp(Timestamp.D_TIMEE10, days=2)
        user_name: Str = Str(data_type="name")
        user_email: Str = Str(data_type="email")
        user_age: Int = Int(byte_nums=6, unsigned=True)
        user_symbol: ProviderField = ProviderField(MyProvider().symbol)
        user_marriage: Bool = Bool()

    data = UserInfoMocker().mock(to_json=True)
    print(data)
