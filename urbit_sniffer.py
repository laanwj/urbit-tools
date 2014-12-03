#!/usr/bin/python3
# Copyright (c) 2014 Wladimir J. van der Laan, Visucore
# Distributed under the MIT software license, see
# http://www.opensource.org/licenses/mit-license.php.
'''
urbit UDP sniffer

Usage: urbit_sniffer.py [-p <port1>-<port2>,<port3>,...] [-i <interface>]
'''
import socket, struct, sys, io, argparse
from struct import pack,unpack
from binascii import b2a_hex
from urbit.util import format_hexnum,from_le,to_le,strings
from urbit.cue import cue
from urbit.pname import pname
from urbit.crua import de_crua

if sys.version_info[0:2] < (3,0):
    print("Requires python3", file=sys.stderr)
    exit(1)

class Args: # default args
    # interface we're interested in
    interface = b'eth0'
    # ports we're interested in
    ports = set(list(range(4000,4008)) + [13337, 41954])
    # known keys for decrypting packets
    keys = {}

# constants...
CRYPTOS = {0:'%none', 1:'%open', 2:'%fast', 3:'%full'}
SO_BINDTODEVICE = 25
ETH_P_ALL = 0x0300 # =htons(0x03) from /usr/include/linux/if_ether.h

# utilities...
def ipv4str(addr):
    '''Bytes to IPv4 address'''
    return '.'.join(['%i' % i for i in addr])

def crypto_name(x):
    '''Name for crypto algo'''
    if x in CRYPTOS:
        return CRYPTOS[x]
    else:
        return 'unk%02i' % x

def hexstr(x):
    '''Bytes to hex string'''
    return b2a_hex(x).decode()

def colorize(str, col):
    return ('\x1b[38;5;%im' % col) + str + ('\x1b[0m')

# cli colors and glyphs
COLOR_IP = 21
COLOR_HEADER = 27
COLOR_VALUE = 33
COLOR_DATA = 250
COLOR_DATA_ENC = 245
v_arrow = colorize('→', 240)
v_attention = colorize('>', 34) + colorize('>', 82) + colorize('>', 118)
v_colon = colorize(':', 240)
v_equal = colorize('=', 245)

def parse_args():
    args = Args()
    parser = argparse.ArgumentParser(description='Urbit sniffer. Dump incoming and outgoing urbit packets.')
    pdefault = '4000-4007,13337,41954' # update this when Args changes...
    idefault = args.interface.decode()
    parser.add_argument('-p, --ports', dest='ports', help='Ports to listen on (default: '+pdefault+')')
    parser.add_argument('-i, --interface', dest='interface', help='Interface to listen on (default:'+idefault+')', default=idefault)
    parser.add_argument('-k, --keys', dest='keys', help='Import keys from file (with <keyhash> <key> per line)', default=None)

    r = parser.parse_args()
    args.interface = r.interface.encode()
    if r.ports is not None:
        args.ports = set()
        for t in r.ports.split(','):
            (a,_,b) = t.partition('-')
            ai = int(a)
            bi = int(b) if b else ai
            args.ports.update(list(range(int(ai), int(bi)+1)))
    if r.keys is not None:
        args.keys = {}
        print(v_attention + ' Loading decryption keys from ' + r.keys)
        with open(r.keys, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                l = line.split()
                # filter out '.' so that keys can be copied directly
                args.keys[int(l[0].replace('.',''))] = int(l[1].replace('.',''))

    return args

def dump_urbit_packet(args, srcaddr, sport, dstaddr, dport, data):
    try:
        # Urbit header and payload
        urhdr = unpack('<L', data[0:4])[0]
        proto = urhdr & 7
        mug = (urhdr >> 3) & 0xfffff
        yax = (urhdr >> 23) & 3
        yax_bytes = 1<<(yax+1)
        qax = (urhdr >> 25) & 3
        qax_bytes = 1<<(qax+1)
        crypto = (urhdr >> 27)
        sender = from_le(data[4:4+yax_bytes])
        receiver = from_le(data[4+yax_bytes:4+yax_bytes+qax_bytes])
        payload = data[4+yax_bytes+qax_bytes:]
        if crypto == 2: # %fast
            keyhash = from_le(payload[0:16])
            payload = payload[16:]
        else:
            keyhash = None
    except (IndexError, struct.error):
        print('Warn: invpkt')
        return

    # Decode packet if crypto known
    decrypted = False
    if crypto == 0:
        decrypted = True
    if crypto == 2 and keyhash in args.keys: # %fast
        payload = from_le(payload)
        payload = de_crua(args.keys[keyhash], payload)
        payload = to_le(payload)
        decrypted = True
    # Print packet
    hdata = [('proto', str(proto)),
             ('mug', '%05x' % mug),
             ('crypto', crypto_name(crypto)),
             ('sender', pname(sender)),
             ('receiver', pname(receiver))]
    if keyhash is not None:
         hdata += [('keyhash', format_hexnum(keyhash))]
    print(  colorize(ipv4str(srcaddr), COLOR_IP) + v_colon + colorize(str(sport), COLOR_IP) + ' ' +
            v_arrow + ' ' +
            colorize(ipv4str(dstaddr), COLOR_IP) + v_colon + colorize(str(dport), COLOR_IP) + ' ' +
            ' '.join(colorize(key, COLOR_HEADER) + v_equal + colorize(value, COLOR_VALUE) for (key,value) in hdata))
    if decrypted: # decrypted or unencrypted data
        print('    ' + colorize(hexstr(payload), COLOR_DATA))
        cake = cue(from_le(payload))
        print('    ' + (', '.join(repr(x) for x in strings(cake))))
    else: # [sealed]
        print('    [' + colorize(hexstr(payload), COLOR_DATA_ENC)+']')


def main(args):
    # would be better as filtering happens in the kernel but doesn't catch outgoing packets:
    #s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    s = socket.socket(socket.PF_PACKET, socket.SOCK_DGRAM, ETH_P_ALL)
    print(v_attention + ' Listening on ' + args.interface.decode() + ' ports ' + (',').join(str(x) for x in args.ports))
    s.setsockopt(socket.SOL_SOCKET,SO_BINDTODEVICE,pack("%ds" % (len(args.interface)+1,), args.interface))

    while True:
        packet = s.recvfrom(65565)
        packet = packet[0] # drop extra information

        try:
            # IP header
            iph = unpack('!BBHHHBBH4s4s', packet[0:20])
            ihl = (iph[0] & 15)*4
            if ihl < 20: # cannot handle IP headers <20 bytes
                # print("Warn: invhdr")
                continue
            protocol = iph[6]
            srcaddr = iph[8]
            dstaddr = iph[9]
            if protocol != 17: # not UDP or no place for header
                #print("Warn: invproto")
                continue

            # UDP header
            (sport, dport, ulength, uchecksum) = unpack('!HHHH', packet[ihl:ihl+8])

            data = packet[ihl+8:ihl+ulength]
            if len(data) != (ulength-8):
                print("Warn: invlength")
                continue # invalid length packet

            if dport not in args.ports and sport not in args.ports: # only urbit ports
                continue
        except (IndexError, struct.error):
            print('Warn: invpkt')
            continue

        dump_urbit_packet(args, srcaddr, sport, dstaddr, dport, data)

if __name__ == '__main__':
    # Force UTF8 out
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf8', line_buffering=True)
    try:
        main(parse_args())
    except KeyboardInterrupt:
        pass

