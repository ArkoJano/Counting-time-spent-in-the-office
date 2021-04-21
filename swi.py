from pprint import pprint
import csv
from datetime import datetime, timedelta, date, time

        #testy :
        #- sprawdzic z ujemna data
        #- sprawdzic z jakimis zlymi danymi, zrobic validacje tego wszystkiego
        #   np. pusty wiersz
        #       niepoprawny format: daty, eventu, bramki
        #

# def get_one_day(input_list):
    
#     one_day = list()

#     for dates in input_list:    # funkcja zbiera jeden dzien
        
#         one_date = datetime.strptime(dates[date], "%Y-%m-%d %H:%M:%S ")

#         if ( len(one_day) == 0 or one_date.day == one_day[-1].day):
#             one_day.append(one_date)
#         else:
#             break

#     return one_day

# def get_all_days(input_read):
#     tmp_dict = dict()

#     for day in input_read:
#         one_date = datetime.strptime(day[date], "%Y-%m-%d %H:%M:%S ")
#         tmp_dict[one_date.day] = list()
    
#     return tmp_dict

# def fill_all_days_with_time(input_read, dict_of_days):
#     for time in input_read:
#         one_day = datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S ")
#         dict_of_days[one_day.date()].append(one_day.time())
#     return dict_of_days


# ------------------------- To dziala ------------------------------------

#   DZIALAJACA WERSJA NA KULCZACH-TYGODNIACH, WARTOSCIACH-DNIACH
def get_last_days(dict_of_days):

    list_of_last_days = dict()

    last_day = list(dict_of_days.keys())[0] #pierwszy wiersz w slowniku

    week_of_last_day = last_day.isocalendar()[1]

    list_of_last_days[week_of_last_day] = last_day

    for day in dict_of_days:

        week_of_last_day = last_day.isocalendar()[1] #zwraca tydzien w ktotrym znajduje sie ten dzien
        week_of_this_day = day.isocalendar()[1]      #to samo tylko dla rozpatrywanego dnia

        # jesli rok jest ten sam
        if day.year == last_day.year:
                #jesli tydzien jest ten dam
            if  week_of_last_day ==  week_of_this_day:
                    #numer dnia w tygodniu danego dnia jest wiekszy od "ostatniego", np: czwartek > wtorku
                if day.weekday() >= list_of_last_days[week_of_last_day].weekday():
                    # zamien ostatni dzien na aktualnie rozpatrywany pod tym kluczem 
                    list_of_last_days[week_of_last_day] = day
                    # i zmienna last_day ustaw na rozpatrywany dzien
                    last_day = day
            else:
                #jesli sa z roznych tygodni to stworz nowy klucz z tym dniem
                list_of_last_days[week_of_this_day] = day
                # i przypisz do zmiennej last_day
                last_day = day
        else:
            #jesli sa z roznych lat to stworz nowy klucz z tym dniem
            list_of_last_days[week_of_this_day] = day
            # i przypisz do zmiennej last_day
            last_day = day


    return(list_of_last_days)


        



date_format = "%Y-%m-%d %H:%M:%S "

with open('input.csv', 'r') as input_file:
    input_read = csv.reader(input_file, delimiter=';')


    next(input_read)        #pomija pierwszy element
    


    input_list = list(input_read)
    


    _date  = 0   # zmienne odpowiadajace wartosciom w liscie
    event = 1   # zebranej z pliku "input.csv"
    gate  = 2 

    #zmienne odpowiedzialne za wypisywanie odpowiednich koncowek
    # weekend = ""
    # overtime = ""
    # undertime = ""
    # inconclusive = ""
    

    dict_of_days = dict()


  


    
    # stworzenie slownika dni i w nim kolejnego slownika z godzinami wejscia/wyjsca
    # i wpisanie godzin wyjsca wejsca pogrupowane dniami
    for index in range(len(input_list)):

        formated_date = datetime.strptime( input_list[index][_date], date_format ).date()
        if formated_date not in dict_of_days.keys():
            dict_of_days[formated_date] = { 
                'entry_hours':list(),
                'exit_hours':list(),
                'sum_of_work': int(),
                'flags':{
                    'weekend':"",
                    'overtime':"", 
                    'undertime':"", 
                    'inconclusive':""}
            }
        
        formated_date = datetime.strptime( input_list[index][_date], date_format ).date()
        formated_time = datetime.strptime( input_list[index][_date], date_format ).time()
        
        if "entry" in input_list[index][event]:
            dict_of_days[formated_date]['entry_hours'].append(formated_time)

        elif "exit" in input_list[index][event]:
           dict_of_days[formated_date]['exit_hours'].append(formated_time)
        

# ------------------------- To dziala ------------------------------------

    # oblicza czas pracy tego dnia
    for day in dict_of_days:
        tmp_date = date(1, 1, 1)

        if ( len(dict_of_days[day]['entry_hours']) == 0 ):
            dict_of_days[day]['flags']['inconclusive'] = "i"

            start_work = datetime.combine(tmp_date, dict_of_days[day]['exit_hours'][0])
            end_work = datetime.combine(tmp_date, dict_of_days[day]['exit_hours'][-1])
            suma = end_work - start_work 
            

            dict_of_days[day]['sum_of_work'] =  timedelta(seconds = suma.seconds)

        elif (len(dict_of_days[day]['exit_hours']) == 0):
            dict_of_days[day]['flags']['inconclusive'] = "i"

            start_work = datetime.combine(tmp_date, dict_of_days[day]['entry_hours'][0])
            end_work = datetime.combine(tmp_date, dict_of_days[day]['entry_hours'][-1])
            suma = end_work - start_work 

            dict_of_days[day]['sum_of_work'] =  timedelta(seconds = suma.seconds)
        
        else:
            
            start_work = datetime.combine(tmp_date, dict_of_days[day]['entry_hours'][0])
            end_work = datetime.combine(tmp_date, dict_of_days[day]['exit_hours'][-1])
            suma = end_work - start_work 
            print("start: ", start_work, "end: ", end_work, "sum: ", suma)

            dict_of_days[day]['sum_of_work'] =  timedelta(seconds = suma.seconds)

    
    #pprint(dict_of_days)

    # wypisywanie ostatecznego komunikatu
    for day in dict_of_days:
        time_of_work = str(dict_of_days[day]['sum_of_work'])

        hours_of_work = datetime.strptime(time_of_work, "%H:%M:%S").hour
        
        default_time_of_work = timedelta( hours= 40 )

        weekly_time_of_work = ""
        

        if (day.weekday() == 5 or day.weekday() == 6):  #weekend
            dict_of_days[day]['flags']['weekend'] = "w"
        
        if ( dict_of_days[day]['sum_of_work'] > timedelta(hours=9) ):
            dict_of_days[day]['flags']['overtime'] = "ot"
        
        if ( dict_of_days[day]['sum_of_work'] < timedelta(hours=6) ):
            dict_of_days[day]['flags']['undertime'] = "ut"

        #to nie chodzi tylko o piatek ale o kazdy ostatni dzien tygodnia

        # print( day.isocalendar()[1] )
        # day.isocalendar()[1] - zwraca numer tygodnia w roku

        #last_day = list(dict_of_days.keys())[0]
        # if day.isocalendar()[1] == last_day.isocalendar()[1]:
        #     if day.weekday() == 4 or day.weekday() == 5 or day.weekday() == 6:
        #         last_day = day
        #         pass
        #     last_day = day
        # else:
        #     pass


        dict_of_last_days = get_last_days(dict_of_days)
        
        #print("last_days: ", dict_of_last_days.items() )
        
        # ostatni dzien - suma calego przepracowanego czasu
        for item in dict_of_last_days:

            if day in dict_of_last_days.values():

                weekly_time_of_work = timedelta(seconds=0)                                     #zmienna przechowujaca przepracowany czas
                days_to_Monday = day.weekday()                    #zmienna ktora pomaga przeskoczyc na poniedzialek
                next_day = timedelta(days=1)                                  #nastepny dzien
                week_day = day - timedelta(days=days_to_Monday)              #ustawione na poniedzialek
                while week_day != (day+next_day):                            # dopoki nie dojdzie do piatku
                    if week_day in dict_of_days.keys():                     #sprawdzamy czy ten dzien jest w slowniku
                        sum_of_work = dict_of_days[week_day]['sum_of_work']         #ladujemy do zmiennej prace w sekundach
                        
                        weekly_time_of_work += sum_of_work
                    else:
                        pass
                    week_day = week_day + next_day
                


        weekend = dict_of_days[day]['flags']['weekend']
        overtime = dict_of_days[day]['flags']['overtime']
        undertime = dict_of_days[day]['flags']['undertime']
        inconclusive = dict_of_days[day]['flags']['inconclusive']


        print(f"Day {day} Work {time_of_work} {weekend} {overtime} {undertime} {inconclusive} {weekly_time_of_work}")
    


    
    # potrzebuje funkcji ktora bedzie sprawdzac czy wszedl czy wyszedl
    # i dopiero bedzie dodawac odpowiednio czas spedzony w pracy

 

            # jesli w GATE poziom 0 (E/0/*)
            # to znaczy ze wyszedl z pracy
            # reszta bram to nadal bramy
            # w pracy


    with open('result', 'w') as result:
        pass   # plik wyjsciowy 