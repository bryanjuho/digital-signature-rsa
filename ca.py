import binascii
from uuid import uuid4

import click
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def generate_key_pair():
    # generate key pair
    private_key = RSA.generate(2048)
    pubkey = private_key.publickey()

    # signer object
    signer = pkcs1_15.new(private_key)

    # create key filename
    uuid = str(uuid4())

    # export private key
    with open(f'./{uuid}.pem', 'wb') as f:
        f.write(private_key.exportKey('PEM'))

    # export public key
    with open(f'./valid_pubkeys/{uuid}.pem', 'wb') as f:
        f.write(pubkey.exportKey('PEM'))

    print(f'Private key saved to ./{uuid}.pem')

    return signer


@click.command()
@click.option('--signature', prompt='Enter digital signature to verify')
@click.option('--digest', prompt='Enter generated digest from the file')
@click.option('--key_uuid', prompt='Enter the key\'s uuid')
def validate_signature(signature, digest, key_uuid):
    # import public key
    with open(f'./valid_pubkeys/{key_uuid}.pem', 'rb') as f:
        pubkey = RSA.importKey(f.read())

    # convert digital signature to bytes
    hash_object = SHA384.new(digest.encode())

    # verify
    signer = pkcs1_15.new(pubkey)

    # string to bytes
    signature = binascii.unhexlify(signature.encode())

    try:
        signer.verify(hash_object, signature)
        print('The signature is valid.')
    except (ValueError, TypeError):
        print('The signature is not valid.')


if __name__ == '__main__':
    validate_signature()
