def encode_bwt(origin_data, block_size):
    indices = []
    data = bytearray()

    for i in range(0, len(origin_data), block_size):
        block = origin_data[i:i + block_size]
        rotations = sorted((block[j:] + block[:j], j) for j in range(len(block)))
        index = next(j for j, (rot, _) in enumerate(rotations) if rot == block)
        encoded_block = bytes(rot[0][-1] for rot in rotations)

        data.extend(encoded_block)
        indices.append(index)

    return bytes(data), indices


def decode_bwt(encoded_data, indices, block_size):
    restored_data = bytearray()

    for i in range(len(indices)):
        start = i * block_size
        end = min(start + block_size, len(encoded_data))
        block = encoded_data[start:end]
        original_ind = indices[i]
        row = original_ind

        result = bytearray()
        table = sorted((char, idx) for idx, char in enumerate(block))

        for _ in range(len(block)):
            char, row = table[row]
            result.append(char)
        restored_data.extend(result)

    return bytes(restored_data)

