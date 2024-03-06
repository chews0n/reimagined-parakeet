import pandas as pd
import os

class AESOmerger:
    def __init__(self, folder_path):
        """Initialize the AESOmerger with the folder containing the CSV files."""
        self.folder_path = folder_path

    def merge_aeso_files(self, file_prefix, start_year, end_year, output_file):
        """A method to merge CSV files."""
        merged_data = []

        for year in range(start_year, end_year + 1):
            file_name = f"{file_prefix}_{year}.csv"
            file_path = os.path.join(self.folder_path, file_name)
            
            if os.path.exists(file_path):
                # Check if the file_path of CSV files exists.
                df = pd.read_csv(file_path)
                merged_data.append(df)
            else:
                print(f"File not found: {file_path}")

        if merged_data:
            # Check if merged_data list is not empty. Then, concat all dataframes into one.
            final_df = pd.concat(merged_data, ignore_index=True)
            final_df.to_csv(output_file, index=False)
            print(f"Merged data saved to {output_file}")
        else:
            print("No data to merge.")
