import math
import matplotlib.pyplot as plt

# Исходные данные
n = 27
k = 4               # заявок/мес от одного источника
t = 2.2             # дней
P_percent = 80      # требуемый процент исправных источников

# Константы
days_in_month = 30
lambda_ = k / days_in_month      # заявок/день от одного источника
mu = 1 / t                       # заявок/день
rho = lambda_ / mu

print("[Параметры системы]")
print(f"n = {n}")
print(f"λ = {lambda_:.6f} заявок/день")
print(f"μ = {mu:.6f} заявок/день")
print(f"ρ = λ/μ = {rho:.6f}")
print()

# Вычисление вероятностей P_i по формуле Энгсета
# Для i = 0..n: числитель = n!/(n-i)! * ρ^i, знаменатель - сумма всех числителей
# Используем рекуррентное соотношение для устойчивости:
# P_0 = 1 / S, где S = sum_{i=0}^n C_i, C_i = C_{i-1} * ρ * (n - i + 1)/i, C_0 = 1

C = [0.0] * (n+1)
C[0] = 1.0
for i in range(1, n+1):
    C[i] = C[i-1] * rho * (n - i + 1) / i

S = sum(C)
P = [c / S for c in C]

print("[Вероятности состояний (первые 10)]")
for i in range(min(10, n+1)):
    print(f"P({i:2d}) = {P[i]:.8f}")
print("...")
print()

# 1. Вероятность, что исправны не менее 80% (т.е. не более 5 заявок)
i_max = n - int(math.ceil(P_percent / 100.0 * n))   # i_max = n - ceil(0.8*n) = 27-22=5
prob_active_ge_80 = sum(P[:i_max+1])
print(f"[Пункт 1]")
print(f"Число источников, исправных не менее {P_percent}%: >= {int(math.ceil(P_percent/100*n))}")
print(f"Для этого число заявок в системе должно быть <= {i_max}")
print(f"Искомая вероятность: {prob_active_ge_80:.8f}  ({prob_active_ge_80:.2%})")
print()

# 2. Дополнительные характеристики
# Среднее число заявок в системе (неисправных источников)
L = sum(i * P[i] for i in range(n+1))
# Абсолютная пропускная способность
A = mu * (1 - P[0])
# Эффективная интенсивность поступления (должна совпадать с A)
lambda_eff = lambda_ * (n - L)
# Среднее время пребывания
W = L / A if A > 0 else float('inf')
# Среднее время ожидания
Wq = W - 1/mu if mu > 0 else float('inf')

print("[Пункт 2]")
print(f"Среднее число неисправных источников (в ремонте и очереди): L = {L:.6f}")
print(f"Абсолютная пропускная способность: A = {A:.6f} заявок/день")
print(f"Среднее время ремонта и ожидания ремонта (время в системе): W = {W:.4f} дней")
print(f"Среднее время ожидания в очереди: W_q = {Wq:.4f} дней")
print()

# Проверка: среднее число активных источников
active_mean = n - L
print(f"Среднее число активных источников: {active_mean:.2f} (из {n})")
print(f"Эффективная интенсивность поступления: λ_eff = {lambda_eff:.6f} заявок/день (совпадает с A: {abs(lambda_eff-A)<1e-6})")

# Построим график распределения вероятностей
plt.figure(figsize=(10,6))
plt.bar(range(n+1), P, width=0.8, color='skyblue', edgecolor='black')
plt.axvline(x=i_max+0.5, color='red', linestyle='--', label=f'Порог i ≤ {i_max}')
plt.xlabel('Число заявок в системе (i)')
plt.ylabel('Вероятность P(i)')
plt.title('Распределение вероятностей состояний замкнутой СМО (n=27)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()