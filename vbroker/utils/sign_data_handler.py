import json
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring


def get_rsa_key(private_key: str):
    key = base64.b64decode(private_key.encode('utf-8'))
    key_json = json.loads(json.dumps(bf.data(fromstring(key))))
    cc = key_json['RSAKeyValue']
    n = int.from_bytes(base64.b64decode(cc['Modulus']['$']), byteorder='big')
    e = int.from_bytes(base64.b64decode(cc['Exponent']['$']), byteorder='big')
    d = int.from_bytes(base64.b64decode(cc['D']['$']), byteorder='big')
    p = int.from_bytes(base64.b64decode(cc['P']['$']), byteorder='big')
    q = int.from_bytes(base64.b64decode(cc['Q']['$']), byteorder='big')
    return RSA.construct((n, e, d, p, q))


def sign(data: str, private_key: str):
    rsa_key = get_rsa_key(private_key)
    h = SHA256.new(data.encode('utf-8'))
    return pkcs1_15.new(rsa_key).sign(h).hex()
