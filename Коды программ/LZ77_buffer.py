
import matplotlib.pyplot as plt
from lz77 import lz77_compress


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
