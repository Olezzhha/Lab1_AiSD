from lz77 import lz77_compress, decode_LZ77
from sizes import size_text

def read_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        return file.read()


def write_file(filename: str, data: bytes):
    with open(filename, "wb") as file:
        file.write(data)


def calculate_compression_ratio(original_size, compressed_size):
    return round(original_size / compressed_size, 3)

txt_input_rus = 'Rus_text.txt'
txt_input_enw = 'enwik7.txt'
txt_input_exe = 'exeshnik.exe'
txt_input_color = 'color2.bmp'
txt_input_gray = 'gray.bmp'
txt_input_black = 'black.bmp'

output_compressed = "compressed.lz77"
output_decompressed = "decoded_lz77.bin"

original = read_file(txt_input_rus)
print("compress")
compressed = lz77_compress(original)

write_file(output_compressed, compressed)
print("decompress")
decompressed = decode_LZ77(compressed)
write_file(output_decompressed, decompressed)

print("Файл сжат и сохранен в", output_compressed)
print("Файл декомпрессирован и сохранен в", output_decompressed)

size_text(original,compressed,decompressed)
