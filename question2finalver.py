#question 2 with def

import os
import glob
import pandas as pd

def load_csv_data(folderpath):
    if not os.path.exists(folderpath):
        raise Exception("Folder does not exist!") #check for existence of folder

    csv_files = glob.glob(os.path.join(folderpath, "*.csv")) #joins all csv files in the folder
    if not csv_files:
        raise Exception("No CSV files found in the folder!") #check for existence of csv files

    all_data = [pd.read_csv(file) for file in csv_files] #read all csv files into a list of dataframes
        
    combined_data = pd.concat(all_data, ignore_index = True) #combine all dataframes into one list

    extremes_data = combined_data[["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]] #filter the dataframe for all months
    
    return combined_data, extremes_data

def temp_average(folderpath, outpath):
    combined_data = load_csv_data(folderpath)

    summer_data = combined_data[["December", "January", "February"]] #filter the dataframe for summer months
    winter_data  = combined_data[["June", "July", "August"]] #filter the dataframe for winter months
    autumn_data = combined_data[["March", "April", "May"]] #filter the dataframe for autumn months
    spring_data = combined_data[["September", "October", "November"]] #filter the dataframe for spring months


    with open(outpath, "w") as f:
      print("Seasonal Average Temperatures: \n", file=f)
      print(f"The average temperature over winter is: {winter_data.mean().mean():.2f}°C", file=f) #print the average temperature over winter
      print(f"The average temperature over summer is: {summer_data.mean().mean():.2f}°C", file=f) #print the average temperature over summer
      print(f"The average temperature over autumn is: {autumn_data.mean().mean():.2f}°C", file=f) #print the average temperature over autumn
      print(f"The average temperature over spring is: {spring_data.mean().mean():.2f}°C", file=f) #print the average temperature over spring

outpath = r"C:\Users\Gabriel\Desktop\Assignment 2\seasonal_average.txt"
folderpath = r"C:\Users\Gabriel\Desktop\Assignment 2\temperatures"