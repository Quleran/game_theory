import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

np.random.seed(42)
n, m = 12, 12
A = np.random.randint(-100, 101, size=(n, m))

# Вывод матрицы без переносов
print("Матрица платежей A ({}x{}):".format(n, m))
for i in range(n):
    row_str = ""
    for j in range(m):
        row_str += "{:4d} ".format(A[i, j])
    print(row_str)

# 1. Метод Брауна-Робинсона (фиктивное разыгрывание)
iterations = 5000
p1_strategy_counts = np.zeros(n)  # Счетчик выбора строк игроком 1
p2_strategy_counts = np.zeros(m)  # Счетчик выбора столбцов игроком 2
p1_sums = np.zeros(n)  # Накопленные выигрыши для каждой строки
p2_sums = np.zeros(m)  # Накопленные выигрыши для каждого столбца
lower_bounds = []  # Нижняя цена игры
upper_bounds = []  # Верхняя цена игры

row = np.random.randint(n)  # Начальная стратегия игрока 1
col = np.random.randint(m)  # Начальная стратегия игрока 2

for t in range(1, iterations + 1):
    # Обновление счетчиков выбранных стратегий
    p1_strategy_counts[row] += 1
    p2_strategy_counts[col] += 1

    # Накопление выигрышей
    p1_sums += A[:, col]  # Игрок 1 получает выигрыш за выбранный столбец
    p2_sums += A[row, :]  # Игрок 2 получает выигрыш за выбранную строку

    # Вычисление текущих оценок цены игры
    lower_bound = np.max(p1_sums) / t  # Нижняя цена (максимин)
    upper_bound = np.min(p2_sums) / t  # Верхняя цена (минимакс)
    lower_bounds.append(lower_bound)
    upper_bounds.append(upper_bound)

    # Выбор следующих стратегий (наилучший ответ)
    row = np.argmax(p1_sums)  # Игрок 1 выбирает строку с макс. накопленным выигрышем
    col = np.argmin(p2_sums)  # Игрок 2 выбирает столбец с мин. накопленным выигрышем

# Эмпирические смешанные стратегии
p1_fp = p1_strategy_counts / iterations
p2_fp = p2_strategy_counts / iterations
val_fp = (lower_bounds[-1] + upper_bounds[-1]) / 2.0

# 2. Решение через линейное программирование
c_shift = A.min() - 1
if c_shift <= 0:
    A_pos = A - c_shift
else:
    A_pos = A
    c_shift = 0

# Задача для игрока 1 (максимин)
c_p1 = np.ones(n)
A_ub_p1 = -A_pos.T
b_ub_p1 = -np.ones(m)
res_p1 = linprog(c=c_p1, A_ub=A_ub_p1, b_ub=b_ub_p1, bounds=(0, None))
v_p1 = 1 / res_p1.fun
p1_lp = res_p1.x * v_p1

# Задача для игрока 2 (минимакс)
c_p2 = -np.ones(m)
res_p2 = linprog(c=c_p2, A_ub=A_pos, b_ub=np.ones(n), bounds=(0, None))
v_p2 = 1 / (-res_p2.fun)
p2_lp = res_p2.x * v_p2
val_lp = v_p1 + c_shift

# Вывод результатов
print("\n" + "=" * 60)
print("РЕЗУЛЬТАТЫ МЕТОДА БРАУНА-РОБИНСОНА ({} итераций):".format(iterations))
print("=" * 60)
print("Смешанная стратегия игрока 1 (вероятности строк):")
# Вывод стратегии игрока 1 в одну строку
print( "".join([f"{prob:.4f}, " for prob in p1_lp]))
print("\nСмешанная стратегия игрока 2 (вероятности столбцов):")
print( "".join([f"{prob:.4f}, " for prob in p2_lp]))
print("\nНижняя цена игры на последней итерации: {:.6f}".format(lower_bounds[-1]))
print("Верхняя цена игры на последней итерации: {:.6f}".format(upper_bounds[-1]))
print("Приближенная цена игры: {:.6f}".format(val_fp))

print("\n" + "=" * 60)
print("РЕЗУЛЬТАТЫ ЛИНЕЙНОГО ПРОГРАММИРОВАНИЯ:")
print("=" * 60)
print("Оптимальная стратегия игрока 1:")
print( "".join([f"{prob:.4f}, " for prob in p1_lp]))
print("\nОптимальная стратегия игрока 2:")
print( "".join([f"{prob:.4f}, " for prob in p2_lp]))
print("Точная цена игры: {:.6f}".format(val_lp))

print("\n" + "=" * 60)
print("СРАВНЕНИЕ:")
print("=" * 60)
print("Разница в цене игры: {:.6f}".format(abs(val_fp - val_lp)))
print("Относительная погрешность: {:.4f}%".format(abs(val_fp - val_lp) / abs(val_lp) * 100))

# Построение графика сходимости
plt.figure(figsize=(12, 7))
plt.plot(lower_bounds, label="Нижняя цена", color='orange', alpha=0.7, linewidth=1)
plt.plot(upper_bounds, label="Верхняя цена", color='purple', alpha=0.7, linewidth=1)
plt.axhline(val_lp, color='darkgreen', linestyle='--', linewidth=2, label="Точная цена")
plt.fill_between(range(len(lower_bounds)), lower_bounds, upper_bounds, alpha=0.2, color='gray')
plt.title("Сходимость метода Брауна-Робинсона (Fictitious Play)", fontsize=14)
plt.xlabel("Номер итерации", fontsize=12)
plt.ylabel("Оценка цены игры", fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\nГрафик сходимости отображен на экране")