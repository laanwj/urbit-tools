
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

def _read_varint(a, ofs):
    count = -1
    while (a&1) == 0: # number of trailing zeros -> length of length
        a >>= 1
        ofs += 1
        count += 1
    a >>= 1
    ofs += 1
    if count < 0:
        return (a, ofs, 0)
    b = (1<<count) + (a & ((1 << count)-1))
    a >>= count
    ofs += count
    val = (a & ((1 << b)-1))
    a >>= b
    ofs += b
    return (a, ofs, val)

def _read_value(m, ofs, a):
    ostart = ofs
    if a == 0:
        raise ValueError('cue: invalid value zero')
    if (a&1) == 0: # varint
        a >>= 1
        ofs += 1
        (a, ofs, val) = _read_varint(a, ofs)
        m[ostart] = val # memorize w/ bit offset
        return (a, ofs, val)
    elif (a&3) == 1: # cell
        a >>= 2
        ofs += 2
        (a, ofs, val1) = _read_value(m, ofs, a)
        (a, ofs, val2) = _read_value(m, ofs, a)
        val = (val1,val2)
        m[ostart] = val # memorize w/ bit offset
        return (a, ofs, val)
    else: # (a&3) == 3 seems to mean 'repeat'
        a >>= 2
        ofs += 2
        (a, ofs, val1) = _read_varint(a, ofs)
        return (a, ofs, m[val1])
    
def cue(a):
    '''unpack noun'''
    # naive recursive interpretation
    return _read_value({}, 0, a)[2]

