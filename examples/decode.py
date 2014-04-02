def decode(input_string):
    result = ""
    curr_char_already_added = False
    prev_char = None

    for curr_char in input_string:
        if curr_char != prev_char:
            curr_char_already_added = False
        else:
            if not curr_char_already_added:
                if curr_char == '#':
                    if result == "":
                        return None    # error mark
                    else:
                        result += result[-1]
                else:
                    result += curr_char
                curr_char_already_added = True

        prev_char = curr_char

    return result



assert decode("") == ""
assert decode("##") is None
assert decode("1") == ""
assert decode("12345#") == ""
assert decode("11") == "1"
assert decode("1111") == "1"
assert decode("1122") == "12"
assert decode("112211221122") == "121212"
assert decode("11##") == "11"
assert decode("11##11##") == "1111"
assert decode("11##22##11") == "11221"
assert decode("1111111#####2222222333333#3") == "1123"
assert decode("1###") is None
assert decode("221133444##") == "21344"