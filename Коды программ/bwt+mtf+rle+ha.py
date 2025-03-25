import heapq
import struct
from collections import defaultdict
from sizes import size_text
from HA import huffman_decode, huffman_encode
from mtf import mtf_encode, mtf_decode
from bwt import encode_bwt, decode_bwt
from rle_nM import rle_encode, rle_decode

# def encode_bwt(origin_data, block_size):
#     indices = []
#     data = bytearray()
#     for i in range(0, len(origin_data), block_size):
#         block = origin_data[i:i + block_size]
#         rotations = sorted((block[j:] + block[:j], j) for j in range(len(block)))
#         index = next(j for j, (rot, _) in enumerate(rotations) if rot == block)
#         encoded_block = bytes(rot[0][-1] for rot in rotations)
#         data.extend(encoded_block)
#         indices.append(index)
#
#     return bytes(data), indices
#
#
# def decode_bwt(encoded_data, indices, block_size):
#     restored_data = bytearray()
#     for i in range(len(indices)):
#         start = i * block_size
#         end = min(start + block_size, len(encoded_data))
#         block = encoded_data[start:end]
#         original_ind = indices[i]
#         row = original_ind
#         result = bytearray()
#         table = sorted((char, idx) for idx, char in enumerate(block))
#         for _ in range(len(block)):
#             char, row = table[row]
#             result.append(char)
#         restored_data.extend(result)
#     return bytes(restored_data)

# def mtf_encode(data: bytes) -> list:
#     symbol_table = list(range(256))
#     encoded = []
#     for byte in data:
#         index = symbol_table.index(byte)
#         encoded.append(index)
#         symbol_table.pop(index)
#         symbol_table.insert(0, byte)
#     return encoded
#
#
# def mtf_decode(encoded: list) -> bytes:
#     symbol_table = list(range(256))
#     decoded = bytearray()
#     for index in encoded:
#         byte = symbol_table[index]
#         decoded.append(byte)
#         symbol_table.pop(index)
#         symbol_table.insert(0, byte)
#     return bytes(decoded)
# def rle_encode(data):
#     encoded_data = bytearray()
#     n = len(data)
#     i = 0
#     while i < n:
#         current_char = data[i]
#         count = 1
#         while i + count < n and data[i + count] == current_char and count < 127:
#             count += 1
#         if count > 1:
#             encoded_data.append(count)
#             encoded_data.append(current_char)
#             i += count
#         else:
#             non_repeat_chars = bytearray()
#             non_repeat_chars.append(current_char)
#             i += 1
#             while i < n and (i + 1 >= n or data[i] != data[i + 1]) and len(non_repeat_chars) < 127:
#                 non_repeat_chars.append(data[i])
#                 i += 1
#             encoded_data.append(0x80 | len(non_repeat_chars))
#             encoded_data.extend(non_repeat_chars)
#     return bytes(encoded_data)
#
#
# def rle_decode(encoded_data):
#     decoded_data = bytearray()
#     n = len(encoded_data)
#     i = 0
#     while i < n:
#         control_byte = encoded_data[i]
#         i += 1
#         if control_byte & 0x80:
#             length = control_byte & 0x7F
#             decoded_data.extend(encoded_data[i:i + length])
#             i += length
#         else:
#             count = control_byte
#             char = encoded_data[i]
#             decoded_data.extend([char] * count)
#             i += 1
#     return bytes(decoded_data)


# class Node:
#     def __init__(self, char, freq):
#         self.char = char
#         self.freq = freq
#         self.left = None
#         self.right = None
#
#     def __lt__(self, other):
#         return self.freq < other.freq
#
#
# def build_huffman_tree(text: bytes):
#     frequency = defaultdict(int)
#     for byte in text:
#         frequency[byte] += 1
#
#     priority_queue = [Node(byte, freq) for byte, freq in frequency.items()]
#     heapq.heapify(priority_queue)
#
#     while len(priority_queue) > 1:
#         left = heapq.heappop(priority_queue)
#         right = heapq.heappop(priority_queue)
#         merged = Node(None, left.freq + right.freq)
#         merged.left = left
#         merged.right = right
#         heapq.heappush(priority_queue, merged)
#     return priority_queue[0]
#
#
# def generate_codes(node, current_code=0, bit_length=0, codes={}):
#     if node is not None:
#         if node.char is not None:
#             codes[node.char] = (current_code, bit_length)
#         generate_codes(node.left, (current_code << 1), bit_length + 1, codes)
#         generate_codes(node.right, (current_code << 1) | 1, bit_length + 1, codes)
#     return codes
#
#
# def huffman_encode(text: bytes):
#     root = build_huffman_tree(text)
#     codes = generate_codes(root)
#     encoded_bits = []
#     for byte in text:
#         code, length = codes[byte]
#         for i in reversed(range(length)):
#             encoded_bits.append((code >> i) & 1)
#     return encoded_bits, codes
#
#
# def huffman_decode(encoded_bits, codes):
#     reverse_codes = {v: k for k, v in codes.items()}
#     current_code = 0
#     bit_length = 0
#     decoded_bytes = bytearray()
#
#     for bit in encoded_bits:
#         current_code = (current_code << 1) | bit
#         bit_length += 1
#         if (current_code, bit_length) in reverse_codes:
#             decoded_bytes.append(reverse_codes[(current_code, bit_length)])
#             current_code = 0
#             bit_length = 0
#     return bytes(decoded_bytes)


def combined_encode(data, block_size):
    bwt_encoded, bwt_indices = encode_bwt(data, block_size)
    mtf_encoded = mtf_encode(bwt_encoded)
    rle_encoded = rle_encode(mtf_encoded)
    huffman_encoded, huffman_codes = huffman_encode(rle_encoded)

    return huffman_encoded, huffman_codes, bwt_indices

def combined_decode(encoded_data, huffman_codes, bwt_indices, block_size):
    huffman_decoded = huffman_decode(encoded_data, huffman_codes)
    rle_decoded = rle_decode(huffman_decoded)
    mtf_decoded = mtf_decode(rle_decoded)
    bwt_decoded = decode_bwt(mtf_decoded, bwt_indices, block_size)
    return bwt_decoded

def calculate_compression_ratio(original_data, encoded_data):
    original_size = len(original_data)
    print("original_size",original_size)
    compressed_size = len(encoded_data) // 8
    print("compressed_size", compressed_size)
    return original_size / compressed_size

def write_file(filename: str, data: bytes):
    with open(filename, "wb") as file:
        file.write(data)

if __name__ == "__main__":
    txt_input_rus = 'Rus_text.txt'
    txt_input_enw = 'enwik7.txt'
    txt_input_exe = 'exeshnik.exe'
    txt_input_color = 'color2.bmp'
    txt_input_gray = 'gray.bmp'
    txt_input_black = 'black.bmp'
    txt_decompressed = 'decoded_bwt_mtf_rle_ha.bin'
    with open('Rus_text.txt', "rb") as file:
        data = file.read()

    encoded_data, huffman_codes, bwt_indices = combined_encode(data, block_size=1024)

    with open("encoded_data.bin", "wb") as file:
        file.write(bytearray(encoded_data))

    decoded_data = combined_decode(encoded_data, huffman_codes, bwt_indices, block_size=1024)
    print(data == decoded_data)
    compression_ratio = calculate_compression_ratio(data, encoded_data)
    print(f"Compression ratio: {compression_ratio:.3f}")
    write_file(txt_decompressed, decoded_data)
