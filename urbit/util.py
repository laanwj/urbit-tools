
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

def probable_term(x):
    return all((ch in b'abcdefghijklmnopqrstuvwxyz') for ch in to_le(x))

def dump_noun(noun, f):
    '''
    Dump noun in human-intelligable format.
    '''
    if isinstance(noun, tuple):
        f.write('[')
        dump_noun(noun[0], f)
        f.write(' ')
        while isinstance(noun[1], tuple):
            noun = noun[1]
            dump_noun(noun[0], f)
            f.write(' ')
        dump_noun(noun[1], f)
        f.write(']')
    else:
        if noun == 0:
            f.write('~')
        else:
            if probable_term(noun):
                f.write(num_to_term(noun))
            else:
                f.write(hex(noun))
                s = to_le(noun)
                if all(((ch >= 32 and ch < 127) or ch==10 or ch==13) for ch in s):
                    s = s.decode().replace('\\','\\\\').replace('\n','\\n').replace('\r','\\r').replace('\'','\\\'')
                    f.write('<\''+s+'\'>')

