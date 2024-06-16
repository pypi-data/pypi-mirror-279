def addition(x: float, y: float) -> float:
    z = x + y
    return z


def subtraction(x: float, y: float) -> float:
    z = x - y
    return z


def multiplication(x: float, y: float) -> float:
    z = x * y
    return z


def division(x: float, y: float) -> float:
    if y == 0:
        raise ValueError("Cannot divide by 0")
    else:
        z = x / y
        return z
