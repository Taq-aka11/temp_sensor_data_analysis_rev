import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# サンプルデータ
Vthp = np.array([0.8968, 0.9486, 0.845, 0.922, 0.8716])  # 変数1
Vthn = np.array([0.8702, 0.9303, 0.8092, 0.8391, 0.9014])  # 変数2
correction_val = np.array([1, 1.402, 0.621, 1.064, 0.941])  # 推定したい値

# 特徴量としてVthp, Vthnを結合
X = np.column_stack((Vthp, Vthn))

# データフレーム作成（便利な操作のため）
data = pd.DataFrame({
    "Vthp": Vthp,
    "Vthn": Vthn,
    "correction_val": correction_val
})

# ===== データチェック =====

# 1. データの基本情報
print("データの基本情報:\n", data.info())
print("\nデータの統計量:\n", data.describe())

# 2. 欠損値の確認
print("\n欠損値の確認:\n", data.isnull().sum())

# 3. 相関関係の確認
correlation_matrix = data.corr()
print("\n相関行列:\n", correlation_matrix)

# 特徴量データをDataFrameに変換
X_df = pd.DataFrame(X, columns=["Vthp", "Vthn"])

# VIFの計算
vif_data = pd.DataFrame()
vif_data["Feature"] = X_df.columns
vif_data["VIF"] = [variance_inflation_factor(X_df.values, i) for i in range(X_df.shape[1])]

# VIFの結果を表示
print(vif_data)

# 4. 外れ値の確認（散布図）
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.scatter(Vthp, correction_val, label="Vthp vs correction_val")
plt.xlabel("Vthp")
plt.ylabel("correction_val")
plt.legend()

plt.subplot(1, 2, 2)
plt.scatter(Vthn, correction_val, label="Vthn vs correction_val")
plt.xlabel("Vthn")
plt.ylabel("correction_val")
plt.legend()

plt.tight_layout()
plt.show()

# ===== データ前処理 =====

# 1. スケーリング
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. 線形回帰モデルの作成と学習
model = LinearRegression()
model.fit(X_scaled, correction_val)

# 学習された係数と切片を表示
print("学習後のモデル")
print("係数 (a, b):", model.coef_)
print("切片 (c):", model.intercept_)

# 新しいデータでの予測（スケーリングを適用）
new_data = np.array([[0.86, 0.86], [0.9, 0.885]])
new_data_scaled = scaler.transform(new_data)
predictions = model.predict(new_data_scaled)
print("\n予測結果:", predictions)
