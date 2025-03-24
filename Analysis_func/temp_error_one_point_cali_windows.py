
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib_fontja


def temp_error_plot(csv_file_path, output_file_name):
    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path)
    # print(df.columns)
    # print(df)

    # 回帰モデルを作成
    X = sm.add_constant(df['temp'])
    model = sm.OLS(df['TT'], X).fit()

    # 傾きと切片を取得
    slope = model.params['temp']
    intercept = model.params['const']

    print(f"傾き (slope): {slope:}")
    print(f"切片 (intercept): {intercept:}")

    #理想直線を追加
    df['predicted_TT'] = slope * (df['temp'] - 40) + df['TT'][8]
    df['predicted_SS'] = slope * (df['temp'] - 40) + df['SS'][8]
    df['predicted_FF'] = slope * (df['temp'] - 40) + df['FF'][8]
    df['predicted_FS'] = slope * (df['temp'] - 40) + df['FS'][8]
    df['predicted_SF'] = slope * (df['temp'] - 40) + df['SF'][8]

    # print(df)

    df_diff = pd.DataFrame()
    df_diff = df[['temp']].copy()
    #直線と理想直線の差を追加
    df_diff['diff_TT'] = df['TT'] - df['predicted_TT']
    df_diff['diff_SS'] = df['SS'] - df['predicted_SS']
    df_diff['diff_FF'] = df['FF'] - df['predicted_FF']
    df_diff['diff_FS'] = df['FS'] - df['predicted_FS']
    df_diff['diff_SF'] = df['SF'] - df['predicted_SF']
    # print(df)
    
    df_temp_error = pd.DataFrame()
    df_temp_error = df[['temp']].copy()
    #温度誤差を追加
    df_temp_error['temp_error_TT'] = df_diff['diff_TT'] / slope
    df_temp_error['temp_error_SS'] = df_diff['diff_SS'] / slope
    df_temp_error['temp_error_FF'] = df_diff['diff_FF'] / slope
    df_temp_error['temp_error_FS'] = df_diff['diff_FS'] / slope
    df_temp_error['temp_error_SF'] = df_diff['diff_SF'] / slope
    # print(df)
    
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
    output_filename = VPTAT[:-4] + "_temp_error_one_point_cali.jpg"
    temp_error_plot(VPTAT, output_filename)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()
