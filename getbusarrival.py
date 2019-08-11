import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_bus_schedule():
    URL = "https://www.scmtd.com/en/stop/1232#tripDiv"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    [s.extract() for s in soup('span', attrs={'class': 'detailsBelow'})]
    [s.extract() for s in soup('td', attrs={'class': 'request-details dim'})]

    table = soup.find('table', attrs={'class': 'metrotable'})

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
        time = get_bus_schedule().iat[0, 0]
        arrival_time = datetime.strptime(time, '%H:%M%p').strftime('%H:%M')
        current_time = datetime.now().strftime('%H:%M')

        print('arrival time: ', arrival_time)
        print('current time: ', current_time)

        delta = datetime.strptime(
            arrival_time, '%H:%M') - datetime.strptime(current_time, '%H:%M')

        return(delta)

    except AttributeError:
        return "No buses running"


def main():
    print('next bus arrives in: ', time_until_next_bus())


if __name__ == "__main__":
    main()
