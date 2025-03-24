import pandas as pd
import matplotlib.pyplot as plt

from sorted_csv_gen_for_mV import sorted_csv_gen

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
    TT = df['TT']
    SS = df['SS']
    FF = df['FF']
    FS = df['FS']
    SF = df['SF']
    
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
    filename = input("プロットしたいCSVファイルのパスを入力してください: ")
    sorted_data = sorted_csv_gen(filename)
    y_label_name = input("グラフのYラベルの名前を単位付きで入力してください: ")
    image_filename = filename[:-4]+".jpg"
    data_plot(sorted_data, y_label_name, image_filename)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()