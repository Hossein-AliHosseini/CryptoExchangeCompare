import sys
from flask import Flask, request
from kavenegar import *

app = Flask(__name__)


@app.route('/send-activation-sms', endpoint='index')
def index():
    params = request.args
    phone_number = params.get('phone-number')
    eid = params.get('eid')
    token = params.get('token')
    api = KavenegarAPI('35735655744145536B744D3545546A55654553652B6A7A6231533550674A4C627042496639742B6A6A67733D')
    params = {'sender': '10008663',
              'receptor': phone_number,
              'message': '127.0.0.1:8000/v1/users/activate/' + eid + '/' + token}
    try:
        response = api.sms_send(params)
        sys.stdout.write(str(response))
        return 'Success'
    except Exception as e:
        sys.stderr.write(str(e))
        return 'Failure'


@app.route('/send-reset-password-sms', endpoint='indexx')
def indexx():
    params = request.args
    phone_number = params.get('phone-number')
    uid = params.get('uid')
    token = params.get('token')
    api = KavenegarAPI('35735655744145536B744D3545546A55654553652B6A7A6231533550674A4C627042496639742B6A6A67733D')
    params = {'sender': '10008663',
              'receptor': phone_number,
              'message': '127.0.0.1:8000/v1/users/password/reset/confirm/?uid=' + uid + '&token=' + token}
    try:
        response = api.sms_send(params)
        sys.stdout.write(str(response))
        return 'Success'
    except Exception as e:
        sys.stderr.write(str(e))
        return 'Failure'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
