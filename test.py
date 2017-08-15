import pytest


def test_raises():
    with pytest.raises(Exception) as excinfo:
        raise Exception('some info')
    assert excinfo.value.message == 'some info'