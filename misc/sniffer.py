'''
Basic network sniffing / pcap import functionality
'''
# Copyright (c) 2014 Wladimir J. van der Laan, Visucore
# Distributed under the MIT software license, see
# http://www.opensource.org/licenses/mit-license.php.
import socket, struct, sys, io, time

SO_BINDTODEVICE = 25
ETH_P_ALL = 0x0300 # =htons(0x03) from /usr/include/linux/if_ether.h

class Sniffer:
    '''Load packet stream from network'''
    def __init__(self, interface):
        # would be better as filtering happens in the kernel but doesn't catch outgoing packets:
        #s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        s = socket.socket(socket.PF_PACKET, socket.SOCK_DGRAM, ETH_P_ALL)
        s.setsockopt(socket.SOL_SOCKET,SO_BINDTODEVICE,struct.pack("%ds" % (len(interface)+1,), interface))
        self.s = s
        self.name = 'if:' + interface.decode()

    def __iter__(self):
        return self

    def __next__(self):
        packet = self.s.recvfrom(65565)
        packet = packet[0] # drop extra information
        return (time.time(),packet)

class PCapLoader:
    '''Load packet stream from file.
    @see man pcap-savefile(5) for the format description.
    '''
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        hdr = self.f.read(24)
        hdrp = struct.unpack('=IHHIIII', hdr)
        assert(hdrp[0] == 0xa1b2c3d4) # magic, only support LE w/ microsecond timestamps for now
        assert(hdrp[6] == 1) # link-level header type
        self.name = 'file:' + filename

    def __iter__(self):
        return self

    def __next__(self):
        hdr = self.f.read(16)
        if not hdr:
            raise StopIteration
        # pcap header
        hdrp = struct.unpack('=IIII', hdr)
        data = self.f.read(hdrp[2])
        timestamp = hdrp[0] + hdrp[1]*1e-6
        # ethernet header
        mac_dst = data[0:6]
        mac_src = data[6:12]
        ethertype = data[12:14]
        if ethertype != b'\x08\x00': # only return IP packets
            return b''
        return (timestamp, data[14:]) # strip ethernet header


