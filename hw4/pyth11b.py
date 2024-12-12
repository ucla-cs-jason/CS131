def parse_csv(lines):
    return [(fruit, int(num)) for line in lines for fruit, num in [line.split(',')]]

assert parse_csv(["apple,8", "pear,24", "gooseberry,-2"]) == [("apple", 8), ("pear", 24), ("gooseberry", -2)]