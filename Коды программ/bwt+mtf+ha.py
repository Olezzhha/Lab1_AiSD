from sizes import size_text
from HA import huffman_decode, huffman_encode
from mtf import mtf_encode, mtf_decode
from bwt import encode_bwt, decode_bwt

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