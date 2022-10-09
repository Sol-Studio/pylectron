import webview
from flask import Flask, send_from_directory, request, Response
import sys, os, re, contextlib, time, ctypes, threading, json
from io import StringIO
import backend_apis
@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old


app = Flask(__name__)
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r





@app.route("/page/<path:path>")
def page_route(path):
    html = open(os.path.join('pages', path+".html"), encoding="utf-8").read()
    return html

@app.route("/static/<path:path>")
def static_route(path):
    return send_from_directory("static", path)


@app.route("/api/<name>")
def api_route(name):
    with stdoutIO() as s:
        return_value = eval("backend_apis."+name)(request.args.to_dict())
    
    return Response(json.dumps({"return_value": return_value["return_value"], "stdout":s.getvalue()[:-1]}), status=return_value["status"])


class thread_with_exception(threading.Thread):
    def __init__(self, app): 
        threading.Thread.__init__(self) 
        self.app = app
              
    def run(self):
        try: 
            self.app.run("127.0.0.1", 8080)
        finally:
            pass
           
    def get_id(self): 
  
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure')
       
serverThread = thread_with_exception(app) 
window = webview.create_window(title="loading", url='http://127.0.0.1:8080/page/index')

def on_close():
    serverThread.raise_exception() 
    serverThread.join()
window.events.closing += on_close


def on_load():
    window.set_title(window.evaluate_js("""document.querySelector("title").text"""))
window.events.loaded += on_load




backend_apis.init(window)
serverThread.start()
webview.start(gui="edgechromium", debug=True)
