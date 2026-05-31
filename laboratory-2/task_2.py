import math

# Исходные данные
lambda_day = 350  # заявок в сутки
t_min = 10  # минут на обслуживание
alpha = 7
n = 4

# Перевод в минуты
minutes_per_day = 24 * 60
lambda_min = lambda_day / minutes_per_day  # заявок/мин
mu = 1 / t_min  # заявок/мин
rho = lambda_min / mu  # приведённая нагрузка

print(f"λ (заявок/мин) = {lambda_min:.6f}")
print(f"μ (заявок/мин) = {mu}")
print(f"ρ = {rho:.6f}\n")


# Функция расчёта характеристик для заданного k
def smm_inf(k, lam, mu, rho):
    # Проверка стационарности
    if rho / k >= 1:
        raise ValueError(f"Нестационарный режим: ρ/k = {rho / k:.4f} >= 1")

    # Вычисление P0
    sum1 = sum(rho ** i / math.factorial(i) for i in range(k))
    term2 = (rho ** k / math.factorial(k)) * (1 / (1 - rho / k))
    P0 = 1 / (sum1 + term2)

    # Средняя длина очереди Lq
    Lq = (rho ** (k + 1) / (math.factorial(k) * k * (1 - rho / k) ** 2)) * P0

    # Среднее число заявок в системе Ls
    Ls = Lq + rho

    # Времена
    Wq = Lq / lam  # минут
    Ws = Wq + 1 / mu  # минут

    # (Опционально) массив вероятностей для i=0..k+n
    probs = []
    for i in range(k + n + 1):
        if i < k:
            Pi = (rho ** i / math.factorial(i)) * P0
        else:
            Pi = (rho ** i / (math.factorial(k) * k ** (i - k))) * P0
        probs.append(Pi)

    return P0, Lq, Ls, Wq, Ws, probs


# 1. Минимальное k
k_min = int(rho) + 1
print(f"k_min = {k_min}\n")
P0_min, Lq_min, Ls_min, Wq_min, Ws_min, probs_min = smm_inf(k_min, lambda_min, mu, rho)

print("[Характеристики при k_min]")
print(f"P0 = {P0_min:.6f}")
print(f"Lq = {Lq_min:.4f} заявок")
print(f"Ls = {Ls_min:.4f} заявок")
print(f"Wq = {Wq_min:.3f} мин")
print(f"Ws = {Ws_min:.3f} мин\n")

# 2. Оптимальное k по минимуму C(k) = k/λ + α*Wq
k_candidates = range(k_min, k_min + 15)
best_k = None
best_C = float('inf')
results = []
for k in k_candidates:
    try:
        _, _, _, Wq, _, _ = smm_inf(k, lambda_min, mu, rho)
        C = k / lambda_min + alpha * Wq
        results.append((k, Wq, C))
        if C < best_C:
            best_C = C
            best_k = k
    except ValueError:
        break

print("[Оптимизация затрат C(k) = k/λ + α·Wq]")
print("  k    Wq (мин)    C(k) (мин)")
for k, wq, c in results:
    print(f"  {k}    {wq:.3f}       {c:.2f}")
print(f"\nОптимальное число каналов k_opt = {best_k}")
print(f"Минимальное значение C = {best_C:.2f}\n")

# Характеристики при k_opt
P0_opt, Lq_opt, Ls_opt, Wq_opt, Ws_opt, probs_opt = smm_inf(best_k, lambda_min, mu, rho)
print("[Характеристики при k_opt]")
print(f"P0 = {P0_opt:.6f}")
print(f"Lq = {Lq_opt:.4f} заявок")
print(f"Ls = {Ls_opt:.4f} заявок")
print(f"Wq = {Wq_opt:.3f} мин")
print(f"Ws = {Ws_opt:.3f} мин\n")

# 3. Сравнение
print("[Сравнение характеристик]")
print(f"{'Параметр':<25} {'k_min = ' + str(k_min):<20} {'k_opt = ' + str(best_k):<20}")
print(f"{'Lq (заявок)':<25} {Lq_min:<20.4f} {Lq_opt:<20.4f}")
print(f"{'Ls (заявок)':<25} {Ls_min:<20.4f} {Ls_opt:<20.4f}")
print(f"{'Wq (мин)':<25} {Wq_min:<20.3f} {Wq_opt:<20.3f}")
print(f"{'Ws (мин)':<25} {Ws_min:<20.3f} {Ws_opt:<20.3f}\n")


# 4. Вероятность очереди не более n заявок
def prob_queue_le_n(probs, k, n):
    # probs содержит P_i для i=0..k+n (рассчитано в smm_inf)
    return sum(probs)


prob_min = prob_queue_le_n(probs_min, k_min, n)
prob_opt = prob_queue_le_n(probs_opt, best_k, n)
print(f"[Вероятность того, что в очереди не более {n} заявок]")
print(f"при k = {k_min}: {prob_min:.4f} ({prob_min * 100:.2f}%)")
print(f"при k = {best_k}: {prob_opt:.4f} ({prob_opt * 100:.2f}%)")