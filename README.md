# temp_sensor_data_analysis_rev
**コードの中身の大まかな説明**

Analysis_funcのフォルダの中にデータ解析で使用していたファイルがあります(コードの説明はコメントでところどころ記載してあります)

**1. データをプロットしたいとき**

sorted_csv_gen.pyを実行(データの名前と並べ替えを行う)→data_plot.pyなどを実行(他にもmVでプロットしたいとき、kHz, MHz用がある)

今後、基本的にcsvのデータをソート(sorted_csv_gen.pyを実行)してからデータを分析する流れになります

**2. グローバルばらつきを取り除いてPTAT出力を得たい**

sorted_csv_gen.pyを実行→PTAT_gen_rev.pyなどを実行

補正係数はVREF, VPTAT(VCTAT)のコーナー間のばらつきの比を平均化して求めている(この過程がキャリブレーションになってしまうのではないか？)

**3. 温度誤差を求めたい**

sorted_csv_gen.pyを実行→temp_error_non_cali_average.pyを実行

----

主に使うのは以上の関数。他にも出力の曲率を求める関数などもある。
