"""
Модуль для порівняння ефективності алгоритмів пошуку підрядка.

Цей модуль містить реалізації трьох алгоритмів пошуку підрядка:
Кнута-Морріса-Пратта, Боєра-Мура та Рабіна-Карпа. Він також включає
функції для вимірювання часу виконання цих алгоритмів та порівняння
їх ефективності на різних текстах.
"""


import timeit
from tabulate import tabulate


def read_file(filename):
    """
    Читає вміст файлу.

    Args:
        filename (str): Ім'я файлу для читання.

    Returns:
        str: Вміст файлу.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def measure_time(func, text, pattern):
    """
    Вимірює час виконання функції пошуку.

    Args:
        func (callable): Функція пошуку підрядка.
        text (str): Текст, в якому здійснюється пошук.
        pattern (str): Підрядок для пошуку.

    Returns:
        float: Час виконання функції (у секундах).
    """
    return timeit.timeit(lambda: func(text, pattern), number=100)


def compute_lps(pattern):
    """
    Обчислює масив найдовших префікс-суфіксів для алгоритму КМП.

    Args:
        pattern (str): Шаблон для пошуку.

    Returns:
        list: Масив LPS.
    """
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def kmp_search(main_string, pattern):
    """
    Виконує пошук підрядка за алгоритмом Кнута-Морріса-Пратта.

    Args:
        main_string (str): Текст, в якому здійснюється пошук.
        pattern (str): Підрядок для пошуку.

    Returns:
        int: Індекс першого входження підрядка або -1, якщо підрядок не знайдено.
    """
    M, N = len(pattern), len(main_string)
    lps = compute_lps(pattern)
    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
            if j == M:
                return i - j
        elif j:
            j = lps[j - 1]
        else:
            i += 1

    return -1


def build_shift_table(pattern):
    """
    Створює таблицю зсувів для алгоритму Боєра-Мура.

    Args:
        pattern (str): Шаблон для пошуку.

    Returns:
        dict: Таблиця зсувів.
    """
    table = {}
    length = len(pattern)
    for i, char in enumerate(pattern[:-1]):
        table[char] = length - i - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    """
    Виконує пошук підрядка за алгоритмом Боєра-Мура.

    Args:
        text (str): Текст, в якому здійснюється пошук.
        pattern (str): Підрядок для пошуку.

    Returns:
        int: Індекс першого входження підрядка або -1, якщо підрядок не знайдено.
    """
    shift_table = build_shift_table(pattern)
    i = 0
    pattern_length = len(pattern)
    text_length = len(text)

    while i <= text_length - pattern_length:
        j = pattern_length - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + pattern_length - 1], pattern_length)

    return -1


def polynomial_hash(s, base=256, modulus=101):
    """
    Обчислює поліноміальний хеш рядка.

    Args:
        s (str): Рядок для хешування.
        base (int): Основа для обчислення хешу.
        modulus (int): Модуль для обчислення хешу.

    Returns:
        int: Хеш-значення рядка.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    """
    Виконує пошук підрядка за алгоритмом Рабіна-Карпа.

    Args:
        main_string (str): Текст, в якому здійснюється пошук.
        substring (str): Підрядок для пошуку.

    Returns:
        int: Індекс першого входження підрядка або -1, якщо підрядок не знайдено.
    """
    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    h_multiplier = pow(base, substring_length - 1, modulus)

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus

    return -1


def compare_algorithms(text1, text2, existing_pattern, non_existing_pattern):
    """
    Порівнює ефективність алгоритмів пошуку підрядка.

    Args:
        text1 (str): Перший текст для пошуку.
        text2 (str): Другий текст для пошуку.
        existing_pattern (str): Підрядок, який існує в текстах.
        non_existing_pattern (str): Підрядок, якого немає в текстах.

    Returns:
        list: Результати порівняння алгоритмів.
    """
    algorithms = [
        ("Кнута-Морріса-Пратта", kmp_search),
        ("Боєра-Мура", boyer_moore_search),
        ("Рабіна-Карпа", rabin_karp_search)
    ]

    results = []
    for name, func in algorithms:
        times = [measure_time(func, text, pattern) for text in (text1, text2) for pattern in (existing_pattern, non_existing_pattern)]
        avg_time = sum(times) / len(times)
        results.append([name] + [f"{t:.6f}" for t in times] + [f"{avg_time:.6f}"])

    return results


if __name__ == "__main__":
    # Читаємо тексти з файлів
    text1 = read_file("article 1.txt")
    text2 = read_file("article 2.txt")

    # Вибираємо підрядки для пошуку
    existing_pattern = "елемент"
    non_existing_pattern = "підрядокутекстінеіснує"

    # Порівнюємо алгоритми
    results = compare_algorithms(text1, text2, existing_pattern, non_existing_pattern)

    # Виводимо результати у вигляді таблиці
    headers = ["Алгоритм", "Текст 1 (існує)", "Текст 1 (не існує)", "Текст 2 (існує)", "Текст 2 (не існує)", "Середній час"]
    print(tabulate(results, headers=headers, tablefmt="fancy_grid"))

    # Визначаємо найшвидший алгоритм
    fastest = min(results, key=lambda x: float(x[-1]))
    print(f"\nНайшвидший алгоритм: {fastest[0]}")
