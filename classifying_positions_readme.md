# Readme for the classifying_positions_v3.py

This python file contains _five_ functions:
  1. `get_index_x_y` - function to automatically get the index of 'x', 'y' in the excel sheet.
  1. `get_index_sex` - function to automatically get the index of where the string 'FishSex' in the excel sheet.
  1. `get_index_fps` - function to automatically get the index of where the string 'FrameRate' in the excel sheet.
  1. `assign_left_tank` - function to extract the positional information of the subject that has its companion at the _left_ side of the tank.
  1. `assign_right_tank` - function to extract the positional information of the subject that has its companion at the _right_ side of the tank
  
List of packages necessary:
  - pandas
  - numpy
  - regex
  
## Lines 6 - 11

```
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
```

This function takes in a dataframe and return _two_ lists, each containing _two_ elements containing the row and column specification of where the string `x` and `y` are located. The function processes the data frame in 3 steps:
  1. The lists are initialized with values `[0, 0]`.
  1. The rows and columns are iterated through the data frame.
  1. Once the strings `'x'` and `'y'` are found, the function assigns the value to the lists respectively and returns them.

❗️**Caveat (hard-code alert)**: This function literally *only* looks for the string `'x'` and `'y'` exactly. If the future excel files have the x and y positions with a different label, the if statement of the code should be changed.

## Lines 19 - 37

```
def get_index_sex(df):
    index_sex = [0, 0]
    df = df.fillna('empty')
    for row in list(df.index):
        for col in list(df.columns):
            if bool(re.match('FishSex.*', str(df.loc[row, col]))):
            	index_sex[0] = row
                index_sex[1] = col
                return index_sex
```

I am only showing the code snippet of `get_index_sex` here because the logic of this function and `get_index_fps` is exactly the same. In actual fact, the logic with the `get_index_x_y` function is also very similar with the following differences:
  1. The function fills the non-filled cells with the string `'empty'`.
  1. The function looks for the row and column that contains the substring `FishSex` for `get_index_sex` and `FrameRate` for `get_index_fps`.
  
❗️**Caveat (hard-code alert)**: The functions literally *only* looks for the substring `FishSex` or `FrameRate`. In the future if the information of the fish sex and framerate is not stored in this way, the if statement of the function has to be changed.
