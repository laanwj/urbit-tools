#!/usr/bin/python3
from __future__ import division,print_function
from urbit.syllables import sis,dex
from collections import defaultdict
import argparse

class Args: # Default arguments
    enable_partial = False
    dict_file = '/usr/share/dict/words'
    #dict_file = '/usr/share/dict/dutch'
    #dict_file = '/usr/share/dict/ogerman'

args = Args()

def parse_args():
    args = Args()
    parser = argparse.ArgumentParser(description='Urbit ship name generator.')
    parser.add_argument('-p, --partial', dest='enable_partial', action='store_true', help='Enable partial matches', default=False)
    parser.add_argument('-d, --dict', dest='dict_file', help='Use dictionary file (default:'+args.dict_file+')', default=args.dict_file)

    return parser.parse_args()

def main(args):
    with open(args.dict_file, 'rb') as f:
        words = []
        for w in f: # skip words that are invalid utf8
            try:
                words.append(w.decode())
            except UnicodeDecodeError:
                pass
        words = [x.strip() for x in words]
        words = [x.lower() for x in words]
        words = [x for x in words if not x.endswith("'s")]

    # Create set of full and partial matches
    full = []
    partial = []
    for syllist in sis,dex:
        f = set()
        p = defaultdict(list)
        for w in syllist:
            f.add(w)
            p[w[0:1]].append(w)
            p[w[0:2]].append(w)
        full.append(f)
        partial.append(p)

    # Look for words that consist of sis/dex pairs
    result = {}
    for w in words:
        if len(w)<=3:
            continue
        ptr = 0
        dictid = 0
        syls = []
        while ptr < len(w):
            syl = w[ptr:ptr+3]
            if syl in full[dictid]:
                syls.append([syl])
            elif args.enable_partial and syl in partial[dictid]:
                syls.append(partial[dictid][syl])
            else:
                break
            ptr += 3
            dictid = 1-dictid

        if ptr < len(w):
            continue

        # assume partial matches can be only on end
        base = [x[0] for x in syls[0:-1]]
        for alt in syls[-1]:
            term = tuple(base + [alt])
            if not term in result or len(w) > len(result[term]):
                result[term] = w

    def render_term(x):
        rv = ''
        ptr = 0
        while ptr < len(x):
            if ptr:
                rv += '-'
            if (ptr+1) < len(x):
                rv += x[ptr+0] + x[ptr+1]
                ptr += 2
            else:
                rv += x[ptr+0]
                ptr += 1
        return rv

    keys = sorted(result.keys())
    for term in keys:
        w = result[term]
        print('%-6s: %s' % (render_term(term), w))

if __name__ == '__main__':
    main(parse_args())

