from typing import Union


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def is_prime(number: Union[int, float]) -> bool:
    if number <= 1:
        return False
    if number % 2 == 0:
        return False
    if number == 2:
        return True
    for i in range(3, int(number**0.5) + 1, 2):
        if number % i == 0:
            return False
    return True
