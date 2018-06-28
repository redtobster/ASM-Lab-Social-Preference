from __future__ import division
from getting_excel import categorize_files, getting_name
import pandas as pd
import os
import math
import numpy as np
import re

# getting the directory that contains the excel files
desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
print('Input the folder in which the excel files are located:')
excel = raw_input('')
path = desktop + '\\Webcam\\' + excel + '\\'

# checker function to ensure the input is correct
def check_input(tank_length_or_width): # helper function to make sure input is integer
		while not bool(re.match('[0-9]+', str(tank_length_or_width))):
			print("Please enter a valid response (only integers)")
			tank_length_or_width = raw_input('')
		return tank_length_or_width

# getting the tank length (in mm) from the users
print('Input the tank length (in mm)')
tank_length = raw_input('')
tank_length = int(check_input(tank_length))

# getting the tank width (in mm) from the users
print('Input the tank width (in mm)')
tank_width = raw_input('')
tank_width = int(check_input(tank_width))

# getting the names of the excel file
print('organizing data..')
first_two_minutes_left, first_two_minutes_right, left_tank, right_tank = categorize_files(path)

# creating the csv file for the first excel file to have the header
# opening the excel file
file_name = path + left_tank[0]
df = pd.read_excel(io=file_name, sheet_name='Tank1', header=None)

# getting the index of 'x' and 'y'
def get_index_x_y(df):
    index_x = [0, 0]
    index_y = [0, 0]
    for row in list(df.index):
        for col in list(df.columns):
            if df.loc[row, col] == 'x':
                index_x[0] = row
                index_x[1] = col
            if df.loc[row, col] == 'y':
                index_y[0] = row
                index_y[1] = col
                return index_x, index_y

# home made arctan function that allows division by 0
def safe_arctan(n1, n2):
    if n2 == 0:
        if n1 >= 0:
            return(math.pi/2)
        else:
            return(-math.pi/2)
    else:
        return(np.arctan(n1/n2))

def compute_velocity_df(df, tank_length, tank_width):
	# giving names to the columns of the df
	col = 'col'
	col_names = [col + str(i) for i in range(len(df.columns))]
	df.columns = col_names

	# getting the indices where 'x' and 'y' are located in the excel file
	index_x, index_y = get_index_x_y(df)

	# getting the length and width of tanks in pixels. This part is still hard coded
	x_min = df.loc[5, 'col2']
	x_max = df.loc[6, 'col2']
	delta_x = x_max - x_min
	y_min = df.loc[5, 'col3']
	y_max = df.loc[6, 'col3']
	delta_y = y_max - y_min

	# deleting the frames in which the fish is not tracked
	row_number = index_x[0] + 2
	col_number = int(re.findall('[0-9]+', index_y[1])[0])
	i = row_number-1
	lst = []
	while (i < len(df)):
	    if (df.iloc[i, col_number-1] < x_min or df.iloc[i, col_number-1] > x_max):
	        lst.append(i)
	    elif (df.iloc[i, col_number] < y_min or df.iloc[i, col_number] > y_max):
	        lst.append(i)
	    i = i+1
	df.drop(df.index[lst], inplace=True)
	df = df.reset_index(drop=True)

	row_number = index_x[0] + 2
	col_number = int(re.findall('[0-9]+', index_y[1])[0])
	# computing the information about the velocity and assigning it to the rows
	for i in range(row_number, len(df)-1):
	    df.iloc[i+1, col_number+1] = (df.iloc[i+1, col_number-1] - df.iloc[i, col_number-1])*(tank_length/delta_x)
	    df.iloc[i+1, col_number+2] = (df.iloc[i+1, col_number] - df.iloc[i, col_number])*(tank_width/delta_y)
	    df.iloc[i+1, col_number+3] = math.sqrt((df.iloc[i+1, col_number+1])**2 + (df.iloc[i+1, col_number+2]**2))
	    df.iloc[i+1, col_number+4] = safe_arctan(df.iloc[i+1, col_number+2], df.iloc[i+1, col_number+1])

	# assigning the names of the header which the below rows contain info about velocity
	df.iloc[index_x[0], col_number+1], df.iloc[index_x[0], col_number+2], df.iloc[index_x[0], col_number+3], df.iloc[index_x[0], col_number+4] = 'velocity_x', 'velocity_y', 'velocity', 'angle'

	# dropping the first frame of the velocity row
	df.drop(index_x[0]+1, axis = 0, inplace = True)
	df.drop(index_x[0]+2, axis = 0, inplace = True)

	return df

# function to modify the excel in place with the velocity information
def modify_excel_with_velocity(excel_name):
	excel_name = path + excel_name
	df = pd.read_excel(io=excel_name, sheet_name=0, header=None)
	df = compute_velocity_df(df, tank_length, tank_width)
	df.to_excel(excel_name, 'Tank1', header=None, index=False)

# iterating through the excel files in the folder
for i in range(len(left_tank)):
	print('initializing sheet modification..')
	modify_excel_with_velocity(left_tank[i])
	print('computing velocity %s completed' % (left_tank[i]))

for i in range(len(right_tank)):
	modify_excel_with_velocity(right_tank[i])
	print('computing velocity %s completed' % (right_tank[i]))

for i in range(len(first_two_minutes_left)):
	modify_excel_with_velocity(first_two_minutes_left[i])
	print('computing velocity %s completed' % (first_two_minutes_left[i]))

for i in range(len(first_two_minutes_right)):
	modify_excel_with_velocity(first_two_minutes_right[i])
	print('computing velocity %s completed' % (first_two_minutes_right[i]))

print('sheet modification completed')