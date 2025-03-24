import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_fontja

def temp_error_plot(csv_file_path, output_file_name):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path)

    # キャリブレーションポイントを設定
    t_low = 0  # 低温キャリブレーション温度
    t_high = 80  # 高温キャリブレーション温度

    # キャリブレーションポイントのインデックスを取得
    t_low_idx = df[df['temp'] == t_low].index[0]
    t_high_idx = df[df['temp'] == t_high].index[0]

    # 各プロセスコーナーのキャリブレーション値を取得
    vptat_low = {corner: df[corner][t_low_idx] for corner in ['TT', 'SS', 'FF', 'FS', 'SF']}
    vptat_high = {corner: df[corner][t_high_idx] for corner in ['TT', 'SS', 'FF', 'FS', 'SF']}

    # スロープと切片の計算
    slopes = {corner: (vptat_high[corner] - vptat_low[corner]) / (t_high - t_low) for corner in vptat_low}
    intercepts = {corner: vptat_low[corner] - slopes[corner] * t_low for corner in vptat_low}

    # 理想直線と温度誤差を計算
    df_temp_error = pd.DataFrame()
    df_temp_error['temp'] = df['temp']

    for corner in ['TT', 'SS', 'FF', 'FS', 'SF']:
        df[f'predicted_{corner}'] = slopes[corner] * df['temp'] + intercepts[corner]
        df[f'diff_{corner}'] = df[corner] - df[f'predicted_{corner}']
        df_temp_error[f'temp_error_{corner}'] = df[f'diff_{corner}'] / slopes[corner]

    # 温度誤差の全列の最大値と最小値を取得
    temp_error_columns = [f'temp_error_{corner}' for corner in ['TT', 'SS', 'FF', 'FS', 'SF']]
    max_temp_errors = df_temp_error[temp_error_columns].max().max()
    min_temp_errors = df_temp_error[temp_error_columns].min().min()

    print(f"温度誤差の最大値: {max_temp_errors:.2f}")
    print(f"温度誤差の最小値: {min_temp_errors:.2f}")

    # プロット
    plt.figure(figsize=(10, 6))
    for corner, marker, color in zip(['TT', 'SS', 'FF', 'FS', 'SF'], ['o', 's', '^', 'D', 'x'], ['b', 'r', 'g', 'm', 'orange']):
        plt.plot(df_temp_error['temp'], df_temp_error[f'temp_error_{corner}'], marker=marker, linestyle='-', color=color, label=corner)

    plt.xlabel('温度[℃]')
    plt.ylabel('温度誤差[℃]')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_file_name)
    plt.show()

def main():
    # CSVファイルのパスを入力
    csv_file_path = input("温度誤差を求めたいCSVファイルのパスを入力してください: ")
    output_filename = csv_file_path[:-4] + "_temp_error_two_point_cali_fixed.jpg"
    temp_error_plot(csv_file_path, output_filename)

if __name__ == "__main__":
    main()
