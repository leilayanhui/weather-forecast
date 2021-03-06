# -*- coding:utf-8 -*-

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from omw import main, his_list, modify_weat, db
from manu import manu, record


app = Flask(__name__)
bootstrap = Bootstrap(app)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="kirolan",
    password="msQl1234",
    hostname="kirolan.mysql.pythonanywhere-services.com",
    databasename="kirolan$weather_opm_daily"
)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/', methods=['POST', 'GET'])
def query_weather():
    error = None
    if request.method == 'POST':
        if request.form['submit'] == "help":
            return render_template('main_ch5.html', help=manu())

        elif request.form['submit'] == "history":
            return render_template('main_ch5.html', history=set(his_list))

        elif request.form['submit'] == '查询':
            user_enter = request.form['location']
            user_enter = user_enter.strip().capitalize()
            result = main(user_enter)
            return render_template('main_ch5.html', location=result)

        elif request.form['submit'] == '更改':
            user_enter = request.form['location']
            location = user_enter.strip().capitalize().split(' ')[0]
            weather = user_enter.strip().capitalize().split(' ')[1]
            res = modify_weat(location, weather)
            return render_template('main_ch5.html', update=res)
        else:
            error = 'Something wrong'

    elif request.method == 'GET':
        return render_template('main_ch5.html')

    else:
        error = 'Something wrong'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
