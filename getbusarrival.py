import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def get_bus_schedule():

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


def time_until_next_bus():
    try:
        # getting first entry for now, as it is the next upcoming bus
        time = get_bus_schedule().iat[0, 0]
        am_or_pm = time[-2:]
        print(am_or_pm)
        print(time)

        # format the time
        arrival_time = datetime.strptime(time, '%H:%M%p').strftime('%H:%M')
        arrival_time = datetime.strptime(arrival_time, '%H:%M')

        if (am_or_pm == 'pm'):
            print('its pm!')
            arrival_time = arrival_time + timedelta(hours=12)

        current_time = datetime.now().strftime('%H:%M')
        current_time = datetime.strptime(current_time, '%H:%M')

        print('arrival time: ', arrival_time)
        print('current time: ', current_time)

        # get difference
        delta = arrival_time - current_time

        return(delta)

    except AttributeError:
        return "No buses running"


def main():
    print('next bus arrives in: ', time_until_next_bus())


if __name__ == "__main__":
    main()
