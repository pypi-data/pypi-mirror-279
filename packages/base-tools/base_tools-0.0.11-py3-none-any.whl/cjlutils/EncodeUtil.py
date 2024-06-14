import hashlib
import hmac


def encode_hmac_sha256(secret_key: bytes, message: bytes) -> None | bytes:
    if secret_key is None or message is None:
        return None
    return hmac.new(secret_key, message, hashlib.sha256).digest()


if __name__ == '__main__':
    pass
