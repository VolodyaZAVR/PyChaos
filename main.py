import math
from base64 import b64encode
from base64 import b64decode
import pickle
from PIL import Image
from io import BytesIO
import binascii


class Encrypter:
    key = []
    vector_init = []
    binary = []
    binary_encode = []
    binary_decode = []

    @staticmethod
    def generate_key(x0, y0, k, s, alpha, n):
        x = x0
        y = y0
        key = [0] * n
        for i in range(n):
            xn = math.cos(alpha) * x + math.sin(alpha) * (y + k * s * math.sin(x))
            xn = math.fmod(xn, 1)
            b = int(math.fmod(abs(int(xn * 10 ** 9)), 2))
            yn = -math.sin(alpha) * x + math.cos(alpha) * (y + k * s * math.sin(x)) + (1 - s) * k * math.sin(xn)
            yn = math.fmod(yn, 1)
            x = xn
            y = yn
            key[i] = b
        return key

    @staticmethod
    def logical_xor(a, b):
        if bool(a) == bool(b):
            return 0
        else:
            return 1

    def encode_algorithm(self, binary, key, vector, option=True):
        temp_binary = binary[:]
        for i in range(len(temp_binary)):
            temp_binary[i] = int(self.logical_xor(temp_binary[i], key[i]))
        temp_key = vector[:]
        i = 0
        j = 0
        while 128 * i + j < len(temp_binary):
            temp_binary[128 * i + j] = int(self.logical_xor(temp_binary[128 * i + j], temp_key[j]))
            j += 1
            if j >= 128:
                i += 1
                for j in range(128):
                    if option:  # option = Encode
                        temp_key[j] = temp_binary[128 * (i - 1) + j]
                    else:  # option = Decode
                        temp_key[j] = binary[128 * (i - 1) + j]
                j = 0
        return temp_binary

    @staticmethod
    def convert_to_binary(filename):
        with open(filename, 'rb') as file:
            binary_content = b64encode(file.read())
        binary = [0] * (len(binary_content) * 7)
        for i in range(len(binary_content)):
            temp = bin(binary_content[i])
            delta = 0
            if len(temp) < 9:
                binary[i * 7] = 0
                delta = 1
            for k in range(len(temp) - 2):
                binary[i * 7 + k + delta] = int(temp[2 + k])
        return binary

    @staticmethod
    def write_in_file(binary, filename):
        with open(filename, 'wb') as outfile:
            pickle.dump(binary, outfile)

    @staticmethod
    def get_from_file(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def convert_to_data(binary):
        byte_code = b''
        for i in range(len(binary) // 7):
            char_bytes = ''
            for j in range(7):
                char_bytes += str(binary[i * 7 + j])
            char_to_int = int(char_bytes, 2)
            byte_code += binascii.unhexlify('%x' % char_to_int)
        pic_decoded = BytesIO(b64decode(byte_code))
        img_restored = Image.open(pic_decoded)
        img_restored.save("output2.jpg")


class Encoder(Encrypter):
    def __init__(self, filename):
        binary = self.convert_to_binary(filename)
        key = self.generate_key(0.5, 0.5, 3, 0.5, math.pi / 2, len(binary))
        vector_init = self.generate_key(0.5, 0.5, 3, 0.5, math.pi / 2, 256)
        vector_init = vector_init[128:]
        binary_encode = self.encode_algorithm(binary, key, vector_init)
        self.write_in_file(binary_encode, 'output.txt')


class Decoder(Encoder):
    def __init__(self, filename):
        binary_encode = self.get_from_file(filename)
        key = self.generate_key(0.5, 0.5, 3, 0.5, math.pi / 2, len(binary_encode))
        vector_init = self.generate_key(0.5, 0.5, 3, 0.5, math.pi / 2, 256)
        vector_init = vector_init[128:]
        binary_decode = self.encode_algorithm(binary_encode, key, vector_init, False)
        self.convert_to_data(binary_decode)
