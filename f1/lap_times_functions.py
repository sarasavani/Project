import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import yticks

from lap_times_functions_support import *

#given a driverId as an input
#returns a list with all the races he competed in
def select_races_list(driver_input,lap_times,races) : #select all the races that a driver has done
    # variables for the loop
    races_output = []
    index = 0
    curr = 0
    last = 0
    for d in lap_times.iloc[:, 1]:  # for all the values in lap_times.csv in the column driverId
        curr = d
        if curr != last:  # verify if the raceId is still the same
            if d == driver_input:  # if the driverId of the selected line is equal to the driver the user selected
                curr_raceId = lap_times.iloc[index, 0]  # raceId of the specific selected line (where selected driverId== race driverId )
                race_curr=races[races["raceId"] == curr_raceId] #select the race with raceId==raceId of the
                if not race_curr.empty:
                    year = int(race_curr.iloc[0]['year'])
                    name = str(race_curr.iloc[0]['name'])
                    id = int(race_curr.iloc[0]['raceId'])
                    race_add = (id, year, name)
                    races_output.append(race_add)

        last = curr  # set last id computed as the current id computed
        index = index + 1

    return races_output

#print (or not if flg!=0) all the drivers and make the user select one driverId
#returns driver_input, the driverId of the selected driver
def select_driver(flg,drivers) :
    #FLG 0 == print all drivers
    ##FLG
    if flg==0 : #print all that only the first time
        for row in drivers.itertuples():
            print(f"{row.driverId}, {row.code}, {row.forename}, {row.surname}, {row.number}")

    driver_input=-1

    while True:
        err=0
        try:
            driver_input = int(input("Select your driver from the ones above (insert the driverId) : "))

        except:
            error("You need to insert a valid driverId! ")
            err=1

        if driver_input<1 or driver_input >860:
            if err!=1:
                error("You need to insert a valid driverId! ")

        else :
            print("\n You selected driver ", driver_input, "\n",
                  (drivers[drivers["driverId"] == driver_input]).iloc[:, [0, 3, 4, 5, 2]], "\n\n")
            return driver_input

#call select_races_list() and select_driver() and make the user select a single race
#that the driver they selected competed in
#returns driver_input (driverId of the selected driver) and race_input (raceId of the selected race)
def select_race(drivers, lap_times , races, num) :

    driver_input=[]
    races_driver =[]
    race_input=0

    for i in range(num):

        # select the driver
        driver_input.append(select_driver(i,drivers))

        # select only the races where the selected driver has competed
        races_driver.append(select_races_list(driver_input[i],lap_times,races))


        #if there is only one driver
        if num==1:
            race_input=select_race_driver(races_driver,drivers, lap_times, races, driver_input)
            return driver_input, race_input


        elif i==(num-1):
            race_input=select_race_drivers(races_driver,drivers, lap_times, races, driver_input,num)
            return driver_input, race_input

        else :
            race_input = 0
    error("Big Error")

#given a single driverId, and a list of all its races, make the user choose a race, return race_input
#(used in select_race)
def select_race_driver(races_driver,drivers,lap_times,races,driver_input):
    ctr = 0

    while True:
        if ctr == 0:
            print("Races where the selected driver competed:\n")
            for year, name, id in races_driver[0]:
                print(f"{year}, {name}, {id}")

        ctrl = 1

        if len(races_driver[0]) == 0:
            error("Your driver didn't compete in any race! ")
            driver_input[0]=select_driver(1,drivers)
            races_driver[0]=select_races_list(driver_input[0],lap_times,races)

        else:
            err = 0
            try:
                race_input = int(input("Select your race from the ones above (insert the raceId) : "))

            except:
                error("You need to insert a valid raceId! ")
                err = 1

            if err != 1:
                for id, year, name in races_driver[0]:
                    if id == race_input:
                        test = 1

                if test != 1:
                    error("You need to insert a valid raceId! ")
                else:
                    print("race Input")
                    return race_input

#given a list of races_driver[], and a list of all their races, make the user choose a race, return race_input
#(used in select_race)
def select_race_drivers(races_driver,drivers,lap_times,races,driver_input,num):

    #using a set select all the common races
    ids = []
    for j in range(num):
        ids.append({id for id, _, _ in races_driver[j]})
    if num==2:
        common_races= ids[0] & ids[1]
    if num==3:
        common_races= ids[0] & ids[1] & ids[2]
    if num==4:
        common_races= ids[0] & ids[1] & ids[2] & ids[3]


    ctr=0
    while True:
        if len(common_races) != 0:
            if ctr==0:
                print("Races where all your drivers competed: ")
                for id, year, name in races_driver[0]:
                    if id in common_races:
                        print(f"{id}, {year}, {name}")
            err = 0
            ctr=1
            try:
                race_input = int(input("Select your race from the ones above (insert the raceId) : "))

            except:
                error("You need to insert a valid raceId! ")
                err = 1

            if err != 1:
                test=0
                for id, year, name in races_driver[0]:
                    if id == race_input:
                        test = 1
                if test != 1:
                    error("You need to insert a valid raceId! ")
                else:
                    return race_input
        else:
            error("Your drivers don't share any race !") #make the user select other drivers
            for l in range(num):
                driver_input[l] = select_driver(1, drivers)
                races_driver[l] = select_races_list(driver_input[l], lap_times, races)
            ids=[]
            for j in range(num):
                ids.append({id for id, _, _ in races_driver[j]})
            if num == 2:
                common_races = ids[0] & ids[1]
            if num == 3:
                common_races = ids[0] & ids[1] & ids[2]
            if num == 4:
                common_races = ids[0] & ids[1] & ids[2] & ids[3]

#select rows to analyze, order the data, select variables for the title, then call create_plot()
def compute_data(race_input, driver_input, races, drivers, lap_times, num, flg) :

    laps_row=[]
    laps_str=[]
    times=[]
    laps=[]
    laps_sorted=[]
    times_sorted=[]
    ignore=[]
    index=[]
    driver_name=[]
    driver_surname=[]

    for i in range(num):

            laps_row.append(lap_times[(lap_times['raceId'] == race_input) & (lap_times['driverId'] == driver_input[i])]) #select the rows

            laps_str.append(list(laps_row[i].iloc[:,2])) #select the laps
            laps.append([int(x) for x in laps_str[i]] ) #convert all elements in int
            times.append(list((laps_row[i].iloc[:,4]))) #select the times

            #convert times to sort them
            times_in_seconds = [time_to_seconds(t) for t in times[i] if isinstance(t, str) and ':' in t]

            #sort the data
            #combine the three lists and order them for the third element (times_in_seconds)
            sorted_data = sorted(zip(laps[i], times[i], times_in_seconds), key=lambda x: x[2])

            #divide the three elements (the last one is not used)
            laps_tmp, time_tmp, ignore_values = zip(*sorted_data)

            laps_sorted.append(laps_tmp)
            times_sorted.append(time_tmp)

            index=find_row_driver(driver_input[i],drivers) #find the index
            driver_name.append(str(drivers.iloc[index,4]))
            driver_surname.append(str(drivers.iloc[index,5]))

    i = 0
    for race in races.iloc[:, 0]:  # for each raceId in races
        if race == race_input:  # if  raceId selected == raceId input we found our race
            race_name = str(races.iloc[i, 4])
            race_year = str(races.iloc[i, 1])
            break
        else:
            i = i + 1

    #if you selected visualize
    if flg==1:
        create_plot(laps_sorted, times_sorted, num, race_name, race_year, driver_name, driver_surname)

    #if you selected stats
    elif flg==0:
        for j in range(num):
            stat_driver(driver_name[j],driver_surname[j],laps_sorted[j],times_sorted[j],laps_row[j])

##FUNCTION 1
#create plot for the time analysis, given the number of drivers (num)  and arrays for drivers names and surnames
def create_plot(laps_sorted, times_sorted, num, race_name, race_year, driver_name, driver_surname):
    plt.rcParams["figure.figsize"] = (15, 10) #set dimension of the plot

    #create the subplots dynamically, based on the number of drivers selected
    cols = (num + 1) // 2
    rows = 2 if num > 1 else 1

    fig, axs = plt.subplots(rows, cols, squeeze=False)  # create a grid for sublots
    if num!=1:
        fig.suptitle(f"{race_name} {race_year}", fontsize=14)  # global title for more than one driver (the specific driver will be specified later)
    else:
        fig.suptitle(f"Times for Lap for {driver_name[0]} {driver_surname[0]} at The  {race_name} {race_year}", fontsize=14)  # global title for one driver


    #calculate the number of laps of the gp
    number_laps = []
    for j in laps_sorted:
        number_laps.append(max(j))

    laps_total = max(number_laps)
    laps_driver = []

    for i in range(num):

        # colors of the subplot
        if i==0:
            color='red'
        elif i==1:
            color='blue'
        elif i==2:
            color='green'
        else:
            color='yellow'

        col, row = divmod(i, 2)  # calculate row and coloumns
        axs[row, col].bar(laps_sorted[i], times_sorted[i], color=color, edgecolor='black')
        if num!=1:
         axs[row, col].set_title(f"Times for Lap for {driver_name[i]} {driver_surname[i]}", fontsize=10) #subtitle for more than one driver (later)

        laps_driver.append(max(laps_sorted[i])) #calculate the laps the driver has completed

        #show only first, last and one every 5 times in the plot
        yticks=[]
        for t in range(laps_driver[i]):
            if t==1:
                yticks.append(times_sorted[i][0])
            if t%5==0:
                yticks.append(times_sorted[i][t-1])
            elif t==number_laps:
                yticks.append(times_sorted[i][t-1])


        axs[row, col].set_yticks(yticks) #set the ticks on the y-axis

    #remove empty subplots
    for j in range(num, rows * cols):
        row, col = divmod(j, 2)
        fig.delaxes(axs[row, col])

    #layout of the plot
    plt.style.use('dark_background')
    plt.tight_layout(rect=[0, 0, 1, 0.95])  #space for the global title
    fig.subplots_adjust(hspace=0.5)
    plt.show()


##FUNCTION 2
#calculate the stats FOR EACH DRIVER (cycle in ln 244) given driver name and surname
def stat_driver(name, surname, laps_sorted, times_sorted, laps_row):

    fastest_lap = times_sorted[0]
    slowest_lap = times_sorted[len(times_sorted)-1]
    biggest_delta = time_to_seconds(slowest_lap)-time_to_seconds(fastest_lap)
    times_in_seconds = [time_to_seconds(t) for t in times_sorted]
    total_time = sum(times_in_seconds)
    medium_pace = total_time / len(laps_sorted)

    #calculate the lap of the fastest and slowest time
    i=0
    for t in laps_row.iloc[:, 4]:
        if t==fastest_lap :
            fastest_lap_number = int(laps_row.iloc[i,2])
        elif t == slowest_lap:
            slowest_lap_number = int(laps_row.iloc[i,2])
        i=i+1

    positions = list(laps_row.iloc[:, 3])
    best_position = min(positions)
    worst_position= max(positions)
    best_laps=[]
    worst_laps=[]

    #calculate the lap(s) with the best and worst position
    i=0
    for t in laps_row.iloc[:, 3]:
        if t==best_position:
            best_laps.append(laps_row.iloc[i,2])
        elif t==worst_position:
            worst_laps.append(laps_row.iloc[i,2])
        i=i+1
    best_laps_int = [int(x) for x in best_laps]
    worst_laps_int = [int(x) for x in worst_laps]

    starting_position= laps_row.iloc[min(laps_sorted) - 1,3]
    finishing_position = laps_row.iloc[max(laps_sorted) - 1,3]


    ###PRINT
    print("\n")
    print("Statistics for", str(name), " ", str(surname),"\n")
    print("Fastest Lap: ", fastest_lap, " on Lap ", fastest_lap_number)
    print("Slowest Lap: ", slowest_lap, " on Lap ",slowest_lap_number )
    print("The Biggest Delta Between Laps is: ", seconds_to_time_str(biggest_delta))
    print("The Total Time is: ", seconds_to_time_str(total_time))
    print("The Medium Pace is: ", seconds_to_time_str(medium_pace))


    print("Starting Position: ", starting_position)
    print("Finishing Position: ",finishing_position )

    #calculate if the driver gained/lost positions or remained the same
    if starting_position > finishing_position:
        delta_positions = starting_position - finishing_position
        print("Positions Gained: ", delta_positions)
    elif starting_position < finishing_position:
        delta_positions = finishing_position - starting_position
        print("Positions Lost: ", delta_positions)
    else:
        delta_position = 0
        print("No Positions Gained or Lost")
    if best_position==worst_position :
        print("The driver didnt change its position during the race (",best_position,")")
    else:
        print("The Best Position is ", best_position, " on Lap(s) ", best_laps_int)
        print("The Worst Position is ", worst_position, " on Lap(s) ", worst_laps_int)

    print("\n")

##FUNCTION 3
#make the user choose a race and create a plot with the positions of the drivers in that gp
def races_grid(lap_times,races,drivers):

    print_all_races(races)

    while True:
        try:
            grand_prix_input = int(input("Select your Grand Prix from the ones above (insert the raceId): "))
            if grand_prix_input not in lap_times["raceId"].values:
                if 1<=grand_prix_input<=1144:
                    error("Race not present in the database")
            else:
                break
        except ValueError:
            print("You need to insert a valid raceId!")


    print("\nYou selected raceId:", grand_prix_input)
    print(races[races["raceId"] == grand_prix_input].iloc[:, [0, 3, 4, 5, 2]], "\n")

    #extract the driverId of the drivers in that gp
    drivers_grand_prix = lap_times[lap_times["raceId"] == grand_prix_input]["driverId"].unique()

    #create matrix with positions of the drivers
    matrix = []
    laps = []

    for driver in drivers_grand_prix:
        driver_lap_times = lap_times[
            (lap_times["raceId"] == grand_prix_input) &
            (lap_times["driverId"] == driver)
        ].sort_values("lap")

        laps.append(driver_lap_times["lap"].tolist())  # Lista dei giri
        matrix.append(driver_lap_times["position"].tolist())  # Posizioni nei giri

    plt.figure(figsize=(10, 6), facecolor='black')

    #set color to black
    ax = plt.gca()
    ax.set_facecolor('black')

    # set colors to white (to see them with dark background
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')


    #graph for each driver
    for i, driver in enumerate(drivers_grand_prix):
        driver_info = drivers[drivers['driverId'] == driver].iloc[0]
        driver_label = f"{driver_info['forename']} {driver_info['surname']}"

        plt.plot(laps[i], matrix[i])

        x_position = laps[i][-1] + 0.5
        y_position = matrix[i][-1]

        plt.text(
            x_position, y_position, driver_label,  # Coordina X e Y (aggiusta per evitare sovrapposizioni)
            fontsize=8, color="white", ha='left', va='center',
            bbox=dict(facecolor='none', edgecolor='none')
        )



    i = 0
    for race in races.iloc[:, 0]:  # for each raceId in races
        if race == grand_prix_input:  # if  raceId selected == raceId input we found our race
            race_name = str(races.iloc[i, 4])
            race_year = str(races.iloc[i, 1])
            break
        else:
            i = i + 1

    max_y = max(max(posizioni) for posizioni in matrix)  # Posizione massima
    plt.yticks(range(1, max_y + 1))  # Mostra i numeri da 1 a max_y

    #plot settings
    plt.title(f"Driver Positions at {race_name} {race_year}", color='white')
    plt.xlabel("Lap",color='white')
    plt.ylabel("Position",color='white')
    plt.gca().invert_yaxis() #invert y-axis (1st place up)
    plt.tight_layout()
    plt.show()

