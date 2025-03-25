def size_text(text,encoded_text, decoded_text):
    original_size = len(text)
    compressed_size = len(encoded_text)
    decompressed_size = len(decoded_text)
    compression_ratio = original_size / compressed_size
    compression_ratio = round(compression_ratio, 3)

    print("Размер до компрессии:", original_size, "байт")
    print("Размер после компрессии:", compressed_size, "байт")
    print("Размер после декомпрессии:", decompressed_size, "байт")
    print("Коэффициент сжатия:", compression_ratio)
    print("данные совпадают:", text == decoded_text)