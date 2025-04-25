from multiprocessing import Process

from gevent import pywsgi

from app import app, db
from home_api import home_api
from project_api import project_api


app.register_blueprint(home_api)
app.register_blueprint(project_api)

if __name__ == "__main__":

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    # print("db done!")

    server = pywsgi.WSGIServer((app.config.get("SERVER_IP"), app.config.get("SERVER_PORT")), app)
    server.serve_forever()


# def build_server(port):
#     server = pywsgi.WSGIServer((app.config.get("SERVER_IP"), port), app)
#     server.serve_forever()
#     print("server start at port:{}".format(port))


# if __name__ == '__main__':
#     ports = app.config.get("SERVER_PORT")
#     if ports is None or len(ports) == 0:
#         raise Exception("server port is not config")
#     if len(ports) == 1:
#         server = pywsgi.WSGIServer(listener=(app.config.get("SERVER_IP"), ports[0]), application=app)
#         server.serve_forever()
#     else:
#         for port in ports:
#             Process(target=build_server, args=(port,)).start()
