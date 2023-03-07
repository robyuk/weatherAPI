from flask import Flask, render_template
import pandas as pd
from pathlib import Path

data_folder = 'data_small'
stations = pd.read_csv(f'{data_folder}/stations.txt', skiprows=17)  # , index_col=0)
stations.set_index('STAID', drop=True)  # , inplace=True, drop=True)
# stations = stations.rename_axis(stations.index.name, axis=1).rename_axis()

app = Flask(__name__)


def get_station_data(station):
    """
    Reads the station data as a dataframe, ldf
    Calculates Celsius and Fahrenheit values and adds them as rows to the dataframe
    returns the dataframe.
    """
    # filepath = f'{data_folder}/TG_STAID{str(station).zfill(6)}.txt'
    filepath = Path(data_folder, f'TG_STAID{str(station).zfill(6)}.txt')
    if filepath.is_file():
        ldf = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
        ldf['Date'] = ldf['    DATE'].astype(str)
        ldf['Celsius'] = ldf['   TG'].mask(ldf[' Q_TG'] == 9) / 10
        ldf['Fahrenheit'] = ldf['Celsius'] * (9 / 5) + 32
    else:
        ldf = pd.DataFrame()
    return ldf


@app.route('/')
def home():
    example = {
        'data': {
            "    DATE": "Wed, 26 Oct 1988 00:00:00 GMT",
            " Q_TG": 0,
            " SOUID": 36122,
            "Celsius": 1.5,
            "Date": "1988-10-26",
            "Fahrenheit": 34.7
        },
        "location": {
            "       LON": "+018:03:00",
            "      LAT": "+59:21:00",
            "CN": "SE",
            "HGHT": 44,
            "STAID": 10,
            "STANAME                                 ": "STOCKHOLM                               "
        }
    }

    return render_template('home.html', example=example, data=stations.to_html(index=False))


@app.route('/api/v1/<station>/<date>')
def stn_data(station, date):
    df = get_station_data(station)
    location = stations.loc[stations['STAID'] == int(station)].squeeze().to_dict()
    # print(type(location), location)
    if location['STAID'] == {}:
        return {'status': 'Station not found'}

    status = 'OK'

    if len(date) == 8:
        datestamp = f'{date[:4]}-{date[4:6]}-{date[6:]}'
        data = df[df['Date'].str.startswith(str(datestamp))][
            [' SOUID', '    DATE', 'Date', 'Celsius', 'Fahrenheit', ' Q_TG']
        ].squeeze().to_dict()

        if data['Date'] == {}:
            status = 'Date out of range'

        return {'location': location,
                'data': data,
                'status': status}

    elif len(date) == 4:
        datestamp = str(date)
    elif len(date) == 6:
        datestamp = f'{date[:4]}-{date[4:6]}'
    else:
        return {'status': 'Invalid Date'}

    data = df[df['Date'].str.startswith(str(datestamp))][
        [' SOUID', '    DATE', 'Date', 'Celsius', 'Fahrenheit', ' Q_TG']
        ].to_dict(orient='records')

    if data == []:
        status = 'Date out of range'

    return {'location': location,
            'dataframe': data,
            'status': status}


@app.route('/api/v1/<station>')
def all_data(station):
    df = get_station_data(station)

    data = df[[' SOUID', '    DATE', 'Date', 'Celsius', 'Fahrenheit', ' Q_TG']].to_dict(orient='records')
    return {'station': station,
            'data': data}


if __name__ == '__main__':
    app.run(debug=True, port=5001)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
