import hashlib
import sys
import multiprocessing
from time import time

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

def crack_hash(password, hash_func, hash_list):
    """Проверка пароля против списка хешей."""
    password_hash = hash_password(password, hash_func)
    return f"{password}:{password_hash}" if password_hash in hash_list else None

def read_hashes(file_path, encoding='utf-8'):
    """Чтение списка хешей из файла."""
    with open(file_path, 'r', encoding=encoding) as f:
        return set(f.read().splitlines())

def read_wordlist(file_path, encoding='utf-8'):
    """Чтение словаря паролей из файла."""
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read().splitlines()

def process_chunk(chunk, hash_func, hash_list, results):
    """Обработка части словаря паролей."""
    for password in chunk:
        result = crack_hash(password, hash_func, hash_list)
        if result:
            results.append(result)

def main():
    if len(sys.argv) != 5:
        print("Usage: python password_cracker.py <wordlist> <encoding> <hash_function> <hashlist>")
        sys.exit(1)

    wordlist_file = sys.argv[1]
    encoding = sys.argv[2]
    hash_func = sys.argv[3].upper()
    hashlist_file = sys.argv[4]

    if hash_func not in ["MD4", "MD5", "SHA1", "SHA256", "SHA512"]:
        print(f"Error: Unsupported hash function '{hash_func}'. Supported functions are: MD4, MD5, SHA1, SHA256, SHA512.")
        sys.exit(1)
    if encoding not in ["UTF-8", "UTF-16-LE"]:
        print(f"Error: Unsupported encoding '{encoding}'. Supported encodings are: UTF-8, UTF-16-LE.")
        sys.exit(1)

    # Чтение хешей из файла
    print("Reading hashes...")
    start_time = time()
    hash_list = read_hashes(hashlist_file, encoding)
    print(f"Loaded {len(hash_list)} hashes in {time() - start_time:.4f} seconds.")

    # Чтение словаря паролей из файла
    print("Reading wordlist...")
    start_time = time()
    wordlist = read_wordlist(wordlist_file, encoding)
    print(f"Loaded {len(wordlist)} passwords in {time() - start_time:.4f} seconds.")

    # Разделяем словарь на части для многопоточной обработки
    num_processes = multiprocessing.cpu_count()
    chunk_size = max(1, len(wordlist) // num_processes)
    chunks = [list(wordlist)[i:i + chunk_size] for i in range(0, len(wordlist), chunk_size)]

    # Обработка в нескольких процессах
    manager = multiprocessing.Manager()
    results = manager.list()
    processes = []

    print("Cracking hashes...")
    start_time = time()
    for chunk in chunks:
        process = multiprocessing.Process(target=process_chunk, args=(chunk, hash_func, hash_list, results))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Hash cracking completed in {time() - start_time:.4f} seconds.")

    # Вывод результатов
    if results:
        print("\nMatching results:")
        for result in results:
            print(result)
    else:
        print("No matching hashes found.")

if __name__ == "__main__":
    main()
