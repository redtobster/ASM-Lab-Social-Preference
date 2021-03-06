from getting_velocity_fun import check_input, modify_excel_with_velocity
from getting_excel import categorize_files
import os

# getting the directory that contains the excel files
desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
print('Input the folder in which the excel files are located:')
excel = raw_input('')
path = desktop + '\\Webcam\\' + excel + '\\'

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

# iterating through the excel files in the folder
print('initializing sheet modification..')
for i in range(len(left_tank)):
	modify_excel_with_velocity(left_tank[i], 'left', path, tank_length, tank_width)
	print('modifying sheet %s completed' % (left_tank[i]))

for i in range(len(right_tank)):
	modify_excel_with_velocity(right_tank[i], 'right', path, tank_length, tank_width)
	print('modifying sheet %s completed' % (right_tank[i]))

for i in range(len(first_two_minutes_left)):
	modify_excel_with_velocity(first_two_minutes_left[i], 'left', path, tank_length, tank_width)
	print('modifying sheet %s completed' % (first_two_minutes_left[i]))

for i in range(len(first_two_minutes_right)):
	modify_excel_with_velocity(first_two_minutes_right[i], 'right', path, tank_length, tank_width)
	print('modifying sheet %s completed' % (first_two_minutes_right[i]))

print('sheet modification and velocity analysis completed')
