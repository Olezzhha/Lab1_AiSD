import heapq
from collections import defaultdict
from sizes import size_text
from HA import huffman_decode, huffman_encode
from mtf import mtf_encode, mtf_decode
from bwt import encode_bwt, decode_bwt

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

# # Huffman Encoding
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
def write_file(filename: str, data: bytes):
    with open(filename, "wb") as file:
        file.write(data)

def encode_combined(input_data, block_size):
    encoded_bwt, indices = encode_bwt(input_data, block_size)
    mtf_encoded = mtf_encode(encoded_bwt)
    huffman_bits, huffman_codes = huffman_encode(bytes(mtf_encoded))

    return huffman_bits, huffman_codes, indices


def decode_combined(encoded_bits, huffman_codes, indices, block_size):
    decoded_mtf = huffman_decode(encoded_bits, huffman_codes)
    mtf_decoded = mtf_decode(list(decoded_mtf))
    decoded_bwt = decode_bwt(mtf_decoded, indices, block_size)

    return decoded_bwt

txt_input_rus = 'Rus_text.txt'
txt_input_enw = 'enwik7.txt'
txt_input_exe = 'exeshnik.exe'
txt_input_color = 'color2.bmp'
txt_input_gray = 'gray.bmp'
txt_input_black = 'black.bmp'

txt_decompressed = 'decoded_bwt_mtf_ha.bin'

txt_input = 'Rus_text.txt'
block_size = 1000

with open(txt_input, "rb") as file:
    text = file.read().strip()

encoded_bits, huffman_codes, indices = encode_combined(text, block_size)
encoded_bytes = bytearray(int(''.join(map(str, encoded_bits[i:i + 8])), 2) for i in range(0, len(encoded_bits), 8))
decoded_text = decode_combined(encoded_bits, huffman_codes, indices, block_size)
write_file(txt_decompressed, decoded_text)

with open('decoded_output.txt', "wb") as file:
    file.write(decoded_text)

size_text(text, encoded_bytes, decoded_text)