def mtf_encode(data: bytes) -> list:
    symbol_table = list(range(256))
    encoded = []
    for byte in data:
        index = symbol_table.index(byte)
        encoded.append(index)
        symbol_table.pop(index)
        symbol_table.insert(0, byte)
    return encoded

def mtf_decode(encoded: list) -> bytes:
    symbol_table = list(range(256))
    decoded = bytearray()
    for index in encoded:
        byte = symbol_table[index]
        decoded.append(byte)
        symbol_table.pop(index)
        symbol_table.insert(0, byte)
    return bytes(decoded)