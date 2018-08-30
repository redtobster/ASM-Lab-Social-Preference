import pandas as pd
import numpy as np
import re


# functions to assign x,y positions to their respective quadrants for the first two minutes
# and the entire experiment
def assign_left_tank(df_left_tank, excel_name):
	# giving names to the columns of the df
	df_left_tank.columns = ['col0', 'col1', 'col2', 'col3', 'col4', 'col5' ,'col6', 'col7']

	# parameters that should be obtained from the excel files
	frame_rate = int(re.findall('[0-9]+', df_left_tank.loc[0, 'col6'])[0]) # usually 12 fps
	experiment_time = (df_left_tank.shape[0] / frame_rate) / 60 # experiment time is in minutes
	sex = re.match('FishSex:(.*)', df_left_tank.loc[8,'col4']).group(1) 

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
	column_no = 3
	for i in range(10, len(df_left_tank)):
	    if ((i-9) % (frame_rate*60) == 0) and (column_no < len(df_quad1.columns)):
	        column_no = column_no + 1
	        if df_left_tank.loc[i, 'col2'] < x_mid:
	            if df_left_tank.loc[i, 'col3'] > y_mid:
	                df_quad1.loc[0, column_no] = int(df_quad1.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	            else:
	                df_quad3.loc[0, column_no] = int(df_quad3.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	        elif df_left_tank.loc[i, 'col3'] > y_mid:
	            df_quad2.loc[0, column_no] = int(df_quad2.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	        else:
	            df_quad4.loc[0, column_no] = int(df_quad4.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	    else:
	        if df_left_tank.loc[i, 'col2'] < x_mid:
	            if df_left_tank.loc[i, 'col3'] > y_mid:
	                df_quad1.loc[0, column_no] = int(df_quad1.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	            else:
	                df_quad3.loc[0, column_no] = int(df_quad3.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	        elif df_left_tank.loc[i, 'col3'] > y_mid:
	            df_quad2.loc[0, column_no] = int(df_quad2.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	        else:
	            df_quad4.loc[0, column_no] = int(df_quad4.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1

	column_no = 3
	for i in range(10, len(df_left_tank)):
	    if ((i-9) % (frame_rate*60) == 0) and (column_no < len(df_quad1.columns)):
	        column_no = column_no + 1
	        if df_left_tank.loc[i, 'col2'] < x_mid:
	        	df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	       	else:
	            df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	    else:
	        if df_left_tank.loc[i, 'col2'] < x_mid:
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
	df_right_tank.columns = ['col0', 'col1', 'col2', 'col3', 'col4', 'col5' ,'col6', 'col7']
	
	# parameters that should be obtained from the excel file
	frame_rate = int(re.findall('[0-9]+', df_right_tank.loc[0, 'col6'])[0]) # usually 12 fps
	experiment_time = (df_right_tank.shape[0] / frame_rate) / 60 # experiment time is in minutes
	sex = re.match('FishSex:(.*)', df_right_tank.loc[8,'col4']).group(1)

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
	column_no = 3
	for i in range(10, len(df_right_tank)):
	    if ((i-9) % (frame_rate*60) == 0) and (column_no < len(df_quad1.columns)):
	        column_no = column_no + 1
	        if df_right_tank.loc[i, 'col2'] > x_mid:
	            if df_right_tank.loc[i, 'col3'] > y_mid:
	                df_quad1.loc[0, column_no] = int(df_quad1.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	            else:
	                df_quad3.loc[0, column_no] = int(df_quad3.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	        elif df_right_tank.loc[i, 'col3'] > y_mid:
	            df_quad2.loc[0, column_no] = int(df_quad2.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	        else:
	            df_quad4.loc[0, column_no] = int(df_quad4.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1

	    else:
	        if df_right_tank.loc[i, 'col2'] > x_mid:
	            if df_right_tank.loc[i, 'col3'] > y_mid:
	                df_quad1.loc[0, column_no] = int(df_quad1.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	            else:
	                df_quad3.loc[0, column_no] = int(df_quad3.loc[0, column_no]) + 1
	                # df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	        elif df_right_tank.loc[i, 'col3'] > y_mid:
	            df_quad2.loc[0, column_no] = int(df_quad2.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	        else:
	            df_quad4.loc[0, column_no] = int(df_quad4.loc[0, column_no]) + 1
	            # df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1

	column_no = 3
	for i in range(10, len(df_right_tank)):
	    if ((i-9) % (frame_rate*60) == 0) and (column_no < len(df_quad1.columns)):
	        column_no = column_no + 1
	        if df_right_tank.loc[i, 'col2'] > x_mid:
	        	df_half1.loc[0, column_no] = int(df_half1.loc[0, column_no]) + 1
	       	else:
	            df_half2.loc[0, column_no] = int(df_half2.loc[0, column_no]) + 1
	    else:
	        if df_right_tank.loc[i, 'col2'] > x_mid:
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