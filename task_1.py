"""
Модуль реалізації хеш-таблиці
"""


class HashTable:
    """
    Реалізація хеш-таблиці.
    """

    def __init__(self, size):
        """
        Ініціалізує хеш-таблицю.

        Args:
            size (int): Розмір хеш-таблиці.
        """
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        """
        Обчислює хеш для заданого ключа.

        Args:
            key: Ключ для хешування.

        Returns:
            int: Хеш-значення ключа.
        """
        return hash(key) % self.size

    def insert(self, key, value):
        """
        Вставляє пару ключ-значення в хеш-таблицю.

        Args:
            key: Ключ для вставки.
            value: Значення для вставки.

        Returns:
            bool: True, якщо вставка успішна.
        """
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if not self.table[key_hash]:
            self.table[key_hash] = [key_value]
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
        return True

    def get(self, key):
        """
        Отримує значення за ключем з хеш-таблиці.

        Args:
            key: Ключ для пошуку.

        Returns:
            Значення, пов'язане з ключем, або None, якщо ключ не знайдено.
        """
        key_hash = self.hash_function(key)
        if self.table[key_hash]:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        """
        Видаляє пару ключ-значення з хеш-таблиці.

        Args:
            key: Ключ для видалення.

        Returns:
            bool: True, якщо видалення успішне, False, якщо ключ не знайдено.
        """
        key_hash = self.hash_function(key)
        if self.table[key_hash]:
            for i, pair in enumerate(self.table[key_hash]):
                if pair[0] == key:
                    self.table[key_hash].pop(i)
                    return True
        return False

# Тестування хеш-таблиці
def test_hash_table():
    """
    Функція для демонстрації та тестування 
    функціональності хеш-таблиці
    """
    print("Тестування хеш-таблиці:")
    ht = HashTable(5)

    # Тест вставки та отримання значення
    print("\nТест 1: Вставка та отримання значення")
    ht.insert("apple", 10)
    ht.insert("orange", 20)
    ht.insert("banana", 30)
    print(f"apple: {ht.get('apple')}")  # Очікується: 10
    print(f"orange: {ht.get('orange')}")  # Очікується: 20
    print(f"banana: {ht.get('banana')}")  # Очікується: 30

    # Тест оновлення значення
    print("\nТест 2: Оновлення значення")
    ht.insert("apple", 40)
    print(f"apple після оновлення: {ht.get('apple')}")  # Очікується: 40

    # Тест видалення
    print("\nТест 3: Видалення")
    ht.delete("orange")
    print(f"orange після видалення: {ht.get('orange')}")  # Очікується: None

    # Тест неіснуючого ключа
    print("\nТест 4: Неіснуючий ключ")
    print(f"grape: {ht.get('grape')}")  # Очікується: None


if __name__ == "__main__":
    test_hash_table()
