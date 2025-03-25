from sizes import size_text
from bwt import encode_bwt, decode_bwt
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

txt_input = 'Rus_text.txt'
txt_encoded = 'encoded_bwt+rle.bin'
txt_decoded = 'decoded_bwt+rle.bin'
txt_compressed = 'compressed_bwt.rle'
txt_decompressed = 'decoded_bwt_rle.bin'
block_size = 1000

with open(txt_input, "rb") as file:
    text = file.read().strip()

encoded_text_bwt, indices = encode_bwt(text, block_size)
M = detect_m(encoded_text_bwt)
encoded_text_rle = rle_encode(encoded_text_bwt, M)
write_file(txt_compressed, encoded_text_rle)
decoded_text_rle = rle_decode(encoded_text_rle, M)
decoded_text_bwt = decode_bwt(decoded_text_rle, indices, block_size)
write_file(txt_decompressed, decoded_text_bwt)

size_text(text,encoded_text_rle,decoded_text_bwt)



