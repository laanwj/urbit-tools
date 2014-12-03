from . import sbox
from .syllables import sis,dex

# ++  xafo  |=([a=@ b=@] +((mod (add (dec b) a) 255)))
def _xafo(a,b):
    return ((a + b - 1) % 255) + 1
# ++  xaro  |=([a=@ b=@] +((mod (add (dec b) (sub 255 (mod a 255))) 255)))
def _xaro(a,b):
    return (((b - 1) + (255 - (a % 255))) % 255) + 1
def wren_un(pyn):
    ln = (pyn.bit_length()+7)//8
    if ln == 0:
        return 0
    ln -= 1
    mig = sbox.zaft[_xafo(ln, (pyn>>(ln*8))&0xff)]
    out = mig << (ln*8)
    while ln > 0:
        ln -= 1
        mog = sbox.zyft[mig ^ (ln&0xff) ^ (pyn>>(ln*8))&0xff]
        out |= mog << (ln*8)
        mig = mog
    return out

def _dname(x):
    '''destroyer name'''
    rv = wren_un(x)
    aa = (rv >> 16)
    bb = rv & 0xffff
    aa = (aa - bb) & 0xffff
    return (sis[aa & 0xff] + dex[(aa >> 8) & 0xff] + '-' +
            sis[bb & 0xff] + dex[(bb >> 8) & 0xff])

def pname(x): # @p
    if x < 0x100: # 8-bit carrier
        return dex[x]
    elif x < 0x10000: # 16-bit cruiser
        return sis[x & 0xff] + dex[(x >> 8) & 0xff]
    elif x < 0x100000000: # 32-bit destroyer
        return _dname(x)
    elif x < 0x10000000000000000: # 64-bit yacht
        return _dname(x >> 32) + '-' + _dname(x & 0xffffffff)
        # shorter submarines happen?
        # `@p`0x2fb1.9a42.f0b3.79a0.92ca.21f6 ~ ~matnyl-firpub-sabfyr-ralfyl--bacwyt-hinmul
    elif x < 0x100000000000000000000000000000000: # 128-bit submarine
        return (_dname((x >> 96) & 0xffffffff) + '-' + _dname((x >> 64) & 0xffffffff) + '--' +
                _dname((x >> 32) & 0xffffffff) + '-' + _dname((x >> 0) & 0xffffffff))
    else:
        raise ValueError # @p is actually valid for even larger numbers

