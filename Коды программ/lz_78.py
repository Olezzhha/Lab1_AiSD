
import os

def lz78_compress(input_filename: str, output_filename: str):

    with open(input_filename, 'rb') as input_file:
        data = input_file.read()
    dictionary = {}
    output = []
    str_curr = bytearray()
    ind = 1
    i = 0
    while i < len(data):
        str_curr.append(data[i])
        bytes_curr = bytes(str_curr)
        if bytes_curr in dictionary:
            i += 1
        else:
            output.append((dictionary.get(bytes(str_curr[:-1]), 0), str_curr[-1]))
            dictionary[bytes_curr] = ind
            ind += 1
            str_curr = bytearray()
            i += 1
    if str_curr:
        output.append((dictionary.get(bytes(str_curr[:-1]), 0), str_curr[-1]))

    with open(output_filename, 'wb') as output_file:
        for pair in output:
            ind_bytes = pair[0].to_bytes(4, 'big')
            char_bytes = bytes([pair[1]])
            output_file.write(ind_bytes + char_bytes)

    print(f"Сжатые данные записаны в {output_filename}")
    original_size = os.path.getsize(input_filename)
    compressed_size = os.path.getsize(output_filename)
    print("original_size", original_size)
    print("compressed_size", compressed_size)
    compression_ratio = original_size / compressed_size
    print(f"Коэффициент сжатия: {compression_ratio:.3f}")


def lz78_decompress(input_filename: str, output_filename: str):
    with open(input_filename, 'rb') as input_file:
        compressed_data = input_file.read()
    dictionary = {}
    output = bytearray()
    index = 1
    i = 0
    while i < len(compressed_data):
        index_bytes = compressed_data[i:i + 4]
        current_index = int.from_bytes(index_bytes, 'big')
        i += 4
        char_bytes = compressed_data[i:i + 1]
        char = char_bytes[0]
        i += 1
        if current_index == 0:
            output.append(char)
            dictionary[index] = bytearray([char])
        else:
            str_dict = dictionary[current_index]
            output.extend(str_dict)
            output.append(char)
            dictionary[index] = str_dict + bytearray([char])
        index += 1
    with open(output_filename, 'wb') as output_file:
        output_file.write(output)
    print(f"Данные записаны в {output_filename}")



txt_input_enw = "enwik7.txt"
txt_input_exe = "exeshnik.exe"
txt_input_color = "color2.bmp"
txt_input_gray = "gray.bmp"
txt_input_black = "black.bmp"

# сюда название
txt_input_rus = "Rus_text.txt"
output_filename_compressed = "output.lz78"
output_filename_decompressed = "decoded_lz78.bin"


lz78_compress(txt_input_rus, output_filename_compressed)
lz78_decompress(output_filename_compressed, output_filename_decompressed)

with open(txt_input_rus, 'rb') as original_file:
    original_data = original_file.read()

with open(output_filename_decompressed, 'rb') as decompressed_file:
    decompressed_data = decompressed_file.read()

print("данные совпадают:", original_data == decompressed_data)


