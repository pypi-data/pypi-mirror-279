import random
import sympy


def generate_keypair(bits):
    # Генерация двух простых чисел p и q
    p = sympy.randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2))
    q = sympy.randprime(2 ** (bits // 2 - 1), 2 ** (bits // 2))

    # Вычисление модуля n и функции Эйлера phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Выбор открытого экспонента e (обычно выбирают e = 65537)
    e = 65537

    # Проверка на взаимно простые числа e и phi(n)
    while sympy.gcd(e, phi_n) != 1:
        e = random.randrange(2, phi_n)

    # Вычисление закрытого экспонента d (мультипликативно обратное к e по модулю phi(n))
    d = sympy.mod_inverse(e, phi_n)

    # Возвращение открытого ключа (e, n) и закрытого ключа (d, n)
    return ((e, n), (d, n))


def encrypt(message, public_key):
    e, n = public_key
    # Преобразование сообщения в число m
    m = int.from_bytes(message.encode(), 'big')
    # Шифрование: c = m^e % n
    c = pow(m, e, n)
    return c


def decrypt(ciphertext, private_key):
    d, n = private_key
    # Расшифрование: m = c^d % n
    m = pow(ciphertext, d, n)
    # Преобразование числа m обратно в строку
    message = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
    return message


# Пример использования:
def rsa_encrypt(message):
# Генерация ключей
    public_key, private_key = generate_keypair(bits=1024)

# Шифрование сообщения

    encrypted_message = encrypt(message, public_key)
    print("Зашифрованное сообщение:", encrypted_message)

# Дешифрование сообщения
    decrypted_message = decrypt(encrypted_message, private_key)
    print("Расшифрованное сообщение:", decrypted_message)
