# **Readme for the social_behaviour_v4.py**
User is to run this python program to get the analysis results of the excel files that are obtained from the social recognition experiments.
List of packages necessary:
  - numpy
  - pandas
  - scipy
  - xlrd

## Lines 12-15

```
desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
print('Input the folder in which the excel files are located:')
excel = raw_input('')
path = desktop + '\\Webcam\\' + excel + '\\'
```

Getting the directory that contains the excel file in 3 steps:
  1. Using the os package, I can find the directory of desktop on any device automatically.
  1. Ask the user what is the name of the excel folder.
  1. Create the directory name that is to be accessed.
  
❗️**Caveat (hard-code alert)**: The program assumes that the excel files is located in desktop -> Webcam -> (folder_name). The folder Webcam is hardcoded into the program. So if your excel file is in a folder in the desktop that is not called ‘Webcam’, you can change line 15 from ‘\\Webcam\\’ to ‘\\(folder_name)\\’.

## Lines 18 - 33

```
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
```

This chunk of code first gets the names of all the excel files in the directory specified using a function imported from another script `getting_excel.py` (to be explained in the getting_excel_readme.md). Then, it prepares the directory that will save the new CSV files after each excel files have been analyzed. This is done in 3 steps:
  1. Creating the name of the output folder which is based on the name of the excel file
  1. Making the directory of the CSV file if it does not exist.
  1. Removing all csv files in the directory (if any).
  
## Lines 37 - 51

```
file_name = path + left_tank[0]
df = pd.read_excel(io=file_name, sheet_name='Tank1', header=None)

# using the function to extract the values
print('extracting data..')
df_quad1, df_quad2, df_quad3, df_quad4, df_half1, df_half2, lst_header = assign_left_tank(df, left_tank[0])

# writing the csv file
df_quad1.to_csv(directory + '\\df_quad1.csv', header=lst_header, index=False)
df_quad2.to_csv(directory + '\\df_quad2.csv', header=lst_header, index=False)
df_quad3.to_csv(directory + '\\df_quad3.csv', header=lst_header, index=False)
df_quad4.to_csv(directory + '\\df_quad4.csv', header=lst_header, index=False)
df_half1.to_csv(directory + '\\df_half1.csv', header=lst_header, index=False)
df_half2.to_csv(directory + '\\df_half2.csv', header=lst_header, index=False)
print('extracting %s completed' % (left_tank[0]))
```

This chunk of code writes the first content of the csv file. In this script (although not very elegant), it is sort of necessary to do so because we want to get the header from the function `assign_left_tank` from `classifying_positions_v3.py` to be reflected in the output csv files. In the pandas function `to_csv`, the attribute `header` is specified as `lst_header` which is obtained from the function discussed earlier. To summarize in 3 succint steps this chunk of code,
  1. Reads the first name excel file that is stored in the list called `left_tank`
  1. Gets the header, quadrant and halves information from the function `assign_left_tank`
  1. Writes the csv file with the header specified.
  
## Lines 62 - 98

It does the same thing as the previous code chunk but it is looped through all the excel names that are stored in the two lists called `left_tank` and `right_tank`. A code line of interest that is different would be

```
df.to_csv(f, header=False, index=False, mode = 'a')
```

Notice that the attribute `mode = 'a'` here is used to append the information of the df to the existing csv file.

## Lines 102 - 107

```
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1 + confidence) / 2., n - 1)
    return m.round(2), (m - h).round(2), (m + h).round(2), h.round(2)
```

The function that takes in a data frame and percent of confidence (default at 95 percent) is written. This function is taken from [this stackoverflow page](https://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data) This function is used later on to compute the mean, upper bound, lower bound and the difference between the upper bound and the mean.

## Lines 110 - 236

```
csv1 = directory + "\\df_quad1.csv"
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
with open(directory + "\\df_quad1.csv", "a") as fp:
    wr = csv.writer(fp, dialect='excel', lineterminator='\n')
    wr.writerow(['mean'] + [''] + lst_mean)
    wr.writerow(['lower'] + [''] + lst_lower)
    wr.writerow(['upper'] + [''] + lst_upper)
    wr.writerow(['delta'] + [''] + lst_diff)
```

This code snippet computes the 4 items that is returned from the function `mean_confidence_interval` and then writes in the existing csv file. It loops over the entire column of the csv file to compute the mean and cofidence interval for each column and stores this information in 4 lists. Then these lists get appended to the existing csv file and now the process can repeat itself for the rest of the positions (quadrant 2, 3 and so forth).

I would be happy to receive suggestions to make this code chunk more elegant.
