import pandas as pd
import numpy as np

NumberOfInterpolatedValues = 500

# Read the CSV files
csv1 = pd.read_csv('merged_data.csv')
csv2 = pd.read_csv('right_hand_pick_and_place_joint_states.csv')

# Ensure the CSVs have the same columns
assert csv1.columns.equals(csv2.columns), "CSV files must have the same columns"

# Get the last row of csv1 and the first row of csv2
last_row_csv1 = csv1.iloc[-1]
first_row_csv2 = csv2.iloc[0]

# Create a DataFrame for the interpolated values
interpolated_values = pd.DataFrame([np.linspace(last_row_csv1[i], first_row_csv2[i], num=NumberOfInterpolatedValues) for i in range(len(last_row_csv1))]).T
interpolated_values.columns = csv1.columns

# Get the last timestamp of csv1
last_timestamp_csv1 = csv1.iloc[-1, 0]

# Adjust the timestamps in the first column of the interpolated values
interpolated_values.iloc[:, 0] = last_timestamp_csv1 + 0.005 * np.arange(1, NumberOfInterpolatedValues + 1)

# Get the last timestamp of the interpolated values
last_timestamp_interpolated = interpolated_values.iloc[-1, 0]

# Adjust the timestamps in the first column of csv2
csv2.iloc[:, 0] = last_timestamp_interpolated + 0.005 * np.arange(1, len(csv2) + 1)

# Merge the CSV files with interpolation
merged_csv = pd.concat([csv1, interpolated_values, csv2])

# Ensure the merged CSV has the same columns as the input CSVs
merged_csv.columns = csv1.columns

# Save the merged CSV to a new file
merged_csv.to_csv('merged_data.csv', index=False, encoding='utf-8', lineterminator='\n')