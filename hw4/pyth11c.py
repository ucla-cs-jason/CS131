def unique_characters(s):
    return {ch for ch in s}

assert unique_characters("happy") == {"h", "a", "p", "y"}