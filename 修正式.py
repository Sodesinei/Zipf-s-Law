import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# 读取数据并预处理
df = pd.read_excel("英文词频统计结果.xlsx")
df = df.sort_values(by="次数", ascending=False).reset_index(drop=True)
df["排名"] = df.index + 1
df = df[df["次数"] > 0]  # 关键清洗步骤

# 准备拟合数据
observed_freq = df["次数"].values
rank = df["排名"].values

# =================================================================
# 定义修正后的拟合函数
def safe_mandelbrot_law(r, C, alpha, beta):
    """添加数值稳定性保护的芒代尔布罗公式"""
    return C / (r + beta + 1e-10) ** alpha

# 带约束的拟合
initial_guess = [observed_freq[0]*2, 1.0, 1.0]
try:
    params, _ = curve_fit(
        safe_mandelbrot_law,
        rank,
        observed_freq,
        p0=initial_guess,
        bounds=(
            [0.1, 0.1, -0.9],    # 下限
            [np.inf, 3, 10]      # 上限
        ),
        maxfev=10000
    )
except RuntimeError as e:
    print(f"拟合失败: {e}")
    params = initial_guess  # 使用初始值作为保底

C_fit, alpha_fit, beta_fit = params
# =================================================================

# 安全计算理论值
epsilon = 1e-10
df["理论PR值"] = C_fit / (df["排名"] + beta_fit + epsilon) ** alpha_fit

# 过滤无穷值
df = df[np.isfinite(df["理论PR值"])]

# 保存结果
df.to_excel("Zipf-Mandelbrot英文分析结果2.xlsx", index=False)

print(f"拟合参数：C={C_fit:.2f}, α={alpha_fit:.2f}, β={beta_fit:.2f}")
print("结果已保存至 Zipf-Mandelbrot分析结果.xlsx")