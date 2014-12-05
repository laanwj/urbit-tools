What is this?
--------------

    As much fun as a barrel of puppies
    - Vernor Vinge, A fire Upon the Deep

Urbit utility functions implemented in Python 3:

- `cue` - Unpack ('unjam') nouns as nested tuples
- `de:crua` - Decode %fast network packets ("Cryptosuite A" symmetric decryption)
- `@p` - Number to scrambled ship name

Command-line tools:

- `urbit_sniffer.py` - Network sniffer that parses urbit packets, decodes them (if the key is available) and
   dumpes their contents to the console.

    - Also opens nested forwarded packets (using %fore). No automatic reassembly of fragmented %carp packets happens yet.

    - Current output (`-r` mode):
```
    198.199.112.32:37132 → 192.168.1.123:12345 proto=4 mug=f95f1 crypto=%fast sender=doznec receiver=satfyl-saldyl keyhash=0x84e9.cc31.960e.b3d5.fc58.e393.1a86.0108
        015facce8d9c058f07fe0c1de0910b234b7b1bc8be0c3b3839e0ebbdb99d037e5bd9dc3c0001000000000000c2009fb01e230d000080011720e0ce016f2e2c0ff0d7190ba303297941cb6b737b417b7b5b03
        (1684960610, (0, ((113, (26727, (478509556082, 0))), (2429, (6, (100, (1735290746, (1936942445, (170141184501304421605047107635422167040, (108462336, (7954803, 142806000102157565365653161490641937210)))))))))))
        'bund', 'q', 'gh', 'radio', 'd', 'zong', 'mess', 'say', ':cat %/hymn/hook'
```

- `namebrute.py` - Find ship names that match entries in a word list or dictionary

Extracting crypto keys
-----------------------

For the sniffer to be able to decrypt messages encrypted using %fast symmetric
encryption, it needs a keyhash -> key map.

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

