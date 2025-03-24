import pandas as pd

def read_csv(file_path):
  return pd.read_csv(file_path)

def calculate_difference(file1, file2, output_file):
  df1 = read_csv(file1)
  df2 = read_csv(file2)
  
  if df1.shape != df2.shape:
    raise ValueError("The two CSV files must have the same shape.")
  
  diff_df = df1.copy()
  diff_df.iloc[:, 1:] = df1.iloc[:, 1:] - df2.iloc[:, 1:]
  diff_df.to_csv(output_file, index=False)

# Example usage
file1 = 'Temp_Sensor_Core_PMOS_ADC/rppoly_mim_cap_freq_test/freq_ptat_sorted_curvature.csv'
file2 = 'Temp_Sensor_Core_PMOS_ADC/rppoly_mim_cap_freq_test/freq_ref_sorted_curvature.csv'
output_file = 'Temp_Sensor_Core_PMOS_ADC/rppoly_mim_cap_freq_test/freq_curvature_diff.csv'

calculate_difference(file1, file2, output_file)