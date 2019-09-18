import csv
import pandas as pd
import requests
import sys
from Adafruit_CharLCD import Adafruit_CharLCD
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, time
from time import sleep


def get_bus_schedule():
    """Retrieve the bus schedule for a given bus stop, put everything into pandas dataframe
    output: pandas dataframe
    """

    # bus stop number is received via command line argument
    stop = sys.argv[1]
    URL = 'https://www.scmtd.com/en/stop/' + stop
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    # remove garbage information
    [s.extract() for s in soup('span', attrs={'class': 'detailsBelow'})]
    [s.extract() for s in soup('td', attrs={'class': 'request-details dim'})]

    # locate the metro table
    table = soup.find('table', attrs={'class': 'metrotable'})

    # load metro table to data frame
    bus_times_table = pd.DataFrame(columns=range(0, 5), index=range(0, 60))
    row_marker = 0

    try:
        for row in table.find('tbody').find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                bus_times_table.iat[row_marker,
                                    column_marker] = column.get_text()
                column_marker += 1
            row_marker += 1

        return(bus_times_table)

    except:
        message = "no bus times!"
        print(message)
        print_on_display(message)


def time_until_next_bus():
    """Display the countdown
    input: datetime object
    """

    arrival_time = get_arrival_time(get_bus_schedule())
    current_time = datetime.now()

    print('arrival time: ', arrival_time)
    print('current time: ', current_time)

    while (arrival_time > current_time):
        delta = get_delta(arrival_time, current_time)
        message = "Next bus in: \n %dh %dm %ds" % remaining_time(
            delta)

        print(message)
        print_on_display(message)
        sleep(1)
        current_time = datetime.now()

        if(delta == 0):
            arrival_time = get_arrival_time(get_bus_schedule())
            current_time = datetime.now()


def get_delta(arrival, now):
    """Calculate the time difference, convert to seconds
    input: datetime object
    output: datetime object
    """

    delta = arrival - now
    delta = delta.days * 24 * 3600 + delta.seconds

    return(delta)


def remaining_time(seconds):
    """Calculate the remaining time
    input: datetime object
    output: datetime object
    """

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    return (hours, minutes, seconds)


def get_arrival_time(metro_df):
    """Grab soonest bus arrival time from the dataframe
    convert to 24 hour time if time is pm, and make change date to today
    input: pandas dataframe
    output: datetime object

    TODO: Currently the while loop  will go on infinitely if metro_df.iat[0, 0] holds a time
    from tomorrow.
    """

    arrival_time = datetime.now()
    i = 0

    while(arrival_time <= datetime.now()):
        print(arrival_time)
        time = metro_df.iat[i, 0]
        am_or_pm = time[-2:]
        i += 1

        arrival_time = datetime.strptime(time, '%H:%M%p')
        arrival_time = arrival_time.replace(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

        # convert to 24 hour time if pm
        if (am_or_pm == 'pm'):
            arrival_time = arrival_time + timedelta(hours=12)

    return(arrival_time)


def print_on_display(message):
    lcd = Adafruit_CharLCD(rs=26, en=19,
                           d4=13, d5=6, d6=5, d7=11,
                           cols=16, lines=2)

    lcd.clear()
    lcd.message(message)


def main():
    time_until_next_bus()


if __name__ == "__main__":
    main()
