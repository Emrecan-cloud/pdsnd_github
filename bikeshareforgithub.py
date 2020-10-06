import time
import pandas as pd
import numpy as np
import click
import datetime as dt


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday')

# providing the right inputs which come from users otherwise it will not let it start.
def choice(prompt, choices=('y', 'n')):


    while True:
        choice = input(prompt).lower().strip()
# if the input is end, it will terminate the program
        if choice == 'leave':
            raise SystemExit
# triggering if the input has only one name
        elif ',' not in choice:
            if choice in choices:
                break
# triggering if the input has more than one name
        elif ',' in choice:
            choice = [a.strip().lower() for a in choice.split(',')]
            if list(filter(lambda b: b in choices, choice)) == choice:
                break

        prompt = ("\nThere is something wrong with your choices. You should be more careful while typing and formatting\n>")

    return choice


def get_filters():
    """Ask user to specify city(ies) and filters, month(s) and weekday(s).
    Returns:
        (str) city -name of the city(ies) to analyze
        (str) month -name of the month(s) to filter
        (str) day -name of the day(s) of week to filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    print("Hellooooo")
    print("Greetings from Turkey")


    print("Please type leave if you would like to leave the program.\n")

    while True:
# TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

        city = choice("\nWhat city or cities do you want to select? New York City, Chicago or Washington? Please use commas to list them.\n>", CITY_DATA.keys())

# TO DO: get user input for month (all, january, february, ... , june)   
        month = choice("\nWhat month or months from january to june do you want to select? Please use commas to list them.\n>", months)
    
# TO DO: get user input for day of week (all, monday, tuesday, ... sunday)      
        day = choice("\nWhat weekday or weekdays do you want to select? Please use commas to list them.\n>", weekdays)

# Now we are going to confirm the choices to go on.
        decision = choice("\nAnd now please make sure that you are applying following filter for the bikeshare data.\n\n City: {}\n Month: {}\n Weekday"
                              ": {}\n\n [y] Yes\n [n] No\n\n>".format(city, month, day))
        if decision == 'y':
            break
        else:
            print("\nSorry! You must try again!")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified filters of city(ies), month(s) and
       day(s) whenever applicable.
    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    print("\nNow we will be loading the data for the filters of your choices.")
    start_time = time.time()

#filtering the data for the selected city filter
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)
#DataFrame columns after a city concatenation
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

#coloumns for showing statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

# filtering the data for the selected month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] == (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nIt takes {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

# TO DO: display the most common month

    most_common_month = df['Month'].mode()[0]
    print('According to your choices, the month which has the most travels is: ' + str(months[most_common_month-1]).title())

# TO DO: display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('According to your choices, the most common day is: ' + str(most_common_day))


# TO DO: display the most common start hour
    most_common_starthour = df['Start Hour'].mode()[0]
    print('According to your choices, the most common start hour is: ' + str(most_common_starthour))

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

# TO DO: display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("Acccording to your choices, the most commonly used start station is: " + most_common_start_station)

# TO DO: display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("According to your choices, the most commonly used end station is: " + most_common_end_station)

 # TO DO: display most frequent combination of start station and end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' + df['End Station'])
    
    most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print("According to your choices, the most common start-end combination is: " + most_common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

# TO DO: display total travel time
    travel_time_intotal = df['Trip Duration'].sum()
    travel_time_intotal = (str(int(travel_time_intotal//86400)) + 'days ' + str(int((travel_time_intotal % 86400)//3600)) +'hours ' + str(int(((travel_time_intotal % 86400) % 3600)//60)) + 'minutes ' + str(int(((travel_time_intotal % 86400) % 3600) % 60)) + 'seconds')
    
    print('According to your choices, the total travel time is : ' + travel_time_intotal)

# TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'minutes ' + str(int(mean_travel_time % 60)) + 'seconds')
    
    print('According to your choices, the mean travel time is : ' + mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

# TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    
    print("Distribution of user types:")
    print(user_types)


# TO DO: Display counts of gender
    try:
        gender_dist = df['Gender'].value_counts().to_string()
        print("\nDistribution for each gender:")
        print(gender_dist)
    except KeyError:
        print("\nSorry! We couldn't find any data of user genders for {}.".format(city.title()))


# TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nAccording to your choices, the oldest person who rides one bike was born in: " + earliest_birth_year)
        
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("\nAccording to your choices, the youngest person who rides one bike was born in: " + most_recent_birth_year)
        
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("\nAccording to your choices, the most common birth year is: " + most_common_birth_year)
    except:
        print("\nSorry! We couldn't find any data of birth year for {}.".format(city.title()))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# 5 line of sorted raw data each time
def raw_data(df, signed_point):
    

#the variable which holds where the user stopped
    if signed_point > 0:
        last_point = choice("\nDo you want to go on from where you stopped last time? \n [y] Yes\n [n] No\n\n>")
        if last_point == 'n':
            signed_point = 0

#we sort the data by coloumns
    if signed_point == 0:
        sortedf = choice("\nHow do you think you would you like to sort the data which is displayed? Press Enter to view "
                         "unsorted.\n \n [st] Start Time\n [et] End Time\n "
                         "[td] Trip Duration\n [ss] Start Station\n "
                         "[es] End Station\n\n>", ('st', 'et', 'td', 'ss', 'es', ''))

        as_or_des = choice("\nBe sorted ascending or descending? \n [a] Ascending\n [d] Descending\n>", ('a', 'd'))

        if as_or_des == 'a':
            as_or_des = True
        elif as_or_des == 'd':
            as_or_des = False

        if sortedf == 'st':
            df = df.sort_values(['Start Time'], ascending=as_or_des)
        elif sortedf == 'et':
            df = df.sort_values(['End Time'], ascending=as_or_des)
        elif sortedf == 'td':
            df = df.sort_values(['Trip Duration'], ascending=as_or_des)
        elif sortedf == 'ss':
            df = df.sort_values(['Start Station'], ascending=as_or_des)
        elif sortedf == 'es':
            df = df.sort_values(['End Station'], ascending=as_or_des)
        elif sortedf == '':
            pass

#each loop shows 5 lines of raw data
    while True:
        for i in range(signed_point, len(df.index)):
            print("\n")
            print(df.iloc[signed_point:signed_point+5].to_string())
            print("\n")
            signed_point += 5

            if choice("Do you want to keep printing more raw data?\n\n[y]Yes\n[n]No\n\n>") == 'y':
                continue
            else:
                break
        break

    return signed_point


def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        signed_point = 0
        while True:
            selected_data = choice("\nPlease select what you would like to see here "
                                 "\n\n [ts] Time Status\n [ss] "
                                 "Station Status\n [tds] Trip Duration Status\n "
                                 "[us] User Status\n [rd] Raw Data\n "
                                 "[r] Restart\n\n>",
                                 ('ts', 'ss', 'tds', 'us', 'rd', 'r'))
            click.clear()
            if selected_data == 'ts':
                time_stats(df)
            elif selected_data == 'ss':
                station_stats(df)
            elif selected_data == 'tds':
                trip_duration_stats(df)
            elif selected_data == 'us':
                user_stats(df, city)
            elif selected_data == 'rd':
                signed_point = raw_data(df, signed_point)
            elif selected_data == 'r':
                break

        restart = choice('\nWould you like to restart the program? Enter y or n. \n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()