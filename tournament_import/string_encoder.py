# https://stackoverflow.com/questions/38777818/how-do-i-properly-create-custom-text-codecs
import string

_encode_table = {letter: bytes(letter, 'ascii') for letter in (string.ascii_letters + string.digits + string.punctuation)}
_encode_table.update({'ą': b'\xa0',
                      'ć': b'\x9b',
                      'ę': b'\x82',
                      'ł': b'\x9f',
                      'ń': b'\xa4',
                      'ó': b'\xa2',
                      'ś': b'\x87',
                      'ż': b'\x91',
                      'ź': b'\xa8',
                      'Ą': b'\x8f',
                      'Ć': b'\x80',
                      'Ę': b'\x90',
                      'Ł': b'\x9c',
                      'Ń': b'\xa5',
                      'Ó': b'\x93',
                      'Ś': b'\x98',
                      'Ż': b'\x92',
                      'Ź': b'\x9d',})

_decode_table = {ord(v): k for k, v in _encode_table.items()}


def encode_string(text: str) -> bytes:
    return b''.join(_encode_table[x] for x in text)


def decode_string(binary: bytes) -> str:
    return ''.join(_decode_table[x] for x in binary)