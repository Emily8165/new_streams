import hashlib
import sys


def password(p: str) -> str:
    result = hashlib.md5(str.encode(p)).hexdigest()
    return result


if __name__ == "__main__":
    password(sys.argv[1])
