import pandas as pd 
import os
import glob 

folderpath = r"C:\Users\Gabriel\Desktop\Assignment 2\temperatures"

if not os.path.exists(folderpath):
    raise Exception("Folder does not exist!") #check for existence of folder

csv_files = glob.glob(os.path.join(folderpath, "*.csv")) #joins all csv files in the folder
if not csv_files:
    raise Exception("No CSV files found in the folder!") #check for existence of csv files

all_data = [pd.read_csv(file) for file in csv_files] #read all csv files into a list of dataframes
    
combined_data = pd.concat(all_data, ignore_index = True) #combine all dataframes into one list

extremes_data = combined_data[["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]] #filter the dataframe for all months


# print(combined_data) #print the first few rows of the combined dataframe
# print(combined_data.shape) #print the shape of the combined dataframe
# print(combined_data.columns) #print the columns of the combined dataframe
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Seasonal Average Temperatures - to 2 decimal places. Writen to a text file.

summer_data = combined_data[["December", "January", "February"]] #filter the dataframe for summer months
winter_data  = combined_data[["June", "July", "August"]] #filter the dataframe for winter months
autumn_data = combined_data[["March", "April", "May"]] #filter the dataframe for autumn months
spring_data = combined_data[["September", "October", "November"]] #filter the dataframe for spring months


with open(r"C:\Users\Gabriel\Desktop\Assignment 2\seasonal_average2.txt", "w") as f:
  print("Seasonal Average Temperatures: \n", file=f)
  print(f"The average temperature over winter is: {winter_data.mean().mean():.2f}°C", file=f) #print the average temperature over winter
  print(f"The average temperature over summer is: {summer_data.mean().mean():.2f}°C", file=f) #print the average temperature over summer
  print(f"The average temperature over autumn is: {autumn_data.mean().mean():.2f}°C", file=f) #print the average temperature over autumn
  print(f"The average temperature over spring is: {spring_data.mean().mean():.2f}°C", file=f) #print the average temperature over spring


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Temerature Extremes (aesthetics only)

max_temp = extremes_data.max(axis=1).max()#find the maximum value temperature in the dataframe
min_temp = extremes_data.min(axis=1).min()#find the minimum value temperature in the dataframe

max_idx = extremes_data.max(axis=1).idxmax() #find the relevant index of the maximum temperature
min_idx = extremes_data.min(axis=1).idxmin() #find the relevant index of the minimum temperature
max_loc = combined_data.loc[max_idx, "STATION_NAME"] #link the index to the location name
min_loc = combined_data.loc[min_idx, "STATION_NAME"] #link the index to the location name

print(f"The highest temperature recorded was {max_temp}°C in {max_loc} ") #print the maximum temperature and the year it occurred
print(f"The lowest temperature recorded was {min_temp}°C in {min_loc} ") #print the minimum temperature and the year it occurred
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Temperature ranges individual (aesthetics only-help for verification of range calculations)

row_max = extremes_data.max(axis=1) #find the maximum value temperature in each row
row_min = extremes_data.min(axis=1) #find the minimum value temperature in each row
temp_range = row_max - row_min

range_largest = temp_range.max() #find largest range 
range_lrg_idx = extremes_data.max(axis=1).idxmax() #identify index of largest range
range_lrg_loc = combined_data.loc[range_lrg_idx, "STATION_NAME"] #filter through station names for largest range

range_smallest = temp_range.min() #find smallest range 
range_sml_idx = extremes_data.min(axis=1).idxmax()
range_sml_loc = combined_data.loc[range_sml_idx, "STATION_NAME"]

print(f"The smallest range is {range_sml_loc} at {range_smallest:.2f}°C")
print(f"The largest range is {range_lrg_loc} at {range_largest:.2f}°C")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Temperatrue ranges top 5 and bottom 5 to 2 decimal places with no duplicates. Writen to a text file.

combined_data["Temp Range"] = extremes_data.max(axis=1) - extremes_data.min(axis=1) #calculate and create a new column in the dataframe for the temperature range

max_index_per_station = combined_data.groupby("STATION_NAME")["Temp Range"].idxmax() # find index with max temperature range for each station
station_max_rows = combined_data.loc[max_index_per_station] #get the full rows for those indices and there for the stations
range_large = station_max_rows.sort_values(by="Temp Range", ascending = False).head(5) #get the top 5 largest ranges
range_large["Temp Range"] = range_large["Temp Range"].apply(lambda x: f"{x:.2f}°C") #apply round to 2 decimal places and add °C

min_index_per_station = combined_data.groupby("STATION_NAME")["Temp Range"].idxmin() # find index with min temperature range for each station
station_min_rows = combined_data.loc[min_index_per_station] #get the full rows for those indices and there for the stations
range_small = station_min_rows.sort_values(by="Temp Range", ascending = True).head(5) #get the top 5 smallest ranges
range_small["Temp Range"] = range_small["Temp Range"].apply(lambda x: f"{x:.2f}°C") #apply round to 2 decimal places and add °C

with open(r"C:\Users\Gabriel\Desktop\Assignment 2\temperature_ranges.txt", "w") as f:
  print("5 largest range/s:", file=f)
  print(range_large[["STATION_NAME", "Temp Range"]].to_string(index = False), file=f) #largest ranges
  print("\n5 smallest range/s:", file=f)
  print(range_small[["STATION_NAME", "Temp Range"]].to_string(index = False), file=f) #smallest ranges

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Temperature deviation top 5 and bottom 5 to 2 decimal places with no duplicates. Writen to a text file.

combined_data["Deviation"] = extremes_data.std(axis=1) #deviate each station's temperature data and create a column

max_station_devs = combined_data.groupby("STATION_NAME")["Deviation"].idxmax() #find the index of the maximum deviation for each station
station_max_dev = combined_data.loc[max_station_devs] #get the full rows for those indices and there for the stations
dev_large = station_max_dev.sort_values(by="Deviation", ascending =True).head(5) #get the top 5 largest deviations
dev_large["Deviation"] = dev_large["Deviation"].apply(lambda x: f"{x:.2f}°C") #apply round to 2 decimal places and add °C

min_station_devs = combined_data.groupby("STATION_NAME")["Deviation"].idxmin() #find the index of the minimum deviation for each station
station_min_dev = combined_data.loc[min_station_devs] #get the full rows for those indices and there for the stations
dev_small = station_min_dev.sort_values(by="Deviation", ascending =False).head(5) #get the top 5 smallest deviations
dev_small["Deviation"] = dev_small["Deviation"].apply(lambda x: f"{x:.2f}°C") #apply round to 2 decimal places and add °C

with open(r"C:\Users\Gabriel\Desktop\Assignment 2\temperature_deviations.txt", "w") as f:
    print("Top 5 largest deviations:", file=f)
    [print(dev_large[["STATION_NAME", "Deviation"]].to_string(index=False), file=f)] #largest deviations
    print("\nTop 5 smallest deviations:", file=f)
    [print(dev_small[["STATION_NAME", "Deviation"]].to_string(index=False), file=f)] #smallest deviations

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

