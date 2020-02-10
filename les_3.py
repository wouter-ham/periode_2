def gcd(a: int, b: int):
    if a == b:
        return a
    elif a > b:
        return gcd(b, a)
    while b > 0:
        k = b % a
        a = b
        b = k

    return a


print(gcd(150, 45))
