import numpy as np

# ------------------ Функция преобразования дроби в число ------------------
def parse_number(s):
    """
    Преобразует строку в число.
    Поддерживает: '2', '2.5', '1/3', '3/2', '-1/4'
    """
    s = s.strip()
    if '/' in s:
        num, den = s.split('/')
        return float(num) / float(den)
    else:
        return float(s)

# ------------------ Функция ввода матрицы с поддержкой дробей ------------------
def input_matrix(size, name):
    print(f"\nВведите матрицу парных сравнений '{name}' размером {size}x{size}:")
    print("Допустимые форматы: 2, 2.5, 1/3, 3/2, 1/5 и т.д.")
    matrix = np.zeros((size, size))
    for i in range(size):
        while True:
            try:
                row = input(f"Строка {i+1} (введите {size} значений через пробел): ").strip().split()
                if len(row) != size:
                    print(f"Ошибка: нужно {size} значений. Повторите ввод.")
                    continue
                for j, val in enumerate(row):
                    matrix[i, j] = parse_number(val)
                break
            except Exception as e:
                print(f"Неверный формат: {e}. Повторите строку.")
    return matrix

# ------------------ Проверка обратной симметричности ------------------
def check_reverse_symmetry(matrix, name):
    n = matrix.shape[0]
    ok = True
    for i in range(n):
        for j in range(i+1, n):
            if not np.isclose(matrix[i, j] * matrix[j, i], 1.0, atol=1e-6):
                print(f"Предупреждение: a[{i+1},{j+1}]={matrix[i,j]:.4f}, "
                      f"a[{j+1},{i+1}]={matrix[j,i]:.4f}, произведение={matrix[i,j]*matrix[j,i]:.4f} ≠ 1")
                ok = False
    return ok

# ------------------ Расчёт вектора приоритетов ------------------
def priority_vector(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_idx = np.argmax(eigvals.real)
    max_eigval = eigvals[max_idx].real
    vec = np.abs(eigvecs[:, max_idx].real)
    vec = vec / vec.sum()
    return vec, max_eigval

# ------------------ Индекс согласованности (CI) и отношение (CR) ------------------
def consistency_ratios(matrix, n, name):
    RI = {1:0.0, 2:0.0, 3:0.58, 4:0.9, 5:1.12, 6:1.24, 7:1.32, 8:1.41, 9:1.45, 10:1.49}
    vec, lambda_max = priority_vector(matrix)
    CI = (lambda_max - n) / (n - 1) if n > 1 else 0.0
    CR = CI / RI.get(n, 1.49) if n > 2 else 0.0
    print(f"\nМатрица '{name}':")
    print(f"  λ_max = {lambda_max:.4f}")
    print(f"  CI = {CI:.4f}")
    print(f"  CR = {CR:.4f}")
    if CR > 0.1:
        print(f"  *** CR > 0.1, согласованность недостаточная ***")
    else:
        print(f"  ✅ CR ≤ 0.1, согласованность приемлема")
    return vec, CR

# ------------------ Основной алгоритм ------------------
def main():
    print("\n" + "="*70)
    print("МЕТОД АНАЛИЗА ИЕРАРХИЙ (МАИ) ДЛЯ ВЫБОРА ЯЗЫКА ПРОГРАММИРОВАНИЯ")
    print("="*70)

    goal = "Выбор языка программирования для высоконагруженного микросервиса"

    alternatives = ["Go", "Java", "Rust", "Python", "C#", "Node.js"]
    n_alt = len(alternatives)
    print(f"\nАльтернативы ({n_alt} шт.): {', '.join(alternatives)}")

    criteria = [
        "Производительность (RPS/латентность)",
        "Потребление памяти и CPU",
        "Скорость разработки",
        "Надёжность (типизация, безопасность памяти)"
    ]
    k_crit = len(criteria)
    print(f"\nКритерии ({k_crit} шт.):")
    for i, crit in enumerate(criteria, 1):
        print(f"  {i}. {crit}")

    # Шаг 1: Матрица критериев
    while True:
        criteria_matrix = input_matrix(k_crit, "Критерии относительно цели")
        check_reverse_symmetry(criteria_matrix, "Критерии")
        crit_weights, crit_cr = consistency_ratios(criteria_matrix, k_crit, "Критерии (относительно цели)")
        if crit_cr <= 0.1:
            break
        else:
            print("\nПовторите ввод матрицы критериев (CR > 0.1).\n")

    print("\nВектор приоритетов критериев:")
    for i, w in enumerate(crit_weights):
        print(f"  {criteria[i]}: {w:.4f}")

    # Шаг 2: Матрицы альтернатив по каждому критерию
    alt_weights = []
    for idx, crit in enumerate(criteria):
        print(f"\n--- Критерий: {crit} ---")
        while True:
            matrix_alt = input_matrix(n_alt, f"Альтернативы относительно критерия '{crit}'")
            check_reverse_symmetry(matrix_alt, f"Альтернативы vs {crit}")
            vec, cr = consistency_ratios(matrix_alt, n_alt, f"Альтернативы по критерию '{crit}'")
            if cr <= 0.1:
                alt_weights.append(vec)
                break
            else:
                print(f"\nПовторите ввод матрицы для '{crit}' (CR > 0.1).\n")

        print(f"Локальные приоритеты альтернатив по критерию '{crit}':")
        for i, w in enumerate(vec):
            print(f"  {alternatives[i]}: {w:.4f}")

    # Шаг 3: Глобальные приоритеты
    global_scores = np.zeros(n_alt)
    for i in range(n_alt):
        for j in range(k_crit):
            global_scores[i] += alt_weights[j][i] * crit_weights[j]

    print("\n" + "="*70)
    print("ИТОГОВЫЕ ГЛОБАЛЬНЫЕ ПРИОРИТЕТЫ АЛЬТЕРНАТИВ:")
    print("="*70)
    results = list(zip(alternatives, global_scores))
    results.sort(key=lambda x: x[1], reverse=True)

    for alt, score in results:
        print(f"{alt:12} : {score:.4f}")

    best_alt, best_score = results[0]
    print("\n🏆 ЛУЧШАЯ АЛЬТЕРНАТИВА:", best_alt)
    print(f"   (глобальный приоритет = {best_score:.4f})")

if __name__ == "__main__":
    main()