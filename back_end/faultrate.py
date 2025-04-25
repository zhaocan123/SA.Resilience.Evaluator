from app import app, db


class FaultRate(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    fault_json = db.Column(db.LargeBinary)


def add_fault_rate(FR):
    with app.app_context():
        data = FaultRate.query.filter(FaultRate.name == FR.name).first()
        if data is not None:
            data.fault_json = FR.fault_json
        else:
            db.session.add(FR)
        db.session.comm4it()
