from sizes import size_text
from HA import huffman_decode, huffman_encode
from lz77 import lz77_compress, decode_LZ77

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
