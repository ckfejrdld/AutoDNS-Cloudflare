from flask import *
import api
import config
from urllib.parse import unquote

app = Flask(__name__)

key = config.key
@app.route(f'/autodns/<value>/a/<value1>/<value2>/<value3>/<value4>/<value5>')
def a(value, value1, value2, value3, value4, value5):
    if value in config.key:
        result = api.create_a_record(value1, value2, value3, value4, value5)
        print(result)
        if result == 200:
            return '등록 성공', 200
        elif result == 400:
            return '이미 등록된 도메인', 400
        elif result == 403:
            return '유효하지 않는 로그인 정보', 403
        elif result == 406:
            return '프록시 인증 실패', 406
        elif result == 408:
            return '요청 시간 초과', 408
        elif result == 500:
            return '내부 서버 오류', 500
        else:
            return 'Error'
    else:
        return 'Invalid Authorized Key', 401
    
@app.route(f'/autodns/<value>/cname/<value1>/<value2>/<value3>/<value4>/<value5>')
def cname(value, value1, value2, value3, value4, value5):
    if value in config.key:
        result = api.create_cname_record(value1, value2, value3, value4, value5)
        print(result)
        if result == 200:
            return '등록 성공', 200
        elif result == 400:
            return '이미 등록된 도메인', 400
        elif result == 403:
            return '유효하지 않는 로그인 정보', 403
        elif result == 406:
            return '프록시 인증 실패', 406
        elif result == 408:
            return '요청 시간 초과', 408
        elif result == 500:
            return '내부 서버 오류', 500
        else:
            return 'Error'
    else:
        return 'Invalid Authorized Key', 401
    
@app.route(f'/autodns/<value>/srv/<value1>/<value2>/<value3>/<value4>/<value5>/<value6>')
def srv(value, value1, value2, value3, value4, value5, value6):
    if value in config.key:
        result = api.create_srv_record(value1, value2, value3, value4, value5, value6)
        print(result)
        if result == 200:
            return '등록 성공', 200
        elif result == 400:
            return '이미 등록된 도메인', 400
        elif result == 403:
            return '유효하지 않는 로그인 정보', 403
        elif result == 406:
            return '프록시 인증 실패', 406
        elif result == 408:
            return '요청 시간 초과', 408
        elif result == 500:
            return '내부 서버 오류', 500
        else:
            return 'Error'
    else:
     return 'Invalid Authorized Key', 401
    
@app.route(f'/autodns/<value>/getid/<value1>/<value2>/<value3>/<value4>/<value5>')
def get_id(value, value1, value2, value3, value4, value5):
    if value in config.key:
        result = api.get_id(value1, value2, value3, value4, value5)
        print(result)
        if result[1] == 200:
            return result[0], 200
        else:
            return 'Error'
    else:
        return 'Invalid Authorized Key', 401
    
@app.route(f'/autodns/<value>/removerecord/<value1>/<value2>/<value3>/<value4>')
def remove_record(value, value1, value2, value3, value4):
    if value in config.key:
        result = api.remove_record(value1, value2, value3, value4)
        print(result)
        if result == 200:
            return '삭제 성공', 200
        elif result == 400:
            return '없는 도메인', 400
        else:
            return 'Error'
    else:
     return 'Invalid Authorized Key', 401
    
@app.errorhandler(404)
def not_found(error):
    print(error)
    return 'Please Enter Valid Parameters', 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=2999, use_reloader=True)
