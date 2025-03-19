import struct
import pandas as pd
from lap_times_functions import *

lap_times = pd.read_csv("archive_f1/lap_times.csv")
drivers = pd.read_csv("archive_f1/drivers.csv")
races = pd.read_csv("archive_f1/races.csv")
control=0

while True:
    if control==0:
        print("What do you want to do? ")
        print("1. Visualize Lap Times for driver(s) in a Grand Prix (up to 4)")
        print("2. See Statistics of driver(s) in a Grand Prix (up to 4)")
        print("3. See Position Variation Graph for driver(s) in a Grand Prix")
        print("4. Exit")

    control=0 #parameter to control whether or not to print the above
    try:
        user_input = int(input("Select  an Action: "))
    except:
        user_input = -13

    match user_input:
        case 1:
            control = 1
            while control == 1:
                control = 0
                try:
                    num = int(input("How many drivers you want to compare? (from 1 to 4) : "))
                except:
                    error("You need to insert a number between 1 and 4!")
                    control = 1
                if control == 0 and (5 > num > 0):
                    driver_input, race_input = select_race(drivers, lap_times, races, num)
                    compute_data(race_input,driver_input,races, drivers, lap_times,num, 1)

                elif control == 0:
                    error("You need to insert a number between 1 and 4!")
                    control = 1

        case 2:
            control=1
            while control==1:
                control=0
                try:
                    num = int(input("How many drivers you want to compare? (from 1 to 4) : "))
                except:
                    error("You need to insert a number between 1 and 4!")
                    control = 1
                if control == 0 and (5 > num > 0):
                    driver_input, race_input = select_race(drivers, lap_times, races, num)
                    compute_data(race_input,driver_input,races, drivers, lap_times,num, 0)
                elif control==0 :
                    error("You need to insert a number between 1 and 4!")
                    control = 1

        case 3:
            races_grid(lap_times,races,drivers)
        case 4:
            exit(0)
        case _:
            error("You need to insert a number between 1 and 4!")
            control=1