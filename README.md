# GCwR implementation

## How to compile

1. Clone `liboqs` and build liboqs.

```
bash liboqs.sh
```

2. Run `make`.

```
make
```

3. Run executable

```
./build/gcwr-ake
```

Output should be like this.

```
[--] Setting Classic-McEliece-6688128...
[--] Public key bytes: 1044992
[--] Ciphertext bytes: 240
[--] Secret key bytes: 13892
[--] Shared secret key bytes: 32
[--] NIST level: 5
[--] IND-CCA: Y

[U_A] Generating static keys...
[U_A] ekA1: 1a18d25c0a265dd21639ead7a972b960...4a17d1697fff7d7201cafcd16afd54e8
[U_A] dkA1: 5f0739930a7cf32217d29a76fde1a47e...ee9b74a67622db82d60915ac6dd84efb

[U_B] Generating static keys...
[U_B] ekB1: a62b25ba11e001162a07926c4d41e522...916486aff6b01c2b7eac2ce45a896843
[U_B] dkB1: db2df25d311d74d09038105a03aff54f...cf61117707a43065f1b9da87b2c546de

[U_A] Generating ekA2 and dkA2...
[U_A] ekA2: d7a81a268002b14845f98429fb17562f...a90cb1a5881e66b48da39db33a87dd7b
[U_A] dkA2: 401deac10774cbe31ffadcc175e736cb...ada21322086290ae28b77e01c5881b6a
[U_B] Generating kB1...
[U_B] kB1: 91499fee9faf34e55d4d36122a9d28636bd1491a7b9653cc2b048ab1b0fdf3a2
[U_B] Generating kB2...
[U_B] kB2: 686b3a09fe1635d9b28a7a33a19d220c7a9b490825eb1d3060561f1cf50dea5b
[U_B] Generating kA1...
[U_B] kA1: 906e6b63483522475027b5d8f70465d35b6d00f13bef03cb87588a5aff263760

[U_A] Generating kB1_prime...
[U_A] kB1_prime: 91499fee9faf34e55d4d36122a9d28636bd1491a7b9653cc2b048ab1b0fdf3a2
[U_A] Generating kB2_prime...
[U_A] kB2_prime: 686b3a09fe1635d9b28a7a33a19d220c7a9b490825eb1d3060561f1cf50dea5b

[U_A] skA: ab7878afdd54ac40eec708369eb66a1c9be302305e799750200c91c7faa9a8aa
[U_B] skB: ab7878afdd54ac40eec708369eb66a1c9be302305e799750200c91c7faa9a8aa
[--] Key exchange successful!


Time stats
	Init time       : 0.000s (0.00%)
	Round keys time : 1.320s (72.13%)
	Round alg. Init : 0.510s (27.87%)
	Round alg. B    : 0.000s (0.00%)
	Round alg. A    : 0.000s (0.00%)
	Total time      : 1.830s (100.00%)
----------------------------------------------------------------------------------------
[--] Setting NTRU-HPS-4096-821...
[--] Public key bytes: 1230
[--] Ciphertext bytes: 1230
[--] Secret key bytes: 1590
[--] Shared secret key bytes: 32
[--] NIST level: 5
[--] IND-CCA: Y

[U_A] Generating static keys...
[U_A] ekA1: 072bda4867ca5bcd67e777b24c4c7440...563b2d320a1cc491fa8dce363908927c
[U_A] dkA1: 2b94599c614e3a99d05ac3c6a77ce14a...a6814f816058969e72eca404938fdc42

[U_B] Generating static keys...
[U_B] ekB1: 75cb4a79078866175f0125f2ae465822...73cf71e052f9e960030679433048c609
[U_B] dkB1: b5306181216995e451376a84cc9c8785...793102462332128f16564ede428aaa97

[U_A] Generating ekA2 and dkA2...
[U_A] ekA2: edea6c5efac78250e045f104571ab5f0...91f1647ea64eb200e8659cf517499b36
[U_A] dkA2: 4008d9a1083916a1e7ee347872dad907...17738b5e23e2b66dc2f1551bc9d827f8
[U_B] Generating kB1...
[U_B] kB1: 3f75dae3f8a7c2fcda61aa1f995e3e2b6814dbe50038bb7019a29106ced486d4
[U_B] Generating kB2...
[U_B] kB2: 5b24285579c5ae519da9b8f40035d00f01bd960d8ec8466654151f0c9f16dfb0
[U_B] Generating kA1...
[U_B] kA1: cefef5dd59397b919a5794de0241f294ff178618304ce0cdb32f5e688b0abe68

[U_A] Generating kB1_prime...
[U_A] kB1_prime: 3f75dae3f8a7c2fcda61aa1f995e3e2b6814dbe50038bb7019a29106ced486d4
[U_A] Generating kB2_prime...
[U_A] kB2_prime: 5b24285579c5ae519da9b8f40035d00f01bd960d8ec8466654151f0c9f16dfb0

[U_A] skA: afb6f66c9e0d46250e11a4402c1a7d06aaa4212dc06d5583ab7a4646b67dcf67
[U_B] skB: afb6f66c9e0d46250e11a4402c1a7d06aaa4212dc06d5583ab7a4646b67dcf67
[--] Key exchange successful!


Time stats
	Init time       : 0.000s (0.00%)
	Round keys time : 0.010s (100.00%)
	Round alg. Init : 0.000s (0.00%)
	Round alg. B    : 0.000s (0.00%)
	Round alg. A    : 0.000s (0.00%)
	Total time      : 0.010s (100.00%)
----------------------------------------------------------------------------------------
[--] Setting FireSaber-KEM...
[--] Public key bytes: 1312
[--] Ciphertext bytes: 1472
[--] Secret key bytes: 3040
[--] Shared secret key bytes: 32
[--] NIST level: 5
[--] IND-CCA: Y

[U_A] Generating static keys...
[U_A] ekA1: 363a46b0fecd680e990fcf6954961bd4...658dfd1da8427e644ac60120a1b528b3
[U_A] dkA1: ffdffff7ffffffff01c0ff0f00000000...ff5f05e4edb4be51eee615d62d25ba0f

[U_B] Generating static keys...
[U_B] ekB1: 0c6101dadf9ac3cab940c2beea6e8f04...af07b9a430b0675729b105aef01a39f9
[U_B] dkB1: ff1f00fc7f00e0ff05c0ffffff020000...0d6c80316f9a29ce23174d3ba59312b7

[U_A] Generating ekA2 and dkA2...
[U_A] ekA2: a2c7baf7f032e4450f9fa1dd219f64e0...378e34488c0906bcaa1c6483391221ad
[U_A] dkA2: 010000008000d0ffff3f00f8ff00e0ff...346cfe646e6386d5712c6c7d8b44f336
[U_B] Generating kB1...
[U_B] kB1: 700cefb928c6219096c1341843dfba84da42c5921d207772e844dfd77a527b6a
[U_B] Generating kB2...
[U_B] kB2: 563b18184e9bde7f1103905f59146768592ae973130a0c27567d2503ccd3013c
[U_B] Generating kA1...
[U_B] kA1: 667c89a33e7122aa708ab2a8c35011414c29ac43d23b4949f2aea28839f8bb9d

[U_A] Generating kB1_prime...
[U_A] kB1_prime: 700cefb928c6219096c1341843dfba84da42c5921d207772e844dfd77a527b6a
[U_A] Generating kB2_prime...
[U_A] kB2_prime: 563b18184e9bde7f1103905f59146768592ae973130a0c27567d2503ccd3013c

[U_A] skA: 86cea0dd69184835475d836367a710d0a2ac59cdb02730e2aff93399363d38d6
[U_B] skB: 86cea0dd69184835475d836367a710d0a2ac59cdb02730e2aff93399363d38d6
[--] Key exchange successful!


Time stats
	Init time       : 0.000s (-nan%)
	Round keys time : 0.000s (-nan%)
	Round alg. Init : 0.000s (-nan%)
	Round alg. B    : 0.000s (-nan%)
	Round alg. A    : 0.000s (-nan%)
	Total time      : 0.000s (-nan%)
----------------------------------------------------------------------------------------
[--] Setting Kyber1024...
[--] Public key bytes: 1568
[--] Ciphertext bytes: 1568
[--] Secret key bytes: 3168
[--] Shared secret key bytes: 32
[--] NIST level: 5
[--] IND-CCA: Y

[U_A] Generating static keys...
[U_A] ekA1: 95b43cb34b0065e690610c24faea1d09...95e53fb214ce3174996b2ab49dd7629b
[U_A] dkA1: 78a10cf3e6932371a889d11f3f4aa21f...92a5b77d42e73ac15eb52fd975a635fe

[U_B] Generating static keys...
[U_B] ekB1: 0eec7a63a1cbff52630c1764612334ff...c02dcb7993d69934b6cce5c4777ab2db
[U_B] dkB1: b5a82bc21221b38a3e06b909fe61b03d...4a5d91ade2dc446c3e5b81eeb0814715

[U_A] Generating ekA2 and dkA2...
[U_A] ekA2: a12a1623423209b64bd857296fc47830...0042f22aaacd96970595dfa849ad0f4f
[U_A] dkA2: 58181da0ac850e210d87e5ba63463a08...9c1e7226497974e1d9649f3f8b1be913
[U_B] Generating kB1...
[U_B] kB1: 38d919f464d5f9347b3e0ed2c2a164bcd42c5a0ab514757e4be15921f2bebd95
[U_B] Generating kB2...
[U_B] kB2: 698a01a9dd2a9fc8e01e4e5f31e8a01ca726c15575bed3eb81a9833262274447
[U_B] Generating kA1...
[U_B] kA1: 27cadc5918a5b4cd43c81899d9939d32f6f776b7704d8db3ccb4edef6b43c4c2

[U_A] Generating kB1_prime...
[U_A] kB1_prime: 38d919f464d5f9347b3e0ed2c2a164bcd42c5a0ab514757e4be15921f2bebd95
[U_A] Generating kB2_prime...
[U_A] kB2_prime: 698a01a9dd2a9fc8e01e4e5f31e8a01ca726c15575bed3eb81a9833262274447

[U_A] skA: 403351a6dc31eeeb55f9775a6184b9697b98741fd0e7694f743fed1457526e32
[U_B] skB: 403351a6dc31eeeb55f9775a6184b9697b98741fd0e7694f743fed1457526e32
[--] Key exchange successful!


Time stats
	Init time       : 0.000s (-nan%)
	Round keys time : 0.000s (-nan%)
	Round alg. Init : 0.000s (-nan%)
	Round alg. B    : 0.000s (-nan%)
	Round alg. A    : 0.000s (-nan%)
	Total time      : 0.000s (-nan%)
----------------------------------------------------------------------------------------
```
