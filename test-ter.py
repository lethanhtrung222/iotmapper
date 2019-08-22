#!/usr/bin/env python
from flask import Flask
import subprocess
from multiprocessing import Queue
import random
from threading import Thread
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route("/map/")

def map():
    cmd = ["sh","zim.sh"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out

@app.route('/hello/<name>')
def hello_name(name):
    la = name.split(',')
    return 'Hello '+ la[0] + '!' + la[1]

@app.route('/vtri/<pos>')
def vtri(pos):
    ll = pos.split(',')
    cmd = ["sh","shodan.sh",ll[0],ll[1]]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return ll[0]+" and "+ ll[1]+ " and "+out

@app.route('/nmap/<ip>')

def nmap(ip):
    nip = str(ip)
    cmd = ["nmap",nip,"-sV","-Pn","--script","vuln"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out + " and " +nip

@app.route('/')
def index():
    n = random.randint(0, 100)
    q.put(n)
    return '%s\n' % n


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print('Processing %s' % item)  # do the work e.g. update database
        cmd = ["sh","shodan.sh"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        out,err = p.communicate()
        time.sleep(50)
        q.task_done()

if __name__ == "__main__" :
    q = Queue()
    t = Thread(target=worker)
    t.start()
    app.run(host='127.0.0.1', port=3333, debug=True)
    q.join()
    q.put(None)
    t.join()
