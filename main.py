
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import gevent
from img_handler import *

app = Flask(__name__)
app.config.update({
    'DEBUG' : True,
    'SECRET_KEY' : 'development key',
    'USERNAME' : ['admin'],
    'PASSWORD' : ['default'],
    })
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

job_handler = ImageJobHandler()
jobs = []

def spawn_jobs(ws):
    global jobs, job_handler
    cfg = {
            'ws'            : ws,
            'show_in_opt'   : True,
            'show_out_opt'  : True,
            'receive_opt'   : True,
            'send_opt'      : True,
            'work_opt'      : True,
           }

    jobs = [
            gevent.spawn(job_handler.show_channel_in,  0.1) if app.debug else None,
            gevent.spawn(job_handler.show_channel_out, 0.1) if app.debug else None,
            gevent.spawn(job_handler.receive,   0.1),
            gevent.spawn(job_handler.send,      0.1),
            gevent.spawn(job_handler.work,      0.1),
            gevent.spawn(job_handler.warning,   0.1),
            ]

    job_handler.update(cfg)
    gevent.joinall([job for job in jobs if job not in [None]])


def switch_job(job):
    global jobs, job_handler
    cfg = { 'job' : job }
    job_handler.update(cfg)


def kill_jobs():
    global jobs, job_handler
    cfg = {
            'ws'            : None,
            'show_in_opt'   : False,
            'show_out_opt'  : False,
            'receive_opt'   : False,
            'send_opt'      : False,
            'work_opt'      : False,
           }
    job_handler.update(cfg)
    [job.kill() for job in jobs if job not in [None]]
    job_handler.destory()


@app.route('/')
def show_streams():
    return render_template('show_streams.html')


@app.route('/webhandler')
def webhandler(wait=0.1):
    if request.environ.get('wsgi.websocket'):
        spawn_jobs(request.environ['wsgi.websocket'])
    return render_template('show_streams.html')


@app.route('/listen_job', methods=['POST'])
def listen_job():
    if not session.get('logged_in'):
        abort(401)
    kill_jobs()
    switch_job(request.form['img_proc'])
    flash('switch job was successfully posted')
    return redirect(url_for('show_streams'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] not in app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] not in app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_streams'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    kill_jobs()
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_streams'))


if __name__ == '__main__':
    http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

