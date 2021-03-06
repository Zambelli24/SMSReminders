from flask import Flask, request
import time
from redis import Redis

app = Flask(__name__)
r = Redis(host='redis', port='6379')


@app.route('/', methods=['GET', 'POST'])
def save_reminder():
    if request.method == 'POST':
        return add_new_reminder()
    else:
        return show_remaining_reminders()


def show_remaining_reminders():
    ret_str = ''
    for msg_and_num, time_to_send in r.zscan_iter('reminders'):
        temp_str = msg_and_num.decode('UTF-8').split(",")
        ret_str += temp_str[0]
        ret_str += ' ' + str(int(time_to_send) - int(time.time())) + '\n'
    return ret_str


def add_new_reminder():
    time_to_send = request.form['time']
    message = request.form['message']
    phone_number = request.form['phone_number']
    msg_and_num = message + "," + phone_number
    curr_time = int(time.time())
    exp_time = int(time_to_send) + curr_time
    r.zadd('reminders', msg_and_num, exp_time)
    return 'New reminder added successfully'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
