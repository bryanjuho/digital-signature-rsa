# Digital Signature Implementation in Python
# Author: Juho Hong, Jihyoung Jang, Seungyong Lee
# Date: 2022. 12. 6
# Description: This program signs a document, creates a digital signature
# and verifies the validity/authenticity of the signature.
import binascii
import hashlib
from pathlib import Path

import click
from Crypto.Hash import SHA384
from Crypto.Signature import pkcs1_15

from ca import generate_key_pair


def encrypt(digest):
    # encrypt
    signer = generate_key_pair()

    # Sign the digest
    hash_object = SHA384.new(digest.encode())
    digital_signature = signer.sign(hash_object)

    signature = binascii.hexlify(digital_signature).decode()
    print(f'Digital Signature: {signature}')


@click.command()
@click.option('--file', prompt='Enter the path of the file to sign')
def start_app(file):
    # Read the file
    path_file = Path(file)
    if not path_file.is_file():
        print("File does not exist")
        return

    file_object = path_file.open(mode='rb')

    digest = hashlib.md5(file_object.read()).hexdigest()

    encrypt(digest)

    print(f'Hash is : {digest}')


if __name__ == '__main__':
    start_app()
