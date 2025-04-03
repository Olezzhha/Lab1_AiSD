from bwtmtfha import encode_combined, decode_combined
from sizes import size_text
from bwt import encode_bwt, decode_bwt
from RLE import rle_encode, rle_decode, detect_m
from bwtmtfrleha import combined_encode, combined_decode, calculate_compression_ratio
from HA import huffman_decode, huffman_encode
from lz77 import lz77_compress, decode_LZ77
from lz_78 import lz78_compress, lz78_decompress
from lz78_HA import lz78_compress1, lz78_decompress1
import numpy as np
from PIL import Image
import os

def choose_file():
    files = {
        "1": "Rus_text.txt",
        "2": "enwik7.txt",
        "3": "exeshnik.exe",
        "4": "col.jpg",
        "5": "gray1.jpg",
        "6": "black1.jpg"
    }
    print("Выберите номер одного из следующих файлов:")
    for key, value in files.items():
        print(f"{key}: {value}")
    choice = input("Введите номер файла: ")
    return files.get(choice, None)

def png_to_raw(image_path, output_path):
    image = Image.open(image_path)
    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
        image = image.convert('RGB')

    raw_pixels = np.array(image)
    raw_data = raw_pixels.tobytes()

    with open(output_path, 'wb') as f:
        f.write(raw_data)

def convert_image_to_raw(image_path):
    raw_image_path = f"{os.path.splitext(image_path)[0]}_raw.bin"
    png_to_raw(image_path, raw_image_path)
    return raw_image_path


def read_file(filename):
    with open(filename, "rb") as file:
        return file.read()


def write_file(filename, data):
    with open(filename, "wb") as file:
        file.write(data)


def bwt_mtf_ha():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    txt_decompressed = "decoded_bwt_mtf_ha.bin"
    block_size = 1000
    text = read_file(txt_input).strip()

    encoded_bits, huffman_codes, indices = encode_combined(text, block_size)
    encoded_bytes = bytearray(int(''.join(map(str, encoded_bits[i:i + 8])), 2) for i in range(0, len(encoded_bits), 8))
    decoded_text = decode_combined(encoded_bits, huffman_codes, indices, block_size)

    write_file(txt_decompressed, decoded_text)
    write_file("decoded_output.txt", decoded_text)
    size_text(text, encoded_bytes, decoded_text)


def bwt_rle():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    txt_decompressed = "decoded_bwt_rle.bin"
    block_size = 1000
    text = read_file(txt_input).strip()

    encoded_text_bwt, indices = encode_bwt(text, block_size)
    M = detect_m(encoded_text_bwt)
    encoded_text_rle = rle_encode(encoded_text_bwt, M)

    write_file("compressed_bwt.rle", encoded_text_rle)
    decoded_text_rle = rle_decode(encoded_text_rle, M)
    decoded_text_bwt = decode_bwt(decoded_text_rle, indices, block_size)

    write_file(txt_decompressed, decoded_text_bwt)
    size_text(text, encoded_text_rle, decoded_text_bwt)


def ha():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    txt_encoded = "encoded_HA.bin"
    txt_decoded = "decoded_HA.bin"
    text = read_file(txt_input).strip()

    encoded_bits, codes = huffman_encode(text)
    bit_str = ''.join(map(str, encoded_bits))
    bit_str2 = bit_str + '0' * ((8 - len(bit_str) % 8) % 8)
    encoded_bytes = bytearray(int(bit_str2[i:i + 8], 2) for i in range(0, len(bit_str2), 8))

    write_file(txt_encoded, encoded_bytes)
    decoded_bits = huffman_decode(encoded_bits, codes)
    write_file(txt_decoded, decoded_bits)

    # print("\nКоды Хаффмана для символов:")
    # for byte, (code, length) in codes.items():
    #     print(f"{byte}: {bin(code)[2:].zfill(length)}")

    size_text(text, encoded_bytes, decoded_bits)


def lz77():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    output_compressed = "compressed.lz77"
    output_decompressed = "decoded_lz77.bin"

    original = read_file(txt_input)
    compressed = lz77_compress(original)

    write_file(output_compressed, compressed)
    decompressed = decode_LZ77(compressed)
    write_file(output_decompressed, decompressed)

    size_text(original, compressed, decompressed)


def lz78():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    output_compressed = "output.lz78"
    output_decompressed = "decoded_lz78.bin"

    lz78_compress(txt_input, output_compressed)
    lz78_decompress(output_compressed, output_decompressed)

    original_data = read_file(txt_input)
    decompressed_data = read_file(output_decompressed)

    print("Данные совпадают:", original_data == decompressed_data)

def lz78_ha():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    intermediate_compressed = "lz78_compressed.bin"
    final_compressed = "lz78_ha_compressed.bin"
    final_decompressed = "lz78_ha_decompressed.bin"

    original_data, lz78_compressed = lz78_compress1(txt_input, intermediate_compressed)

    lz78_bytes = bytearray()
    for index, char in lz78_compressed:
        lz78_bytes.extend(index.to_bytes(4, 'big'))
        lz78_bytes.append(char)

    huffman_encoded_bits, huffman_codes = huffman_encode(bytes(lz78_bytes))
    bit_str = ''.join(map(str, huffman_encoded_bits))
    bit_str2 = bit_str + '0' * ((8 - len(bit_str) % 8) % 8)  # Дополнение до байта
    encoded_bytes = bytearray(int(bit_str2[i:i+8], 2) for i in range(0, len(bit_str2), 8))

    write_file(final_compressed, encoded_bytes)

    decoded_huffman_data = huffman_decode(huffman_encoded_bits, huffman_codes)
    _, final_decompressed_data = lz78_decompress1(intermediate_compressed, final_decompressed)

    size_text(original_data, encoded_bytes, final_decompressed_data)

def lz77_ha():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    output_compressed_lz77 = "compressed_lz77.bin"
    output_compressed_final = "compressed_lz77_huffman.bin"
    output_decompressed = "decoded_lz77_ha.bin"

    original = read_file(txt_input)

    compressed_lz77 = lz77_compress(original)
    write_file(output_compressed_lz77, compressed_lz77)

    encoded_bits, huffman_codes = huffman_encode(compressed_lz77)
    bit_str = ''.join(map(str, encoded_bits))
    bit_str2 = bit_str + '0' * ((8 - len(bit_str) % 8) % 8)  # Дополнение до байта
    encoded_bytes = bytearray(int(bit_str2[i:i+8], 2) for i in range(0, len(bit_str2), 8))

    write_file(output_compressed_final, encoded_bytes)
    decoded_huffman = huffman_decode(encoded_bits, huffman_codes)
    decompressed_lz77 = decode_LZ77(decoded_huffman)
    write_file(output_decompressed, decompressed_lz77)
    size_text(original, encoded_bytes, decompressed_lz77)

def bwt_mtf_rle_ha():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    output_compressed = "encoded_data.bin"
    output_decompressed = "decoded_data.txt"
    original_data = read_file(txt_input)

    encoded_data, huffman_codes, bwt_indices = combined_encode(original_data, block_size=1024)

    with open(output_compressed, "wb") as file:
        file.write(bytearray(encoded_data))

    decoded_data = combined_decode(encoded_data, huffman_codes, bwt_indices, block_size=1024)
    if original_data == decoded_data:
        print("Данные совпадают")
    else:
        print("Данные не совпадают")
    write_file(output_decompressed, decoded_data)
    compression_ratio = calculate_compression_ratio(original_data, encoded_data)
    print(f"Коэффициент сжатия: {compression_ratio:.3f}")


def rle():
    txt_input = choose_file()
    if not txt_input:
        print("Ошибка выбора файла.")
        return

    if txt_input.endswith(('.bmp', '.png', '.jpg')):
        txt_input = convert_image_to_raw(txt_input)

    output_compressed = "encoded.rle"
    output_decompressed = "decoded_rle.bin"

    original = read_file(txt_input)
    M = detect_m(original)

    compressed = rle_encode(original, M)
    write_file(output_compressed, compressed)

    decompressed = rle_decode(compressed, M)
    write_file(output_decompressed, decompressed)

    size_text(original, compressed, decompressed)


def main():
    algorithms = {
        "1": ("BWT + MTF + HA", bwt_mtf_ha),
        "2": ("BWT + RLE", bwt_rle),
        "3": ("HA", ha),
        "4": ("LZ77", lz77),
        "5": ("LZ78", lz78),
        "6": ("RLE", rle),
        "7": ("LZ78 + HA", lz78_ha),
        "8": ("LZ77 + HA", lz77_ha),
        "9": ("BWT + MTF + RLE + HA", bwt_mtf_rle_ha)
    }

    print("Выберите алгоритм сжатия:")
    for key, (name, _) in algorithms.items():
        print(f"{key}: {name}")

    choice = input("Введите номер алгоритма: ")
    if choice in algorithms:
        algorithms[choice][1]()
    else:
        print("Ошибка: Неверный ввод.")


if __name__ == "__main__":
    main()
