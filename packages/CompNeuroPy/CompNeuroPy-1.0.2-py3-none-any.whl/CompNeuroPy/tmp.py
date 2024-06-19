def func(x):
    return -1


x0 = 0
a = x0
b = x0 + 1
while func(b) < 0:
    print(f"[{a}, {b}]")
    a = b
    b *= 2
    if b > 1e6:  # Avoid infinite loop in case y_bound is not reachable
        break
