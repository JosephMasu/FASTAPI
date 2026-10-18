
def add(num2: int, num1: int):
    return num1 + num2
def subtract(num1: int, num2: int):
    return num1 - num2

def multiply(num2: int, num1: int):
    return num1 * num2

def divide(num1: int, num2: int):
    if num2 == 0:
        raise ValueError("Cannot divide by zero")
    return num1 / num2
def power(num1: int, num2: int):
    return num1 ** num2

def BankAccount(balance: float):
    def deposit(amount: float):
        nonlocal balance
        balance += amount
        return balance

    def withdraw(amount: float):
        nonlocal balance
        if amount > balance:
            raise ValueError("Insufficient funds")
        balance -= amount
        return balance

    def get_balance():
        return balance

    return {
        "deposit": deposit,
        "withdraw": withdraw,
        "get_balance": get_balance
    }