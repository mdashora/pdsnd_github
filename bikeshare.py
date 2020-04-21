import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print("\nHello! Let's explore some US bikeshare data!")
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ["Chicago","New York City","Washington"]

    while True:
        try:
            city_number = int(input("\nEnter a number for the city you would like to explore?\n1-Chicago \n2-New York City \n3-Washington\n"))
        except:
            continue
        if city_number in range(1, len(city_list)+1):        
            break
        else:
            print("Sorry, I coundn't uderstand that. Please try again.")
            continue

    city = city_list[city_number - 1]
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month_list = ["all","January","February","March","April","May","June"]

    while True:
        try:
            month_number = int(input("\nEnter a number for your favorite month. \n0-All Months \n1-January \n2-February \n3-March \n4-April \n5-May \n6-June \n"))
        except:
            continue
        if month_number in range(0, len(month_list)):        
            break
        else:
            print("Sorry, I coundn't uderstand that. Please try again.")
            continue

    month = month_list[month_number]    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ["all","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    while True:
        try:
            day_number = int(input("\nEnter a number for your favorite day in a week. \n0-All Days \n1-Sunday \n2-Monday \n3-Tuesday \n4-Wednesday \n5-Thursday \n6-Friday \n7-Saturday \n"))
        except:
            continue
        
        if day_number in range(0, len(day_list)):        
            break
        else:
            print("Sorry, I coundn't uderstand that. Please try again.")
            continue

    day = day_list[day_number]

    print('-'*80)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print("Most common month:", most_common_month)


    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("Most common day of week:", most_common_day)


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("Most common start hour:", most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print("Most Commonly used start station:", start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print("Most Commonly used end station:", end_station)


    # TO DO: display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station'])    
    most_frequest_trip = combination['Trip Duration'].count().idxmax()
    print("Most frequest combination of start station and end station trip:", most_frequest_trip[0], " & ", most_frequest_trip[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print("Total travel time:")
    print("Seconds: ", total_travel_time)
    print("Readable Time: ", convert_seconds(total_travel_time))


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("\nMean travel time:")
    print("Seconds: ", mean_travel_time)
    print("Readable Time: ", convert_seconds(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()    
    print("Types of user:\n", user_types)

    # TO DO: Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print("\nTypes of gender:\n", gender_types)
    except:
        print("\nData not available for gender")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_Year = df['Birth Year'].min()
        print("\nEarliest year of birth:", earliest_Year)
    except:
        print("\nData not available. Could not find earliest year of birth")

    try:
        most_recent_year = df['Birth Year'].max()
        print("\nMost recent year of birth:", most_recent_year)
    except:
        print("\nData not available. Could not find most recent year of birth")

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print("\nMost Common Year:", most_common_year)
    except:
        print("\nData not available. Could not find most common year of birth")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def convert_seconds(seconds):
    """
    Converts number of seconds to easily readable string.
    Args:
        (int) seconds - seconds to convert
    Returns:
        (str) converted_time - number days, hours, minutes, and seconds
    """

    time = seconds
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    converted_time = "{} day, {} hour, {} minutes, {} seconds".format(day, hour, minutes, seconds)
    
    return converted_time

def display_raw_data(df):
    """
    This script prompts the user if they want to see 5 lines of raw data, 
    displays that data if the answer is 'yes', and continue these prompts and
    displays until the user says 'no'.
    """
    rows_to_show = 5
    start_row = 0
    end_row = rows_to_show - 1
    
    print("\nWould you like to see some raw data?")
    while True:
        raw_data = input('\nEnter yes or no.\n')
        if raw_data.lower() == 'yes':
            # display five rows from start and then increment of 5 if user continues
            print("\nRows {} to {}:".format(start_row + 1, end_row + 1))

            print('\n', df.iloc[start_row : end_row + 1])
            start_row += rows_to_show
            end_row += rows_to_show

            print('-'*80)
            print("\nWould you like to see more raw data?")
            continue
        elif raw_data.lower() == 'no':
            break
        else:
            print("Sorry, I coundn't uderstand that. Please try again.")
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input("\nWould you like to restart?\nEnter yes to continue and anything else to exit.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()