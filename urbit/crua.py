from .util import from_le, to_le
import hashlib

OG_A = from_le(b'og-a')
OG_B = from_le(b'og-b')

def shax(x):
    return from_le(hashlib.sha256(to_le(x)).digest())

def shas(sal, ruz):
    return shax(sal ^ shax(ruz))

def raw_og(a, b):
    '''generate random stream using sha256'''
    c = shas(OG_A, a ^ b)
    rv = 0
    n = 0
    while b > 0:
        d = shas(OG_B, a ^ b ^ c)
        if b < 256:
            rv |= (d & ((1<<b)-1)) << n
        else:
            rv |= d << n
        c = d
        b -= 256
        n += 256
    return rv

def de_crua(key, cep):
    '''decrypt: cryptosuite a'''
    toh = (cep.bit_length() + 255) // 256
    if toh < 2:
        return None
    adj = toh - 1
    hax = cep & ((1<<256)-1)
    bod = cep >> 256
    msg = raw_og(hax ^ key, 256*adj) ^ bod
    hah = shax(key ^ shax(adj ^ msg))
    if hah == hax:
        return msg
    else:
        return None

