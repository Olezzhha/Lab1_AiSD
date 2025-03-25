from sizes import size_text
from RLE import rle_encode, rle_decode, detect_m

def read_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        return file.read()


def write_file(filename: str, data: bytes):
    with open(filename, "wb") as file:
        file.write(data)


txt_input_rus = 'Rus_text.txt'
txt_input_enw = 'enwik7.txt'
txt_input_exe = 'exeshnik.exe'
txt_input_color = 'color2.bmp'
txt_input_gray = 'gray.bmp'
txt_input_black = 'black.bmp'
output_compressed = "encoded.rle"
output_decompressed = "decoded_rle.bin"

original = read_file(txt_input_rus)

M = detect_m(original)

compressed = rle_encode(original, M)
write_file(output_compressed, compressed)

decompressed = rle_decode(compressed, M)
write_file(output_decompressed, decompressed)

print("Файл сжат и сохранен в", output_compressed)
print("Файл декомпрессирован и сохранен в", output_decompressed)

print("сжатые данные:", compressed)
print("decompressed данные:", decompressed)

size_text(original,compressed,decompressed)