from flask import Flask, request, url_for, json
from celery import Celery
import subprocess
app = Flask(__name__)


app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'amqp'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

#CELERY_QUEUES = (
#    Queue('default', Exchange('default'), routing_key='default'),
#    Queue('for_task_A', Exchange('for_task_A'), routing_key='for_task_A'),
#    Queue('for_task_B', Exchange('for_task_B'), routing_key='for_task_B'),
#)
#CELERY_ROUTES = {
#    'my_taskA': {'queue': 'for_task_A', 'routing_key': 'for_task_A'},
#    'my_taskB': {'queue': 'for_task_B', 'routing_key': 'for_task_B'},
#}


@celery.task
def print_hello(ignore_result=True):
    print 'hello there'

def hello1():
    cmd = ["ls","-l"]
    with open('/tmp/text_output.txt', 'w') as fout:
      subprocess.Popen(cmd, stdout = fout,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)




@app.route('/messages', methods = ['POST'])
def api_message():

    if request.headers['Content-Type'] == 'application/json':        

        n = request.json['message']
        hello1()
        with open("/tmp/test.txt","a") as fo:
         fo.write("This is Test Data" + n + "\n")

        task = print_hello.delay()

        return "JSON Message: " + n
    else:
        return "415 Unsupported Media Type."


if __name__ == "__main__":
    app.run(debug=True)


