import os

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

bind = "0.0.0.0:5020"
#workers = numCPUs() * 2 + 1
workers = 5
backlog = 2048
#worker_class ="sync"
worker_class =  "gevent"
debug = True
#daemon = True
pidfile ="/tmp/gunicorn_starter_vid.pid"
logfile ="/tmp/gunicorn_starter_vid.log"
