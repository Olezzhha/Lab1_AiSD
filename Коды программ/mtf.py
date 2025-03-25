import struct

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


#
# def read_file(filename: str) -> bytes:
#     with open(filename, "rb") as file:
#         return file.read()
#
# def write_binary_file(filename: str, data: list):
#     with open(filename, "wb") as file:
#         file.write(struct.pack(f"{len(data)}B", *data))
#
# def read_binary_file(filename: str) -> list:
#     with open(filename, "rb") as file:
#         return list(file.read())
#
# def write_text_file(filename: str, data: bytes):
#     with open(filename, "wb") as file:
#         file.write(data)
#
# # Файлы
# input_filename = "input.txt"
# output_compressed = "compressed.mtf"
# output_decompressed = "decompressed.txt"
#
# # Чтение и сжатие
# original = read_file(input_filename)
# compressed = mtf_encode(original)
# write_binary_file(output_compressed, compressed)
#
# # Декомпрессия
# compressed_data = read_binary_file(output_compressed)
# decompressed = mtf_decode(compressed_data)
# write_text_file(output_decompressed, decompressed)
#
# print("Файл сжат и сохранен в", output_compressed)
# print("Файл декомпрессирован и сохранен в", output_decompressed)
# print("Исходные данные:", original)
# print("Сжатые данные:", compressed)
# print("Декомпрессированные данные:", decompressed)
#
# print("данные совпадают", original==decompressed)