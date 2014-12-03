#!/usr/bin/python3
from urbit.util import bin_to_num, num_to_bin
import hashlib

def shax(x):
    return bin_to_num(hashlib.sha256(num_to_bin(x)).digest())

def shas(sal, ruz):
    return shax(sal ^ shax(ruz))

def og_raw(b, size):
    pass

print(hex(shas(0x1234, 0x5678)))

