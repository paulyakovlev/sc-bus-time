# Santa Cruz Bus Time

## Description
This python script estimates the amount of time remaining until a bus arrives at your stop.
	
## Installation
[Connect a 16x2 LCD display to the Pi](https://www.rototron.info/lcd-display-tutorial-for-raspberry-pi/)

Clone the repository:
```
$ git clone https://github.com/paulyakovlev/sc-bus-time.git
```

Download the required packages:
```
$ sudo apt-get install python-pandas
$ sudo apt-get install bs4
$ sudo pip install adafruit-charlcd
```
	
## Usage
Simply run the script and provide a Santa Cruz Metro bus stop number via command line argument:

```
$ cd sc-bus-time
$ python bustime.py 1232
```