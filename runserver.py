#!/home/linus/PycharmProjects/flask/bin/python2.7
from flaskr import app

def run():
    app.debug=False
    app.run(host='192.168.1.104',port=8080)
    
run()



