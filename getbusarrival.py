import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_bus_schedule():
    URL = "https://www.scmtd.com/en/stop/1232#tripDiv"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find('table', attrs={'class': 'metrotable'})

    bus_times_table = pd.DataFrame(columns=range(0, 6), index=range(0, 20))

    row_marker = 0

    try:
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                bus_times_table.iat[row_marker,
                                    column_marker] = column.get_text()
                column_marker += 1
            row_marker += 1
        return(bus_times_table)

    except AttributeError:
        raise


def time_until_next_bus():
    try:
        table = get_bus_schedule()
        time = table.iat[1, 1]
        s1 = datetime.strptime(time, '%I:%M%p')
        s2 = datetime.now()
        FMT = '%H:%M:%S'
        tdelta = s2 - s1
        return(tdelta)
    except AttributeError:
        return "No buses running"


def main():
    print(time_until_next_bus())


if __name__ == "__main__":
    main()
