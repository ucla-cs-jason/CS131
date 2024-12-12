def squares_dict(lo, up):
    return {num: num * num for num in range(lo, up + 1)}

assert squares_dict(1, 5) == {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}