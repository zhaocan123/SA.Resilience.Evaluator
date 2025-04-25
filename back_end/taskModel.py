from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app import app, db, redis
import pickle
import warnings

warnings.filterwarnings('ignore')
engine2 = create_engine(app.config['SQLALCHEMY_BINDS']['bak'])


class Task(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Integer)
    runParsing = db.Column(db.Integer)
    info_ext = db.Column(db.Integer)
    merge_fun_info = db.Column(db.Integer)
    merge_pro_info = db.Column(db.Integer)
    callback_info = db.Column(db.Integer)
    layer_info = db.Column(db.Integer)
    pipe_info = db.Column(db.Integer)
    sdg_info = db.Column(db.Integer)
    cg_info = db.Column(db.Integer)
    doc_info = db.Column(db.Integer)
    metric_info = db.Column(db.Integer)


class Task_bak(db.Model):
    __bind_key__ = 'bak'
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    id0 = db.Column(db.Integer)
    done = db.Column(db.Integer)
    runParsing = db.Column(db.Integer)
    info_ext = db.Column(db.Integer)
    merge_fun_info = db.Column(db.Integer)
    merge_pro_info = db.Column(db.Integer)
    callback_info = db.Column(db.Integer)
    layer_info = db.Column(db.Integer)
    pipe_info = db.Column(db.Integer)
    sdg_info = db.Column(db.Integer)
    cg_info = db.Column(db.Integer)
    doc_info = db.Column(db.Integer)
    metric_info = db.Column(db.Integer)


def add_task():
    newTask = Task(
        done=0,
    )
    with app.app_context():
        db.session.add(newTask)
        db.session.commit()
        db.session.refresh(newTask)
        db.session.expunge(newTask)
        newTask_bak = Task_bak(
            done=0,
            id0=newTask.id
        )
        session2 = scoped_session(sessionmaker(bind=engine2))
        session2.add(newTask_bak)
        session2.commit()
        session2.close()
        db.session.close()
    return newTask.id


# def queryTasks():
#     # TODO 读取全部的TASK
#     with app.app_context():
#         t = Task.query.all()
#     res = {}
#     for item in t:
#         res[str(item.id)] = {
#             "done": item.done,
#             "runParsing": item.runParsing,
#             "info_ext": item.info_ext,
#             "merge_fun_info": item.merge_fun_info,
#             "merge_pro_info": item.merge_pro_info,
#             "callback_info": item.callback_info,
#             "layer_info": item.layer_info,
#             "pipe_info": item.pipe_info,
#             "backend_ast": item.backend_ast,
#             "backend_input_analyze": item.backend_input_analyze,
#             "backend_myCodeAnalyze": item.backend_myCodeAnalyze,
#             "backend_CMakeProject": item.backend_CMakeProject
#         }
#     return res


def get_task_from_mysql(task_id):
    with app.app_context():
        item = Task.query.get(task_id)
    if item:
        res = {
            "done": item.done,
            "runParsing": item.runParsing,
            "info_ext": item.info_ext,
            "merge_fun_info": item.merge_fun_info,
            "merge_pro_info": item.merge_pro_info,
            "callback_info": item.callback_info,
            "layer_info":   item.layer_info,
            "pipe_info": item.pipe_info,
            "sdg_info": item.sdg_info,
            "cg_info": item.cg_info,
            "doc_info": item.doc_info,
            "metric_info": item.metric_info,
        }
        return res
    else:
        print("Task not found")
        return {}


def get_task(task_id):
    res = get_task_from_mysql(task_id)
    return res


def update_task(task_id, task_data):
    with app.app_context():
        t = Task.query.get(task_id)
        newTask_bak = Task_bak(
            id0=task_id
        )
        newTask_bak.runParsing = task_data["runParsing"]
        t.runParsing = task_data["runParsing"]
        newTask_bak.info_ext = task_data["info_ext"]
        t.info_ext = task_data["info_ext"]
        newTask_bak.merge_fun_info = task_data["merge_fun_info"]
        t.merge_fun_info = task_data["merge_fun_info"]
        newTask_bak.merge_pro_info = task_data["merge_pro_info"]
        t.merge_pro_info = task_data["merge_pro_info"]
        newTask_bak.callback_info = task_data["callback_info"]
        t.callback_info = task_data["callback_info"]
        newTask_bak.layer_info = task_data["layer_info"]
        t.layer_info = task_data["layer_info"]
        newTask_bak.pipe_info = task_data["pipe_info"]
        t.pipe_info = task_data["pipe_info"]
        newTask_bak.sdg_info = task_data["sdg_info"]
        t.sdg_info = task_data["sdg_info"]
        newTask_bak.cg_info = task_data["cg_info"]
        t.cg_info = task_data["cg_info"]
        newTask_bak.doc_info = task_data["doc_info"]
        t.doc_info = task_data["doc_info"]
        newTask_bak.metric_info = task_data["metric_info"]
        t.metric_info = task_data["metric_info"]
        newTask_bak.done = task_data["done"]
        t.done = task_data["done"]
        session2 = scoped_session(sessionmaker(bind=engine2))
        session2.add(newTask_bak)
        session2.commit()
        session2.close()
        db.session.commit()

# id = add_task()
# print(get_task(id))
# task_dict = {
#             "done": 1,
#             "runParsing": None,
#             "info_ext": None,
#             "merge_fun_info": None,
#             "merge_pro_info": None,
#             "callback_info": None,
#             "layer_info": None,
#             "pipe_info": None,
# }
# update_task(6, task_dict)
# get_task(6)
# add_task()
