def fib(n: int):
    """
    Генератор чисел Фибоначчи по индексам 0..n включительно.
    Аргументы:
        n (int): индекс, на котором следует остановиться (неотрицательное целое).
    Пример:
        list(fib(5)) -> [0, 1, 1, 2, 3, 5]
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")

    a, b = 0, 1
    for _ in range(n + 1):
        yield a
        a, b = b, a + b


if __name__ == "__main__":
    # пример использования
    print(list(fib(10)))