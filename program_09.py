
# coding: utf-8
#!/bin/env python
'''
Date created: 4/2/2020
Author: Gargeya Vunnava
Purdue username: vvunnava
Github name: gargeyavunnava
Assignment 09: Processing data to remove different type of errors
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
  
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""

    # Tracking index of values matching check01 conditions
    for i in range(len(DataDF.columns)):
        ReplacedValuesDF.iloc[:,i]=len(DataDF.loc[DataDF.iloc[:,i] == -999].index.tolist())
    
    #Replacing values in tracked index with NaN characters 
    DataDF = DataDF.replace(-999, np.nan)

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    # Precipitation column gross errors
    # Tracking index of values matching check02 conditions
    precip_gross_error_index = DataDF['Precip'].loc[(DataDF['Precip'] < 0) | (DataDF['Precip'] > 25)].index.tolist()
    for i in precip_gross_error_index:
        #Replacing values in tracked index with NaN characters 
        DataDF.loc[i,'Precip'] = np.nan
    ReplacedValuesDF.loc['2. Gross Error','Precip'] = len(precip_gross_error_index)

    # Max temp column gross errors
    # Tracking index of values matching check02 conditions
    max_T_gross_error_index = DataDF['Max Temp'].loc[(DataDF['Max Temp'] < -25) | (DataDF['Max Temp'] > 35)].index.tolist()
    for i in max_T_gross_error_index:
        #Replacing values in tracked index with NaN characters 
        DataDF.loc[i,'Max Temp'] = np.nan    
    ReplacedValuesDF.loc['2. Gross Error','Max Temp'] = len(max_T_gross_error_index)

    # Min temp column gross errors
    # Tracking index of values matching check02 conditions
    min_T_gross_error_index = DataDF['Min Temp'].loc[(DataDF['Min Temp'] < -25) | (DataDF['Min Temp'] > 35)].index.tolist()
    for i in min_T_gross_error_index:
        DataDF.loc[i,'Min Temp'] = np.nan 
    ReplacedValuesDF.loc['2. Gross Error','Min Temp'] = len(min_T_gross_error_index)

    # Wind speed column gross errors
    # Tracking index of values matching check02 conditions
    wind_gross_error_index = DataDF['Wind Speed'].loc[(DataDF['Wind Speed'] < 0) | (DataDF['Wind Speed'] > 35)].index.tolist()
    for i in wind_gross_error_index:
        #Replacing values in tracked index with NaN characters
        DataDF.loc[i,'Wind Speed'] = np.nan    
    ReplacedValuesDF.loc['2. Gross Error','Wind Speed'] = len(wind_gross_error_index)
    ReplacedValuesDF = ReplacedValuesDF.replace(np.nan,0)

    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    #Tracking index of values that have to swapped based on check03 conditions
    swap_index = DataDF.loc[DataDF['Max Temp']<DataDF['Min Temp']].index.tolist()
    #swapping values at tracked index locations
    for i in swap_index:
        tmp = DataDF.loc[i,'Min Temp']
        DataDF.loc[i,'Min Temp'] = DataDF.loc[i,'Max Temp']
        DataDF.loc[i,'Max Temp'] = tmp
    ReplacedValuesDF.loc['3. Swapped','Min Temp'] = len(swap_index)
    ReplacedValuesDF.loc['3. Swapped','Max Temp'] = len(swap_index)
    ReplacedValuesDF = ReplacedValuesDF.replace(np.nan,0)
    
    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    #Tracking index of values that have to swapped based on check04 conditions
    range_exceed_index = DataDF.loc[((DataDF['Max Temp'] - DataDF['Min Temp'])>25)].index.tolist()
    for i in range_exceed_index:
        #Replaing values are tracked index locations with NaN characters
        DataDF.loc[i,'Min Temp'] = np.nan
        DataDF.loc[i,'Max Temp'] = np.nan
    ReplacedValuesDF.loc['4. Range','Min Temp'] = len(range_exceed_index)
    ReplacedValuesDF.loc['4. Range','Max Temp'] = len(range_exceed_index)
    ReplacedValuesDF = ReplacedValuesDF.replace(np.nan,0)
    return( DataDF, ReplacedValuesDF )
    
# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':
    
    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
   
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)

    
#writing the processed data into a file (in the original format)
DataDF.to_csv("DataQualityChecking_postchecking.txt", header=None, sep=' ')

#Writing the info about replaced values in a txt file
ReplacedValuesDF.to_csv("Replaced_values_info.txt", sep="\t")   


#Loading unprocessed data to a dataframe
df = ReadData(fileName)[0]

# Plotting data for each variable before and after checks
df = pd.concat([df,DataDF], axis=1)
variables = DataDF.columns.tolist()
variables_full_names = ['Daily precipitation - mm', 'maximum air temperature - degree C','minimum air temperature - degree C','wind speed - meters per second']

for i in range(len(variables)):
    df1 = df[variables[i]]
    df1.columns = ['before checks','after checks']
    fig1 = df1.plot(color=['r','b'],alpha=0.65,figsize = (7,5))
    fig1.set_ylabel(variables_full_names[i]) # set y label
    fig1.set_xlabel('Date') # set x label
    fig1.set_title(variables_full_names[i]+' - before and after checks')
    plt.savefig(variables_full_names[i]+'.svg')
    plt.close() #remove this line to get inline plots

