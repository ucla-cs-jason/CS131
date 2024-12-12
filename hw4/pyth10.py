def get_func(x):
    return lambda y: y + x

func = get_func(3)
print(func(5))