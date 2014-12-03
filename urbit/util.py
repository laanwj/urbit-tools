
def varnum_le(x):
    '''Little-endian bytes to long'''
    return int.from_bytes(x, 'little') 

def format_hexnum(x):
    '''Format hexadecimal number for urbit shell'''
    rv = '%x' % x
    rem = len(rv)%4
    groups = [rv[0:rem]] if rem else []
    groups += [rv[rem+i:rem+i+4] for i in range(0,len(rv)-rem,4)]
    return '0x'+('.'.join(groups))

# need: jam, en:crua, de:crua

# jam format
# 0                     10
# 1                   1100
# 2               100.1000
# 3               110.1000
# 4              1001.1000
# 5              1011.1000
# 7              1111.1000
# 8          100.0001.0000
# 15         111.1001.0000
# 31        1111.1011.0000
# 63      1.1111.1101.0000
#127     11.1111.1111.0000
#128 1.0000.0000.0010.0000
#255 1.1111.1110.0010.0000
# [0 0]            10.1001
# [1 0]          1011.0001
# [0 1]          1100.1001
# [1 1]       11.0011.0001
# [0 [0 0]]   10.1001.1001
# [[0 0] 0]   10.1010.0101

# (&3)==1  -> cell
# (&3)==2  -> 0
# (&3)==0  -> count trailing zeros
#    2    0 count bits, 1 bit
#    3    1 count bit,  2+x bits
#    4    2 count bits, 4+x bits

def _read_value(a):
    if a == 0:
        #raise ValueError('cue: invalid value zero')
        return (0, None)
    if (a&3) == 0: # varint
        a >>= 2
        count = 0
        while (a&1) == 0: # number of trailing zeros -> length of length
            a >>= 1
            count += 1
        a >>= 1
        b = (1<<count) + (a & ((1 << count)-1))
        a >>= count
        val = (a & ((1 << b)-1))
        a >>= b
        return (a, val)
    elif (a&3) == 1: # cell
        a >>= 2
        (a, val1) = _read_value(a)
        (a, val2) = _read_value(a)
        return (a, (val1,val2))
    elif (a&3) == 2: # zero
        a >>= 2
        return (a, 0)
    else:
        #raise ValueError('cue: invalid marker 3')
        return (0, None)
    
def cue(a):
    '''unpack noun'''
    # naive recursive interpretation that does not concatenate successive
    # cells
    return _read_value(a)[1]

def num_to_bin(x):
    size = (x.bit_length()+7)//8
    return x.to_bytes(size, 'little')

def bin_to_num(x):
    return int.from_bytes(x, 'little')

def num_to_term(x):
    '''@tas'''
    return '%' + num_to_bin(x).decode()
