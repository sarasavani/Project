import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import yticks


#converts seconds into string
def seconds_to_time_str(total_seconds):
    # Calcola ore, minuti, secondi e millisecondi
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)

    # Crea la stringa formattata, rimuovendo ore e minuti se sono 0
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}.{milliseconds:03}"
    else:
        return f"{minutes}:{seconds:02}.{milliseconds:03}"

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
            print("in")
            race_input=select_race_driver(races_driver,drivers, lap_times, races, driver_input)
            return driver_input, race_input


        elif i==(num-1):
            race_input=select_race_drivers(races_driver,drivers, lap_times, races, driver_input,num)
            return driver_input, race_input

        else :
            race_input = 0
    error("Big Error")


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

def select_race_drivers(races_driver,drivers,lap_times,races,driver_input,num):
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
            error("Your drivers don't share any race !")
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


#given the error string, print the error
def error(error_string) :
    print("Error! " + error_string)

#given the driverId, finds the row of the selected driver in drivers
#returns row, the row in which the driver is located (the dataset is a bit random with indexes)
def find_row_driver(driver_input,drivers) :
    row=0
    for d in drivers.iloc[:,0] :
        if driver_input==d:
            return row
        else: row=row+1
    error("driver not found")

#given a time in a string format, convert it into seconds (used for sorting values)

#select rows to analyze, order the data, select variables for the title, then call create_plot()
def compute_data(race_input, driver_input, races, drivers, lap_times, num, flg) :
    #Flg 0 == print stat, else dont print stats
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
            laps_tmp, time_tmp, ignore_values = zip(*sorted_data)  # Scomponi sorted_data

            laps_sorted.append(laps_tmp)  # Aggiungi laps alla lista
            times_sorted.append(time_tmp)  # Aggiungi times alla lista

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


    if flg==1:
        create_plot(laps_sorted, times_sorted, num, race_name, race_year, driver_name, driver_surname)

    elif flg==0:
        for j in range(num):
            stat_driver(driver_name[j],driver_surname[j],laps_sorted[j],times_sorted[j],laps_row[j])



def create_plot(laps_sorted, times_sorted, num, race_name, race_year, driver_name, driver_surname):
    # Imposta la dimensione della figura
    plt.rcParams["figure.figsize"] = (15, 10)

    # Crea i subplot dinamicamente
    cols = (num + 1) // 2  # Numero di righe: arrotonda verso l'alto ogni 2 subplot
    rows = 2 if num > 1 else 1  # Usa 2 colonne solo se ci sono più di 1 subplot

    fig, axs = plt.subplots(rows, cols, squeeze=False)  # Crea la griglia di subplot
    fig.suptitle(f"{race_name} {race_year}", fontsize=14)  # Titolo globale della figura

    number_laps = []
    for j in laps_sorted:
        number_laps.append(max(j))

    laps_total = max(number_laps)
    laps_driver=[]

    for i in range(num):
        # Determina posizione del subplot
        if i==0:
            color='red'
        elif i==1:
            color='blue'
        elif i==2:
            color='green'
        else:
            color='yellow'

        col, row = divmod(i, 2)  # Calcola riga e colonna
        axs[row, col].bar(laps_sorted[i], times_sorted[i], color=color, edgecolor='black')
        axs[row, col].set_title(f"Times for Lap for {driver_name[i]} {driver_surname[i]}", fontsize=10)
        #axs[row, col].set_xlabel("Lap", fontsize=8)
        #axs[row, col].set_ylabel("Time", fontsize=8)

        laps_driver.append(max(laps_sorted[i]))
        yticks=[]

        for t in range(laps_driver[i]):
            if t==1:
                yticks.append(times_sorted[i][0])
            if t%5==0:
                yticks.append(times_sorted[i][t-1])
            elif t==number_laps:
                yticks.append(times_sorted[i][t-1])


        axs[row, col].set_yticks(yticks)

        # Rimuovi eventuali subplot vuoti
    for j in range(num, rows * cols):
        row, col = divmod(j, 2)
        fig.delaxes(axs[row, col])  # Rimuovi assi vuoti

    # Ottimizza il layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Lascia spazio per il titolo globale
    fig.subplots_adjust(hspace=0.5)
    plt.show()

def compute_data_compare(lap_times,race_input,first_driver,second_driver,races,drivers):

    laps_row_first = lap_times[(lap_times['raceId'] == race_input) & (lap_times['driverId'] == first_driver)]  # select the rows
    laps_row_second = lap_times[(lap_times['raceId'] == race_input) & (lap_times['driverId'] == second_driver)]  # select the rows


    laps_str_first = list(laps_row_first.iloc[:,2]) #select the laps
    laps_first = [int(x) for x in laps_str_first]  #convert all elements in int
    times_first= list((laps_row_first.iloc[:,4])) #select the times

    laps_str_second = list(laps_row_second.iloc[:, 2])  # select the laps
    laps_second = [int(x) for x in laps_str_second]  # convert all elements in int
    times_second = list((laps_row_second.iloc[:, 4]))  # select the times

    #convert times to sort them
    times_in_seconds_1 = [time_to_seconds(t) for t in times_first]
    times_in_seconds_2 = [time_to_seconds(t) for t in times_second]


    #sort the data
    #combine the three lists and order them for the third element (times_in_seconds)
    sorted_data_first = sorted(zip(laps_first, times_first, times_in_seconds_1), key=lambda x: x[2])
    #divide the three elements (the last one is not used)
    laps_sorted_first, times_sorted_first, _ = zip(*sorted_data_first)

    # combine the three lists and order them for the third element (times_in_seconds)
    sorted_data_second = sorted(zip(laps_second, times_second, times_in_seconds_2), key=lambda x: x[2])
    # divide the three elements (the last one is not used)
    laps_sorted_second, times_sorted_second, _ = zip(*sorted_data_second)
####### common
    i = 0
    for race in races.iloc[:, 0]:  # for each raceId in races
        if race == race_input:  # if  raceId selected == raceId input we found our race
            race_name = str(races.iloc[i, 4])
            race_year = str(races.iloc[i, 1])
            break
        else:
            i = i + 1

#######not common
    index_first = find_row_driver(first_driver, drivers)  # find the index
    first_driver_name = str(drivers.iloc[index_first, 4])
    first_driver_surname = str(drivers.iloc[index_first, 5])

    index_second = find_row_driver(second_driver, drivers)  # find the index
    second_driver_name = str(drivers.iloc[index_second, 4])
    second_driver_surname = str(drivers.iloc[index_second, 5])

    print("\n")
    stat_driver(first_driver_name,first_driver_surname,laps_sorted_first,times_sorted_first,laps_row_first)
    stat_driver(second_driver_name,second_driver_surname,laps_sorted_second,times_sorted_second,laps_row_second)

def seconds_to_time_2(seconds):
    """Converti un tempo in secondi in formato stringa (mm:ss.SSS)."""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes}:{seconds:.3f}"

def stat_driver(name, surname, laps_sorted, times_sorted, laps_row):

    fastest_lap = times_sorted[0]
    slowest_lap = times_sorted[len(times_sorted)-1]
    biggest_delta = time_to_seconds(slowest_lap)-time_to_seconds(fastest_lap)
    times_in_seconds = [time_to_seconds(t) for t in times_sorted]
    total_time = sum(times_in_seconds)
    medium_pace = total_time / len(laps_sorted)

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
    i=0
    for t in laps_row.iloc[:, 3]:
        if t==best_position:
            best_laps.append(laps_row.iloc[i,2])
        elif t==worst_position:
            worst_laps.append(laps_row.iloc[i,2])
        i=i+1


    starting_position= laps_row.iloc[min(laps_sorted) - 1,3]
    finishing_position = laps_row.iloc[max(laps_sorted) - 1,3]

    best_laps_int = [int(x) for x in best_laps]
    worst_laps_int = [int(x) for x in worst_laps]


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


def create_plot_v2(laps_sorted, times_sorted, num, race_name, race_year, driver_name, driver_surname):
    # Imposta la dimensione della figura
    plt.rcParams["figure.figsize"] = (15, 10)

    # Determina le dimensioni della griglia dei subplot
    cols = (num + 1) // 2  # Numero di righe: arrotonda verso l'alto ogni 2 subplot
    rows = 2 if num > 1 else 1  # Usa 2 colonne solo se ci sono più di 1 subplot

    fig, axs = plt.subplots(rows, cols, squeeze=False)  # Crea la griglia di subplot
    fig.suptitle(f"{race_name} {race_year}", fontsize=14)  # Titolo globale della figura

    for i in range(num):
        # Determina posizione del subplot
        col, row = divmod(i, 2)  # Calcola riga e colonna

        # Converti i tempi in secondi
        times_in_seconds = [time_to_seconds(t) for t in times_sorted[i]]

        # Colori personalizzati per ogni subplot
        colors = ['red', 'blue', 'green', 'yellow']
        color = colors[i % len(colors)]

        # Disegna il grafico
        axs[row, col].bar(laps_sorted[i], times_in_seconds, color=color, edgecolor='black')
        axs[row, col].set_title(f"Times for Lap for {driver_name[i]} {driver_surname[i]}", fontsize=10)
        axs[row, col].set_xlabel("Lap", fontsize=8)
        axs[row, col].set_ylabel("Time", fontsize=8)

        # Calcola i tick dinamicamente per l'asse Y
        yticks = np.linspace(min(times_in_seconds), max(times_in_seconds), num=6)  # 6 tick uniformi
        axs[row, col].set_yticks(yticks)
        axs[row, col].set_yticklabels([seconds_to_time(t) for t in yticks])  # Converti in formato mm:ss.SSS

    # Rimuovi eventuali subplot vuoti
    for j in range(num, rows * cols):
        row, col = divmod(j, 2)
        fig.delaxes(axs[row, col])  # Elimina subplot inutilizzati

    # Ottimizza il layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Lascia spazio per il titolo globale
    fig.subplots_adjust(hspace=0.5)
    plt.show()


def time_to_seconds(time_str):
    """Converti un tempo stringa (mm:ss.SSS) in secondi float."""
    minutes, seconds = time_str.split(":")
    return int(minutes) * 60 + float(seconds)


def seconds_to_time(seconds):
    """Converti un tempo in secondi in formato stringa (mm:ss.SSS)."""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes}:{seconds:.3f}"
