import pandas as pd

from data_plot_for_mV import data_plot

def PTAT_csv_gen(VBGR, VREF, output_file_csv):
    """
    
    """

    # VBGRのcsvファイルを読み込む
    df_VBGR = pd.read_csv(VBGR)
    
    # VREFのcsvファイルを読み込む
    df_VREF = pd.read_csv(VREF)

    # 両方のデータフレームが同じサイズであることを確認
    if df_VBGR.shape != df_VREF.shape:
        raise ValueError("VBGRとVREFのデータフレームは同じ形状でなければなりません。")

    # 計算を行う列を指定（temp列以外）
    columns_to_calculate = ['TT', 'SS', 'FF', 'FS', 'SF']

    # temp列を保持しつつ、指定した列に対してVPTATを計算
    df_VREF_curv_comp = df_VREF[['temp']].copy()  # temp列をそのままコピー
    df_VREF_curv_comp[columns_to_calculate] = df_VBGR[columns_to_calculate] + df_VREF[columns_to_calculate]

    # VPTATのデータフレームをCSVに保存
    df_VREF_curv_comp.to_csv(output_file_csv, index=False)
    print(f"VREF_curv_compのデータが {output_file_csv} に保存されました。")


# メインの処理
def main():
    # ファイルパスを手動で入力する
    VBGR = input("ソート後のVBGRのCSVファイルのパスを入力してください: ")
    VREF = input("ソート後のVREFのCSVファイルのパスを入力してください: ")
    file_path = input("VREF_curv_comp.csvの保存場所のパスを入力してください: ")
    
    output_file_csv = file_path + "\VREF_curv_comp.csv"
    print(output_file_csv)
    PTAT_csv_gen(VBGR, VREF, output_file_csv)

    output_file_jpg = output_file_csv[:-4] + ".jpg"

    data_plot(output_file_csv, "VREF_curv_comp[V]", output_file_jpg)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()

