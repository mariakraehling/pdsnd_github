import time
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 100)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = ['chicago', 'new york city', 'washington']
    city = ''
    while True:
        try:
            city = input('For which city would you like to see data? (Chicago, New York City or Washigton?) ').lower()
            if city in valid_cities:
                break
            else:
                print('Please enter a valid city name: Chicago, New York City or Washington ')
        except:
            print('Please enter a valid city name: Chicago, New York City or Washington ')

    # get user input for month (all, january, february, ... , june)
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = ''
    while True:
        answer = input('Would you like to filter by month? (yes, no) ').lower()
        if answer == 'yes':
            while True:
                month = input('By which month would you like to filter? (january, february, ... , june) ').lower()
                if month in valid_months:
                    break
                else:
                    print('Please enter a valid month name: january, february, march, april, may or june.')
            break
        elif answer == 'no':
            month = 'all'
            break
        else:
            print('Please enter yes or no.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = ''
    while True:
        answer = input('Would you like to filter by day? (yes, no) ').lower()
        if answer == 'yes':
            while True:
                day = input('By which day would you like to filter? (Monday, Tuesday, ... , Sunday) ').title()
                if day in valid_days:
                    break
                else:
                    print('Please enter a valid day name: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.')
            break
        elif answer == 'no':
            day = 'all'
            break
        else:
            print('Please enter yes or no.')

    print('-'*40)

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
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of the week'] = df['Start Time'].dt.weekday


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        days =  ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day)
        df = df[df['Day of the week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('The most common month is ', popular_month)

    # display the most common day of week
    popular_day = df['Day of the week'].mode()[0]
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    popular_day = day_dict[popular_day]
    print('The most common day is ', popular_day)

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Hour'].mode()[0]
    print('The most common hour is ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most common start station is ', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most common end station is ', popular_end)

    # display most frequent combination of start station and end station trip
    df['Trip'] = 'from ' + df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Trip'].mode()[0]
    print('The most common trip is ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #print('The total travel time is ', round((df['Trip Duration'].sum()/60/60), 0), ' hours.')
    total_time = df['Trip Duration'].sum()
    print('The total travel time is ', int(total_time//(3600*24)), ' days and ', int(total_time%(3600*24)//3600), 'hours.' )

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The mean travel time per trip is ', int(mean_time//60), ' minutes and ', int(round((mean_time%60), 0)), ' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city_name):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types[0], ' users are of type ', user_types.index[0])
    print(user_types[1], ' users are of type ', user_types.index[1])
    print("\n")

    # Display counts of gender
    if city_name != 'washington':
        gender_types = df['Gender'].value_counts()
        print(gender_types[0], ' users are ', gender_types.index[0])
        print(gender_types[1], ' users are ', gender_types.index[1])
        print("\n")

    # Display earliest, most recent, and most common year of birth
    if city_name != 'washington':
        print('The earliest year of birth is ', df['Birth Year'].min())
        print('The most recent year of birth is ', df['Birth Year'].max())
        print('The most common year of birth is ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # get user input, if raw should be displayed
        show_data = input('\nWould you like to see some raw data? Please enter yes or no. ')
        if show_data == 'yes':
            print(df.head())
            n_lines = 10
            while True:
                show_more = input('\nWould you like to see more data?')
                if show_more == 'yes':
                    print(df.head(n_lines))
                    n_lines += 5
                else:
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
