
def format_hexnum(x):
    '''Format hexadecimal number for urbit shell'''
    rv = '%x' % x
    rem = len(rv)%4
    groups = [rv[0:rem]] if rem else []
    groups += [rv[rem+i:rem+i+4] for i in range(0,len(rv)-rem,4)]
    return '0x'+('.'.join(groups))

# need: jam, en:crua, de:crua

def to_le(x):
    '''Long to little-endian bytes'''
    size = (x.bit_length()+7)//8
    return x.to_bytes(size, 'little')

def from_le(x):
    '''Little-endian bytes to long'''
    return int.from_bytes(x, 'little') 

def num_to_term(x):
    '''@tas'''
    return '%' + to_le(x).decode()

def strings(t):
    '''Naively find ASCII strings/terms in noun.'''
    if isinstance(t, tuple):
        return strings(t[0]) + strings(t[1])
    elif t:
        s = to_le(t)
        if any(ch < 32 or ch >= 127 for ch in s):
            return []
        return [s.decode('ascii')]
    else:
        return []

