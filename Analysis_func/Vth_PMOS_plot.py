import matplotlib.pyplot as plt
import numpy as np

# 全体のフォントサイズを変更
plt.rcParams["font.size"] = 15  

# データ
corners = ['FF', 'FS', 'TT', 'SF', 'SS']
vth_40 = [0.845, 0.922, 0.8968, 0.8716, 0.9486]
vth_neg273 = [0.8395, 0.9168, 0.89, 0.8631, 0.9397]

# 差分（誤差）を計算し、mVに変換
delta_vth = [(v40 - v273) * 1000 for v40, v273 in zip(vth_40, vth_neg273)]  # mVに変換

# 誤差率を計算 (%)
error_percentage = [(delta / (v273 * 1000)) * 100 for delta, v273 in zip(delta_vth, vth_neg273)]

# 誤差率を出力
for corner, error in zip(corners, error_percentage):
    print(f"{corner}: Error = {error:.2f}%")

# プロットのレイアウト設定
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [2, 1]})

# 左側: 散布図
ax1.scatter(corners, vth_40, color='blue', label='Vth from compensation circuit(T=40°C)')
ax1.scatter(corners, vth_neg273, color='green', label='Vth from fabrication data(T=-273°C)')

# 軸ラベルとタイトル
ax1.set_xlabel('Process Corner')
ax1.set_ylabel('Vth(V)')
ax1.legend()
ax1.grid(True)

# 目盛りラベルのフォントサイズを変更
# ax1.tick_params(labelsize=12)

# 右側: 誤差（ΔVth）を棒グラフで表示
ax2.bar(corners, delta_vth, color='orange', label='Error (ΔV)')
ax2.axhline(0, color='black', linestyle='--')  # 0基準線
ax2.set_xlabel('Process Corner')
ax2.set_ylabel('Error (ΔV) [mV]')
ax2.legend()
ax2.grid(True)

# 目盛りラベルのフォントサイズを変更
# ax2.tick_params(labelsize=12)

# レイアウト調整
plt.tight_layout()
plt.show()
