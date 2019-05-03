def generate(count, init=0):
    x = init
    while count > 0:
        count -= 1
        x = (17 * x**2 - 2*x + 23) % 65536
        yield x
