What is this?
--------------

    As much fun as a barrel of puppies
    - Vernor Vinge, A fire Upon the Deep

The Martian Communications Kit allows the wielder a level of access to martian communications using earth technology.
At the base are a few Urbit equivalent utilities implemented in Python 3:

- `cue` - urbit.cue - Unpack ('unjam') nouns as nested tuples
- `de:crua` - urbit.crua - Decode %fast network packets ("Cryptosuite A" symmetric decryption)
- `@p` - urbit.pame - Number to scrambled ship name

Functionality for encoding earth data to martian data representations is not available in this version of the Communications Kit.

Command-line tools:

- `urbit_sniffer.py` - Network sniffer that parses and decodes martian packets ("cards"), and
   prints their contents to the console in a way more or less understandable by those coming from earth.

    - Also opens nested forwarded packets (using %fore). No automatic reassembly of fragmented %carp packets happens yet.

    - Current output (`-r` mode):
```
    132417.149947 198.199.112.32:36148 doznec → 192.168.1.14:4006 michep-banlur: proto=5 mug=3ab51 crypto=%fast
    [%bund ~ [%q %gh %radio ~] 0xe3 0x2 %d %zong %mess 0x8000000d232262804f70000000000000 0x6820100 
        %say 0x7327303920656874206f74206b6361626b63696b20612073277461687420776f6e202c696763<'cgi, now that's a kickback to the 90's'>]
```

- `namebrute.py` - Find ship names that match entries in a word list or dictionary

Extracting crypto keys
-----------------------

For the sniffer to be able to decrypt messages encrypted using %fast symmetric
encryption, it needs a keyhash to key map.
This key map can only be aquired by interrogating the state of the martian computing equipment.
Urbit uses a different set of keys per ship it communicates with. These can be queried
from ames using:

    .^(a//=tell=/~zod)

The part of the structure that contains the keys is:

      [ 7.430.499  # %caq
        [ 0
          33.123.819.867.594.127.606.031.000.000.000.000.000
          41.033.688.202.860.769.050.685.819.551.090.085.818.000.000.000.000.000.000.000.000.000.000.000.000.000
        ]
        0
        [ 33.123.819.867.594.127.606.031.000.000.000.000.000
          41.033.688.202.860.769.050.685.819.551.090.085.818.000.000.000.000.000.000.000.000.000.000.000.000.000
        ]
        [ [ 109.594.677.981.129.231.109.000.000.000.000.000.000
            45.386.121.200.585.567.397.574.921.028.396.432.000.000.000.000.000.000.000.000.000.000.000.000.000.000
          ]
          0
          [ 48.135.180.979.525.712.064.000.000.000.000.000.000
            81.419.295.166.239.671.930.722.758.837.403.867.000.000.000.000.000.000.000.000.000.000.000.000.000.000
          ]
          0
          0
        ]
        0
      ]

Extract the number pairs and put these in a file, e.g. `crypto_keys.txt`, in a two-column format. You can remove duplicates:

      33.123.819.867.594.127.606.031.000.000.000.000.000  41.033.688.202.860.769.050.685.819.551.090.085.818.000.000.000.000.000.000.000.000.000.000.000.000.000
      109.594.677.981.129.231.109.000.000.000.000.000.000 45.386.121.200.585.567.397.574.921.028.396.432.000.000.000.000.000.000.000.000.000.000.000.000.000.000
      48.135.180.979.525.712.064.000.000.000.000.000.000  81.419.295.166.239.671.930.722.758.837.403.867.000.000.000.000.000.000.000.000.000.000.000.000.000.000

The resulting file can be passed as `-k crypto_keys.txt` to `urbit_sniffer.py`.

Using tcpdump
---------------

Instead of capturing directly from the network, which requires `root` privileges on most operating systems,
Urbit Sniffer can also read `.pcap` files as produced by e.g.

```bash
tcpdump -w urbit.pcap -p -i eth0 'udp portrange 4000-4008'
```

Pass the resulting file using `-l urbit.pcap`.

