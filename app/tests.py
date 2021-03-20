import unittest
from app import app, db
from app.models import Stat
from datetime import datetime
import requests


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_part_data(self):
        date = datetime.strptime("2021.03.20", '%Y.%m.%d').date()
        stat = Stat(date=date)
        db.session.add(stat)
        db.session.commit()
        count = len(Stat.query.all())
        stat1 = Stat.query.first()
        self.assertEqual(count, 1)
        self.assertEqual(stat1, stat)

    def test_add_full_data(self):
        date = datetime.strptime("2021.03.20", '%Y.%m.%d').date()
        stat = Stat(date=date, views=100, clicks=50, cost=13.54)
        db.session.add(stat)
        db.session.commit()
        count = len(Stat.query.all())
        stat1 = Stat.query.first()
        self.assertEqual(count, 1)
        self.assertEqual(stat1, stat)

    def test_simple_show(self):
        date1 = datetime.strptime("2021.03.20", '%Y.%m.%d').date()
        stat = Stat(date=date1, views=100, clicks=50, cost=13.54)
        db.session.add(stat)

        date2 = datetime.strptime("2021.03.21", '%Y.%m.%d').date()
        stat = Stat(date=date2, views=100, clicks=50, cost=13.54)
        db.session.add(stat)

        date3 = datetime.strptime("2021.03.22", '%Y.%m.%d').date()
        stat = Stat(date=date3, views=100, clicks=50, cost=13.54)
        db.session.add(stat)

        db.session.commit()
        result = Stat.get_range(date1, date2, None)
        self.assertEqual(len(result), 2)

    def test_save(self):
        response = requests.post('http://localhost:5000/save', json={
            'date': '2018.04.04',
            'clicks': 10,
            'views': 50
        })
        self.assertEqual(response.status_code, 200)

    def test_show(self):
        date1 = datetime.strptime("2021.03.20", '%Y.%m.%d').date()
        stat = Stat(date=date1, views=100, clicks=50, cost=13.54)
        db.session.add(stat)

        date2 = datetime.strptime("2021.03.21", '%Y.%m.%d').date()
        stat = Stat(date=date2, views=100, clicks=51, cost=13.54)
        db.session.add(stat)

        date3 = datetime.strptime("2021.03.22", '%Y.%m.%d').date()
        stat = Stat(date=date3, views=100, clicks=52, cost=13.54)
        db.session.add(stat)

        db.session.commit()
        response = requests.get('http://localhost:5000/show?from=2010.01.01&to=2021.03.21&order_by=clicks')
        self.assertEqual(response.status_code, 200)