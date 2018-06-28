# **Readme for the social_behaviour_v4.py**
- List of packages necessary:
  - Numpy
  - Pandas
  - Scipy
  - xlrd

## Lines 12-15

```
desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
print('Input the folder in which the excel files are located:')
excel = raw_input('')
path = desktop + '\\Webcam\\' + excel + '\\'
```

1. Getting the directory that contains the excel file in 3 steps:
  1. Using the os package, I can find the directory of desktop on any device automatically.
  1. Ask the user what is the name of the excel folder.
  1. Create the directory name that is to be accessed.
  
❗️Caveat (hard-code alert): The program assumes that the excel files is located in desktop -> Webcam -> (folder_name). The folder Webcam is hardcoded into the program. So if your excel file is in a folder in the desktop that is not called ‘Webcam’, you can change line 15 from ‘\\Webcam\\’ to ‘\\(folder_name)\\’.
