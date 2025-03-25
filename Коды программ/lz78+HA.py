from sizes import size_text
from HA import huffman_decode, huffman_encode

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
            index_bytes = pair[0].to_bytes(4, 'big')
            char_bytes = bytes([pair[1]])
            output_file.write(index_bytes + char_bytes)
    print(f"Данные сжаты LZ78 и записаны в {output_filename}")
    return data, output

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
            string_from_dict = dictionary[current_index]
            output.extend(string_from_dict)
            output.append(char)
            dictionary[index] = string_from_dict + bytearray([char])
        index += 1
    with open(output_filename, 'wb') as output_file:
        output_file.write(output)
    print(f"Данные восстановлены LZ78 и записаны в {output_filename}")
    return compressed_data, output


txt_input_rus = 'Rus_text.txt'
txt_input_enw = 'enwik7.txt'
txt_input_exe = 'exeshnik.exe'
txt_input_color = 'color2.bmp'
txt_input_gray = 'gray.bmp'
txt_input_black = 'black.bmp'

input_filename = 'Rus_text.txt'
intermediate_compressed = "output.lz78"
final_compressed = "output_huffman.bin"
final_decompressed = "decoded_78_ha.bin"

original_data, lz78_compressed = lz78_compress(input_filename, intermediate_compressed)

lz78_bytes = bytearray()
for index, char in lz78_compressed:
    lz78_bytes.extend(index.to_bytes(4, 'big'))
    lz78_bytes.append(char)

huffman_encoded_bits, huffman_codes = huffman_encode(bytes(lz78_bytes))
bit_str = ''.join(map(str, huffman_encoded_bits))
bit_str2 = bit_str + '0' * ((8 - len(bit_str) % 8) % 8)
encoded_bytes = bytearray(int(bit_str2[i:i+8], 2) for i in range(0, len(bit_str2), 8))

with open(final_compressed, "wb") as file:
    file.write(encoded_bytes)

print(f"Данные сжаты с помощью Хаффмана и записаны в {final_compressed}")

decoded_huffman_data = huffman_decode(huffman_encoded_bits, huffman_codes)
lz78_decompressed_data, final_decompressed_data = lz78_decompress(intermediate_compressed, final_decompressed)
size_text(original_data, encoded_bytes, final_decompressed_data)



