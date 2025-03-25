import os
import matplotlib.pyplot as plt
from lz77 import lz77_compress, decode_LZ77

# def LZ77(data, window_size=1024, buffer_size=16):
#     i = 0
#     n = len(data)
#     compressed_data = []
#     window = deque(maxlen=window_size)
#     while i < n:
#         match_len = 0
#         match_pos = 0
#         for j in range(max(0, i - window_size), i):
#             k = 0
#             while k < buffer_size and i + k < n and data[j + k] == data[i + k]:
#                 k += 1
#             if k > match_len:
#                 match_len = k
#                 match_pos = i - j
#         if match_len >= 3:
#             if i + match_len < n:
#                 compressed_data.append((match_pos, match_len, data[i + match_len]))
#                 i += match_len + 1
#             else:
#                 compressed_data.append((0, 0, data[i]))
#                 i += 1
#         else:
#             compressed_data.append((0, 0, data[i]))
#             i += 1
#         window.append(data[i - 1])
#     result = bytearray()
#     for pos, length, char in compressed_data:
#         result.extend(pos.to_bytes(2, 'big'))
#         result.extend(length.to_bytes(2, 'big'))
#         result.append(char)
#     return bytes(result)
#
# def LZ77_decode(data):
#     i = 0
#     n = len(data)
#     decompressed_data = bytearray()
#     while i < n:
#         pos = int.from_bytes(data[i:i + 2], 'big')
#         length = int.from_bytes(data[i + 2:i + 4], 'big')
#         char = data[i + 4]
#         if pos == 0 and length == 0:
#             decompressed_data.append(char)
#         else:
#             start = len(decompressed_data) - pos
#             for j in range(length):
#                 decompressed_data.append(decompressed_data[start + j])
#             decompressed_data.append(char)
#         i += 5
#     return bytes(decompressed_data)

def read_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        return file.read()

def write_file(filename: str, data: bytes):
    with open(filename, "wb") as file:
        file.write(data)

def calculate_compression_ratio(original_size, compressed_size):
    return round(original_size / compressed_size, 3)

def test_buffer_sizes(input_filename, window_size=1024, buffer_sizes=[4, 8, 16, 32, 64, 96, 128, 192, 256]):
    original_data = read_file(input_filename)
    ratios = []

    for buffer_size in buffer_sizes:
        compressed_data = lz77_compress(original_data, window_size, buffer_size)
        compressed_size = len(compressed_data)
        print("compressed_size", compressed_size)
        compression_ratio = calculate_compression_ratio(len(original_data), compressed_size)
        print("compression_ratio", compression_ratio)
        ratios.append((buffer_size, compression_ratio))

    return ratios

def plot_compression_ratios(ratios):
    buffer_sizes, compression_ratios = zip(*ratios)
    plt.plot(buffer_sizes, compression_ratios, marker='o', linestyle='-', color='c')
    plt.xlabel('Размер буфера (байты)')
    plt.ylabel('Коэффициент сжатия')
    plt.title('Зависимость коэффициента сжатия от размера буфера (LZ77)')
    plt.grid(True)
    plt.show()

def main():
    input_filename = 'Rus_text.txt'
    ratios = test_buffer_sizes(input_filename)
    plot_compression_ratios(ratios)

if __name__ == "__main__":
    main()
