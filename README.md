# Python Weather API
A web API to provide the average temperature for a given date at a 
given weather station, written in Python and flask

To view the home page, clone the repository, run the main.py

then point your browser to http://localhost:5001

To get the average temperature for <station> on <date> (where the date format is YYYYMMDD), the URL format is:
http://localhost:5001/api/v1/station/date

For example to get the average temperature recorded at station 10 on 25 October 1988:
http://localhost:5001/api/v1/10/19881025

See the home page for the web app for more information about available stations, their locations, and available dates.

## Code is in the 'master' branch