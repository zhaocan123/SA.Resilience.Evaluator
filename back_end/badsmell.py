from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import app, db
engine2 = create_engine(app.config['SQLALCHEMY_BINDS']['bak'])


class BadSmell(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(64), unique=True)
    threshold = db.Column(db.LargeBinary)
    c_overLongFunc = db.Column(db.BLOB(length=2**26-1))
    c_overLongParam = db.Column(db.BLOB(length=2**26-1))
    c_overCommentLineFunc = db.Column(db.BLOB(length=2**26-1))
    c_overDeepCall = db.Column(db.BLOB(length=2**26-1))
    c_overInOutDegreeFunc = db.Column(db.BLOB(length=2**26-1))
    c_funcCopy = db.Column(db.BLOB(length=2**26-1))
    c_overCyclComplexityFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_overLongFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_overLongParam = db.Column(db.BLOB(length=2**26-1))
    cpp_overCommentLineFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_overDeepCall = db.Column(db.BLOB(length=2**26-1))
    cpp_overInOutDegreeFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_funcCopy = db.Column(db.BLOB(length=2**26-1))
    cpp_overCyclComplexityFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_lazyClass = db.Column(db.BLOB(length=2**26-1))
    cpp_largeClass = db.Column(db.BLOB(length=2**26-1))
    cpp_shotgunSurgery = db.Column(db.BLOB(length=2**26-1))
    cpp_featureEnvy = db.Column(db.BLOB(length=2**26-1))
    cpp_dataClass = db.Column(db.BLOB(length=2**26-1))


class BadSmell_bak(db.Model):
    __bind_key__ = 'bak'
    __table_args__ = {'extend_existing': True}
    __tablename__ = "badsmell"
    id = db.Column(db.Integer, primary_key=True)
    id0 = db.Column(db.Integer)
    project_name = db.Column(db.String(64))
    threshold = db.Column(db.LargeBinary)
    c_overLongFunc = db.Column(db.BLOB(length=2**26-1))
    c_overLongParam = db.Column(db.BLOB(length=2**26-1))
    c_overCommentLineFunc = db.Column(db.BLOB(length=2**26-1))
    c_overDeepCall = db.Column(db.BLOB(length=2**26-1))
    c_overInOutDegreeFunc = db.Column(db.BLOB(length=2**26-1))
    c_funcCopy = db.Column(db.BLOB(length=2**26-1))
    c_overCyclComplexityFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_overLongFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_overLongParam = db.Column(db.BLOB(length=2**26-1))
    cpp_overCommentLineFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_overDeepCall = db.Column(db.BLOB(length=2**26-1))
    cpp_overInOutDegreeFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_funcCopy = db.Column(db.BLOB(length=2**26-1))
    cpp_overCyclComplexityFunc = db.Column(db.BLOB(length=2**26-1))
    cpp_lazyClass = db.Column(db.BLOB(length=2**26-1))
    cpp_largeClass = db.Column(db.BLOB(length=2**26-1))
    cpp_shotgunSurgery = db.Column(db.BLOB(length=2**26-1))
    cpp_featureEnvy = db.Column(db.BLOB(length=2**26-1))
    cpp_dataClass = db.Column(db.BLOB(length=2**26-1))

# with app.app_context():
#     db.drop_all()
#
#     db.create_all()


def add_bad_smell(BS):
    with app.app_context():
        data = BadSmell.query.filter(BadSmell.project_name == BS.project_name).first()
        newBadSmell_bak = BadSmell_bak()
        if data is not None:

            data.threshold = BS.threshold
            data.c_overLongFunc = BS.c_overLongFunc
            data.c_overLongParam = BS.c_overLongParam
            data.c_overCommentLineFunc = BS.c_overCommentLineFunc
            data.c_overDeepCall = BS.c_overDeepCall
            data.c_overInOutDegreeFunc = BS.c_overInOutDegreeFunc
            data.c_funcCopy = BS.c_funcCopy
            data.c_overCyclComplexityFunc = BS.c_overCyclComplexityFunc
            data.cpp_overLongFunc = BS.cpp_overLongFunc
            data.cpp_overLongParam = BS.cpp_overLongParam
            data.cpp_overCommentLineFunc = BS.cpp_overCommentLineFunc
            data.cpp_overDeepCall = BS.cpp_overDeepCall
            data.cpp_overInOutDegreeFunc = BS.cpp_overInOutDegreeFunc
            data.cpp_funcCopy = BS.cpp_funcCopy
            data.cpp_overCyclComplexityFunc = BS.cpp_overCyclComplexityFunc
            data.cpp_lazyClass = BS.cpp_lazyClass
            data.cpp_largeClass = BS.cpp_largeClass
            data.cpp_shotgunSurgery = BS.cpp_shotgunSurgery
            data.cpp_featureEnvy = BS.cpp_featureEnvy
            data.cpp_dataClass = BS.cpp_dataClass
            newBadSmell_bak.id0 = data.id
            newBadSmell_bak.threshold = BS.threshold
            newBadSmell_bak.c_overLongFunc = BS.c_overLongFunc
            newBadSmell_bak.c_overLongParam = BS.c_overLongParam
            newBadSmell_bak.c_overCommentLineFunc = BS.c_overCommentLineFunc
            newBadSmell_bak.c_overDeepCall = BS.c_overDeepCall
            newBadSmell_bak.c_overInOutDegreeFunc = BS.c_overInOutDegreeFunc
            newBadSmell_bak.c_funcCopy = BS.c_funcCopy
            newBadSmell_bak.c_overCyclComplexityFunc = BS.c_overCyclComplexityFunc
            newBadSmell_bak.cpp_overLongFunc = BS.cpp_overLongFunc
            newBadSmell_bak.cpp_overLongParam = BS.cpp_overLongParam
            newBadSmell_bak.cpp_overCommentLineFunc = BS.cpp_overCommentLineFunc
            newBadSmell_bak.cpp_overDeepCall = BS.cpp_overDeepCall
            newBadSmell_bak.cpp_overInOutDegreeFunc = BS.cpp_overInOutDegreeFunc
            newBadSmell_bak.cpp_funcCopy = BS.cpp_funcCopy
            newBadSmell_bak.cpp_overCyclComplexityFunc = BS.cpp_overCyclComplexityFunc
            newBadSmell_bak.cpp_lazyClass = BS.cpp_lazyClass
            newBadSmell_bak.cpp_largeClass = BS.cpp_largeClass
            newBadSmell_bak.cpp_shotgunSurgery = BS.cpp_shotgunSurgery
            newBadSmell_bak.cpp_featureEnvy = BS.cpp_featureEnvy
            newBadSmell_bak.cpp_dataClass = BS.cpp_dataClass
            session2 = scoped_session(sessionmaker(bind=engine2))
            session2.add(newBadSmell_bak)
            session2.commit()
            session2.close()
            db.session.commit()
            db.session.close()
        else:
            db.session.add(BS)
            db.session.commit()
            db.session.refresh(BS)
            db.session.expunge(BS)
            db.session.close()
            newBadSmell_bak.id0 = BS.id
            newBadSmell_bak.threshold = BS.threshold
            newBadSmell_bak.c_overLongFunc = BS.c_overLongFunc
            newBadSmell_bak.c_overLongParam = BS.c_overLongParam
            newBadSmell_bak.c_overCommentLineFunc = BS.c_overCommentLineFunc
            newBadSmell_bak.c_overDeepCall = BS.c_overDeepCall
            newBadSmell_bak.c_overInOutDegreeFunc = BS.c_overInOutDegreeFunc
            newBadSmell_bak.c_funcCopy = BS.c_funcCopy
            newBadSmell_bak.c_overCyclComplexityFunc = BS.c_overCyclComplexityFunc
            newBadSmell_bak.cpp_overLongFunc = BS.cpp_overLongFunc
            newBadSmell_bak.cpp_overLongParam = BS.cpp_overLongParam
            newBadSmell_bak.cpp_overCommentLineFunc = BS.cpp_overCommentLineFunc
            newBadSmell_bak.cpp_overDeepCall = BS.cpp_overDeepCall
            newBadSmell_bak.cpp_overInOutDegreeFunc = BS.cpp_overInOutDegreeFunc
            newBadSmell_bak.cpp_funcCopy = BS.cpp_funcCopy
            newBadSmell_bak.cpp_overCyclComplexityFunc = BS.cpp_overCyclComplexityFunc
            newBadSmell_bak.cpp_lazyClass = BS.cpp_lazyClass
            newBadSmell_bak.cpp_largeClass = BS.cpp_largeClass
            newBadSmell_bak.cpp_shotgunSurgery = BS.cpp_shotgunSurgery
            newBadSmell_bak.cpp_featureEnvy = BS.cpp_featureEnvy
            newBadSmell_bak.cpp_dataClass = BS.cpp_dataClass
            session2 = scoped_session(sessionmaker(bind=engine2))
            session2.add(newBadSmell_bak)
            session2.commit()
            session2.close()


def del_bad_smell(name):
    with app.app_context():
        data = BadSmell.query.filter(BadSmell.project_name == name).first()
        if data is not None:
            db.session.delete(data)
            db.session.commit()
        else:
            return False


# add_bad_smell(BadSmell())
