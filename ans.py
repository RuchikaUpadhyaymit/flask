from flask import Flask, request, url_for
from celery import Celery,task
#from kombu import Exchange, Queue
import json
#import requests
app = Flask(__name__)


app.config['CELERY_BROKER_URL'] = 'amqp://'
app.config['CELERY_RESULT_BACKEND'] = 'amqp'
#app.config['CELERY_IMPORTS'] = ("tasks",)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

#CELERY_QUEUES = (
#    Queue('default', Exchange('default'), routing_key='default'),
#    Queue('for_acknowledge', Exchange('for_acknowledge'), routing_key='for_acknowledge'),
#    Queue('for_execute_command', Exchange('for_execute_command'), routing_key='for_execute_command'),
#)
#CELERY_ROUTES = {
#    'acknowledge': {'queue': 'for_acknowledge', 'routing_key': 'for_acknowledge'},
#    'execute_command': {'queue': 'for_execute_command', 'routing_key': 'for_execute_command'},
#}

#respond if valid
#@celery.task
#def acknowledge(ignore_result=True):
#    return


#validate the request
def validate(slack_token,slack_team_domain,slack_channel_name,slack_command):
    if slack_token == "dw4An4rObbXUK182jQQoAWaf" and slack_team_domain == "doselect" and slack_channel_name == "deployment" and slack_command == "/deploy" : 
     return 
    else :
     exit()

#execute the command and send the file
@celery.task
def execute_command():
    import subprocess
    cmd = ["ls","-l"]
    with open('/tmp/text_output.txt', 'w') as fout:
      subprocess.Popen(cmd, stdout = fout,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    return



@app.route('/', methods = ['POST'])
def api_message():

    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':

#retrieve request data
	post_body = json.dumps(request.form)
#        import pdb; pdb.set_trace()        
        slack_token = request.form.getlist('token')[0]
        slack_team_id = request.form.getlist('team_id')[0]
        slack_team_domain = request.form.getlist('team_domain')[0]
        slack_channel_name = request.form.getlist('channel_name')[0]
        slack_user_name = request.form.getlist('user_name')[0]
        slack_response_url = request.form.getlist('response_url')[0]
        slack_command = request.form.getlist('command')[0]
        slack_text = request.form.getlist('text')[0]

#validate the request        
        validate(slack_token,slack_team_domain,slack_channel_name,slack_command)

#audit log file in /tmp/command_access.logs
        import datetime
        time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')       
        with open("/tmp/command_access.logs","a") as fo:
         fo.write("Time :" + time + "\n" +"Log :" + post_body + "\n")

#acknowledge the request
#        task = acknowledge.delay()

#execute command
        task = execute_command.delay()


        return "The token is : " + slack_token + "\t" + slack_team_id + "\t" + slack_command + "\t" + slack_text
    else:
        return "415 Unsupported Media Type."






if __name__ == "__main__":
    app.run(debug=True)


