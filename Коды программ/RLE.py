def rle_encode(data: bytes, M: int) -> bytes:
    if M not in [8, 16, 24]:
        raise ValueError("M должно быть 8, 16 или 24.")
    encoded = bytearray()
    i = 0
    n = len(data)

    while i < n:
        if M == 8:
            symb = data[i]
            symb_size = 1
        elif M == 16:
            if i + 1 >= n:
                raise ValueError("Недостаточно данных 16.")
            symb = data[i:i + 2]
            symb_size = 2
        elif M == 24:
            if i + 2 >= n:
                raise ValueError("Недостаточно данных 24.")
            symb = data[i:i + 3]
            symb_size = 3
        count = 1
        while i + count * symb_size < n and data[i + count * symb_size:i + (count + 1) * symb_size] == symb and count < 127:
            count += 1
        if count > 1:
            encoded.append(count)
            encoded.extend(symb)
            i += count * symb_size
        else:
            start = i
            while i < n and (i + symb_size >= n or data[i:i + symb_size] != data[i + symb_size:i + 2 * symb_size]) and (i - start) // symb_size < 127:
                i += symb_size
            length = (i - start) // symb_size
            encoded.append(0x80 | length)
            encoded.extend(data[start:i])
    return bytes(encoded)


def rle_decode(encoded: bytes, M: int) -> bytes:
    if M not in [8, 16, 24]:
        raise ValueError("M должно быть 8, 16 или 24.")
    decoded = bytearray()
    i = 0
    n = len(encoded)
    while i < n:
        control_byte = encoded[i]
        i += 1
        if control_byte & 0x80:
            length = control_byte & 0x7F
            if M == 8:
                decoded.extend(encoded[i:i + length])
                i += length
            elif M == 16:
                decoded.extend(encoded[i:i + 2 * length])
                i += 2 * length
            elif M == 24:
                decoded.extend(encoded[i:i + 3 * length])
                i += 3 * length
        else:
            count = control_byte
            if M == 8:
                symb = encoded[i]
                decoded.extend([symb] * count)
                i += 1
            elif M == 16:
                symb = encoded[i:i + 2]
                decoded.extend(symb * count)
                i += 2
            elif M == 24:
                symb = encoded[i:i + 3]
                decoded.extend(symb * count)
                i += 3
    return bytes(decoded)


def detect_m(data: bytes) -> int:
    n = len(data)
    if n % 2 == 0:
        is_16_bit = True
        for i in range(0, n, 2):
            if not (0x0000 <= int.from_bytes(data[i:i + 2], 'big') <= 0xFFFF):
                is_16_bit = False
                break
        if is_16_bit:
            return 16
    if n % 3 == 0:
        is_24_bit = True
        for i in range(0, n, 3):
            if not (0x000000 <= int.from_bytes(data[i:i + 3], 'big') <= 0xFFFFFF):
                is_24_bit = False
                break
        if is_24_bit:
            return 24
    return 8