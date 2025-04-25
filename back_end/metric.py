from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import app, db
import json
import metricCheck
engine2 = create_engine(app.config['SQLALCHEMY_BINDS']['bak'])


class Metric(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    metricSelected = db.Column(db.LargeBinary)
    metricWeight = db.Column(db.LargeBinary)
    metricResult = db.Column(db.LargeBinary)


class Metric_bak(db.Model):
    __bind_key__ = 'bak'
    __table_args__ = {'extend_existing': True}
    __tablename__ = "metric"
    id = db.Column(db.Integer, primary_key=True)
    id0 = db.Column(db.Integer)
    name = db.Column(db.String(64))
    metricSelected = db.Column(db.LargeBinary)
    metricWeight = db.Column(db.LargeBinary)
    metricResult = db.Column(db.LargeBinary)


def query_metric(name):
    with app.app_context():
        item = Metric.query.filter(Metric.name == name).first()
        return item


def add_or_update_metric(name, metricSelected=None, metricWeight=None, metricResult=None):
    item = query_metric(name)
    if item is None:
        item = Metric(name=name)
        item_bak = Metric_bak(name=name)
        with app.app_context():
            if metricSelected is not None:
                item.metricSelected = str(metricSelected).encode()
                item_bak.metricSelected = str(metricSelected).encode()
            if metricWeight is not None:
                item.metricWeight = str(metricWeight).encode()
                item_bak.metricWeight = str(metricWeight).encode()
            if metricResult is not None:
                item.metricResult = str(metricResult).encode()
                item_bak.metricResult = str(metricResult).encode()
            db.session.add(item)
            db.session.commit()
            db.session.refresh(item)
            db.session.expunge(item)
            item_bak.id0 = item.id
            session2 = scoped_session(sessionmaker(bind=engine2))
            session2.add(item_bak)
            session2.commit()
            session2.close()

            db.session.close()

    else:
        with app.app_context():
            item_bak = Metric_bak(name=name, id0=item.id)
            item1 = Metric.query.get(item.id)
            if metricSelected is not None:
                item1.metricSelected = str(metricSelected).encode()
                item_bak.metricSelected = str(metricSelected).encode()
            if metricWeight is not None:
                item1.metricWeight = str(metricWeight).encode()
                item_bak.metricWeight = str(metricWeight).encode()
            if metricResult is not None:
                item1.metricResult = str(metricResult).encode()
                item_bak.metricResult = str(metricResult).encode()
            session2 = scoped_session(sessionmaker(bind=engine2))
            session2.add(item_bak)
            session2.commit()
            session2.close()
            db.session.commit()
            db.session.close()


def delete_metric(name):
    with app.app_context():
        p = Metric.query.filter(Metric.name == name).first()
        if p is not None:
            db.session.delete(p)
            db.session.commit()
# item = query_metric("saoleisdsd")
# l= json.loads(str(item.metricResult, "UTF-8").replace("\'", "\"").replace("None", "null")) if item.metricResult is not None else None
# over_one ={
#     "平均响应时间":{
#     "min":0,
#     "max":100000
# },"响应时间的充分性":{"min":0,
# "max":100000},"平均周转时间":{"min":0,
# "max":100000},"周转时间充分性":{"min":0,
# "max":100000},
#                 "平均吞吐量":{"min":0,
# "max":100000},"事务处理容量":{"min":0,
# "max":100000},"用户访问量":{"min":0,
# "max":100000},"用户访问增长的充分性":{"min":0,
# "max":100000},
#                 "平均失效间隔时间(MTBF)":{"min":0,
# "max":100000},"周期失效率":{"min":0,
# "max":100000},"平均故障通告时间":{"min":0,
# "max":100000},"平均恢复时间":{"min":0,
# "max":100000},"修改的效率":{"min":0,
# "max":100000},"安装的时间效率":{"min":0,
# "max":100000}}
# print(metricCheck.get_over_one(l))
# print(metricCheck.normalization(l,over_one))

# add_or_update_metric("123")
