from app import app, db
from app.models import Stat
from flask import request, jsonify
import datetime


@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    date = data['date'] if 'date' in data else None
    views = data['views'] if 'views' in data else 0
    clicks = data['clicks'] if 'clicks' in data else 0
    cost = data['cost'] if 'cost' in data else 0
    try:
        date = datetime.datetime.strptime(date, '%Y.%m.%d').date()
    except ValueError:
        return jsonify(error="Incorrect date"), 400
    except TypeError:
        return jsonify(error="Date not found"), 400
    print(data, date, views, clicks, cost)
    stat = Stat(date=date, views=views, clicks=clicks, cost=cost)
    db.session.add(stat)
    db.session.commit()
    return jsonify(success=True)


@app.route('/show', methods=['GET'])
def show():
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    order_by = request.args.get('order_by')
    print(date_from, date_to)
    try:
        date_from = datetime.datetime.strptime(date_from, '%Y.%m.%d').date()
        date_to = datetime.datetime.strptime(date_to, '%Y.%m.%d').date()
    except ValueError:
        return jsonify(error="Incorrect date"), 400
    except TypeError:
        return jsonify(error="Date not found"), 400
    result = Stat.get_range(date_from, date_to, order_by)
    result_arr = []
    for res in result:
        date_json = {
            'date':  res[0].strftime("%Y.%m.%d"),
            'views': res[1],
            'clicks': res[2],
            'cost': res[3],
        }
        try:
            date_json['cpc'] = round(res[3] / res[2], 2)
        except ZeroDivisionError:
            date_json['cpc'] = 0
        try:
            date_json['cpm'] = round(res[3] / res[1] * 1000, 2)
        except ZeroDivisionError:
            date_json['cpm'] = 0
        result_arr.append(date_json)
    print(result_arr)
    return jsonify(result=result_arr)


@app.route('/clear')
def clear():
    db.session.query(Stat).delete()
    db.session.commit()
    return jsonify(success=True)


