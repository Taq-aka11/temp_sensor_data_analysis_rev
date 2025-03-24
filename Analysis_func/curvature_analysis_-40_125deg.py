
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from sorted_csv_gen import sorted_csv_gen

def curvature_analysis(filename, y_label_name, output_file_name):
    """

    """

    # CSVファイルを読み込む
    df = pd.read_csv(filename)

    # 傾きと切片を取得
    slope_tt = (df['TT'][17] - df['TT'][0]) / (df['temp'].max() - df['temp'].min())
    slope_ss = (df['SS'][17] - df['SS'][0]) / (df['temp'].max() - df['temp'].min())
    slope_ff = (df['FF'][17] - df['FF'][0]) / (df['temp'].max() - df['temp'].min())
    slope_fs = (df['FS'][17] - df['FS'][0]) / (df['temp'].max() - df['temp'].min())
    slope_sf = (df['SF'][17] - df['SF'][0]) / (df['temp'].max() - df['temp'].min())

    # print(slope_tt)


    df_ideal = pd.DataFrame()
    df_ideal = df[['temp']].copy()

    df_ideal['TT'] = slope_tt * (df['temp'] + 40) + df['TT'][0]
    df_ideal['SS'] = slope_ss * (df['temp'] + 40) + df['SS'][0]
    df_ideal['FF'] = slope_ff * (df['temp'] + 40) + df['FF'][0]
    df_ideal['FS'] = slope_fs * (df['temp'] + 40) + df['FS'][0]
    df_ideal['SF'] = slope_sf * (df['temp'] + 40) + df['SF'][0]

    # print(df_ideal)

    df_diff = pd.DataFrame()
    df_diff = df[['temp']].copy()

    df_diff['TT'] = df['TT'] - df_ideal['TT']
    df_diff['SS'] = df['SS'] - df_ideal['SS']
    df_diff['FF'] = df['FF'] - df_ideal['FF']
    df_diff['FS'] = df['FS'] - df_ideal['FS']
    df_diff['SF'] = df['SF'] - df_ideal['SF']

    # print(df_diff)

    output_filename_csv = filename[:-4]+"_curvature.csv"
    df_diff.to_csv(output_filename_csv, index=False)

    # プロットのためにカラムを設定
    temperature = df_diff['temp']
    TT = df_diff['TT']
    SS = df_diff['SS']
    FF = df_diff['FF']
    FS = df_diff['FS']
    SF = df_diff['SF']
    
    # 折れ線グラフを作成
    plt.plot(temperature, TT, marker='o', linestyle='-', color='b', label='TT')
    plt.plot(temperature, SS, marker='s', linestyle='-', color='r', label='SS')
    plt.plot(temperature, FF, marker='^', linestyle='-', color='g', label='FF')
    plt.plot(temperature, FS, marker='D', linestyle='-', color='m', label='FS')
    plt.plot(temperature, SF, marker='x', linestyle='-', color='orange', label='SF')
    plt.xlabel('Temperature[℃]')
    plt.ylabel(y_label_name)
    plt.grid(True)
    plt.legend()
    # グラフを画像ファイルとして保存
    plt.savefig(output_file_name)
    plt.show()  # グラフを表示

# メインの処理
def main():
    # ファイルパスを手動で入力する
    filename = input("曲率を求めたいソート後のCSVファイルのパスを入力してください: ")
    sorted_data = filename
    y_label_name = input("グラフのYラベルの名前を単位付きで入力してください: ")
    image_filename = filename[:-4]+"_curvature.jpg"
    curvature_analysis(sorted_data, y_label_name, image_filename)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()