Hash Tool: Генерация и Восстановление Хешей

Описание:
Данная программа объединяет две основные функции:
1. Генерация хешей:
   - Хеширует пароли из списка.
   - Добавляет случайные хеши, если список паролей меньше заданного количества.
2. Восстановление паролей:
   - Находит пароли из списка хешей с использованием словаря.

Использование:

1. Генерация хешей
   Команда:
   python hash_tool.py generate <password_file> <encoding> <hash_function> <total_hashes> <output_file>

   Аргументы:
   - <password_file>: Файл со списком паролей (по одному паролю на строку).
   - <encoding>: Кодировка файла (UTF-8 или UTF-16-LE).
   - <hash_function>: Хеш-функция (MD4, MD5, SHA1, SHA256, SHA512).
   - <total_hashes>: Общее количество хешей в выходном файле.
   - <output_file>: Имя выходного файла для хешей.

   Пример:
   python hash_tool.py generate passwords.txt UTF-8 SHA256 10 hashes.txt

2. Восстановление паролей
   Команда:
   python hash_tool.py crack <wordlist> <encoding> <hash_function> <hashlist>

   Аргументы:
   - <wordlist>: Файл со словарем паролей (по одному паролю на строку).
   - <encoding>: Кодировка файла (UTF-8 или UTF-16-LE).
   - <hash_function>: Хеш-функция (MD4, MD5, SHA1, SHA256, SHA512).
   - <hashlist>: Файл с хешами.

   Пример:
   python hash_tool.py crack wordlist.txt UTF-8 SHA256 hashes.txt

Примечания:
- Для работы с MD4 требуется библиотека passlib. Установите её:
  pip install passlib
- Поддерживаются кодировки UTF-8 и UTF-16-LE.
- Восстановление паролей использует многопоточность для ускорения работы.

Пример тестирования:
1. Создайте файл passwords.txt:
   password123
   qwerty
   123456

2. Сгенерируйте хеши:
   python hash_tool.py generate passwords.txt UTF-8 SHA256 10 hashes.txt

3. Создайте словарь wordlist.txt:
   password123
   123456
   admin

4. Проверьте хеши:
   python hash_tool.py crack wordlist.txt UTF-8 SHA256 hashes.txt
