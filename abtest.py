import math
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

def ab_test_days(
    daily_traffic,
    base_rate=0.03,
    lift=0.01,
    alpha=0.05,
    power=0.8,
    allocation=0.5
):
    """
    计算 AB 实验所需总样本量和天数（相对提升版本）
    lift: 相对提升比例，例如 0.01 = +1% relative
    """
    p2 = base_rate * (1 + lift)

    effect_size = proportion_effectsize(base_rate, p2)

    analysis = NormalIndPower()
    n_per_group = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=(1 - allocation) / allocation
    )

    total_n = n_per_group / allocation
    days = math.ceil(total_n / daily_traffic)

    return days, total_n


def plot_days_vs_lift(
    daily_traffic=100000,
    base_rate=0.03,
    alpha=0.05,
    power=0.8
):
    # 相对提升从 0.5% 到 20%（0.005 ~ 0.20）
    lifts = np.linspace(0.005, 0.20, 20)
    days_needed = []

    for lift in lifts:
        days, _ = ab_test_days(
            daily_traffic=daily_traffic,
            base_rate=base_rate,
            lift=lift,
            alpha=alpha,
            power=power
        )
        days_needed.append(days)

    plt.figure(figsize=(8, 5))
    plt.plot(lifts * 100, days_needed, marker="o")
    plt.xlabel("相对提升 (%)")
    plt.ylabel("所需天数")
    plt.title("AB实验所需天数 vs 相对提升\n基线转化率={:.1f}%, 日流量={:,}".format(base_rate*100, daily_traffic))
    plt.grid(True)
    plt.show()


# 示例：日流量 100,000，基线转化率 3%
plot_days_vs_lift(daily_traffic=100000, base_rate=0.03)
