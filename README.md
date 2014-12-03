What is this?
--------------

    As much fun as a barrel of puppies                                                                                                                     
    - Vernor Vinge, A fire Upon the Deep                                                                                                                   

Urbit utility functions implemented in Python 3:

- `cue` - Unpack ('unjam') nouns
- `de:crua` - Decode network packets
- `@p` - Ship number to scrambled ship name

Command-line tools:

- `namebrute.py` - Find ship names that match entries a word list or dictionary
- `urbit_sniffer.py` - Network sniffer that parses urbit packets, decodes them (if the key is available) and
   dumpes their contents to the console

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

