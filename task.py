from celery import Celery
app = Celery('task', backend='amqp', broker='amqp://')

@app.task
def print_hello(ignore_result=True):
    print 'hello there'

@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results
