import os                       #used to interact with os creating paths and navigate files 
import glob                     #used to match and join csv files 
import pandas as pd             #used to read the data from csv files and basic format it  
from tabulate import tabulate   #used to create clean looking table form

# ------------------------- Read CSV folder -------------------------
def read_csv_folder(folderpath):
    if not os.path.exists(folderpath):
        raise Exception("Folder does not exist!")             # Check for existence of folder
    csv_files = glob.glob(os.path.join(folderpath, "*.csv"))  # Joins all csv files in the folder
    if not csv_files:
        raise Exception("No CSV files found in the folder!")  # Check for existence of csv files
    all_data = [pd.read_csv(file) for file in csv_files]      # Read all csv files into a list of dataframes
    return pd.concat(all_data, ignore_index=True)

# ------------------------- Seasonal averages -------------------------
def seasonal_averages(df):
    seasons = {
        "Summer": ["December", "January", "February"],
        "Winter": ["June", "July", "August"],
        "Autumn": ["March", "April", "May"],
        "Spring": ["September", "October", "November"] 
    }                                                         # Define seasons with corresponding months
    averages = {}                                             # Dictionary to hold seasonal averages
    for season, months in seasons.items():                  
        averages[season] = df[months].mean().mean()           # Calculate the mean temperature for each season    
    return averages

def write_seasonal_averages(averages, filepath):               # Write seasonal averages to a text file
    with open(filepath, "w") as f:
        print("Seasonal Average Temperatures:\n", file=f)
        for season, avg in averages.items():
            print(f"The average temperature over {season.lower()} is: {avg:.2f}°C", file=f)  # Print formatted average

# ------------------------- Temperature extremes -------------------------
def temperature_extremes(df):
    months = df.columns.drop(["STATION_NAME", "LAT", "LON", "STN_ID"])
    max_temp = df[months].max(axis=1).max()                                     # Find the maximum temperature in the dataframe
    min_temp = df[months].min(axis=1).min()                                     # Find the minimum temperature in the dataframe                                                       
    max_idx = df[months].max(axis=1).idxmax()                                   # Find the relevant index of the maximum temperature
    min_idx = df[months].min(axis=1).idxmin()                                   # Find the relevant index of the minimum temperature
    max_loc = df.loc[max_idx, "STATION_NAME"]
    min_loc = df.loc[min_idx, "STATION_NAME"]                                   # Link the index to the location name
    print(f"The highest temperature recorded was {max_temp}°C in {max_loc}")   
    print(f"The lowest temperature recorded was {min_temp}°C in {min_loc}")      # Print the results   
    return max_temp, min_temp, max_loc, min_loc

# ------------------------- Top/Bottom Temperature Ranges -------------------------
def top_bottom_ranges(df, months): 
    df = df.copy()                                                                    # Work on a copy to avoid modifying original dataframe
    df["Min Temp"] = df[months].min(axis=1)
    df["Max Temp"] = df[months].max(axis=1)                                           #receive max and min values as columns 
    df["Temp Range"] = df["Max Temp"] - df["Min Temp"]                                #gives ranges column

    max_idx = df.groupby("STATION_NAME")["Temp Range"].idxmax()                       # Get the row index of the maximum "Temp Range" for each station
    min_idx = df.groupby("STATION_NAME")["Temp Range"].idxmin()                       #same for minimum 

    max_rows = df.loc[max_idx].sort_values("Temp Range", ascending=False).head(5)     #top 5 results 
    min_rows = df.loc[min_idx].sort_values("Temp Range", ascending=True).head(5)      #bottom 5 results 

   
    for col in ["Min Temp", "Max Temp", "Temp Range"]:
        max_rows[col] = max_rows[col].apply(lambda x: f"{x:.2f}°C")                    # Format values to 2 decimal places with degree celcius   
        min_rows[col] = min_rows[col].apply(lambda x: f"{x:.2f}°C")

    return max_rows, min_rows

# ------------------------- Top/Bottom Temperature Deviations -------------------------
def top_bottom_deviations(df, months):    

    month_data = df[months].copy()
    df = df.copy()                                                                   # Work on a copy to avoid modifying original dataframe
    df["Deviation"] = month_data.std(axis=1)                                         # Calculate standard deviation for each station
    max_idx = df.groupby("STATION_NAME")["Deviation"].idxmax()                       # Get index of max deviation per station
    min_idx = df.groupby("STATION_NAME")["Deviation"].idxmin()                       # Get index of min deviation per station
    max_rows = df.loc[max_idx].sort_values("Deviation", ascending=False).head(5)     # Get top 5 rows with largest deviations
    min_rows = df.loc[min_idx].sort_values("Deviation", ascending=True).head(5)      # Get top 5 rows with smallest deviations
    max_rows["Deviation"] = max_rows["Deviation"].apply(lambda x: f"{x:.2f}°C")      # Format deviations
    min_rows["Deviation"] = min_rows["Deviation"].apply(lambda x: f"{x:.2f}°C")
    return max_rows, min_rows

# ------------------------- Tabulate for top/bottom ranges -------------------------    

def write_top_bottom_table(max_rows, min_rows, filepath, column_name):                         # Write top/bottom tables to a text file
    with open(filepath, "w") as f:
        if column_name == "Temp Range":
            print(f"Top 5 largest {column_name}:\n", file=f)
            print(tabulate(max_rows[["STATION_NAME", "Min Temp", "Max Temp", column_name]],    #if for the min and max temp to be included in column- "temp_range" 
                           headers="keys", tablefmt="pretty", showindex=False), file=f)         #tabulate used to format table- columun name and data specified 

            print(f"\nTop 5 smallest {column_name}:\n", file=f)
            print(tabulate(min_rows[["STATION_NAME", "Min Temp", "Max Temp", column_name]], 
                           headers="keys", tablefmt="pretty", showindex=False), file=f)
        else:
            print(f"Top 5 largest {column_name}:\n", file=f)                                       #else for other conditions- deviation 
            print(tabulate(max_rows[["STATION_NAME", column_name]],                                #tabulate used to format table- columun name and data specified 
                           headers="keys", tablefmt="pretty", showindex=False), file=f)

            print(f"\nTop 5 smallest {column_name}:\n", file=f)
            print(tabulate(min_rows[["STATION_NAME", column_name]], 
                           headers="keys", tablefmt="pretty", showindex=False), file=f)
            
# ------------------------- Example usage -------------------------
if __name__ == "__main__":
    # --- User-defined paths ---
    folderpath = input("Enter folder path containing CSV files: ")             #Define folder path for input files
    folderpath = folderpath.strip().strip('"').strip("'")                      # Clean up input path

    output_folder = input("Enter folder path to save output files: ")          #Define folder path for output files
    output_folder = output_folder.strip().strip('"').strip("'")                # Clean up input path

    os.makedirs(output_folder, exist_ok=True)                                  # Create output folder if it doesn't exist

    # --- Read data ---
    data = read_csv_folder(folderpath) 

    # --- Seasonal averages ---
    averages = seasonal_averages(data)
    write_seasonal_averages(averages, os.path.join(output_folder, "average_temp.txt"))  # Write seasonal averages to file

    # --- Temperature extremes ---
    temperature_extremes(data)

    # --- Months list for ranges and deviations ---
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

    # --- Top/Bottom Ranges ---
    range_max, range_min = top_bottom_ranges(data, months)
    write_top_bottom_table(range_max, range_min, os.path.join(output_folder, "largest_temp_range_station.txt"), "Temp Range")

    # --- Top/Bottom Deviations ---
    dev_max, dev_min = top_bottom_deviations(data, months)
    write_top_bottom_table(dev_max, dev_min, os.path.join(output_folder, "temperature_stability_stations.txt"), "Deviation")


