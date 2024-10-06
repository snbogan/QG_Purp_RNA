import os
import pandas as pd

# Function to parse the alignment summary
def parse_summary(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Extract sample name from file name
    sample_name = os.path.basename(file_path).split('.')[0]

    # Number of reads
    num_reads = int(lines[0].split(' ')[0])

    # Mapping rates
    aligned_0_times = int(lines[2].split(' ')[4])
    aligned_1_time = int(lines[3].split(' ')[4])
    aligned_more_than_1_time = int(lines[4].split(' ')[4])
    total_mapping_rate = float(lines[5].split('%')[0].strip())

    # Calculate uniquely and multi-mapping rates
    unique_mapping_rate = (aligned_1_time / num_reads) * 100
    multi_mapping_rate = (aligned_more_than_1_time / num_reads) * 100

    return {
        'Sample': sample_name,
        'Total Reads': num_reads,
        'Total Mapping Rate (%)': total_mapping_rate,
        'Unique Mapping Rate (%)': unique_mapping_rate,
        'Multi-Mapping Rate (%)': multi_mapping_rate
    }

# Function to process all summaries in a directory
def process_summaries(directory):
    summary_data = []

    for file_name in os.listdir(directory):
        if file_name.endswith('.align_summary.txt'):
            file_path = os.path.join(directory, file_name)
            summary_data.append(parse_summary(file_path))

    return pd.DataFrame(summary_data)

# Main script
def main(input_dir, output_csv):
    df = process_summaries(input_dir)
    df.to_csv(output_csv, index=False)
    print(f'Summary exported to {output_csv}')

# Usage
if __name__ == "__main__":
    input_directory = os.path.expanduser('~/Documents/GitHub/Cross_pHox/Hisat2_Alignment/')  # Update with the path to your directory
    output_file = 'alignment_summary_comb.csv'  # Update with your desired output file name
    main(input_directory, output_file)
