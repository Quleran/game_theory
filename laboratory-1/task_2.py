import numpy as np
from scipy.optimize import linprog

# ==================== ПАРАМЕТРЫ СЕТИ ====================
N = 5

# Ценности узлов (ущерб при успешной атаке)
V = np.array([100, 80, 60, 50, 30])

# Стоимость защиты узла
C = np.array([40, 30, 20, 25, 15])

# Вероятность успеха атаки при защите
P_succ_def = np.array([0.1, 0.15, 0.05, 0.2, 0.1])

# Вероятность успеха атаки без защиты
P_succ_nodef = np.array([0.8, 0.9, 0.95, 0.7, 0.6])

# Бюджет защитника
B = 60

# ==================== ФОРМИРОВАНИЕ ЗАДАЧИ ЛИНЕЙНОГО ПРОГРАММИРОВАНИЯ ====================
# Переменные: [t, x1, x2, x3, x4, x5]
# где t - максимальный ожидаемый ущерб
# x_i - вероятность защиты узла i

# Целевая функция: минимизировать t
c = np.zeros(N + 1)
c[0] = 1  # коэффициент при t

# Ограничения: для каждого узла i
# V[i] * (P_def[i] * x_i + P_nodef[i] * (1-x_i)) <= t
# Преобразуем: V[i]*(P_def[i]-P_nodef[i])*x_i - t <= -V[i]*P_nodef[i]

A_ub = np.zeros((N, N + 1))
b_ub = np.zeros(N)

for i in range(N):
    A_ub[i, 0] = -1  # коэффициент при t
    A_ub[i, i + 1] = V[i] * (P_succ_def[i] - P_succ_nodef[i])
    b_ub[i] = -V[i] * P_succ_nodef[i]

# Бюджетное ограничение: sum(C_i * x_i) <= B
A_budget = np.zeros(N + 1)
for i in range(N):
    A_budget[i + 1] = C[i]

A_ub = np.vstack((A_ub, A_budget))
b_ub = np.append(b_ub, B)

# Границы переменных: t >= 0, 0 <= x_i <= 1
bounds = [(0, None)] + [(0, 1) for _ in range(N)]

# ==================== РЕШЕНИЕ ЗАДАЧИ ОПТИМИЗАЦИИ ====================
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

# ==================== ВЫВОД РЕЗУЛЬТАТОВ ====================
print("=" * 70)
print("МОДЕЛИРОВАНИЕ АТАКИ НА СЕТЬ КАК ИГРА ШТАКЕЛЬБЕРГА")
print("=" * 70)

if not res.success:
    print(f"Ошибка оптимизации: {res.message}")
else:
    t_opt = res.x[0]
    x_opt = res.x[1:]

    print("\n[1] ПАРАМЕТРЫ СЕТИ:")
    print("-" * 70)
    print(f"{'Узел':<6} {'Ценность V':<12} {'Стоимость C':<12} {'P(успех|защита)':<18} {'P(успех|без защиты)':<20}")
    print("-" * 70)
    for i in range(N):
        print(f"{i:<6} {V[i]:<12} {C[i]:<12} {P_succ_def[i]:<18} {P_succ_nodef[i]:<20}")

    print(f"\n[2] БЮДЖЕТ ЗАЩИТНИКА: {B}")
    print(f"    Суммарная стоимость защиты всех узлов: {sum(C)}")
    print(f"    Доступно для защиты: {B / sum(C) * 100:.1f}% узлов (при полной защите)")

    print("\n[3] ОПТИМАЛЬНАЯ СТРАТЕГИЯ ЗАЩИТНИКА (равновесие Штакельберга):")
    print("-" * 70)
    print(f"{'Узел':<6} {'Вероятность защиты':<20} {'Ожидаемые затраты':<20} {'Статус':<15}")
    print("-" * 70)

    total_cost = 0
    for i in range(N):
        cost = C[i] * x_opt[i]
        total_cost += cost
        if x_opt[i] > 0.99:
            status = "Защищен"
        elif x_opt[i] > 0.01:
            status = "Частично"
        else:
            status = "Не защищен"
        print(f"{i:<6} {x_opt[i]:<20.4f} {cost:<20.2f} {status:<15}")

    print("-" * 70)
    print(f"{'ИТОГО:':<6} {'':<20} {total_cost:<20.2f} (бюджет: {B})")

    # Анализ действий атакующего
    print("\n[4] АНАЛИЗ ДЕЙСТВИЙ АТАКУЮЩЕГО:")
    print("-" * 70)

    # Ожидаемый ущерб при атаке на узел i
    expected_damage = V * (x_opt * P_succ_def + (1 - x_opt) * P_succ_nodef)

    print(f"{'Узел':<6} {'P(защиты)':<12} {'Ожидаемый ущерб':<18} {'Цель атаки':<15}")
    print("-" * 70)

    target_node = np.argmax(expected_damage)
    for i in range(N):
        is_target = "← ЦЕЛЬ" if i == target_node else ""
        print(f"{i:<6} {x_opt[i]:<12.4f} {expected_damage[i]:<18.2f} {is_target:<15}")

    print("\n[5] РЕЗУЛЬТАТ ИГРЫ ШТАКЕЛЬБЕРГА:")
    print("-" * 70)
    print(f"• Оптимальный ожидаемый ущерб (минимакс): {t_opt:.2f}")
    print(f"• Атакующий выберет: УЗЕЛ {target_node}")
    print(f"  - Ценность узла: {V[target_node]}")
    print(f"  - Вероятность защиты: {x_opt[target_node]:.3f}")
    print(f"  - Ожидаемый ущерб: {expected_damage[target_node]:.2f}")
    prob_success = x_opt[target_node] * P_succ_def[target_node] + (1 - x_opt[target_node]) * P_succ_nodef[target_node]
    print(f"  - Вероятность успеха атаки: {prob_success:.3f}")

    print("\n[6] ИНТЕРПРЕТАЦИЯ РАВНОВЕСИЯ:")
    print("-" * 70)
    print("Защитник (Лидер) выбрал вероятности защиты, чтобы минимизировать")
    print("максимальный ожидаемый ущерб, учитывая, что Атакующий (Последователь)")
    print("после наблюдения стратегии защиты выберет наиболее уязвимый узел.")
    print("\nЭто классическое равновесие Штакельберга в игре с")
    print("двухуровневой оптимизацией (bilevel optimization).")
    print("=" * 70)