import pytest
from ..download_spreadsheet_file import get_secret, extract_secret_value

@pytest.fixture
def secret_value():
    return '{"key": "value"}'

def test_get_secret(secret_value):
    result = get_secret('secret_name')
    assert result == secret_value

def test_extract_secret_value(secret_value):
    result = extract_secret_value(secret_value, 'key')
    assert result == 'value'