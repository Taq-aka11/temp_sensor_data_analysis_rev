import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# CSVファイルを読み込む
file_path = '/Users/takuto/Desktop/temp_sensor_data_analysis/res_cap_process_variation/rppoly_process_variation_sorted.csv'
data = pd.read_csv(file_path)

# 温度データ (temp) を取得
temp = data['temp'].values.reshape(-1, 1)

# 各列に対して反比例の関係を調べるために逆数を取る
columns = data.columns[1:]  # temp列を除く
results = {}

for column in columns:
    values = data[column].values
    inverse_values = 1 / values  # 逆数を取る
    model = LinearRegression()
    model.fit(temp, inverse_values)
    predictions = model.predict(temp)
    r2 = r2_score(inverse_values, predictions)
    results[column] = r2

# 結果を表示
for column, r2 in results.items():
    print(f'{column}: R² = {r2:.4f}')