from app import db


class Stat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    views = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    cost = db.Column(db.FLOAT)

    @staticmethod
    def get_range(date_from, date_to, order_by):
        order_by = 'date' if not order_by else order_by
        result = db.session.query(
            Stat.date,
            db.func.sum(Stat.views),
            db.func.sum(Stat.clicks),
            Stat.cost
        ).group_by(
            Stat.date
        ).filter(
            Stat.date.between(date_from, date_to)
        )
        if order_by == 'date':
            result = result.order_by(Stat.date)
        if order_by == 'views':
            result = result.order_by(db.func.sum(Stat.views))
        if order_by == 'clicks':
            result = result.order_by(db.func.sum(Stat.clicks))
        if order_by == 'cost':
            result = result.order_by(Stat.cost)
        return result.all()

    def __repr__(self):
        return f'<Stat: {self.id}, date: {self.date}, views: {self.views}, cost: {self.cost}>'
