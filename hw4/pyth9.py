def strip_characters(sentence, chars_to_remove):
  return "".join(filter(lambda x: x not in chars_to_remove, sentence))

print(strip_characters("Hello, world!", {"o", "h", "l"}))