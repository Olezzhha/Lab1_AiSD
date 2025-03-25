def rle_encode(data):
    encoded_data = bytearray()
    n = len(data)
    i = 0
    while i < n:
        char_curr = data[i]
        count = 1
        while i + count < n and data[i + count] == char_curr and count < 127:
            count += 1
        if count > 1:
            encoded_data.append(count)
            encoded_data.append(char_curr)
            i += count
        else:
            non_repeat = bytearray()
            non_repeat.append(char_curr)
            i += 1
            while i < n and (i + 1 >= n or data[i] != data[i + 1]) and len(non_repeat) < 127:
                non_repeat.append(data[i])
                i += 1
            encoded_data.append(0x80 | len(non_repeat))
            encoded_data.extend(non_repeat)
    return bytes(encoded_data)


def rle_decode(encoded_data):
    decoded = bytearray()
    n = len(encoded_data)
    i = 0
    while i < n:
        control_byte = encoded_data[i]
        i += 1
        if control_byte & 0x80:
            length = control_byte & 0x7F
            decoded.extend(encoded_data[i:i + length])
            i += length
        else:
            count = control_byte
            char = encoded_data[i]
            decoded.extend([char] * count)
            i += 1
    return bytes(decoded)