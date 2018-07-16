from __future__ import division
import pandas as pd
import math
import numpy as np

# checker function to ensure the input is correct
def check_input(tank_length_or_width): # helper function to make sure input is integer
		while not bool(re.match('[0-9]+', str(tank_length_or_width))):
			print("Please enter a valid response (only integers)")
			tank_length_or_width = raw_input('')
		return tank_length_or_width

# home made arctan function that allows division by 0
def safe_arctan(n1, n2):
    if n2 == 0:
        if n1 >= 0:
            return(math.pi/2)
        else:
            return(-math.pi/2)
    else:
        return(np.arctan(n1/n2))

# Preparatory function to get the location (quadrant) based on x and y axes.
def determine_quad_left_tank(x, y, x_mid, y_mid):
    quad = 'somestring'
    if x < x_mid:
        if y > y_mid:
            quad = 'Q1'
        else:
            quad = 'Q3'
    elif x >= x_mid:
        if y > y_mid:
            quad = 'Q2'
        else:
            quad = 'Q4'
    return quad

def determine_quad_right_tank(x, y, x_mid, y_mid):
    quad = 'somestring'
    if x < x_mid:
        if y > y_mid:
            quad = 'Q2'
        else:
            quad = 'Q4'
    elif x >= x_mid:
        if y > y_mid:
            quad = 'Q1'
        else:
            quad = 'Q3'
    return quad

def compute_velocity_df(df, tank_length, tank_width, direction):
	# giving names to the columns of the df
	col = 'col'
	col_names = [col + str(i) for i in range(len(df.columns))]
	df.columns = col_names

	# getting the length and width of tanks in pixels. This part is still hard coded
	x_min, x_max, y_min, y_max = df.loc[5, 'col2'], df.loc[6, 'col2'], df.loc[5, 'col3'], df.loc[6, 'col3']
	delta_x, x_mid, delta_y, y_mid= x_max - x_min, (x_max + x_min)/2, y_max - y_min, (y_max + y_min)/2
	# getting the indices where 'x' and 'y' are located in the excel file
	index_x, index_y = get_index_x_y(df)
	index_fps = get_index_fps(df)
	frame_rate = int(re.findall('[0-9]+', df.loc[index_fps[0], index_fps[1]])[0])

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

	print('computing velocity..')
	row_number = index_x[0] + 2
	col_number = int(re.findall('[0-9]+', index_y[1])[0])
	# computing the information about the velocity and assigning it to the rows
	for i in range(row_number, len(df)-1):
	    df.iloc[i+1, col_number+1] = (df.iloc[i+1, col_number-1] - df.iloc[i, col_number-1])*(tank_length/delta_x)
	    df.iloc[i+1, col_number+2] = (df.iloc[i+1, col_number] - df.iloc[i, col_number])*(tank_width/delta_y)
	    df.iloc[i+1, col_number+3] = math.hypot(df.iloc[i+1, col_number+1], df.iloc[i+1, col_number+2])
	    df.iloc[i+1, col_number+4] = safe_arctan(df.iloc[i+1, col_number+2], df.iloc[i+1, col_number+1])

	# assigning the names of the header which the below rows contain info about velocity
	df.iloc[index_x[0], col_number+1], df.iloc[index_x[0], col_number+2], df.iloc[index_x[0], col_number+3], df.iloc[index_x[0], col_number+4] = 'velocity_x', 'velocity_y', 'velocity', 'angle'

	# dropping the first frame of the velocity row
	df.drop(index_x[0]+1, axis = 0, inplace = True)
	df.drop(index_x[0]+2, axis = 0, inplace = True)
	df.reset_index(drop = True, inplace = True)
	
	print('adding freeze counts and locations..')
	# the logic to get the per sec speed and the freeze info
	body_length = 35 # body length is hard coded here. It is assumed to be 35mm
	lst = []
	freeze_info = []
	counter = 0
	acc_value = 0
	i = index_x[0] + 1
	while (i < len(df)):
	    if counter == frame_rate:
	        if acc_value < (body_length * 0.1):
	        	if direction == 'left':
		            quad = determine_quad_left_tank(df.loc[i, index_x[1]], df.loc[i,index_y[1]], x_mid, y_mid)
		        elif direction == 'right':
		        	quad = determine_quad_right_tank(df.loc[i, index_x[1]], df.loc[i,index_y[1]], x_mid, y_mid)
		        while (acc_value < body_length * 0.1):
		        	acc_value = acc_value + df.iloc[i, col_number+3]
		        	i = i + 1
		        	counter = counter + 1
		        freeze_duration = (counter/frame_rate)
		        freeze_info.append((quad, freeze_duration, str(i-counter) + '-' + str(i)))
		        counter = 0
	        counter = 0
	        lst.append(acc_value)
	        acc_value = 0
	        i = i + 1
	    else:
	        counter = counter + 1
	        acc_value = acc_value + df.loc[i, index_fps[1]]
	        i = i + 1

	# setting up the dataframe for writing
	df_velocity = pd.DataFrame(lst)
	df_velocity.set_index(df_velocity.index + 1, inplace = True)
	df_velocity.columns = ['Velocity (mm/s)']
	# check first if freeze_info is empty (does not contain any freezing episode)
	if not freeze_info:
		df_freeze_info = pd.DataFrame(freeze_info)
	else:
		df_freeze_info = pd.DataFrame(freeze_info)
		df_freeze_info.columns = ['Location', 'Duration (s)', 'Frame Number']

	return df, df_velocity, df_freeze_info

# function to modify the excel in place with the velocity information
def modify_excel_with_velocity(excel_name, direction):
	excel_name = path + excel_name
	df = pd.read_excel(io=excel_name, sheet_name='Tank1', header=None)
	df, df_velocity, df_freeze_info = compute_velocity_df(df, tank_length, tank_width, direction)
	writer = pd.ExcelWriter(excel_name)
	df.to_excel(writer, sheet_name = 'Tank1', header=None, index=False)
	df_velocity.to_excel(writer, sheet_name = 'Velocity per Second')
	df_freeze_info.to_excel(writer, sheet_name = 'Freeze Analysis', index=False)
	writer.save()
