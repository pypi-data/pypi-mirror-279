# coding=utf-8
from __future__ import absolute_import, division, print_function
import binascii

# 尝试导入Python 3中的库，如果失败，则回退到Python 2的等效库
import sys

try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding
except ImportError:
    # Python 2的兼容代码，或其他回退代码
    # 注意：cryptography库在Python 2和Python 3中的用法相同，所以这里主要是演示结构
    pass


# 兼容Python 2和3的编码函数
def to_bytes(data, encoding='utf-8'):
    """确保s是字节类型"""
    if sys.version_info[0] < 3:
        # Python 2.x，s已经是字节串
        return data
    else:
        # Python 3.x，确保是bytes
        return data.encode(encoding) if isinstance(data, str) else data


def to_string(data, encoding='utf-8'):
    """
    将数据转换为字符串。

    Args:
        data: 要转换的数据。
        encoding: 字符串编码。

    Returns:
        str: 转换后的字符串。
    """
    if isinstance(data, bytes):
        return data.decode(encoding)
    elif isinstance(data, str):
        return data
    else:
        return str(data)


# 兼容Python 2和3的十六进制解码函数
def from_hex(s):
    try:
        return bytes.fromhex(s)  # Python 3
    except AttributeError:
        return s.decode('hex')  # Python 2


# 兼容Python 2和3的十六进制编码函数
def to_hex(data):
    try:
        return data.hex()  # Python 3
    except AttributeError:
        return binascii.hexlify(data)  # Python 2


def rsa_load_pem_private_key(pri_key):
    private_key = serialization.load_pem_private_key(
        pri_key,
        password=None,
        backend=default_backend()
    )
    return private_key


def rsa_load_pem_public_key(pub_key):
    public_key = serialization.load_pem_public_key(
        pub_key,
        backend=default_backend()
    )
    return public_key


def rsa_public_encrypt(msg, public_key):
    decoded_msg = to_bytes(msg)

    encrypted_msg = public_key.encrypt(
        decoded_msg,
        padding.PKCS1v15()
    )

    return to_hex(encrypted_msg)


def rsa_private_decrypt(encrypted_msg_hex, private_key):
    encrypted_msg = from_hex(encrypted_msg_hex)

    decrypted_msg = private_key.decrypt(
        encrypted_msg,
        padding.PKCS1v15()
    )

    return decrypted_msg


def rsa_sign(message, private_key):
    signature = private_key.sign(
        to_bytes(message),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return to_hex(signature)


def rsa_verify(sign, message, public_key):
    try:
        decoded_sign = from_hex(sign)
    except Exception as e:
        raise ValueError("签名解码失败: {}".format(e))

    public_key.verify(
        decoded_sign,
        to_bytes(message),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
