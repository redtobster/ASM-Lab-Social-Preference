# Readme for the getting_excel.py

This python file contains _two_ functions:
  1. `categorize_files` - to get the names of the excel files and store them into a list.
  1. `getting_name` - to get the more general name of the excel file for the output folder name.

List of packages necessary:
  - Regex

## Lines 11 - 14

```
def categorize_files(path):
  extension = 'xls'
	  os.chdir(path)
	  excel_files = [i for i in glob.glob('*.{}'.format(extension))]
```

This function takes in the directory where the excel files are located. Then, this snippet is responsible for looking the files in that folder with the extension _xls_ (which is an excel file) in the directory that is already specified as the argument of the function. Afterwards, the content of the folder is iterated through and the names of all of the excel files are stored in a list called `excel_files`.

## Lines 18 - 24

```
first_two_minutes_left = []
	first_two_minutes_right = []
	for i in range(0, len(excel_files)):
		if bool(re.match('.*L_A_.*', excel_files[i])):
			first_two_minutes_left.append(excel_files[i])
		elif bool(re.match('.*R_A_.*', excel_files[i])):
			first_two_minutes_right.append(excel_files[i])
```

The list excel files are iterated through and the file names that contains *L_A_* is the first two minute files with companions at the left. While the file names that contains *R_A_* is the first two minute files with companions at the right. The names are then stored in different variables.

❗️**Caveat (hard-code alert)**: The way the companions are on the right and on the left are hard coded. Should there be a change in the way the excel files are named, the future programmer would want to tweak the regular expression matcher that is embedded in these lines of code.

## Lines 27 - 28

```
excel_exp_temp = list(set(excel_files) - set(first_two_minutes_left))
excel_exp = list(set(excel_exp_temp) - set(first_two_minutes_right))
```

These two lines are responsible for getting the excel files that contain only the full experiment excel files. This is done using set subtraction.

## Lines 31 - 37

```
left_tank = []
right_tank = []
	for i in range(0, len(excel_exp)):
		if bool(re.match('.*L_[0-9]+.*', excel_exp[i])):
			left_tank.append(excel_exp[i])
		else:
			right_tank.append(excel_exp[i])
```

Now we can separate the full experiment excel files that have the companions on the right and on the left. The logic is the same as the separation of the first two minute excel files.

❗️**Caveat (hard-code alert)**: The way the companions are on the right and on the left are hard coded. Should there be a change in the way the excel files are named, the future programmer would want to tweak the regular expression matcher that is embedded in these lines of code.

## Lines 40 - 43

```
first_two_minutes_left.sort()
first_two_minutes_right.sort()
left_tank.sort()
right_tank.sort()
```

The code snippet above sorts the lists that have been saved so far. This is important so that the order of the names in the `first_two_minutes_left` and `left_tank` is the same. The same goes for the lists that contain information about companions residing inside the right tank.

## Lines 48 - 50

```
def getting_name(left_tank):
	string = re.match('([A-Z]+).*', left_tank[0]).group(1)
    		return string
```

The [function `getting_name`](#Readme-for-the-getting_excel.py) takes a list of excel file names as argument. Then it gets all letters of the excel file before the character ‘_’. This string is then returned.

As always, I am very happy to receive suggestions to make the code more elegant.
