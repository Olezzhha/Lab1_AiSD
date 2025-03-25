from sizes import size_text
from HA import huffman_decode, huffman_encode
from lz77 import lz77_compress, decode_LZ77

# def LZ77(data, window_size=2048, buffer_size=16):
#     i = 0
#     n = len(data)
#     compressed_data = []
#     window = deque(maxlen=window_size)
#
#     while i < n:
#         match_len = 0
#         match_pos = 0
#
#         for j in range(max(0, i - window_size), i):
#             k = 0
#             while k < buffer_size and i + k < n and data[j + k] == data[i + k]:
#                 k += 1
#             if k > match_len:
#                 match_len = k
#                 match_pos = i - j
#
#         if match_len >= 3:
#             if i + match_len < n:
#                 compressed_data.append((match_pos, match_len, data[i + match_len]))
#                 i += match_len + 1
#             else:
#                 compressed_data.append((0, 0, data[i]))
#                 i += 1
#         else:
#             compressed_data.append((0, 0, data[i]))
#             i += 1
#
#         window.append(data[i - 1])
#
#     result = bytearray()
#     for pos, length, char in compressed_data:
#         result.extend(pos.to_bytes(2, 'big'))
#         result.extend(length.to_bytes(2, 'big'))
#         result.append(char)
#     return bytes(result)
#
# def LZ77_decode(data):
#     i = 0
#     n = len(data)
#     decompressed_data = bytearray()
#
#     while i < n:
#         pos = int.from_bytes(data[i:i + 2], 'big')
#         length = int.from_bytes(data[i + 2:i + 4], 'big')
#         char = data[i + 4]
#         if pos == 0 and length == 0:
#             decompressed_data.append(char)
#         else:
#             start = len(decompressed_data) - pos
#             for j in range(length):
#                 decompressed_data.append(decompressed_data[start + j])
#             decompressed_data.append(char)
#         i += 5
#     return bytes(decompressed_data)

# class Node:
#     def __init__(self, char, freq):
#         self.char = char
#         self.freq = freq
#         self.left = None
#         self.right = None
#
#     def __lt__(self, other):
#         return self.freq < other.freq
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
# def generate_codes(node, current_code=0, bit_length=0, codes={}):
#     if node is not None:
#         if node.char is not None:
#             codes[node.char] = (current_code, bit_length)
#         generate_codes(node.left, (current_code << 1), bit_length + 1, codes)
#         generate_codes(node.right, (current_code << 1) | 1, bit_length + 1, codes)
#     return codes
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


def read_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        return file.read()

def write_file(filename: str, data: bytes):
    with open(filename, "wb") as file:
        file.write(data)

def calculate_compression_ratio(original_size, compressed_size):
    return round(original_size / compressed_size, 3)

def main():
    txt_input_rus = 'Rus_text.txt'
    txt_input_enw = 'enwik7.txt'
    txt_input_exe = 'exeshnik.exe'
    txt_input_color = 'color2.bmp'
    txt_input_gray = 'gray.bmp'
    txt_input_black = 'black.bmp'
    input_filename = "input.txt"
    output_compressed_lz77 = "compressed_lz77.bin"
    output_compressed_final = "compressed_lz77_huffman.bin"
    output_decompressed = "decoded_lz77_ha.bin"

    original = read_file( txt_input_rus)

    compressed_lz77 = lz77_compress(original)
    write_file(output_compressed_lz77, compressed_lz77)

    encoded_bits, huffman_codes = huffman_encode(compressed_lz77)
    bit_str = ''.join(map(str, encoded_bits))
    bit_str2 = bit_str + '0' * ((8 - len(bit_str) % 8) % 8)
    encoded_bytes = bytearray(int(bit_str2[i:i+8], 2) for i in range(0, len(bit_str2), 8))

    write_file(output_compressed_final, encoded_bytes)

    decoded_huffman = huffman_decode(encoded_bits, huffman_codes)
    decompressed_lz77 = decode_LZ77(decoded_huffman)
    write_file(output_decompressed, decompressed_lz77)

    print(f"Файл сжат с помощью LZ77 и Хаффмана и сохранен в {output_compressed_final}")
    print(f"Файл декомпрессирован и сохранен в {output_decompressed}")
    size_text(original, encoded_bytes, decompressed_lz77)

if __name__ == "__main__":
    main()
