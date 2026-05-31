import math

# Параметры
lam = 8.0          # заявок/час
t = 2.0 / 60.0     # время обслуживания (час)
k = 6
n = 5
T = 10.0
C = 75.0

mu = 1.0 / t
a = lam / mu

print("[Исходные данные]")
print(f"λ = {lam} заявок/час")
print(f"t = {t*60} мин = {t} час")
print(f"μ = {mu} заявок/час")
print(f"a = λ/μ = {a:.6f}")
print(f"k = {k}")
print(f"n = {n}")
print(f"T = {T} час")
print(f"C = {C} у.е.\n")

# Вычисление P0
S1 = sum(a**i / math.factorial(i) for i in range(k+1))
S2 = sum(a**i / (math.factorial(k) * (k**(i-k))) for i in range(k+1, k+n+1))
P0 = 1.0 / (S1 + S2)

print("[Предельные вероятности состояний]")
print(f"P0 = {P0:.8f}")
P = [0.0] * (k+n+1)
for i in range(k+1):
    P[i] = (a**i / math.factorial(i)) * P0
for i in range(k+1, k+n+1):
    P[i] = (a**i / (math.factorial(k) * (k**(i-k)))) * P0
for i in range(k+n+1):
    print(f"P{i} = {P[i]:.8f}")

P_otk = P[k+n]
Q = 1 - P_otk
A = lam * Q

L = sum(i * P[i] for i in range(k+n+1))
L_q = sum((i - k) * P[i] for i in range(k+1, k+n+1))
L_s = L - L_q

lambda_eff = A
W = L / lambda_eff
W_q = L_q / lambda_eff
W_s = 1.0 / mu

print("\n[Основные характеристики СМО]")
print(f"Вероятность отказа P_отк = {P_otk:.8f}")
print(f"Относительная пропускная способность Q = {Q:.8f}")
print(f"Абсолютная пропускная способность A = {A:.6f} заявок/час")
print(f"Среднее число заявок в очереди L_q = {L_q:.6f}")
print(f"Среднее число заявок под обслуживанием L_s = {L_s:.6f}")
print(f"Среднее число заявок в системе L = {L:.6f}")
print(f"Среднее время ожидания в очереди W_q = {W_q*60:.4f} мин = {W_q:.6f} час")
print(f"Среднее время обслуживания W_s = {W_s*60:.4f} мин = {W_s:.6f} час")
print(f"Среднее время пребывания в системе W = {W*60:.4f} мин = {W:.6f} час")

S_loss = C * lam * P_otk * T
print(f"\n[Экономическая оценка]")
print(f"Потеря выручки за {T} часов: S_потерь = {S_loss:.2f} у.е.")