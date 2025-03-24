import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


def load_and_rename_columns(csv_file_path):
    """Load CSV and rename columns."""
    column_mapping = {
        0: 'temp',
        1: 'comp_out_ff',
        2: 'comp_out_fs',
        3: 'comp_out_sf',
        4: 'comp_out_ss',
        5: 'comp_out_tt',
        6: 'res_ff',
        7: 'res_fs',
        8: 'res_sf',
        9: 'res_ss',
        10: 'res_tt',
    }
    try:
        df = pd.read_csv(csv_file_path)
        df.rename(columns={df.columns[i]: name for i, name in column_mapping.items()}, inplace=True)
        return df
    except Exception as e:
        raise ValueError(f"Error loading or renaming columns: {e}")


def calculate_regression(df, column):
    """Perform regression on a specified column."""
    X = sm.add_constant(df['temp'])
    model = sm.OLS(df[column], X).fit()
    return model.params['temp'], model.params['const']


def calculate_correction_ratios(df, reference_column):
    """Add resistance ratios to the DataFrame."""
    for corner in ['fs', 'sf', 'ff', 'ss']:
        ratio_column = f'{corner}_ratio_to_tt'
        df[ratio_column] = df[f'res_{corner}'] / df[reference_column]


def apply_corrections(df, slopes):
    """Apply correction to computed outputs."""
    for corner in ['ff', 'fs', 'sf', 'ss']:
        ratio_column = f'{corner}_ratio_to_tt'
        corrected_column = f'after_cor_comp_out_{corner}'
        df[corrected_column] = df[f'comp_out_{corner}'] / df[ratio_column].iloc[8]
    df['after_cor_comp_out_tt'] = df['comp_out_tt']


def add_predicted_lines(df, slope_tt):
    """Add predicted lines to the DataFrame."""
    for corner in ['ff', 'fs', 'sf', 'ss', 'tt']:
        predicted_column = f'predicted_{corner}'
        offset = df[f'after_cor_comp_out_{corner}'].iloc[8]
        df[predicted_column] = slope_tt * (df['temp'] - 40) + offset


def calculate_temperature_errors(df, slope_tt):
    """Calculate temperature errors and add to DataFrame."""
    for corner in ['ff', 'fs', 'sf', 'ss', 'tt']:
        diff_column = f'diff_{corner}'
        error_column = f'temp_error_{corner}'
        df[diff_column] = df[f'after_cor_comp_out_{corner}'] - df[f'predicted_{corner}']
        df[error_column] = df[diff_column] / slope_tt


def plot_graph(df, x_col, y_cols, labels, xlabel, ylabel, output_file):
    """Plot and save a graph."""
    df.plot(x=x_col, y=y_cols, marker='o', linestyle='-', label=labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.savefig(output_file)
    plt.show()

def apply_corrections(df, slopes):
    """Apply correction to computed outputs."""
    corrected_columns = []
    for corner in ['ff', 'fs', 'sf', 'ss']:
        ratio_column = f'{corner}_ratio_to_tt'
        corrected_column = f'after_cor_comp_out_{corner}'
        df[corrected_column] = df[f'comp_out_{corner}'] / df[ratio_column].iloc[8]
        corrected_columns.append(corrected_column)
    df['after_cor_comp_out_tt'] = df['comp_out_tt']
    corrected_columns.append('after_cor_comp_out_tt')
    return corrected_columns

def plot_graph(df, x_col, y_cols, labels, xlabel, ylabel, output_file):
    """
    Plot and save a line graph using the provided data and settings.
    
    Args:
        df: pandas DataFrame containing the data.
        x_col: Column name for the x-axis.
        y_cols: List of column names for the y-axis.
        labels: List of labels for each line in the plot.
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
        output_file: File path to save the plot image.
    """
    temperature = df[x_col]  # 温度データ

    # 各列と対応するラベルで折れ線グラフをプロット
    for y_col, label, marker, color in zip(
        y_cols, 
        labels, 
        ['o', 's', '^', 'D', 'x'], 
        ['b', 'r', 'g', 'm', 'orange']
    ):
        plt.plot(temperature, df[y_col], marker=marker, linestyle='-', color=color, label=label)

    # グラフのラベルとスタイルを設定
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()

    # グラフを保存して表示
    plt.savefig(output_file)
    plt.show()



def process_temperature_data(csv_file_path, csv_file_name, output_file_1, output_file_2):
    """Main processing function."""
    df = load_and_rename_columns(csv_file_path)

    # Regression for all corners
    slopes, intercepts = {}, {}
    for corner in ['tt', 'fs', 'sf', 'ff', 'ss']:
        slopes[corner], intercepts[corner] = calculate_regression(df, f'comp_out_{corner}')

    # Add resistance ratios and apply corrections
    calculate_correction_ratios(df, 'res_tt')
    corrected_columns = apply_corrections(df, slopes)

    # Add predicted lines and calculate errors
    add_predicted_lines(df, slopes['tt'])
    calculate_temperature_errors(df, slopes['tt'])

    # Save corrected columns to a new CSV file
    corrected_csv_path = csv_file_name
    df[['temp'] + corrected_columns].to_csv(corrected_csv_path, index=False)
    print(f"補正後のデータが {corrected_csv_path} に保存されました。")

    # Plot graphs
    plot_graph(
        df,
        x_col='temp',
        y_cols=[f'after_cor_comp_out_{corner}' for corner in ['ff', 'fs', 'sf', 'ss', 'tt']],
        labels=['FF', 'FS', 'SF', 'SS', 'TT'],
        xlabel='Temperature [℃]',
        ylabel='Frequency [Hz]',
        output_file=output_file_1,
    )

    plot_graph(
        df,
        x_col='temp',
        y_cols=[f'temp_error_{corner}' for corner in ['ff', 'fs', 'sf', 'ss', 'tt']],
        labels=['FF', 'FS', 'SF', 'SS', 'TT'],
        xlabel='Temperature [℃]',
        ylabel='Temperature Error [℃]',
        output_file=output_file_2,
    )

    # Print temperature error range
    temp_error_columns = [f'temp_error_{corner}' for corner in ['ff', 'fs', 'sf', 'ss', 'tt']]
    print(f"温度誤差の最大値: {df[temp_error_columns].max().max():.2f}")
    print(f"温度誤差の最小値: {df[temp_error_columns].min().min():.2f}")


# csv_file_path = 'Temp_Sensor_Core_PMOS_ADC/rppoly_mim_cap_freq_test.csv'  # CSVファイルのパス
# csv_file_name = 'Temp_Sensor_Core_PMOS_ADC/corrected_data.csv'
# output_file_1 = 'Temp_Sensor_Core_PMOS_ADC/test_comp_out_after_correction.png'
# output_file_2 = "Temp_Sensor_Core_PMOS_ADC/test_temperature_error_graph.png"

# csv_file_path = '2024情報映像メディア学会/comp_opamp_real/tdiff_real_opamp_comp_2times_period_0.85.csv'  # CSVファイルのパス
# csv_file_name = 'Temp_Sensor_Core_PMOS_ADC/pulse_width_test/corrected_data.csv'
# output_file_1 = 'Temp_Sensor_Core_PMOS_ADC/pulse_width_test/test_comp_out_after_correction.png'
# output_file_2 = "Temp_Sensor_Core_PMOS_ADC/pulse_width_test/test_temperature_error_graph.png"

csv_file_path = 'Temp_Sensor_Core_PMOS_ADC/rppoly_mim_cap_freq_BJT_test/rppoly_mim_cap_freq_BJT_test.csv'  # CSVファイルのパス
csv_file_name = 'Temp_Sensor_Core_PMOS_ADC/rppoly_mim_cap_freq_BJT_test/corrected_data.csv'
output_file_1 = 'Temp_Sensor_Core_PMOS_ADC/rppoly_mim_cap_freq_BJT_test/test_comp_out_after_correction.png'
output_file_2 = "Temp_Sensor_Core_PMOS_ADC/rppoly_mim_cap_freq_BJT_test/test_temperature_error_graph.png"

# データの処理とグラフの生成
process_temperature_data(csv_file_path, csv_file_name, output_file_1, output_file_2)