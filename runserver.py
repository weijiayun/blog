#!/home/linus/PycharmProjects/flask/bin/python2.7
from multiprocessing import Process
from flaskr import app,models

def runWeb():
    app.debug=True
    app.run()

p1=Process(target=runWeb,name='process_runWeb')
p1.start()
p1.join()




