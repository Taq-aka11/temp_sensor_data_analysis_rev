import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# CSVファイルを読み込む
csv_file_path = input("CSVファイルのパスを入力してください: ")
df = pd.read_csv(csv_file_path)

# 温度データと出力データを取得
temperature = df['temp'].values
outputs = df.iloc[:, 1:]  # 温度以外の列

# リニアリティを計算してプロット
plt.figure(figsize=(12, 8))
for column in outputs.columns:
    # 実測値
    measured_values = outputs[column].values

    # 線形回帰を使って近似直線を求める
    model = LinearRegression()
    model.fit(temperature.reshape(-1, 1), measured_values)
    approx_values = model.predict(temperature.reshape(-1, 1))

    # リニアリティ(ΔNL)を計算
    max_deviation = np.max(np.abs(measured_values - approx_values))  # 最大偏差 (a)
    range_b = np.max(approx_values) - np.min(approx_values)  # 温度範囲の直線の値幅 (b)
    delta_nl = (max_deviation / range_b) * 100

    # プロット
    plt.plot(temperature, (approx_values - measured_values) * 100 / range_b, label=f'{column} (ΔNL={delta_nl:.2f}%)')

plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.xlabel('Temperature [°C]')
plt.ylabel('Deviation from Linear Approximation [V]')
plt.title('Linearity (ΔNL) Analysis')
plt.legend()
plt.grid(True)
plt.show()
