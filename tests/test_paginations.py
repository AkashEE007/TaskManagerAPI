import pytest
from fastapi import HTTPException

from src.utils.helpers import pagination_params


def test_pagination_params_returns_requested_values():
    assert pagination_params(skip=10, limit=25) == {"skip": 10, "limit": 25}


def test_pagination_params_uses_defaults():
    assert pagination_params() == {"skip": 0, "limit": 20}


@pytest.mark.parametrize(
    ("skip", "limit"),
    [(-1, 20), (0,0), (0,-1), (-1, -200)],
)
def test_invalid_page_params(skip, limit):
    with pytest.raises(HTTPException) as error:
        pagination_params(skip=skip, limit=limit)

    assert error.value.status_code == 400

