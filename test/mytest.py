
import pytest

from app.calculations import add, subtract, multiply, divide, power

@pytest.mark.parametrize('num1, num2, expected', [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (-5, -5, -10),
    (10, 20, 30)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0
    assert subtract(-5, -10) == 5
    assert subtract(10, 20) == -10


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(0, 10) == 0
    assert multiply(-5, -5) == 25
    assert multiply(10, 20) == 200


def test_divide():
    assert divide(6, 3) == 2
    assert divide(-10, 2) == -5
    assert divide(0, 1) == 0
    assert divide(-9, -3) == 3
    assert divide(5, 2) == 2.5


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)


def test_power():
    assert power(2, 3) == 8
    assert power(3, 2) == 9
    assert power(-1, 1) == -1
    assert power(0, 10) == 0
    assert power(-5, -5) == -0.00032
    assert power(10, 20) == 100000000000000000000

class BankAccount:
    def __init__(self, balance=0.0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance


def test_bank_account():
    account = BankAccount(100.0)

    # Test deposit
    assert account.deposit(50.0) == 150.0
    assert account.get_balance() == 150.0

    # Test withdraw
    assert account.withdraw(30.0) == 120.0
    assert account.get_balance() == 120.0

    # Test insufficient funds
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(200.0)

    # Test final balance
    assert account.get_balance() == 120.0