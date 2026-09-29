import pytest
from fastapi import HTTPException

from src.utils.helpers import check_password_strength


@pytest.mark.parametrize(
    "password",
    ["Password@123", "pASSword!123", "Admin^123", "PASSWORd&*1", "passworD@@@3"]
)
def test_valid_password(password):
    pwd = check_password_strength(password)
    assert pwd == password


@pytest.mark.parametrize(
    "password",
    ["password@123", "admin#123"]
)
def test_invalid_pasword_without_uppercase(password):
    with pytest.raises(HTTPException) as error:
        check_password_strength(password)

    assert error.value.status_code == 400
    assert error.value.detail == "Password must contain an uppercase character"


@pytest.mark.parametrize(
    "password",
    ["PASSWORD@123", "ADMIN@#4"]
)
def test_invalid_password_without_lowercase(password):
    with pytest.raises(HTTPException) as error:
        check_password_strength(password)

    assert error.value.status_code == 400
    assert error.value.detail == "Password must contain a lowercase character"


@pytest.mark.parametrize(
    "password",
    ["Password123", "Admin123", "AdmiN23"]
)
def test_invalid_password_without_specialcase(password):
    with pytest.raises(HTTPException) as error:
        check_password_strength(password)

    assert error.value.status_code == 400
    assert error.value.detail == "Password must contain a special character"


@pytest.mark.parametrize(
    "password",
    ["Password@", "Admin&*()"]
)
def test_invalid_password_without_integers(password):
    with pytest.raises(HTTPException) as error:
            check_password_strength(password)
    
    assert error.value.status_code == 400
    assert error.value.detail == "Password must contain an Integer"

