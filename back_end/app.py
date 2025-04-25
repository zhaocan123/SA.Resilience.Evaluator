import json
import os
from concurrent.futures import ThreadPoolExecutor

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from multiprocessing import cpu_count

from sqlalchemy import create_engine

app = Flask(__name__)

CORS(app, resources=r'/*', supports_credentials=True)

# 加载配置文件
path = os.getcwd()
with open("./config.json", "r", encoding="utf-8") as f:
    content = json.load(f)
app.config['SQLALCHEMY_DATABASE_URI'] = content['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_BINDS'] = {'bak': content['SQLALCHEMY_BIND']}
# app.config['SQLALCHEMY_ECHO'] = content['SQLALCHEMY_ECHO']
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
app.config["UPLOADS_DEFAULT_DEST"] = content["UPLOADS_DEFAULT_DEST"]
app.config["SERVER_IP"] = content["SERVER_IP"]
app.config["SERVER_PORT"] = content["SERVER_PORT"]
app.config["STATIC_FOLDER"] = content["STATIC_FOLDER"]
app.config["EXE_PATH"] = path.replace("\\", "/")
app.config['REDIS_URL'] = content["REDIS_URL"]
redis = FlaskRedis(app)
# db绑定app
db = SQLAlchemy()
db.init_app(app)


# 线程池
executor = ThreadPoolExecutor(max_workers=cpu_count()*4)
# # 缓存
# tasks = {}
