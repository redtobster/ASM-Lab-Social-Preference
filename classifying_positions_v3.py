import pandas as pd
import numpy as np
import re

# Functions to automatically get the index of 'x', 'y', 'fps' and 'FishSex' in a dataframe
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

def get_index_sex(df):
    index_sex = [0, 0]
    df = df.fillna('empty')
    for row in list(df.index):
        for col in list(df.columns):
            if bool(re.match('FishSex.*', str(df.loc[row, col]))):
            	index_sex[0] = row
                index_sex[1] = col
                return index_sex

def get_index_fps(df):
    index_fps = [0, 0]
    df = df.fillna('empty')
    for row in list(df.index):
        for col in list(df.columns):
            if bool(re.match('FrameRate.*', str(df.loc[row, col]))):
                index_fps[0] = row
                index_fps[1] = col
                return index_fps

# functions to assign x,y positions to their respective quadrants for the first two minutes
# and the entire experiment
def assign_left_tank(df_left_tank, excel_name):
	# giving names to the columns of the df
	col = 'col'
	col_names = [col + str(i) for i in range(len(df_left_tank.columns))]
	df_left_tank.columns = col_names

	# Getting the indices of the 'x', 'y', 'sex' and 'framerate'
	index_x, index_y = get_index_x_y(df_left_tank)
	index_sex = get_index_sex(df_left_tank)
	index_fps = get_index_fps(df_left_tank)

	# parameters that should be obtained from the excel files
	frame_rate = int(re.findall('[0-9]+', df_left_tank.loc[index_fps[0], index_fps[1]])[0]) # usually 12 fps
	experiment_time = (df_left_tank.shape[0] / frame_rate) / 60 # experiment time is in minutes
	sex = re.match('FishSex:(.*)', df_left_tank.loc[index_sex[0], index_sex[1]]).group(1) 

	# creating data frame for each quadrant depending on the parameters above
	df_quad1 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_quad2 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_quad3 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_quad4 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_half1 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_half2 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))

	# determining key positions in the tank to create the quadrants
	x_min = df_left_tank.loc[5, 'col2']
	x_max = df_left_tank.loc[6, 'col2']
	x_mid = (x_min + x_max)/2
	y_min = df_left_tank.loc[5, 'col3']
	y_max = df_left_tank.loc[6, 'col3']
	y_mid = (y_min + y_max)/2

	# creating the for loop to assign which quadrant the fish belongs at a given time after the first two minutes
	# start at column 3 because the first two columns are for the name and the sex
	column_no = 3
	# get the row number in which the values of 'x' and 'y' first appear. The values below the row can be extracted immediately 
	row_number_x_and_y = index_x[0] + 1
	for i in range(row_number_x_and_y, len(df_left_tank)):
	    if ((i-9) % (frame_rate*60) == 0) and (column_no < len(df_quad1.columns)):
	        column_no = column_no + 1
	        if df_left_tank.loc[i, index_x[1]] < x_mid:
	            if df_left_tank.loc[i, index_y[1]] > y_mid:
	                df_quad1.loc[0, column_no] = int(df_quad1.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	            else:
	                df_quad3.loc[0, column_no] = int(df_quad3.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	        elif df_left_tank.loc[i, index_y[1]] > y_mid:
	            df_quad2.loc[0, column_no] = int(df_quad2.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	        else:
	            df_quad4.loc[0, column_no] = int(df_quad4.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	    else:
	        if df_left_tank.loc[i, index_x[1]] < x_mid:
	            if df_left_tank.loc[i, index_y[1]] > y_mid:
	                df_quad1.loc[0, column_no] = int(df_quad1.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	            else:
	                df_quad3.loc[0, column_no] = int(df_quad3.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	        elif df_left_tank.loc[i, index_y[1]] > y_mid:
	            df_quad2.loc[0, column_no] = int(df_quad2.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	        else:
	            df_quad4.loc[0, column_no] = int(df_quad4.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1

	column_no = 3
	for i in range(10, len(df_left_tank)):
	    if ((i-9) % (frame_rate*60) == 0) and (column_no < len(df_quad1.columns)):
	        column_no = column_no + 1
	        if df_left_tank.loc[i, index_x[1]] < x_mid:
	        	df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	       	else:
	            df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	    else:
	        if df_left_tank.loc[i, index_x[1]] < x_mid:
	        	df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	       	else:
	            df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1


	# converting raw counts to become percentages inplace with 2dp
	df_quad1.loc[0,:] = (df_quad1.loc[0,:]*100/(frame_rate*60)).round(2)
	df_quad2.loc[0,:] = (df_quad2.loc[0,:]*100/(frame_rate*60)).round(2)
	df_quad3.loc[0,:] = (df_quad3.loc[0,:]*100/(frame_rate*60)).round(2)
	df_quad4.loc[0,:] = (df_quad4.loc[0,:]*100/(frame_rate*60)).round(2)
	df_half1.loc[0,:] = (df_half1.loc[0,:]*100/(frame_rate*60)).round(2)
	df_half2.loc[0,:] = (df_half2.loc[0,:]*100/(frame_rate*60)).round(2)



	# assigning the name of the excel file to the first column of the df
	df_quad1.loc[0, 1] = df_quad2.loc[0, 1] = df_quad3.loc[0, 1] = df_quad4.loc[0, 1] = df_half1.loc[0, 1] = df_half2.loc[0, 1] = excel_name

    # inputting the gender information of the fish to the df
	df_quad1.loc[0, 2] = df_quad2.loc[0, 2] = df_quad3.loc[0, 2] = df_quad4.loc[0, 2] = df_half1.loc[0, 2] = df_half2.loc[0, 2] = sex
	
	# creating the headers for the csv files
	lst_header2 = ['file_name', 'sex']
	lst_header = range(0, len(df_quad1.columns)-2)
	for i in lst_header:
	    lst_header[i] = 'minute %d to %d' % ((lst_header[i]), (lst_header[i]+1))
	lst_header = lst_header2 + lst_header

	# returning the dfs that can be manipulated later
	return df_quad1, df_quad2, df_quad3, df_quad4, df_half1, df_half2, lst_header

def assign_right_tank(df_right_tank, excel_name):
	# giving names to the columns of the df
	col = 'col'
	col_names = [col + str(i) for i in range(len(df_right_tank.columns))]
	df_right_tank.columns = col_names

	# Getting the indices of the 'x', 'y', 'sex' and 'framerate'
	index_x, index_y = get_index_x_y(df_right_tank)
	index_sex = get_index_sex(df_right_tank)
	index_fps = get_index_fps(df_right_tank)
	
	# parameters that should be obtained from the excel file
	frame_rate = int(re.findall('[0-9]+', df_right_tank.loc[index_fps[0], index_fps[1]])[0]) # usually 12 fps
	experiment_time = (df_right_tank.shape[0] / frame_rate) / 60 # experiment time is in minutes
	sex = re.match('FishSex:(.*)', df_right_tank.loc[index_sex[0], index_sex[1]]).group(1)

	# creating data frame for each quadrant depending on the parameters above
	df_quad1 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_quad2 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_quad3 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_quad4 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_half1 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))
	df_half2 = pd.DataFrame(np.random.randint(low=0, high=1, size=(1, experiment_time+2)),
	                     columns=range(1, experiment_time+3))

	# determining key positions in the tank to create the quadrants
	x_min = df_right_tank.loc[5, 'col2']
	x_max = df_right_tank.loc[6, 'col2']
	x_mid = (x_min + x_max)/2
	y_min = df_right_tank.loc[5, 'col3']
	y_max = df_right_tank.loc[6, 'col3']
	y_mid = (y_min + y_max)/2

	# creating the for loop to assign which quadrant the fish belongs at a given time after the first two minutes
	# start at column 3 because the first two columns are for the name and the sex
	column_no = 3
	# get the row number in which the values of 'x' and 'y' first appear. The values below the row can be extracted immediately 
	row_number_x_and_y = index_x[0] + 1
	for i in range(row_number_x_and_y, len(df_right_tank)):
	    if ((i-9) % (frame_rate*60) == 0) and (column_no < len(df_quad1.columns)):
	        column_no = column_no + 1
	        if df_right_tank.loc[i, index_x[1]] > x_mid:
	            if df_right_tank.loc[i, index_y[1]] > y_mid:
	                df_quad1.loc[0, column_no] = int(df_quad1.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	            else:
	                df_quad3.loc[0, column_no] = int(df_quad3.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	        elif df_right_tank.loc[i, index_y[1]] > y_mid:
	            df_quad2.loc[0, column_no] = int(df_quad2.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	        else:
	            df_quad4.loc[0, column_no] = int(df_quad4.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1

	    else:
	        if df_right_tank.loc[i, index_x[1]] > x_mid:
	            if df_right_tank.loc[i, index_y[1]] > y_mid:
	                df_quad1.loc[0, column_no] = int(df_quad1.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	            else:
	                df_quad3.loc[0, column_no] = int(df_quad3.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	        elif df_right_tank.loc[i, index_y[1]] > y_mid:
	            df_quad2.loc[0, column_no] = int(df_quad2.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	        else:
	            df_quad4.loc[0, column_no] = int(df_quad4.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1

	column_no = 3
	for i in range(10, len(df_right_tank)):
	    if ((i-9) % (frame_rate*60) == 0) and (column_no < len(df_quad1.columns)):
	        column_no = column_no + 1
	        if df_right_tank.loc[i, index_x[1]] > x_mid:
	        	df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	       	else:
	            df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	    else:
	        if df_right_tank.loc[i, index_x[1]] > x_mid:
	        	df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	       	else:
	            df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1

	# converting raw counts to become percentages inplace with 2dp
	df_quad1.loc[0,:] = (df_quad1.loc[0,:]*100/(frame_rate*60)).round(2)
	df_quad2.loc[0,:] = (df_quad2.loc[0,:]*100/(frame_rate*60)).round(2)
	df_quad3.loc[0,:] = (df_quad3.loc[0,:]*100/(frame_rate*60)).round(2)
	df_quad4.loc[0,:] = (df_quad4.loc[0,:]*100/(frame_rate*60)).round(2)
	df_half1.loc[0,:] = (df_half1.loc[0,:]*100/(frame_rate*60)).round(2)
	df_half2.loc[0,:] = (df_half2.loc[0,:]*100/(frame_rate*60)).round(2)

	# assigning the name of the excel file to the first column of the df
	df_quad1.loc[0, 1] = df_quad2.loc[0, 1] = df_quad3.loc[0, 1] = df_quad4.loc[0, 1] = df_half1.loc[0, 1] = df_half2.loc[0, 1] = excel_name

	# inputting the gender information of the fish to the df
	df_quad1.loc[0, 2] = df_quad2.loc[0, 2] = df_quad3.loc[0, 2] = df_quad4.loc[0, 2] = df_half1.loc[0, 2] = df_half2.loc[0, 2] = sex

	# creating the headers for the csv files
	lst_header2 = ['file_name', 'sex']
	lst_header = range(0, len(df_quad1.columns)-2)
	for i in lst_header:
	    lst_header[i] = 'minute %d to %d' % ((lst_header[i]), (lst_header[i]+1))
	lst_header = lst_header2 + lst_header
	# returning the dfs that can be manipulated later
	return df_quad1, df_quad2, df_quad3, df_quad4, df_half1, df_half2, lst_header
