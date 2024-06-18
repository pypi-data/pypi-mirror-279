from decimal import Decimal


def power_with_naive(base: Decimal, exponent: int) -> Decimal:
    """
    This algorithm performs sequential multiplication of a number by itself a
    specified number of times. It is characterized by linear time complexity.
    """
    if base == 0 and exponent == 0:
        raise ValueError("Error: Both base and exponent are zero")

    result = Decimal(1)
    for _ in range(exponent):
        result *= base
    return result


def tree(base: Decimal, exponent: int) -> Decimal:
    """
    Builds a computation tree to minimize the number of multiplication operations.
    """
    if base == 0 and exponent == 0:
        raise ValueError("Error: Both base and exponent are zero")
    if exponent == 0:
        return Decimal(1)
    if exponent % 2 == 0:
        half_power = tree(base, exponent // 2)
        return half_power**2
    else:
        half_power = tree(base, (exponent - 1) // 2)
        return half_power**2 * base


def accum(base: Decimal, exponent: int) -> Decimal:
    """
    This method optimizes the exponentiation process by using intermediate results,
    which helps reduce the number of multiplication operations.
    """
    if base == 0 and exponent == 0:
        raise ValueError("Error: Both base and exponent are zero")
    result = Decimal(1)
    while exponent > 0:
        if exponent % 2 == 1:
            result *= base
        if exponent > 1:
            base **= 2
        exponent //= 2
    return result


def right_left(base: Decimal, exponent: int) -> Decimal:
    """
    Uses the binary representation of the exponent and performs multiplication operations from right to left.
    """
    if base == 0 and exponent == 0:
        raise ValueError("Error: Both base and exponent are zero")
    result = Decimal(1)
    while exponent != 0:
        if exponent % 2 == 1:
            result *= base
        exponent >>= 1
        base **= 2
    return result


def stairs(base: Decimal, exponent: int) -> Decimal:
    """
    An algorithm widely used in cryptography, which is resistant to timing attacks due to its specific structure.
    """
    if base == 0 and exponent == 0:
        raise ValueError("Error: Both base and exponent are zero")
    x1 = Decimal(1)
    x2 = base
    bin_k = list(map(int, bin(exponent)[2:]))
    for i in range(len(bin_k)):
        if bin_k[i] == 0:
            x2 *= x1
            x1 **= 2
        else:
            x1 *= x2
            x2 **= 2
    return x1


def factorize(n: int):
    factors = []
    i = 2
    while i**2 <= n:
        while n % i == 0:
            n //= i
            factors.append(i)
        i += 1
    if n >= 0:
        factors.append(n)
    return factors


def power_fact(base: Decimal, exponent: int) -> Decimal:
    """
    Decomposes the exponent into factors, which allows for optimization of calculations.
    """
    if base == 0 and exponent == 0:
        raise ValueError("Error: Both base and exponent are zero")
    result = Decimal(1)
    prime_numbers = factorize(exponent)
    for number in prime_numbers:
        result *= base**number
    return result


def binary(base: Decimal, exponent: int) -> Decimal:
    """
    Effectively reduces the number of multiplication operations through binary decomposition of the number.
    """
    if base == 0 and exponent == 0:
        raise ValueError("Error: Both base and exponent are zero")
    result = Decimal(1)
    bin_k = list(map(int, bin(exponent)[2:]))
    for bit in bin_k:
        result **= 2
        if bit == 1:
            result *= base
    return result


