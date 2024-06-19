# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import datetime
from Crypto.Cipher import AES
import base64

def calc_sign(id, key, type, text):
    version = 0x00
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    high_nibble = (year - 2020) & 0x0F
    combined_byte = (high_nibble << 4) | month
    byte0 = version.to_bytes(1, byteorder='big')
    byte1 = combined_byte.to_bytes(1, byteorder='big')
    byte2 = day.to_bytes(1, byteorder='big')
    sign = byte0 + byte1 + byte2

    key_bytes = bytes.fromhex(key)
    id_bytes = bytes.fromhex(id)
    type_byte = bytes([type])
    sign_bytes = sign

    data = key_bytes + id_bytes + type_byte + sign_bytes + text
    padded_data = data.ljust(32, b'\x00')
    xored_data = bytes(byte ^ 0x35 for byte in padded_data)
    key = b'$PS0t3G6@!eHAn(3'
    iv = b'#^bxpkE3Luw5zn6&'

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(xored_data)
    lisence = base64.b64encode(encrypted_data).decode('utf-8')
    return lisence

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
