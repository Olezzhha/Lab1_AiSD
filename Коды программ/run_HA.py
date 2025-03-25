from HA import huffman_decode, huffman_encode
from sizes import size_text

txt_input = 'Rus_text.txt'
txt_input_rus = 'Rus_text.txt'
txt_input_enw = 'enwik7.txt'
txt_input_exe = 'exeshnik.exe'
txt_input_color = 'color2.bmp'
txt_input_gray = 'gray.bmp'
txt_input_black = 'black.bmp'
txt_encoded = 'encoded_HA.bin'
txt_decoded = 'decoded_HA.bin'

with open(txt_input, "rb") as file:
    text = file.read().strip()

encoded_bits, codes = huffman_encode(text)
bit_str = ''.join(map(str, encoded_bits))
bit_str2 = bit_str + '0' * ((8 - len(bit_str) % 8) % 8)
encoded_bytes = bytearray(int(bit_str2[i:i+8], 2) for i in range(0, len(bit_str2), 8))

with open(txt_encoded, "wb") as file:
    file.write(encoded_bytes)

decoded_bits = huffman_decode(encoded_bits, codes)

if isinstance(decoded_bits, str):
    decoded_bits = decoded_bits.encode('utf-8')

with open(txt_decoded, "wb") as file:
    file.write(decoded_bits)

print("\nКоды Хаффмана для символов:")
for byte, (code, length) in codes.items():
    print(f"{byte}: {bin(code)[2:].zfill(length)}")

size_text(text, encoded_bytes, decoded_bits)
