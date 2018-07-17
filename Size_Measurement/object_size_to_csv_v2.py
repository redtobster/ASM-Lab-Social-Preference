from __future__ import print_function
from __future__ import division
from object_size_to_csv_fun import measure_object_size
import argparse
import os
import csv

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--length", type=int, required=True,
	help="the length of the tank the subject resides (in mm)")
ap.add_argument("-p", "--path", type=str, required=True,
	help="the path of folder that contains the images to be analyzed")
args = vars(ap.parse_args())

# getting the directory of the image and then the length of the tank as pixels
extension = "png"
os.chdir(args["path"])
png_files = glob.glob('*.{}'.format(extension))

# making a new directory to store the csv file
print('creating directory..')
directory = args["path"] + '\\size_analysis'
if not os.path.exists(directory):
    os.makedirs(directory)

# deleting all csv files in the directory
filelist = [f for f in os.listdir(directory) if f.endswith(".csv")]
for f in filelist:
    os.remove(os.path.join(directory, f))

print('initializing measurement..')
lst_header = ['Filename', 'Subject length (mm)', 'Companion 1 length (mm)', 'Companion length 2 (mm)', 'Companion length 3 (mm)', 'Companion length 4 (mm)', 'Companion mean length', 'Delta', 'Subject area (mm^2)', 'Companion 1 area (mm^2)', 'Companion 2 area (mm^2)', 'Companion 3 area (mm^2)', 'Companion 4 area (mm^2)', 'Companion mean area', 'Delta area']
with open(directory + '\\object_size_analysis.csv', 'w') as f:
	wr = csv.writer(f, lineterminator='\n')
	wr.writerow(lst_header)

# now we are in the position to make use of the function and write the lengths in a csv file.
faulty_files = 0
for i in range(0, len(png_files)):
	lst, area = measure_object_size(args["path"] + '\\' + png_files[i])
	print(lst, area)
	file_name = png_files[i]
	mean = sum(lst)/len(lst)
	delta = lst[0] - mean
	mean_area = sum(area)/len(area)
	delta_area = area[0] - mean_area
	if len(lst + area) == len(lst_header) - 5:
		with open(directory + '\\object_size_analysis.csv', 'a') as f:
			wr = csv.writer(f, dialect='excel', lineterminator='\n')
			wr.writerow([file_name] + lst + [mean] + [delta] + area + [mean_area] + [delta_area])
	else:
		faulty_files = faulty_files	+ 1
		with open(directory + '\\object_size_analysis.csv', 'a') as f:
			wr = csv.writer(f, dialect='excel', lineterminator='\n')
			wr.writerow([file_name] + lst + [mean] + [delta]  + area + [mean_area] + [delta_area] + ['check this file!'])
	print('measuring objects in ' + file_name + ' completed')


print('measurement completed and you have %d files to evaluate' % (faulty_files))
