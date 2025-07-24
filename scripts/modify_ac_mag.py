import os
import pandas as pd

# Set the directory containing the CSV files
dirs =  ['../data/alhic2201','../data/alhic2302']  # Change this if needed

for directory in dirs:

    # Loop through files in the directory
    for filename in os.listdir(directory):
        if filename.endswith("-AC.csv"):  # Identify target files
            file_path = os.path.join(directory, filename)
            old_file_path = os.path.join(directory, f"OLD_{filename}")

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Check if the 'meas' column exists
            if 'meas' in df.columns:

                # Modify the 'meas' column
                df['meas'] = df['meas'] / 2

                # Rename the original file
                os.rename(file_path, old_file_path)

                # Save the modified file under the original name
                df.to_csv(file_path, index=False)

                print(f"    Processed: {filename}")
            else:
                print(f"    Skipping: {filename}")

    print("All matching files have been processed.")