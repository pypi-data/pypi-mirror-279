import pytest
from getai.core.utils import convert_to_bytes, get_hf_token, hf_login


def test_convert_to_bytes():
    assert convert_to_bytes("1 KB") == 1024
    assert convert_to_bytes("1 MB") == 1024**2
    assert convert_to_bytes("1 GB") == 1024**3


def test_get_hf_token():
    token = get_hf_token()
    assert token is not None


def test_hf_login():
    hf_login()
    assert True
