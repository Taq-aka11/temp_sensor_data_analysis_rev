import pandas as pd

# CSVファイルの読み込み
data = pd.read_csv('Temp_Core_linearity_test\VREF_test\VREF_PMOS_param_bigger_ver\VREF_PMOS_sorted.csv')

# TCを求めるための関数
def calculate_tc(column, temp_column='temp'):
    # 温度範囲での電圧変動の最大幅と対応する温度を求める
    max_voltage_change = data[column].max() - data[column].min()
    temp_range = data[temp_column].max() - data[temp_column].min()
    vbg_reference = data[column].iloc[8]  # 初期値として最初の値を使用
    
    # 温度係数をppm/℃単位で計算
    tc = (max_voltage_change / (vbg_reference * temp_range)) * 1e6
    return tc

# 各列のTCを計算して表示
for column in data.columns[1:]:
    tc_value = calculate_tc(column)
    print(f"Temperature Coefficient for {column}: {tc_value:.2f} ppm/°C")
