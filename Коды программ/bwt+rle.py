from sizes import size_text
from bwt import encode_bwt, decode_bwt
from RLE import rle_encode, rle_decode, detect_m

# def encode_bwt(origin_data, block_size):
#     indices = []
#     data = bytearray()
#
#     for i in range(0, len(origin_data), block_size):
#         block = origin_data[i:i + block_size]
#         rotations = sorted((block[j:] + block[:j], j) for j in range(len(block)))
#         index = next(j for j, (rot, _) in enumerate(rotations) if rot == block)
#         encoded_block = bytes(rot[0][-1] for rot in rotations)
#
#         data.extend(encoded_block)
#         indices.append(index)
#
#     return bytes(data), indices
#
#
# def decode_bwt(encoded_data, indices, block_size):
#     restored_data = bytearray()
#
#     for i in range(len(indices)):
#         start = i * block_size
#         end = min(start + block_size, len(encoded_data))
#         block = encoded_data[start:end]
#         original_ind = indices[i]
#
#         row = original_ind
#         result = bytearray()
#         table = sorted((char, idx) for idx, char in enumerate(block))
#
#         for _ in range(len(block)):
#             char, row = table[row]
#             result.append(char)
#         restored_data.extend(result)
#
#     return bytes(restored_data)

# def rle_encode(data: bytes, M: int) -> bytes:
#     if M not in [8, 16, 24]:
#         raise ValueError("M должно быть 8, 16 или 24.")
#
#     encoded = bytearray()
#     i = 0
#     n = len(data)
#
#     while i < n:
#         if M == 8:
#             current_symbol = data[i]
#             symbol_size = 1
#         elif M == 16:
#             if i + 1 >= n:
#                 raise ValueError("Недостаточно данных для 16-битного символа.")
#             current_symbol = data[i:i + 2]
#             symbol_size = 2
#         elif M == 24:
#             if i + 2 >= n:
#                 raise ValueError("Недостаточно данных для 24-битного символа.")
#             current_symbol = data[i:i + 3]
#             symbol_size = 3
#
#         repeat_count = 1
#         while i + repeat_count * symbol_size < n and data[i + repeat_count * symbol_size:i + (repeat_count + 1) * symbol_size] == current_symbol and repeat_count < 127:
#             repeat_count += 1
#
#         if repeat_count > 1:
#             encoded.append(repeat_count)
#             encoded.extend(current_symbol)
#             i += repeat_count * symbol_size
#         else:
#             non_repeat_start = i
#             while i < n and (i + symbol_size >= n or data[i:i + symbol_size] != data[i + symbol_size:i + 2 * symbol_size]) and (i - non_repeat_start) // symbol_size < 127:
#                 i += symbol_size
#
#             non_repeat_length = (i - non_repeat_start) // symbol_size
#             encoded.append(0x80 | non_repeat_length)
#             encoded.extend(data[non_repeat_start:i])
#     return bytes(encoded)
#
#
# def rle_decode(encoded: bytes, M: int) -> bytes:
#     if M not in [8, 16, 24]:
#         raise ValueError("M должно быть 8, 16 или 24.")
#
#     decoded = bytearray()
#     i = 0
#     n = len(encoded)
#
#     while i < n:
#         control_byte = encoded[i]
#         i += 1
#
#         if control_byte & 0x80:
#             length = control_byte & 0x7F
#             if M == 8:
#                 decoded.extend(encoded[i:i + length])
#                 i += length
#             elif M == 16:
#                 decoded.extend(encoded[i:i + 2 * length])
#                 i += 2 * length
#             elif M == 24:
#                 decoded.extend(encoded[i:i + 3 * length])
#                 i += 3 * length
#         else:
#             repeat_count = control_byte
#             if M == 8:
#                 current_symbol = encoded[i]
#                 decoded.extend([current_symbol] * repeat_count)
#                 i += 1
#             elif M == 16:
#                 current_symbol = encoded[i:i + 2]
#                 decoded.extend(current_symbol * repeat_count)
#                 i += 2
#             elif M == 24:
#                 current_symbol = encoded[i:i + 3]
#                 decoded.extend(current_symbol * repeat_count)
#                 i += 3
#
#     return bytes(decoded)
#
#
# def detect_m(data: bytes) -> int:
#     n = len(data)
#     if n % 2 == 0:
#         is_16_bit = True
#         for i in range(0, n, 2):
#             if not (0x0000 <= int.from_bytes(data[i:i + 2], 'big') <= 0xFFFF):
#                 is_16_bit = False
#                 break
#         if is_16_bit:
#             return 16
#
#     if n % 3 == 0:
#         is_24_bit = True
#         for i in range(0, n, 3):
#             if not (0x000000 <= int.from_bytes(data[i:i + 3], 'big') <= 0xFFFFFF):
#                 is_24_bit = False
#                 break
#         if is_24_bit:
#             return 24
#
#     return 8


def read_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        return file.read()


def write_file(filename: str, data: bytes):
    with open(filename, "wb") as file:
        file.write(data)

txt_input_rus = 'Rus_text.txt'
txt_input_enw = 'enwik7.txt'
txt_input_exe = 'exeshnik.exe'
txt_input_color = 'color2.bmp'
txt_input_gray = 'gray.bmp'
txt_input_black = 'black.bmp'

txt_input = 'Rus_text.txt'
txt_encoded = 'encoded_bwt+rle.bin'
txt_decoded = 'decoded_bwt+rle.bin'
txt_compressed = 'compressed_bwt.rle'
txt_decompressed = 'decoded_bwt_rle.bin'
block_size = 1000

with open(txt_input, "rb") as file:
    text = file.read().strip()

encoded_text_bwt, indices = encode_bwt(text, block_size)
M = detect_m(encoded_text_bwt)
encoded_text_rle = rle_encode(encoded_text_bwt, M)
write_file(txt_compressed, encoded_text_rle)
decoded_text_rle = rle_decode(encoded_text_rle, M)
decoded_text_bwt = decode_bwt(decoded_text_rle, indices, block_size)
write_file(txt_decompressed, decoded_text_bwt)

size_text(text,encoded_text_rle,decoded_text_bwt)



