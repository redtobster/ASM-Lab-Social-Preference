import os
import glob
import re

# Uncomment the code below and the ones at the bottom to check if the code is working on its own
# desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
# path = desktop + '\\Webcam\\excel\\' # make sure this directory contains your excel files

# A function that categorize the excel files based on the first 2 minutes
# and the location of the peers (left or right). Returns 4 lists.
def categorize_files(path):
	# getting all excel files in the directory
	extension = 'xls'
	os.chdir(path)
	excel_files = [i for i in glob.glob('*.{}'.format(extension))]

	# Separating the excel files based on the first 2 minutes at the left
	first_two_minutes_left = []
	first_two_minutes_right = []
	for i in range(0, len(excel_files)):
		if bool(re.match('.*L_A_.*', excel_files[i])):
			first_two_minutes_left.append(excel_files[i])
		elif bool(re.match('.*R_A_.*', excel_files[i])):
			first_two_minutes_right.append(excel_files[i])
	
	# getting the reminder of the lists
	excel_exp_temp = list(set(excel_files) - set(first_two_minutes_left))
	excel_exp = list(set(excel_exp_temp) - set(first_two_minutes_right))

	# Separating the excel file based on the location of the peers (left or right)
	left_tank = []
	right_tank = []
	for i in range(0, len(excel_exp)):
		if bool(re.match('.*L_[0-9]+.*', excel_exp[i])):
			left_tank.append(excel_exp[i])
		else:
			right_tank.append(excel_exp[i])

	# sorting the lists that have been obtained
	first_two_minutes_left.sort()
	first_two_minutes_right.sort()
	left_tank.sort()
	right_tank.sort()

	return first_two_minutes_left, first_two_minutes_right, left_tank, right_tank

# Function to get the more general names of the excel files (without the time stamp)
def getting_name(left_tank):
		string = re.match('([A-Z]+).*', left_tank[0]).group(1)
    		return string

# Uncomment the codes below to test if the file works
# first_two_minutes_left, first_two_minutes_right, left_tank, right_tank = categorize_files(path)
# print(first_two_minutes_left)
# print(first_two_minutes_right)
# print(left_tank)
# print(right_tank)
# print(range(0, len(right_tank)))

# tank_file_names = getting_name(left_tank)
# print(tank_file_names)
