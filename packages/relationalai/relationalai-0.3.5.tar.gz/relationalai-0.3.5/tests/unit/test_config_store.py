
import pytest

from pathlib import Path
from relationalai.clients.config import ConfigStore, items_with_dots

@pytest.fixture
def basic_config_store():
    return ConfigStore(toml_string=get_config_test_file("raiconfig_example.toml"))

def get_config_test_file(name: str):
    with open(Path(__file__).parent / f"test_configs/{name}", "r") as f:
        return f.read()

def test_config(basic_config_store):
    config = basic_config_store.get_config()
    assert str(config) == get_config_test_file("printed_config.txt")

def test_new_profile(basic_config_store):
    config = basic_config_store.get_config()
    config.set("compiler.dry_run", True)
    config.profile = "foo"
    computed = basic_config_store.with_new_profile(config).as_string()
    actual = get_config_test_file("config_with_new_profile.toml")
    assert computed == actual

def test_items_with_dots():
    D = {
        "a": {
            "b": {
                "c": 1
            }
        },
        "d": 2
    }
    assert tuple(items_with_dots(D)) == (("a.b.c", 1), ("d", 2))

