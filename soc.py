import pandas as pd
import requests
from datetime import datetime, time
import io

# URL to your Google Sheet CSV export
sheet_url = "https://docs.google.com/spreadsheets/d/12R7-BG7LlopWHAY5sheyupNvHfgDffhMovkXis-63dc/export?format=csv&gid=237457137"

# Fetch the CSV data
response = requests.get(sheet_url)
response.raise_for_status()  # Check if the request was successful

# Save the content to a CSV file
csv_content = response.content.decode('utf-8')

# Read the CSV content into a DataFrame, ensuring the first row is included
data = pd.read_csv(io.StringIO(csv_content), header=None)

# Indexes for columns
index_time = 21  # "V" column index (22nd column, 0-indexed)
index_ip = 40    # "AO" column index (41st column, 0-indexed)

# Extract the relevant columns
time_data = data.iloc[:, index_time].astype(str)
ip_data = data.iloc[:, index_ip].astype(str)

# Create a new DataFrame with the extracted columns
details_df = pd.DataFrame({'row_number': data.index, 'ip': ip_data, 'time': time_data})

# Debug: Check the extracted data
print("Extracted time data head:")
print(time_data.head())
print("\nExtracted IP data head:")
print(ip_data.head())

# Function to clean the IP data and validate time data
def clean_ip(ip):
    return ip.strip(' "\'')

def valid_time(t):
    try:
        return datetime.strptime(t, "%H:%M:%S").time()
    except ValueError:
        return None

# Clean up the IP data and validate time data
details_df['ip'] = details_df['ip'].apply(clean_ip)
details_df['time'] = details_df['time'].apply(valid_time)

# Debug: Check the cleaned data
print("\nCleaned Details DataFrame head:")
print(details_df.head())

# Remove rows with invalid times
details_df = details_df.dropna(subset=['time'])

# Define working hours (9 AM to 6 PM)
start_time = time(9, 0, 0)
end_time = time(18, 0, 0)

# Filter records outside working hours
non_working_hours_data = details_df[(details_df['time'] < start_time) | (details_df['time'] > end_time)]

# Display the resulting DataFrame
print("\nNon-working hours DataFrame head:")
print(non_working_hours_data.head())

# Output the result in simple format: row_number, IP, and time
print("\nRow number, IP, and Time outside working hours:")
for index, row in non_working_hours_data.iterrows():
    print(f"Row: {row['row_number']}, IP: {row['ip']}, Time: {row['time']}")

# Calculate the number of unique IPs
unique_ips = non_working_hours_data['ip'].unique()
num_unique_ips = len(unique_ips)

# Display the number of unique IPs and the list of those IPs
print(f"\nNumber of unique IPs outside working hours: {num_unique_ips}")
print("List of unique IPs outside working hours:")
for ip in unique_ips:
    print(ip)
