#with open('/home/adam/Downloads/Poznan_2018_export/poznan.re', 'rb') as f:
#    print(f.read(1))
#    print(f.read(1))
#    print(f.read(2))
#    print(ord(f.read(1)))
#    print(f.read(2))
    #n_gracze = f.read(2)
    #n_rundy = f.read(2)
    #n_wakat = f.read(2)
    #_ = f.read(7*2)
    #_ = f.read(2*int(n_gracze))

#print(n_gracze, n_rundy, n_wakat)

import struct

filename = '/home/adam/Downloads/Poznan_2018_export/poznan.re'
struct_fmt = '=bBHHH' # int[5], float, byte[255]
struct_len = struct.calcsize(struct_fmt)
struct_unpack = struct.Struct(struct_fmt).unpack_from

def read_chunks(f, length):
    while True:
        data = f.read(length)
        if not data: break
        yield data

with open(filename, "rb") as f:
    results = [struct_unpack(chunk) for chunk in read_chunks(f, struct_len)]

print(results[-11:])
print(len(results)-3)
print((len(results)-3)/14)
