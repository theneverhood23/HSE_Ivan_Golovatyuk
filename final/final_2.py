import sys

# final_2.py
# GitHub Copilot

def roman_to_int(s: str) -> int:
    """
    Конвертирует римское число в целое.
    Поддерживает стандартные вычитания: IV, IX, XL, XC, CD, CM.
    """
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    s = s.strip().upper()
    total = 0
    n = len(s)
    for i in range(n):
        v = vals.get(s[i], 0)
        if i + 1 < n and v < vals.get(s[i + 1], 0):
            total -= v
        else:
            total += v
    return total

if __name__ == "__main__":
    # Читает одну строку с римским числом и печатает результат.
    # Примеры ввода: III  или  "MCMXCIV"
    if sys.stdin.isatty():
        s = input().strip()
    else:
        s = sys.stdin.read().strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    if s:
        print(roman_to_int(s))
    test_inputs = ["III", "IV", "MCMXCIV", "XLIX"]
    for test in test_inputs:
        print(f"Ввод: {test} → Результат: {roman_to_int(test)}")