#!/home/linus/PycharmProjects/flask/bin/python2.7
from flaskr import app

def run():
    app.debug=False
    app.run(host='127.0.0.1',port=5000)
    
run()



