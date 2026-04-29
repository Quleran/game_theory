import numpy as np
import matplotlib.pyplot as plt

# Данные
outcomes = {"Success": 1_000_000, "Partial": 200_000, "Fail": -500_000}
env_probs = {"Stable": 0.5, "Peak": 0.3, "Failure": 0.2}

strategies = {
    "Fast": {
        "Stable": {"Success": 0.7, "Partial": 0.2, "Fail": 0.1},
        "Peak": {"Success": 0.2, "Partial": 0.3, "Fail": 0.5},
        "Failure": {"Success": 0.0, "Partial": 0.2, "Fail": 0.8}
    },
    "Test": {
        "Stable": {"Success": 0.9, "Partial": 0.1, "Fail": 0.0},
        "Peak": {"Success": 0.5, "Partial": 0.4, "Fail": 0.1},
        "Failure": {"Success": 0.1, "Partial": 0.4, "Fail": 0.5}
    },
    "Cancel": {
        "Stable": {"Success": 0.0, "Partial": 0.0, "Fail": 0.0},
        "Peak": {"Success": 0.0, "Partial": 0.0, "Fail": 0.0},
        "Failure": {"Success": 0.0, "Partial": 0.0, "Fail": 0.0}
    }
}


def compute_emv_and_std(strategy_name, strategy_data):
    if strategy_name == "Cancel":
        return 0, 0

    values = []
    probs = []
    for env, env_p in env_probs.items():
        for outcome, outcome_p in strategy_data[env].items():
            if outcome_p > 0:
                values.append(outcomes[outcome])
                probs.append(env_p * outcome_p)

    emv = sum(p * v for p, v in zip(probs, values))
    variance = sum(p * (v - emv) ** 2 for p, v in zip(probs, values))
    return emv, np.sqrt(variance)


def draw_tree():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Позиции узлов
    pos = {
        'root': (6, 7),
        'Fast': (2, 5.5), 'Test': (6, 5.5), 'Cancel': (10, 5.5),
        'Fast_S': (0.5, 4), 'Fast_P': (2, 4), 'Fast_F': (3.5, 4),
        'Test_S': (4.5, 4), 'Test_P': (6, 4), 'Test_F': (7.5, 4),
        'Cancel_S': (9, 4), 'Cancel_P': (10.5, 4), 'Cancel_F': (11.5, 4),
    }

    # Листья
    leaf_y = 2
    leaf_x = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]
    leaf_idx = 0
    leaf_texts = {}

    for strategy in ['Fast', 'Test', 'Cancel']:
        for env in ['Stable', 'Peak', 'Failure']:
            env_key = f'{strategy}_{env[0]}'
            x = pos[env_key][0]

            if strategy == 'Cancel':
                leaf_texts[f'leaf_{leaf_idx}'] = (x, leaf_y, '0 ₽\n100%')
                leaf_idx += 1
            else:
                for outcome, prob in strategies[strategy][env].items():
                    if prob > 0:
                        money = outcomes[outcome]
                        leaf_texts[f'leaf_{leaf_idx}'] = (x + (leaf_idx % 3 - 1) * 0.4, leaf_y,
                                                          f'{outcome[:3]}\n{prob:.0%}\n{money / 1000:.0f}k')
                        leaf_idx += 1

    # Рисуем узлы
    for name, (x, y) in pos.items():
        if name == 'root':
            ax.text(x, y, 'Менеджер', ha='center', va='center', fontsize=11, weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray'))
        elif name in ['Fast', 'Test', 'Cancel']:
            colors = {'Fast': '#FFE5B4', 'Test': '#C8E6C9', 'Cancel': '#FFCDD2'}
            ax.text(x, y, name, ha='center', va='center', fontsize=10, weight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=colors[name]))
        elif '_S' in name or '_P' in name or '_F' in name:
            env = {'_S': 'Stable', '_P': 'Peak', '_F': 'Failure'}[name[-2:]]
            prob = env_probs[env]
            ax.text(x, y, f'{env}\n{prob:.0%}', ha='center', va='center', fontsize=8,
                    bbox=dict(boxstyle='circle,pad=0.15', facecolor='#B3E5FC'))

    # Рисуем листья
    for (x, y, text) in leaf_texts.values():
        ax.text(x, y, text, ha='center', va='center', fontsize=7,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8E8E8'))

    # Рисуем рёбра
    edges = [
        ('root', 'Fast'), ('root', 'Test'), ('root', 'Cancel'),
        ('Fast', 'Fast_S'), ('Fast', 'Fast_P'), ('Fast', 'Fast_F'),
        ('Test', 'Test_S'), ('Test', 'Test_P'), ('Test', 'Test_F'),
        ('Cancel', 'Cancel_S'), ('Cancel', 'Cancel_P'), ('Cancel', 'Cancel_F'),
    ]

    for start, end in edges:
        x1, y1 = pos[start]
        x2, y2 = pos[end]
        ax.annotate('', xy=(x2, y2 + 0.1), xytext=(x1, y1 - 0.1),
                    arrowprops=dict(arrowstyle='->', lw=0.8, color='gray'))

    # Рёбра к листьям
    leaf_idx = 0
    for strategy in ['Fast', 'Test', 'Cancel']:
        for env in ['Stable', 'Peak', 'Failure']:
            env_key = f'{strategy}_{env[0]}'
            x1, y1 = pos[env_key]

            if strategy == 'Cancel':
                x2, y2, _ = leaf_texts[f'leaf_{leaf_idx}']
                ax.annotate('', xy=(x2, y2 + 0.1), xytext=(x1, y1 - 0.1),
                            arrowprops=dict(arrowstyle='->', lw=0.8, color='gray'))
                leaf_idx += 1
            else:
                for outcome, prob in strategies[strategy][env].items():
                    if prob > 0:
                        x2, y2, _ = leaf_texts[f'leaf_{leaf_idx}']
                        ax.annotate('', xy=(x2, y2 + 0.1), xytext=(x1, y1 - 0.1),
                                    arrowprops=dict(arrowstyle='->', lw=0.8, color='gray'))
                        ax.text((x1 + x2) / 2, (y1 + y2) / 2, f'{prob:.0%}',
                                ha='center', va='center', fontsize=6, color='blue')
                        leaf_idx += 1

    # Таблица результатов
    results = {}
    for name in ['Fast', 'Test', 'Cancel']:
        emv, std = compute_emv_and_std(name, strategies[name])
        results[name] = (emv, std)

    table_data = [['Стратегия', 'EMV (k₽)', 'σ (k₽)']]
    for name in ['Fast', 'Test', 'Cancel']:
        emv, std = results[name]
        table_data.append([name, f'{emv / 1000:.0f}', f'{std / 1000:.0f}'])

    table = ax.table(cellText=table_data, loc='lower right', bbox=[0.75, 0.02, 0.23, 0.15])
    table.auto_set_font_size(False)
    table.set_fontsize(8)

    for i in range(4):
        for j in range(3):
            table[(i, j)].set_facecolor('#E0E0E0' if i == 0 else 'white')

    # Заголовок и вывод
    ax.set_title('Дерево решений', fontsize=14, weight='bold', pad=15)
    ax.text(6, 0.3,
            f'Оптимально: Test (EMV = {results["Test"][0] / 1000:.0f}k₽, σ = {results["Test"][1] / 1000:.0f}k₽)',
            ha='center', fontsize=9, color='green', weight='bold',
            bbox=dict(boxstyle='round', facecolor='#E8F5E9'))

    plt.tight_layout()
    plt.savefig('decision_tree.png', dpi=150, bbox_inches='tight')
    plt.show()

    # Вывод в консоль
    print("\n" + "=" * 45)
    print("РЕЗУЛЬТАТЫ")
    print("=" * 45)
    for name in ['Fast', 'Test', 'Cancel']:
        emv, std = results[name]
        cv = std / emv if emv > 0 else float('inf')
        print(f"\n{name}:")
        print(f"  EMV = {emv:>10,.0f} ₽")
        print(f"  σ   = {std:>10,.0f} ₽")
        print(f"  σ/EMV = {cv:>8.2f}")

    print("\n" + "=" * 45)
    print("ВЫБОР: Test")
    print(f"  Максимальная доходность: {results['Test'][0]:,.0f} ₽")
    print(f"  Лучшее отношение риск/доходность: {results['Test'][1] / results['Test'][0]:.2f}")
    print("=" * 45)


if __name__ == "__main__":
    draw_tree()