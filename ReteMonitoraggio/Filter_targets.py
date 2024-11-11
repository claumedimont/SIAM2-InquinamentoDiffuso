'''
Code to filter the targets from a ready-to-import csv file with target information.
Filtering by npoints (number of records)
'''
# %%
import csv
import os
# Input and output file paths
in_dir = "C:/Users/user/OneDrive - Politecnico di Milano/SF2-Inquinamento_diffuso/Elaborazioni/E_AnalisiChimiche/Target_concentrazione_modello/"
input_csv = os.path.join(in_dir,"PCE_import.csv")
output_csv = os.path.join(in_dir,"PCE_filtered_30.csv")
# %%
# Open the input file for reading and the output file for writing
with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Skip the header row (column names)
    header_row = next(reader)

    # Write the header row to the output file as well (optional)
    writer.writerow(header_row)

    # Loop through the file to process observation points
    while True:
        try:
            # Read the header row (observation point metadata)
            header = next(reader)

            # Extract 'npoints' (number of time-series records) as an integer
            npoints = int(header[5].strip())  # 'npoints' is the 6th column

            # Skip this observation point if it has fewer than 10 records
            if npoints < 30:
                # Skip the next 'npoints' rows (time-series records)
                for _ in range(npoints):
                    next(reader)
                continue

            # Write the header row to the output file
            writer.writerow(header)

            # Write the time-series records for this observation point
            for _ in range(npoints):
                time_series_record = next(reader)
                writer.writerow(time_series_record)

        except StopIteration:
            # End of file reached
            break

print("Filtered observations saved to:", output_csv)

# %%
# count observation points
point_count = 0

# Open the filtered output file and count header rows
with open(output_csv, mode='r') as outfile:
    reader = csv.reader(outfile)

    # Skip the header row
    next(reader)

    # Loop through the rows and count header rows (assuming header rows have 'npoints' as the 6th column)
    for row in reader:
        # Check if the row is a header row by looking at the length (typically longer than time-series rows)
        if len(row) >= 6 and row[5].isdigit():
            point_count += 1

print(f"Total number of observation points in the output file: {point_count}")
# %%
#