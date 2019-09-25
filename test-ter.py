#!/usr/bin/env python
import random
import subprocess
import sys
import time
from threading import Thread

import Queue
from flask import Flask, Response

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route("/a/map/")

def map():
    cmd = ["sh","zim.sh"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out

@app.route('/a/hello/<name>')
def hello_name(name):
    la = name.split(',')
    return 'Hello '+ la[0] + '!' + la[1]
@app.route('/a/info/')
def info():
    cmd = ["lshw"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out

@app.route('/a/vtri/<pos>')
def vtri(pos):
    ll = pos.split(',')
    cmd = ["sh","shodan.sh",ll[0],ll[1]]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()

    return Response(out, mimetype='application/json')


@app.route('/a/camera/<pos>')
def camera(pos):
    ll = pos.split(',')
    cmd = ["sh","camera.sh",ll[0],ll[1]]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()

    return Response(out, mimetype='application/json')


@app.route('/a/printer/<pos>')
def printer(pos):
    ll = pos.split(',')
    cmd = ["sh","printer.sh",ll[0],ll[1]]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()

    return Response(out, mimetype='application/json')



#Brute Admin
@app.route('/a/bruteadmin/<mlink>')
def bruteadmin(mlink):
    #ll = mlink.split(',')
    cmd = ["sh","bruteadmin.sh",mlink]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()

    return Response(out, mimetype='application/json')



# Site bruteadmin
@app.route('/a/sbruteadmin/<slink>')
def sbruteadmin(slink):
    #ll = mlink.split(',')
    cmd = ["sh","sbruteadmin.sh",slink]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()

    return Response(out, mimetype='application/json')



#Brute Password
@app.route('/a/brutepass/<plink>')
def brutepass(plink):
    #ll = mlink.split(',')
    cmd = ["sh","bruteadmin.sh",plink]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()

    return Response(out, mimetype='application/json')


@app.route('/a/host/<ip>')

def host(ip):
    nip = str(ip)
    cmd = ["shodan","host",nip]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out + " and " +nip



@app.route('/a/nmap/<ip>')

def nmap(ip):
    nip = str(ip)
    cmd = ["nmap",nip,"-sV","-Pn"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out + " and " +nip


@app.route('/a/uread/') 
def ureadall(id):
    #ll = mlink.split(',') urlid = 
    #"http://45.63.121.172/api/Uread.php?id=" + str(id)
    cmd = ["curl","http://45.63.121.172/api/Uread.php"]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out,err = p.communicate()
    return Response(out, mimetype='application/json')




@app.route('/') 
def index():
#    return Response(out, mimetype='application/json')
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
    q = Queue.Queue()
    t = Thread(target=worker)
    t.start()
    app.run(host='0.0.0.0', port=3333, debug=True)
    q.join()
    q.put(None)
    t.join()
