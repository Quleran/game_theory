import math

# Входные данные
alpha = 2.5          # часов на одну заявку
n = 48               # заявок в сутки
k_given = 6          # заданное число каналов

# Перевод в заявки в час
lambda_ = n / 24      # заявок в час
mu = 1 / alpha        # заявок в час на канал

# Приведённая нагрузка
a = lambda_ * alpha   # a = λ/μ

print("[Входные параметры]")
print(f"λ = {lambda_:.4f} заявок/час")
print(f"μ = {mu:.4f} заявок/час (на канал)")
print(f"a = λ/μ = {a:.4f} Эрланг")
print()

# Формула Эрланга B для вероятности отказа
def P_block(a, k):
    sum_ = 0
    for i in range(k + 1):
        sum_ += (a ** i) / math.factorial(i)
    return (a ** k / math.factorial(k)) / sum_

# Пункт 1: минимальное число каналов для Q >= 95%
k_min = 1
while True:
    P_b = P_block(a, k_min)
    Q = 1 - P_b
    if Q >= 0.95:
        break
    k_min += 1

print("[Пункт 1]")
print(f"Минимальное число каналов для Q ≥ 95%: {k_min}")
print(f"При k={k_min}: P_отк = {P_block(a, k_min):.6f}, Q = {1 - P_block(a, k_min):.6f}")
print()

# Пункт 2: решить задачу для k = 6
k = k_given
P_b = P_block(a, k)
Q = 1 - P_b
A = lambda_ * Q
avg_busy = a * Q          # среднее число занятых каналов
load_factor = avg_busy / k

print("[Пункт 2 и 3]")
print(f"Для k = {k} каналов:")
print(f"Вероятность отказа P_отк = {P_b:.6f}")
print(f"Относительная пропускная способность Q = {Q:.6f}")
print(f"Абсолютная пропускная способность A = {A:.4f} заявок/час")
print(f"Среднее число занятых каналов = {avg_busy:.4f}")
print(f"Коэффициент загрузки каналов = {load_factor:.4f}")

# Пункт 3 (предельные вероятности состояний)
# P_i = (a^i / i!) / sum_{j=0..k} (a^j / j!), i=0..k
sum_denom = 0
for i in range(k + 1):
    sum_denom += (a ** i) / math.factorial(i)

print("\n[Предельные вероятности состояний]")
for i in range(k + 1):
    Pi = (a ** i / math.factorial(i)) / sum_denom
    print(f"P{i} = {Pi:.6f} (вероятность, что занято {i} каналов)")