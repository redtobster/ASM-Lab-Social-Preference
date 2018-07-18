# ASM-Lab-Social-Preference
Python and R code, alongside with their descriptions to analyze and visualize the Zebra Fish social preference experiment.

After getting the raw excel data that is taken from running the experiments, `getting_velocity.py` and `social_behaviour_v4.py` are scripts that you can run in order to analyze the data. Subsequently, you will be able to visualize the extracted data by clicking this [link](https://hanstobylimanto.shinyapps.io/ASM_SB_Viz/). This readme briefly describes the steps you would take to run the analysis. You should have python 2.7.15 installed in your machine in order to run the program.

## getting_velocity.py

This python script requires the following packages:
  - numpy
  - pandas
  - regex
 
Also, make sure that the python scripts `getting_velocity_fun.py`, `getting_excel.py` and `index_fun.py` are installed and stored in the same location as `getting_velocity.py`.

Once you have these packages and programs installed, you are ready to run the script `getting_velocity.py`, specify the folder that contains the excel sheet, tank length (usually 295mm) and tank width (usually 52mm). What you will get are processed excel files that are in the same folder with the same name. However, new sheets on the velocity per second and freezing analysis are added where information on freezing duration and location is added. 
  
## social_behaviour_v4.py

This python script requires the following packages:
  - pandas
  - numpy
  - scipy
  - regex

Also, make sure that the python scripts `classifying_positions_v3.py` and `getting_excel.py` are installed and stored in the same location as `social_behaviour_v4.py`.

Once you have these packages and programs installed, you are ready to run the script `social_behaviour_v4.py`, specify the folder that contains the excel sheet and then a new folder called _extracted_info_(something)_ will appear that contains 6 csv files. These csv files will contain the positional information of the fish. At a given minute, the percentage of time the fish spends in a particular quadrant is specified.

## app.R

This is the visualization tool to visualize the positional information of the fish. Upload the 6 csv files per type of fish and the usage of the app should be self-explanatory. You could download the plots as pdf too. Click this [link](https://hanstobylimanto.shinyapps.io/ASM_SB_Viz/) to access the app once your analysis is completed.
