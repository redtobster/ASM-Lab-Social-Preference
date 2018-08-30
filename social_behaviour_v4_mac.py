from getting_excel_mac import categorize_files, getting_name
from classifying_positions_v2_mac import assign_left_tank, assign_right_tank
import os
import pandas as pd
import glob
import numpy as np
import scipy as sp
import scipy.stats
import csv

# Getting the directory that contains the excel files
# desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
desktop = os.path.expanduser("~/Desktop/Webcam/")
print('Input the folder in which the excel files are located:')
excel = raw_input('')
path = desktop + excel + '/'

# getting the names of the excel file
print('organizing data..')
first_two_minutes_left, first_two_minutes_right, left_tank, right_tank = categorize_files(path)

# getting the ext of the ouput folder name
output_folder = getting_name(left_tank)

# making the directory
print('creating directory..')
directory = path + 'extracted_info_' + output_folder
if not os.path.exists(directory):
    os.makedirs(directory)

# deleting all csv files in the directory
filelist = [f for f in os.listdir(directory) if f.endswith(".csv")]
for f in filelist:
    os.remove(os.path.join(directory, f))

# creating the csv file for the first excel file to have the header
# opening the excel file
file_name = path + left_tank[0]
df = pd.read_excel(io=file_name, sheet_name='Tank1', header=None)

# using the function to extract the values
print('extracting data..')
df_quad1, df_quad2, df_quad3, df_quad4, df_half1, df_half2, lst_header = assign_left_tank(df, left_tank[0])

# writing the csv file
df_quad1.to_csv(directory + '/df_quad1.csv', header=lst_header, index=False)
df_quad2.to_csv(directory + '/df_quad2.csv', header=lst_header, index=False)
df_quad3.to_csv(directory + '/df_quad3.csv', header=lst_header, index=False)
df_quad4.to_csv(directory + '/df_quad4.csv', header=lst_header, index=False)
df_half1.to_csv(directory + '/df_half1.csv', header=lst_header, index=False)
df_half2.to_csv(directory + '/df_half2.csv', header=lst_header, index=False)
print('extracting %s completed' % (left_tank[0]))

# assigning the x, y positions of the fish to different quadrants (left tank)
for i in range(1, len(left_tank)):
    # opening the excel file
    file_name = path + left_tank[i]
    df = pd.read_excel(io=file_name, sheet_name='Tank1', header=None)
    # using the function to extract the values
    df_quad1, df_quad2, df_quad3, df_quad4, df_half1, df_half2, lst_header = assign_left_tank(df, left_tank[i])

    # writing the csv files with respect to the quadrants
    with open(directory + '/df_quad1.csv', 'a') as f:
        df_quad1.to_csv(f, header=False, index=False, mode = 'a')
        with open(directory + '/df_quad2.csv', 'a') as f:
            df_quad2.to_csv(f, header=False, index=False, mode = 'a')
            with open(directory + '/df_quad3.csv', 'a') as f:
                df_quad3.to_csv(f, header=False, index=False, mode = 'a')
                with open(directory + '/df_quad4.csv', 'a') as f:
                    df_quad4.to_csv(f, header=False, index=False, mode = 'a')
                    with open(directory + '/df_half1.csv', 'a') as f:
                        df_half1.to_csv(f, header=False, index=False, mode = 'a')
                        with open(directory + '/df_half2.csv', 'a') as f:
                            df_half2.to_csv(f, header=False, index=False, mode = 'a')
    print('extracting %s completed' % (left_tank[i]))

# assigning the x, y positions of the fish to different quadrants (right tank)
for i in range(0, len(right_tank)):
    # opening the excel file
    file_name = path + right_tank[i]
    df = pd.read_excel(io=file_name, sheet_name='Tank1', header=None)

    # using the function to extract the values
    df_quad1, df_quad2, df_quad3, df_quad4, df_half1, df_half2, lst_header = assign_right_tank(df, right_tank[i])

    # writing the csv files with respect to the quadrants
    with open(directory + '/df_quad1.csv', 'a') as f:
        df_quad1.to_csv(f, header=False, index=False, mode = 'a')
        with open(directory + '/df_quad2.csv', 'a') as f:
            df_quad2.to_csv(f, header=False, index=False, mode = 'a')
            with open(directory + '/df_quad3.csv', 'a') as f:
                df_quad3.to_csv(f, header=False, index=False, mode = 'a')
                with open(directory + '/df_quad4.csv', 'a') as f:
                    df_quad4.to_csv(f, header=False, index=False, mode = 'a')
                    with open(directory + '/df_half1.csv', 'a') as f:
                        df_half1.to_csv(f, header=False, index=False, mode = 'a')
                        with open(directory + '/df_half2.csv', 'a') as f:
                            df_half2.to_csv(f, header=False, index=False, mode = 'a')
    print('extracting %s completed' % (right_tank[i]))


# a function to find mean and confidence interval is written
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1 + confidence) / 2., n - 1)
    return m.round(2), (m - h).round(2), (m + h).round(2), h.round(2)


print('additional computations..')
# mean and confidence interval for quadrant 1
csv1 = directory + "/df_quad1.csv"
df_quad1 = pd.read_csv(csv1, sep=",", header=None, skiprows=1, error_bad_lines=False)
lst_mean = range(2, len(df_quad1.columns))
lst_lower = range(2, len(df_quad1.columns))
lst_upper = range(2, len(df_quad1.columns))
lst_diff = range(2, len(df_quad1.columns))
for i in range(2, len(df_quad1.columns)):
    lst_mean[i - 2] = mean_confidence_interval(df_quad1.loc[:, i])[0]
    lst_lower[i - 2] = mean_confidence_interval(df_quad1.loc[:, i])[1]
    lst_upper[i - 2] = mean_confidence_interval(df_quad1.loc[:, i])[2]
    lst_diff[i - 2] = mean_confidence_interval(df_quad1.loc[:, i])[3]

# append the lists to the csv file
with open(directory + "/df_quad1.csv", "a") as fp:
    wr = csv.writer(fp, dialect='excel', lineterminator='\n')
    wr.writerow(['mean'] + [''] + lst_mean)
    wr.writerow(['lower'] + [''] + lst_lower)
    wr.writerow(['upper'] + [''] + lst_upper)
    wr.writerow(['delta'] + [''] + lst_diff)

# mean and confidence interval for quadrant 2
csv2 = directory + "/df_quad2.csv"
df_quad2 = pd.read_csv(csv2, sep=",", header=None, skiprows=1, error_bad_lines=False)
lst_mean = range(2, len(df_quad2.columns))
lst_lower = range(2, len(df_quad2.columns))
lst_upper = range(2, len(df_quad2.columns))
lst_diff = range(2, len(df_quad2.columns))
for i in range(2, len(df_quad2.columns)):
    lst_mean[i - 2] = mean_confidence_interval(df_quad2.loc[:, i])[0]
    lst_lower[i - 2] = mean_confidence_interval(df_quad2.loc[:, i])[1]
    lst_upper[i - 2] = mean_confidence_interval(df_quad2.loc[:, i])[2]
    lst_diff[i - 2] = mean_confidence_interval(df_quad2.loc[:, i])[3]

# append the lists to the csv file
with open(directory + "/df_quad2.csv", "a") as fp:
    wr = csv.writer(fp, dialect='excel', lineterminator='\n')
    wr.writerow(['mean'] + [''] + lst_mean)
    wr.writerow(['lower'] + [''] + lst_lower)
    wr.writerow(['upper'] + [''] + lst_upper)
    wr.writerow(['delta'] + [''] + lst_diff)

# mean and confidence interval for quadrant 3
csv3 = directory + "/df_quad3.csv"
df_quad3 = pd.read_csv(csv3, sep=",", header=None, skiprows=1, error_bad_lines=False)
lst_mean = range(2, len(df_quad3.columns))
lst_lower = range(2, len(df_quad3.columns))
lst_upper = range(2, len(df_quad3.columns))
lst_diff = range(2, len(df_quad3.columns))
for i in range(2, len(df_quad3.columns)):
    lst_mean[i - 2] = mean_confidence_interval(df_quad3.loc[:, i])[0]
    lst_lower[i - 2] = mean_confidence_interval(df_quad3.loc[:, i])[1]
    lst_upper[i - 2] = mean_confidence_interval(df_quad3.loc[:, i])[2]
    lst_diff[i - 2] = mean_confidence_interval(df_quad3.loc[:, i])[3]

# append the lists to the csv file
with open(directory + "/df_quad3.csv", "a") as fp:
    wr = csv.writer(fp, dialect='excel', lineterminator='\n')
    wr.writerow(['mean'] + [''] + lst_mean)
    wr.writerow(['lower'] + [''] + lst_lower)
    wr.writerow(['upper'] + [''] + lst_upper)
    wr.writerow(['delta'] + [''] + lst_diff)

# mean and confidence interval for quadrant 4
csv4 = directory + "/df_quad4.csv"
df_quad4 = pd.read_csv(csv4, sep=",", header=None, skiprows=1, error_bad_lines=False)
lst_mean = range(2, len(df_quad4.columns))
lst_lower = range(2, len(df_quad4.columns))
lst_upper = range(2, len(df_quad4.columns))
lst_diff = range(2, len(df_quad4.columns))
for i in range(2, len(df_quad4.columns)):
    lst_mean[i - 2] = mean_confidence_interval(df_quad4.loc[:, i])[0]
    lst_lower[i - 2] = mean_confidence_interval(df_quad4.loc[:, i])[1]
    lst_upper[i - 2] = mean_confidence_interval(df_quad4.loc[:, i])[2]
    lst_diff[i - 2] = mean_confidence_interval(df_quad4.loc[:, i])[3]

# append the lists to the csv file
with open(directory + "/df_quad4.csv", "a") as fp:
    wr = csv.writer(fp, dialect='excel', lineterminator='\n')
    wr.writerow(['mean'] + [''] + lst_mean)
    wr.writerow(['lower'] + [''] + lst_lower)
    wr.writerow(['upper'] + [''] + lst_upper)
    wr.writerow(['delta'] + [''] + lst_diff)

# mean and confidence interval for quadrant 3
csv3 = directory + "/df_half1.csv"
df_half1 = pd.read_csv(csv3, sep=",", header=None, skiprows=1, error_bad_lines=False)
lst_mean = range(2, len(df_half1.columns))
lst_lower = range(2, len(df_half1.columns))
lst_upper = range(2, len(df_half1.columns))
lst_diff = range(2, len(df_half1.columns))
for i in range(2, len(df_half1.columns)):
    lst_mean[i - 2] = mean_confidence_interval(df_half1.loc[:, i])[0]
    lst_lower[i - 2] = mean_confidence_interval(df_half1.loc[:, i])[1]
    lst_upper[i - 2] = mean_confidence_interval(df_half1.loc[:, i])[2]
    lst_diff[i - 2] = mean_confidence_interval(df_half1.loc[:, i])[3]

# append the lists to the csv file
with open(directory + "/df_half1.csv", "a") as fp:
    wr = csv.writer(fp, dialect='excel', lineterminator='\n')
    wr.writerow(['mean'] + [''] + lst_mean)
    wr.writerow(['lower'] + [''] + lst_lower)
    wr.writerow(['upper'] + [''] + lst_upper)
    wr.writerow(['delta'] + [''] + lst_diff)

# mean and confidence interval for quadrant 3
csv3 = directory + "/df_half2.csv"
df_half2 = pd.read_csv(csv3, sep=",", header=None, skiprows=1, error_bad_lines=False)
lst_mean = range(2, len(df_half2.columns))
lst_lower = range(2, len(df_half2.columns))
lst_upper = range(2, len(df_half2.columns))
lst_diff = range(2, len(df_half2.columns))
for i in range(2, len(df_half2.columns)):
    lst_mean[i - 2] = mean_confidence_interval(df_half2.loc[:, i])[0]
    lst_lower[i - 2] = mean_confidence_interval(df_half2.loc[:, i])[1]
    lst_upper[i - 2] = mean_confidence_interval(df_half2.loc[:, i])[2]
    lst_diff[i - 2] = mean_confidence_interval(df_half2.loc[:, i])[3]

# append the lists to the csv file
print('saving files..')
with open(directory + "/df_half2.csv", "a") as fp:
    wr = csv.writer(fp, dialect='excel', lineterminator='\n')
    wr.writerow(['mean'] + [''] + lst_mean)
    wr.writerow(['lower'] + [''] + lst_lower)
    wr.writerow(['upper'] + [''] + lst_upper)
    wr.writerow(['delta'] + [''] + lst_diff)

print('analysis completed')
