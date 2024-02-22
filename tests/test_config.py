import pytest

from finex_etf_calc.app.config import config_class, CONFIG_FILE
from finex_etf_calc.app.utils import yaml_loader


@pytest.mark.parametrize("input_value,expected", [
    (True, True),
    ("true", True),
    ("false", False),
    (False, False),
])
def test_to_bool(input_value, expected):
    assert config_class._to_bool(input_value) == expected


def test_merge_dicts():
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    expected = {"a": 1, "b": 3, "c": 4}
    assert config_class._merge_dicts(dict1, dict2) == expected


def test_get_value():
    attrs_info = {"test_attr": "default"}
    params = {"test_attr": "override"}
    assert config_class._get_value("test_attr", str, attrs_info, params) == "override"


def test_from_file():
    with open(CONFIG_FILE) as f:
        raw_data = yaml_loader.load(f)

    config = config_class.from_file(CONFIG_FILE)
    for k, v in raw_data.items():
        assert getattr(config, k) == v
