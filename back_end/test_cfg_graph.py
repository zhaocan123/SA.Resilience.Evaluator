from flask import Flask, Response
app = Flask(__name__, static_folder=r"E:\CPP_master\dev0815\CPP_support\back_end\static")

@app.get('/cfg_graph.html')
def cfg_pdg_graph():
    with open("static/cfg_graph.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@app.get('/sdg.html')
def sdg_graph():
    with open("static/sdg.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@app.get('/comp.html')
def comp_graph():
    with open("static/comp.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@app.get('/FLCG.dot.html')
def flcg_graph():
    with open("static/FLCG.dot.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@app.get('/PLCG.dot.html')
def plcg_graph():
    with open("static/PLCG.dot.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@app.get('/pipe_filter.html')
def pipe_filter_graph():
    with open("static/pipe_filter.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@app.get('/callback.html')
def call_back_html():
    with open("static/callback.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

@app.get('/level.html')
def level_html():
    with open("static/level.html", 'rb') as f:
        fileas = f.read()
        resp = Response(fileas)
    return resp

# @app.get('/CFGPDG/dot_file_to_html/<filename>')
# def cfg_pdg_resource(filename):
#     print(filename)
#     with open(f"static_graphs/dot_file_to_html/{filename}", 'rb') as f:
#         fileas = f.read()
#         resp = Response(fileas)
#     return resp

if __name__ == "__main__":
    app.run(host='127.0.0.1', port="12456")