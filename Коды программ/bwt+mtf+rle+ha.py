
from HA import huffman_decode, huffman_encode
from mtf import mtf_encode, mtf_decode
from bwt import encode_bwt, decode_bwt
from rle_nM import rle_encode, rle_decode

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
