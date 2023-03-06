from flask import Flask, render_template
import pandas as pd

data_folder = 'data_small'
stations = pd.read_csv(f'{data_folder}/stations.txt', skiprows=17, index_col=0)
stations = stations.rename_axis(stations.index.name, axis=1).rename_axis(None)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html', data=stations.to_html())


@app.route('/api/v1/<station>/<date>')
def about(station, date):
    filepath = f'{data_folder}/TG_STAID{str(station).zfill(6)}.txt'
    df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
    datestamp = f'{date[:4]}-{date[4:6]}-{date[6:]}'
    temperature = df.loc[df['    DATE'] == datestamp]['   TG'].squeeze() / 10
    return {'station': station,
            'date': date,
            'temperature': temperature}


if __name__ == '__main__':
    app.run(debug=True, port=5001)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
