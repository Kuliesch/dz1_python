import numpy as np

# 1. Створення одновимірного масиву з 200 випадкових чисел від -100 до 100
np.random.seed(42)  # для відтворюваності
arr = np.random.randint(-100, 101, size=200)
print("1. Вихідний масив (перші 20 елементів):\n", arr[:20], "...")

# 2. Фільтрація додатних чисел за допомогою маски
mask_positive = arr > 0
positive_numbers = arr[mask_positive]
print("\n2. Кількість додатних чисел у масиві:", len(positive_numbers))
print("   Приклад відфільтрованих додатних чисел (перші 10):", positive_numbers[:10])

# 3. Заміна всіх від'ємних значень на нулі
arr_modified = arr.copy()  # копія, щоб не змінювати оригінал
arr_modified[arr_modified < 0] = 0
print("\n3. Масив після заміни від'ємних на нулі (перші 20 елементів):\n", arr_modified[:20], "...")

# 4. Обчислення середнього значення отриманого масиву
mean_value = np.mean(arr_modified)
print("\n4. Середнє значення модифікованого масиву:", mean_value)

# Додатково: перевірка кількості нулів для контролю
zeros_count = np.sum(arr_modified == 0)
print(f"   (У масиві замінено на нулі {zeros_count} від'ємних чисел)")