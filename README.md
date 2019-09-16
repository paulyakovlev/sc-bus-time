# Santa Cruz Bus Time

## Description
This python script estimates the amount of time remaining until a bus arrives at your stop.
	
## Installation
[Connect a 16x2 LCD display to the Pi](https://www.rototron.info/lcd-display-tutorial-for-raspberry-pi/)

Download the required packages:

```
$ sudo apt-get install python-pandas
$ sudo apt-get install bs4
$ sudo pip install adafruit-charlcd
```
	
## Usage
To run this project, simply clone the repo and run the Python script:

```
$ git clone https://github.com/paulyakovlev/sc-bus-time.git
$ cd sc-bus-time
$ python bustime.py
```