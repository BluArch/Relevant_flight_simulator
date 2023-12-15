[![Made with C](https://img.shields.io/badge/Made%20with-C-yellow.svg)](https://en.wikipedia.org/wiki/C_(programming_language))  

This assignment was made for the SENG265 course at the University of Victoria. 

Generator_C is written in C and takes a .csv file of a number of different flight routes. Based on the given input from the command line, flights with specified keywords are found. I created a loop that reads through the .csv file one line at a time, searching for the desired keywords. The desired flights are outputted in a .txt file

Generator_Python is in Python and takes a .yaml of flight routes. Command line inputs determine which flights are searched. By using the Pandas library, the contents of the .yaml file were converted into a data frame. Pandas helped sift out the unwanted flight, and the wanted ones were again outputted into a .txt file
