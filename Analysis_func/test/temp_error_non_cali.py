import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

def temp_error_plot(csv_file_path, output_file_name):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path, header=None)
    
    # 温度と測定値の抽出
    df.columns = ['temp', 'TT', 'SS', 'FF', 'FS', 'SF']
    
    # TT, SS, FF, FS, SFの平均値を計算して新しい列 'average' に追加
    df['average'] = df[['TT', 'SS', 'FF', 'FS', 'SF']].mean(axis=1)

    # 回帰モデルを作成
    X = sm.add_constant(df['temp'])
    model = sm.OLS(df['average'], X).fit()

    # 傾きと切片を取得
    slope = model.params['temp']
    intercept = model.params['const']

    # 理想直線を追加
    df['predicted'] = slope * df['temp'] + intercept

    # 直線と理想直線の差を追加
    df_diff = pd.DataFrame()
    df_diff = df[['temp']].copy()
    df_diff['diff_TT'] = df['TT'] - df['predicted']
    df_diff['diff_SS'] = df['SS'] - df['predicted']
    df_diff['diff_FF'] = df['FF'] - df['predicted']
    df_diff['diff_FS'] = df['FS'] - df['predicted']
    df_diff['diff_SF'] = df['SF'] - df['predicted']

    # 温度誤差を追加
    df_temp_error = pd.DataFrame()
    df_temp_error = df[['temp']].copy()
    df_temp_error['temp_error_TT'] = df_diff['diff_TT'] / slope
    df_temp_error['temp_error_SS'] = df_diff['diff_SS'] / slope
    df_temp_error['temp_error_FF'] = df_diff['diff_FF'] / slope
    df_temp_error['temp_error_FS'] = df_diff['diff_FS'] / slope
    df_temp_error['temp_error_SF'] = df_diff['diff_SF'] / slope

    # 温度誤差の全列の最大値と最小値を取得
    temp_error_columns = ['temp_error_TT', 'temp_error_SS', 'temp_error_FF', 'temp_error_FS', 'temp_error_SF']
    max_temp_errors = df_temp_error[temp_error_columns].max().max()
    min_temp_errors = df_temp_error[temp_error_columns].min().min()

    print(f"温度誤差の最大値: {max_temp_errors:.2f}")
    print(f"温度誤差の最小値: {min_temp_errors:.2f}")

    # プロットのためにカラムを設定
    temperature = df_temp_error['temp']
    TT = df_temp_error['temp_error_TT']
    SS = df_temp_error['temp_error_SS']
    FF = df_temp_error['temp_error_FF']
    FS = df_temp_error['temp_error_FS']
    SF = df_temp_error['temp_error_SF']

    # 折れ線グラフを作成
    plt.plot(temperature, TT, marker='o', linestyle='-', color='b', label='TT')
    plt.plot(temperature, SS, marker='s', linestyle='-', color='r', label='SS')
    plt.plot(temperature, FF, marker='^', linestyle='-', color='g', label='FF')
    plt.plot(temperature, FS, marker='D', linestyle='-', color='m', label='FS')
    plt.plot(temperature, SF, marker='x', linestyle='-', color='orange', label='SF')

    plt.xlabel('温度[℃]')
    plt.ylabel('温度誤差[℃]')
    plt.grid(True)
    plt.legend()
    # グラフを画像ファイルとして保存
    plt.savefig(output_file_name)
    plt.show()  # グラフを表示

# メインの処理
def main():
    # ファイルパスを手動で入力する
    VPTAT = input("温度誤差を求めたいCSVファイルのパスを入力してください: ")
    output_filename = VPTAT[:-4] + "_temp_error_non_cali_average.jpg"
    temp_error_plot(VPTAT, output_filename)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()