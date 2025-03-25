
import os
from collections import deque


def lz77_compress(input_data, window_size=2048, buffer_size=64):
    data_len = len(input_data)
    output = []
    window = deque(maxlen=window_size)
    ind = 0
    while ind < data_len:
        length_l,pos_l = 0,0
        for st in range(max(0, ind - window_size), ind):
            lenght = 0
            while lenght < buffer_size and ind + lenght < data_len and input_data[
                st + lenght] == input_data[ind + lenght]:
                lenght += 1
            if lenght > length_l:
                length_l = lenght
                pos_l = ind - st
        if length_l >= 3:
            if ind + length_l < data_len:
                output.append((pos_l, length_l, input_data[ind + length_l]))
                ind += length_l + 1
            else:
                output.append((0, 0, input_data[ind]))
                ind += 1
        else:
            output.append((0, 0, input_data[ind]))
            ind += 1
        window.append(input_data[ind - 1])
    res = bytearray()
    for pos, length, char in output:
        res.extend(pos.to_bytes(2, 'big'))
        res.extend(length.to_bytes(2, 'big'))
        res.append(char)
    return bytes(res)


def decode_LZ77(data):
    ind = 0
    decode = bytearray()
    data_length = len(data)
    while ind < data_length:
        position, lenght = int.from_bytes(data[ind:ind + 2], 'big'),int.from_bytes(data[ind + 2:ind + 4], 'big')
        byte = data[ind + 4]
        if position == 0 and lenght == 0:
            decode.append(byte)
        else:
            st_ind = len(decode) - position
            for _ in range(lenght):
                decode.append(decode[st_ind])
                st_ind += 1
            decode.append(byte)
        ind += 5
    return bytes(decode)

