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
