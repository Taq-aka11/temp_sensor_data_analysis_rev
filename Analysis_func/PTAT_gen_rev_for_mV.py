import pandas as pd

from data_plot_for_mV import data_plot

def PTAT_csv_gen(VREF, VCTAT, output_file_csv, cor_val):
    """
    VREFとVCTATのCSVファイルを読み込み、VPTAT = VREF * cor_val - VCTATを計算し、
    結果を新しいCSVファイルに保存する関数
    """

    # VREFのcsvファイルを読み込む
    df_VREF = pd.read_csv(VREF)
    
    
    # VCTATのcsvファイルを読み込む
    df_VCTAT = pd.read_csv(VCTAT)

    # 両方のデータフレームが同じサイズであることを確認
    if df_VREF.shape != df_VCTAT.shape:
        raise ValueError("VREFとVCTATのデータフレームは同じ形状でなければなりません。")

    # 計算を行う列を指定（temp列以外）
    columns_to_calculate = ['TT', 'SS', 'FF', 'FS', 'SF']

    # temp列を保持しつつ、指定した列に対してVPTATを計算
    df_VPTAT = df_VREF[['temp']].copy()  # temp列をそのままコピー
    df_VPTAT[columns_to_calculate] = df_VREF[columns_to_calculate] * cor_val - df_VCTAT[columns_to_calculate]

    df_VPTAT.iloc[:, 1:] = df_VPTAT.iloc[:, 1:].applymap(lambda x: f"{x*1000:.1f}E-3")

    # VPTATのデータフレームをCSVに保存
    df_VPTAT.to_csv(output_file_csv, index=False)
    print(f"VPTATデータが {output_file_csv} に保存されました。")

def calculate_cor_val(VREF, VCTAT):
    """
    VREFおよびVCTATのCSVファイルから40℃に対応するデータを抽出し、
    各コーナー（SS, SF, TT, FS, FF）の差分を計算した後に、
    VCTATおよびVREFの差分を基にして補正係数（cor_val）を計算する関数です。

    Parameters:
    VREF (str): VREFのCSVファイルパス。
    VCTAT (str): VCTATのCSVファイルパス。

    Returns:
    float: 40℃での各コーナーの相対差の平均値。
    """


    # VCTATのcsvファイルを読み込む
    df_VCTAT = pd.read_csv(VCTAT)
    df_VREF = pd.read_csv(VREF)

    # 40℃のデータを抽出
    df_40C_VCTAT = df_VCTAT[df_VCTAT['temp'] == 40.0].copy()
    df_40C_VREF = df_VREF[df_VREF['temp'] == 40.0].copy()
    if df_40C_VCTAT.empty:
        raise ValueError("VCTATの40℃に対応するデータが見つかりません。")
    if df_40C_VREF.empty:
        raise ValueError("VREFの40℃に対応するデータが見つかりません。")
    
    # SS - SF, SF - TT, TT - FS, FS - FFを計算
    df_40C_VCTAT['SS-SF'] = round(df_40C_VCTAT['SS'] - df_40C_VCTAT['SF'], 4)
    df_40C_VCTAT['SF-TT'] = round(df_40C_VCTAT['SF'] - df_40C_VCTAT['TT'], 4)
    df_40C_VCTAT['TT-FS'] = round(df_40C_VCTAT['TT'] - df_40C_VCTAT['FS'], 4)
    df_40C_VCTAT['FS-FF'] = round(df_40C_VCTAT['FS'] - df_40C_VCTAT['FF'], 4)
    # SS - SF, SF - TT, TT - FS, FS - FFを計算
    df_40C_VREF['SS-SF'] = round(df_40C_VREF['SS'] - df_40C_VREF['SF'], 4)
    df_40C_VREF['SF-TT'] = round(df_40C_VREF['SF'] - df_40C_VREF['TT'], 4)
    df_40C_VREF['TT-FS'] = round(df_40C_VREF['TT'] - df_40C_VREF['FS'], 4)
    df_40C_VREF['FS-FF'] = round(df_40C_VREF['FS'] - df_40C_VREF['FF'], 4)

    # 計算した列のみを新しいデータフレームに保存
    df_corner_diff_VCTAT = df_40C_VCTAT[['temp', 'SS-SF', 'SF-TT', 'TT-FS', 'FS-FF']]
    df_corner_diff_VREF = df_40C_VREF[['temp', 'SS-SF', 'SF-TT', 'TT-FS', 'FS-FF']]

    # 計算を行う列を指定（temp列以外）
    columns_to_calculate = ['SS-SF', 'SF-TT', 'TT-FS', 'FS-FF']
    df_cor_val = df_corner_diff_VCTAT[columns_to_calculate] / df_corner_diff_VREF[columns_to_calculate]

    # 各列の平均値を計算
    cor_val = round((df_cor_val['SS-SF'] + df_cor_val['SF-TT'] + df_cor_val['TT-FS'] + df_cor_val['FS-FF']) / 4, 2 )
    print(cor_val)
    print(df_VCTAT)
    print(df_VREF)
    return cor_val


# メインの処理
def main():
    # ファイルパスを手動で入力する
    VREF = input("ソート後のVREFのCSVファイルのパスを入力してください: ")
    VCTAT = input("ソート後のVCTATのCSVファイルのパスを入力してください: ")
    file_path = input("VPTAT.csvの保存場所のパスを入力してください: ")
    cor_val = float(calculate_cor_val(VREF, VCTAT))
    cor_val_str = str(cor_val)
    
    output_file_csv = file_path + "\PTAT_cor_val=" + cor_val_str +".csv"
    print(output_file_csv)
    PTAT_csv_gen(VREF, VCTAT, output_file_csv, cor_val)

    output_file_jpg = output_file_csv[:-4] + ".jpg"

    data_plot(output_file_csv, "VPTAT[mV]", output_file_jpg)

# スクリプトのエントリーポイント
if __name__ == "__main__":
    main()

