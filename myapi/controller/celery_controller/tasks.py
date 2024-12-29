from controller.celery_controller.celery_base import app

@app.task
def add(x, y):
    return x + y

@app.task
def send_email():
    print("Sending email")