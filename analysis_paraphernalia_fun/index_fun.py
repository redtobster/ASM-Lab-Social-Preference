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
