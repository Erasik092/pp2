import re

# Читаем файл
with open('receipt.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- РЕЗУЛЬТАТЫ ОБРАБОТКИ ЧЕКА ---")

# 1. Все цены (шаблон ищет числа с запятой)
prices = re.findall(r'\d[\d\s]*,\d{2}', text)
print(f"1. Все цены: {prices}")

# 2. Названия товаров (берем строку после цифры с точкой)
products = re.findall(r'\d+\.\n(.*?)\n', text)
print(f"2. Товары: {products}")

# 3. Итоговая сумма
total = re.search(r'ИТОГО:\s+([\d\s,]+)', text)
print(f"3. Итого: {total.group(1).strip() if total else 'Не найдено'}")

# 4. Дата и время
dt = re.search(r'(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', text)
print(f"4. Дата: {dt.group(1) if dt else '—'}, Время: {dt.group(2) if dt else '—'}")

# 5. Способ оплаты (ищем текст перед ИТОГО)
payment = re.search(r'([А-Яа-я\s]+):\s*\n[\d\s,]+\nИТОГО', text)
print(f"5. Оплата: {payment.group(1).strip() if payment else 'Не найдено'}")

# 6. Структурированный вид (простой вывод списка)
print("\n6. Чек в кратком виде:")
for i, name in enumerate(products, 1):
    print(f"   {i}. {name}")