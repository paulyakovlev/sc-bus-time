import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, time
from time import sleep


def get_bus_schedule():
    """Retrieve the bus schedule for a given bus stop, put everything into pandas dataframe
    output: pandas dataframe
    """

    # currently looking at bus stop id 1232, but can be changed to others
    URL = "https://www.scmtd.com/en/stop/1232#tripDiv"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    # remove garbage information
    [s.extract() for s in soup('span', attrs={'class': 'detailsBelow'})]
    [s.extract() for s in soup('td', attrs={'class': 'request-details dim'})]

    # locate the metro table
    table = soup.find('table', attrs={'class': 'metrotable'})

    # load metro table to data frame
    bus_times_table = pd.DataFrame(columns=range(0, 5), index=range(0, 41))
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
        print(bus_times_table)
        return(bus_times_table)

    except AttributeError:
        raise


def time_until_next_bus(arrival_time):
    """Display the countdown
    input: datetime object
    """

    try:
        current_time = datetime.now()

        print('arrival time: ', arrival_time)
        print('current time: ', current_time)

        while (arrival_time > current_time):
            print("%dd %dh %dm %ds" % remaining_time(
                get_delta(arrival_time, current_time)))
            sleep(1)
            current_time = datetime.now()

    except AttributeError:
        return "No buses running"


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
    """Grab first element from the metro dataframe, which should be the soonest bus arrival time
    convert to 24 hour time if time is pm, and make change date to today
    input: pandas dataframe
    output: datetime object
    """

    time = metro_df.iat[0, 0]
    am_or_pm = time[-2:]

    #
    arrival_time = datetime.strptime(time, '%H:%M%p')
    arrival_time = arrival_time.replace(
        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

    # convert to 24 hour time if pm
    if (am_or_pm == 'pm'):
        arrival_time = arrival_time + timedelta(hours=12)

    return(arrival_time)


def main():
    time_until_next_bus(get_arrival_time(get_bus_schedule()))


if __name__ == "__main__":
    main()
