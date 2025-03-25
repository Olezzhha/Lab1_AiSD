import heapq
from collections import defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text: bytes):
    frequency = defaultdict(int)
    for byte in text:
        frequency[byte] += 1

    queue_p = [Node(byte, freq) for byte, freq in frequency.items()]
    heapq.heapify(queue_p)

    while len(queue_p) > 1:
        left = heapq.heappop(queue_p)
        right = heapq.heappop(queue_p)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(queue_p, merged)
    return queue_p[0]

def generate_codes(node, code=0, bit_length=0, codes={}):
    if node is not None:
        if node.char is not None:
            codes[node.char] = (code, bit_length)
        generate_codes(node.left, (code << 1), bit_length + 1, codes)
        generate_codes(node.right, (code << 1) | 1, bit_length + 1, codes)
    return codes

def huffman_encode(text: bytes):
    root = build_huffman_tree(text)
    codes = generate_codes(root)
    encoded_bits = []
    for byte in text:
        code, length = codes[byte]
        for i in reversed(range(length)):
            encoded_bits.append((code >> i) & 1)
    return encoded_bits, codes

def huffman_decode(encoded_bits, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    code = 0
    bit_length = 0
    decoded_bytes = bytearray()

    for bit in encoded_bits:
        code = (code << 1) | bit
        bit_length += 1
        if (code, bit_length) in reverse_codes:
            decoded_bytes.append(reverse_codes[(code, bit_length)])
            code = 0
            bit_length = 0
    return bytes(decoded_bytes)


# txt_input = 'Rus_text.txt'
# txt_input_rus = 'Rus_text.txt'
# txt_input_enw = 'enwik7.txt'
# txt_input_exe = 'exeshnik.exe'
# txt_input_color = 'color2.bmp'
# txt_input_gray = 'gray.bmp'
# txt_input_black = 'black.bmp'
# txt_encoded = 'encoded_HA.bin'
# txt_decoded = 'decoded_HA.bin'
#
# with open(txt_input_color, "rb") as file:
#     text = file.read().strip()
#
# encoded_bits, codes = huffman_encode(text)
# bit_str = ''.join(map(str, encoded_bits))
# bit_str2 = bit_str + '0' * ((8 - len(bit_str) % 8) % 8)
# encoded_bytes = bytearray(int(bit_str2[i:i+8], 2) for i in range(0, len(bit_str2), 8))
#
# with open(txt_encoded, "wb") as file:
#     file.write(encoded_bytes)
#
# decoded_text = huffman_decode(encoded_bits, codes)
#
# with open(txt_decoded, "wb") as file:
#     file.write(decoded_text)
#
# print("\nКоды Хаффмана для символов:")
# for byte, (code, length) in codes.items():
#     print(f"{byte}: {bin(code)[2:].zfill(length)}")
#
# size_text(text,encoded_bytes, decoded_text)