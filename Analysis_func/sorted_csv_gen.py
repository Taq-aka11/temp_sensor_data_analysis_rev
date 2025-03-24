import pandas as pd
import matplotlib.pyplot as plt

def sorted_csv_gen(filename):
    """
    CSVファイルを読み込み、'temp', 'TT', 'SS', 'FF', 'FS', 'SF'の順にソートします.
    ソートしたCSVファイルをfilenameのあるディレクトリにfilename_sorted.csvとして保存します.
    """

    # CSVファイルを読み込む
    df = pd.read_csv(filename)

    # ソートのための基準リストを定義
    sort_order = ['temp', 'tt', 'ss', 'ff', 'fs', 'sf']

    # ソート基準に従ってカラム名を並び替える関数
    def sort_columns(col_name):
        for idx, key in enumerate(sort_order):
            if key in col_name:
                return idx
        return len(sort_order)  # 見つからない場合は最後に並べる

    # カラム名をソート
    sorted_columns = sorted(df.columns, key=sort_columns)

    # データフレームを並び替えたカラムで再構成
    df_sorted = df[sorted_columns]

    # CSVファイルのラベルを変更
    new_column_labels = {
        df_sorted.columns[0]: 'temp',
        df_sorted.columns[1]: 'TT',
        df_sorted.columns[2]: 'SS',
        df_sorted.columns[3]: 'FF',
        df_sorted.columns[4]: 'FS',
        df_sorted.columns[5]: 'SF',
    }
    df_sorted.rename(columns=new_column_labels, inplace=True)

    # 並び替えたデータフレームをCSVファイルに保存
    output_filename = filename[:-4]+"_sorted.csv"
    df_sorted.to_csv(output_filename, index=False)

    return output_filename

# メインの処理
def main():
    # ファイルパスを手動で入力する
    filename = input("CSVファイルのパスを入力してください: ")
    sorted_csv_gen(filename)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()