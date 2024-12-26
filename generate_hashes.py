import hashlib
import random
import string
import sys

SIZE_OF_HASH = 512

def hash_password(password, hash_func):
    """Генерация хеша для заданного пароля и хеш-функции."""
    if hash_func == "MD4":
        try:
            from passlib.hash import nthash
            return nthash.hash(password)
        except ImportError:
            raise ImportError("MD4 requires the passlib library. Install it using 'pip install passlib'.")
    hash_func = getattr(hashlib, hash_func.lower())
    return hash_func(password.encode()).hexdigest()

def generate_random_string(length: int) -> str:
    """Генерация случайной строки из букв, цифр и специальных символов."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_hash(hash_func):
    """Генерация случайного хеша для случайной строки."""
    random_data = generate_random_string(SIZE_OF_HASH)
    return hash_password(random_data, hash_func)

def generate_hashes(password_file, encoding, hash_func, total_hashes, output_file):
    """Генерация хешей для заданного списка паролей."""
    with open(password_file, "r", encoding=encoding) as f:
        passwords = f.read().splitlines()

    hashes = [hash_password(password, hash_func) for password in passwords[:total_hashes]]

    while len(hashes) < total_hashes:
        hashes.append(generate_random_hash(hash_func))

    with open(output_file, "w", encoding=encoding) as f:
        f.write("\n".join(hashes))

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python generate_hashes.py <password_file> <encoding> <hash_function> <total_hashes> <output_file>")
        sys.exit(1)

    password_file = sys.argv[1]
    encoding = sys.argv[2]
    hash_func = sys.argv[3].upper()
    total_hashes = int(sys.argv[4])
    output_file = sys.argv[5]

    if hash_func not in ["MD4", "MD5", "SHA1", "SHA256", "SHA512"]:
        print(f"Error: Unsupported hash function '{hash_func}'. Supported functions are: MD4, MD5, SHA1, SHA256, SHA512.")
        sys.exit(1)
    if encoding not in ["UTF-8", "UTF-16-LE"]:
        print(f"Error: Unsupported encoding '{encoding}'. Supported encodings are: UTF-8, UTF-16-LE.")
        sys.exit(1)
    try:
        generate_hashes(password_file, encoding, hash_func, total_hashes, output_file)
        print(f"Hashes successfully generated and saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
