import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from sorted_csv_gen import sorted_csv_gen

def data_plot(filename, y_label_name, output_file_name):
    """
    指定されたCSVファイルからデータを読み込み、温度に対する各コーナーのデータ列の折れ線グラフを作成し、保存する関数。
    
    パラメータ:
    filename (str): 入力のCSVファイルのファイル名。
    y_label_name (str): グラフのY軸ラベル。
    output_file_name (str): 保存する画像ファイルの名前。
    """

    # CSVファイルを読み込む
    df = pd.read_csv(filename)

    # プロットのためにカラムを設定
    temperature = df['temp']
    TT = df['TT'] / 1000000  # [Hz] -> [MHz]
    SS = df['SS'] / 1000000  # [Hz] -> [MHz]
    FF = df['FF'] / 1000000  # [Hz] -> [MHz]
    FS = df['FS'] / 1000000  # [Hz] -> [MHz]
    SF = df['SF'] / 1000000  # [Hz] -> [MHz]
    
    # 折れ線グラフを作成
    plt.plot(temperature, TT, marker='o', linestyle='-', color='b', label='TT')
    plt.plot(temperature, SS, marker='s', linestyle='-', color='r', label='SS')
    plt.plot(temperature, FF, marker='^', linestyle='-', color='g', label='FF')
    plt.plot(temperature, FS, marker='D', linestyle='-', color='m', label='FS')
    plt.plot(temperature, SF, marker='x', linestyle='-', color='orange', label='SF')
    plt.xlabel('Temperature[℃]')
    plt.ylabel(y_label_name)
    
    # 縦軸の単位を自動で調整 
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.grid(True)
    plt.legend(fontsize=8)
    # plt.legend(fontsize=8, loc='upper left', bbox_to_anchor=(0.03, 0.9))
    plt.savefig(output_file_name)
    plt.show()

# メインの処理
def main():
    # ファイルパスを手動で入力する
    filename = input("プロットしたいソート後のCSVファイルのパスを入力してください: ")
    sorted_data = filename
    y_label_name = "f_BIAS[MHz]"  # 単位を[kHz]に設定
    image_filename = filename[:-4]+".jpg"
    data_plot(sorted_data, y_label_name, image_filename)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()
