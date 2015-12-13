#!/opt/usr/bin/python

from flup.server.fcgi import WSGIServer
from digihouseapp import app

if __name__ == '__main__':
    WSGIServer(app).run()
